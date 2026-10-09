"""Các công cụ dùng chung cho mọi bài: so sánh phương pháp số, khớp dữ liệu, can thiệp và SEIR."""
import numpy as np
import pandas as pd
import streamlit as st
from scipy.integrate import solve_ivp

from tien_ich import (DON_VI_THOI_GIAN, analysis, bao_loi_an_toan, chu_trinh, data, doc_csv_tai_len, hinh, models,
                      nhan_mo_phong, nut_tai_matlab, solvers, tai_csv)

PP = {"Euler": (solvers.euler, 1), "Heun (hình thang hiện)": (solvers.heun, 2),
      "Điểm giữa hiện": (solvers.diem_giua, 2), "RK4": (solvers.rk4, 4)}


def cong_cu_phuong_phap_so():
    st.title("Công cụ: so sánh phương pháp số và sai số")
    st.markdown("So sánh công bằng: **cùng** bài toán, **cùng** bước $h$, sai số đo tại **cùng** thời điểm. "
                "Ba hướng: phương trình vô hướng, phương trình cấp hai quy về hệ, hệ nhiều biến.")
    bai = st.radio("Bài toán", ["Vô hướng: logistic có nghiệm chính xác", "Cấp hai: dao động x'' + ω²x = 0 (năng lượng)",
                                "Hệ: SIR tình huống cúm (so với nghiệm tham chiếu)", "Ổn định: phương trình thử y' = λy"],
                   key="ss_bai")
    chu_trinh("1")
    st.radio("Dự đoán: giảm h một nửa thì sai số RK4 giảm khoảng bao nhiêu lần?", ["2", "4", "8", "16"], index=None, key="ss_dd")
    if bai.startswith("Vô hướng"):
        r, K, P0 = 0.55, 665.0, 9.6
        f = models.logistic_rhs(r, K)
        T = st.select_slider("Thời điểm đánh giá T (giờ)", [2.0, 5.0, 10.0, 15.0], value=10.0, key="ss_T")
        chu_trinh("2")
        h = st.select_slider("Bước h (giờ)", [2.0, 1.0, 0.5, 0.25, 0.125, 0.0625], value=1.0, key="ss_h")
        if bao_loi_an_toan(solvers.luoi, 0.0, T, h, thong_bao="Bước không hợp lệ") is None:
            return
        ex = float(models.logistic_chinh_xac(T, P0, r, K))
        chu_trinh("3")

        def ve(ax):
            tf = np.linspace(0, T, 400)
            ax.plot(tf, models.logistic_chinh_xac(tf, P0, r, K), "k-", label="nghiệm chính xác")
            for ten, (m, _) in PP.items():
                t, y = m(f, 0.0, [P0], h, T)
                ax.plot(t, y[:, 0], "o--", ms=3, label=ten)
            ax.set_xlabel("t (giờ)"); ax.set_ylabel("P"); ax.legend(fontsize=8)
        hinh(ve)
        dong = []
        for ten, (m, so_f) in PP.items():
            e = [abs(m(f, 0.0, [P0], hh, T)[1][-1, 0] - ex) for hh in (h, h / 2)]
            dong.append({"phương pháp": ten, f"sai số h={h:g}": e[0], f"sai số h={h / 2:g}": e[1],
                         "bậc thực nghiệm": np.log2(e[0] / e[1]) if e[1] > 0 else np.nan, "lượt tính f": so_f * round(T / h)})
        bang = pd.DataFrame(dong)
        st.dataframe(bang.style.format(precision=4), hide_index=True)
        chu_trinh("4")
        st.markdown("Bậc lý thuyết (sai số toàn cục): Euler 1, Heun 2, điểm giữa 2, RK4 4. Với $h$ lớn, bậc đo được có thể "
                    "lệch; nó tiến tới lý thuyết khi $h$ nhỏ dần. Sai số một bước *chưa chia* $h$ có bậc cao hơn một bậc.")
        tai_csv(bang, "so_sanh_logistic.csv", key="ss_csv1")
    elif bai.startswith("Cấp hai"):
        om = st.slider("ω (rad/đơn vị thời gian)", 0.5, 4.0, 2.0, 0.5, key="ss_om")
        h = st.select_slider("Bước h", [0.2, 0.1, 0.05, 0.025], value=0.1, key="ss_h2")
        T = 10.0
        f = models.dao_dong_rhs(om)
        E = lambda y: 0.5 * y[:, 1] ** 2 + 0.5 * om ** 2 * y[:, 0] ** 2  # noqa: E731
        chu_trinh("3")

        def ve(ax):
            for ten, (m, _) in PP.items():
                t, y = m(f, 0.0, [1.0, 0.0], h, T)
                ax.plot(t, E(y) / E(y[:1])[0], label=ten)
            ax.axhline(1, color="k", lw=0.8); ax.set_yscale("log")
            ax.set_xlabel("t"); ax.set_ylabel("E(t)/E(0) (thang log)"); ax.legend(fontsize=8)
        hinh(ve)
        t, y = solvers.euler(f, 0.0, [1.0, 0.0], h, T)
        st.write(f"Euler: E(T)/E(0) = {E(y)[-1] / E(y)[0]:.4f}, công thức $(1+h^2\\omega^2)^n$ = "
                 f"{(1 + h ** 2 * om ** 2) ** round(T / h):.4f}.")
        chu_trinh("4")
        st.markdown("Nghiệm đúng bảo toàn năng lượng; phương pháp tường minh thì không. Tiêu chí kiểm chứng hợp lý: "
                    "**trôi năng lượng giảm khi $h$ giảm** (RK4: theo $h^5$), không đòi bảo toàn chính xác (VD44).")
    elif bai.startswith("Hệ"):
        N, S0, I0, beta, gamma = 1000.0, 995.0, 5.0, 1.407, 0.6
        f = models.sir_rhs(beta, gamma, N)
        chu_trinh("2")
        h = st.select_slider("Bước h (tuần)", [3.0, 2.0, 1.0, 0.5, 0.25, 0.1], value=1.0, key="ss_h3")
        T = 30.0
        ref, td = models.sir_giai(S0, I0, N, beta, gamma, T)
        tf = np.linspace(0, T, 600)
        chu_trinh("3")
        dong = []

        def ve(ax):
            ax.plot(tf, ref.sol(tf)[1], "k-", label="I tham chiếu")
            for ten, (m, _) in PP.items():
                t, y = m(f, 0.0, [S0, I0, 0.0], h, T)
                ax.plot(t, y[:, 1], "o--", ms=3, label=ten)
                k = int(np.argmax(y[:, 1]))
                dong.append({"phương pháp": ten, "max I trên lưới": y[k, 1], "tại t": t[k], "min S": y[:, 0].min(),
                             "min I": y[:, 1].min(), "max|S+I+R−N|": np.max(np.abs(y.sum(axis=1) - N))})
            ax.axhline(0, color="k", lw=0.6); ax.set_xlabel("t (tuần)"); ax.set_ylabel("I"); ax.legend(fontsize=8)
        hinh(ve)
        bang = pd.DataFrame(dong)
        st.dataframe(bang.style.format(precision=3), hide_index=True)
        if (bang["min I"] < 0).any() or (bang["min S"] < 0).any():
            st.error("THẤT BẠI: có phương pháp cho **số người âm** — vô nghĩa dù tổng vẫn bảo toàn. "
                     "Không 'sửa' bằng cách cắt về 0; hãy giảm h (VD38).")
        st.write(f"Tham chiếu: đỉnh {models.sir_dinh_dich(S0, I0, N, beta, gamma)['I_max']:.3f} tại t ≈ {td:.3f} tuần.")
        chu_trinh("4")
        st.markdown("Euler bước lớn làm lệch đỉnh dịch: sai số của **phương pháp**, không phải đặc điểm của dịch.")
        tai_csv(bang, "so_sanh_sir.csv", key="ss_csv3")
    else:
        lam = st.slider("λ (thời gian⁻¹)", -60.0, -1.0, -30.0, 1.0, key="ss_lam")
        h = st.select_slider("h", [0.2, 0.1, 0.075, 0.05, 0.02], value=0.1, key="ss_h4")
        z = h * lam
        chu_trinh("3")
        st.write(f"z = hλ = {z:g}")
        st.dataframe(pd.DataFrame([{"phương pháp": ten, "Q(hλ)": Q(z), "|Q| < 1 (ổn định tuyệt đối)": abs(Q(z)) < 1}
                                   for ten, Q in solvers.HE_SO_KHUECH_DAI.items()]), hide_index=True)
        chu_trinh("4")
        st.markdown("$y_n=Q(h\\lambda)^ny_0$ suy giảm như nghiệm đúng khi và chỉ khi $|Q(h\\lambda)|<1$. Ổn định tuyệt đối "
                    "(bước cố định) khác ổn định trên khoảng hữu hạn (khi $h\\to0$). RK4 bậc bốn vẫn có thể phân kỳ (VD37); "
                    "bài toán cứng cần phương pháp ẩn (VD40).")
    chu_trinh("5")
    nhan_mo_phong()
    nut_tai_matlab("vd_phuong_phap_so.m", key="ss_m")


def cong_cu_khop_du_lieu():
    st.title("Công cụ: khớp mô hình với dữ liệu")
    st.markdown("Dữ liệu mẫu là dữ liệu **quan sát** có nguồn (nấm men, Pearl 1927). Có thể tải lên CSV hai cột `t`, `P`; "
                "tệp chỉ được đọc như số liệu trên máy chạy ứng dụng, không thực thi và không gửi ra ngoài.")
    nguon = st.radio("Dữ liệu", ["Nấm men (quan sát, có nguồn)", "Tải lên CSV"], horizontal=True, key="kd_nguon")
    don_vi = st.selectbox("Đơn vị thời gian của cột t", list(DON_VI_THOI_GIAN), index=0, key="kd_dv")
    try:
        if nguon.startswith("Nấm"):
            t, P = data.NAM_MEN["t"], data.NAM_MEN["P"]
            if don_vi != "giờ":
                st.warning("Dữ liệu nấm men đo theo **giờ**; đơn vị đã chọn không khớp nguồn. Kết quả r sẽ bị hiểu sai đơn vị.")
        else:
            tep = st.file_uploader("CSV có hai cột t, P (P > 0, t tăng ngặt, dấu chấm thập phân)", type="csv", key="kd_tep")
            if tep is None:
                st.info("Chưa có tệp.")
                return
            t, P = doc_csv_tai_len(tep)
    except analysis.DuLieuKhongHopLe as e:
        st.error(f"Dữ liệu không hợp lệ: {e}")
        return
    st.write(f"{len(t)} quan sát, t từ {t[0]:g} đến {t[-1]:g} {don_vi}, P từ {P.min():g} đến {P.max():g}.")
    chu_trinh("2")
    tc = st.slider(f"Mốc cắt t_c ({don_vi}): chỉ dùng t ≤ t_c để ước lượng MỌI tham số", float(t[2]), float(t[-2]),
                   float(t[min(len(t) - 2, len(t) // 2)]), key="kd_tc")
    kq = bao_loi_an_toan(analysis.thi_nghiem_chia_thoi_gian, t, P, tc, thong_bao="Không khớp được")
    if kq is None:
        return
    lg = kq["logistic"]
    chu_trinh("3")

    def ve(ax):
        tr = kq["mask_huan_luyen"]
        ax.plot(t[tr], P[tr], "ko", ms=3.5, label="huấn luyện")
        ax.plot(t[~tr], P[~tr], "o", mfc="none", mec="k", ms=4, label="giữ lại (kiểm tra)")
        ax.plot(t, np.minimum(kq["du_bao"]["malthus"], 3 * P.max()), "C0-", label="Malthus")
        ax.plot(t, kq["du_bao"]["logistic"], "C3--", label="logistic")
        ax.set_ylim(0, 1.5 * P.max()); ax.set_xlabel(f"t ({don_vi})"); ax.set_ylabel("P"); ax.legend(fontsize=8)
    hinh(ve)
    se_K = lg["sai_so_chuan"][1]
    if not np.isfinite(se_K) or se_K > lg["K"]:
        st.warning(f"K **không nhận diện được trong thực hành** từ dữ liệu t ≤ {tc:g} (K ≈ {lg['K']:.3g}, sai số chuẩn rất lớn): "
                   "dữ liệu giai đoạn đầu gần như hàm mũ, không chứa thông tin về sức chứa.")
    bang = pd.DataFrame({"mô hình": ["Malthus", "logistic"],
                         f"r ({don_vi}⁻¹)": [kq["malthus"]["r"], lg["r"]], "K": [np.nan, lg["K"]],
                         "RMSE huấn luyện": [kq["rmse_huan_luyen"]["malthus"], kq["rmse_huan_luyen"]["logistic"]],
                         "RMSE kiểm tra": [kq["rmse_kiem_tra"]["malthus"], kq["rmse_kiem_tra"]["logistic"]]})
    st.dataframe(bang.style.format(precision=4), hide_index=True)
    chu_trinh("4")
    st.markdown("RMSE **kiểm tra** đo dự báo trên dữ liệu không dùng để ước lượng; RMSE huấn luyện nhỏ không bảo đảm dự báo tốt. "
                "Hàm mục tiêu: tổng bình phương sai số trên thang gốc; ràng buộc $r>0$ và $K\\ge\\max P$ (trên phần huấn luyện) "
                "là **lựa chọn khi khớp** cho dữ liệu tăng đơn điệu, không phải hệ quả của mô hình; phương pháp vùng tin cậy.")
    chu_trinh("5")
    tai_csv(bang, "khop_du_lieu.csv", key="kd_csv")
    nhan_mo_phong()


def cong_cu_can_thiep_seir():
    st.title("Công cụ: can thiệp theo thời điểm và mô hình SEIR")
    cum = data.CUM_GIAO_KHOA
    N, S0, I0, beta, gamma = cum["N"], cum["S0"], cum["I0"], cum["beta"], cum["gamma"]
    st.caption("Tham số cơ sở: tình huống cúm giáo khoa, β = 1,407 tuần⁻¹ (tham số cố định).")
    st.subheader("1. Giảm tiếp xúc bắt đầu tại t_c")
    st.markdown("Giả thiết: β giảm **tức thời** tại $t_c$ và giữ nguyên. Tích phân từng giai đoạn: trạng thái tại $t_c$ là "
                "điều kiện đầu của giai đoạn sau; không áp β mới cho quá khứ.")
    c1, c2 = st.columns(2)
    giam = c1.slider("Mức giảm β (%)", 0, 90, 40, key="ct_giam")
    tc = c2.slider("Thời điểm bắt đầu t_c (tuần)", 0.0, 20.0, 5.0, 0.5, key="ct_tc")
    beta2 = beta * (1 - giam / 100)
    t, y = models.sir_can_thiep(S0, I0, N, beta, beta2, gamma, tc, 60.0, n_diem=3000)
    _, y0 = models.sir_can_thiep(S0, I0, N, beta, beta, gamma, 0.0, 60.0, n_diem=3000)
    hinh(lambda ax: (ax.plot(t, y0[1], "k:", label="không can thiệp"), ax.plot(t, y[1], "C3-", label=f"giảm β {giam}% từ t = {tc:g}"),
                     ax.axvline(tc, color="0.5", ls="--"), ax.set_xlabel("t (tuần)"), ax.set_ylabel("I (đang nhiễm)"),
                     ax.legend(fontsize=8)))
    k = int(np.argmax(y[1]))
    st.write(f"Đỉnh: {y[1][k]:.2f} người tại t ≈ {t[k]:.2f} tuần; 𝓡_eff ngay sau t_c = "
             f"{beta2 / gamma * np.interp(tc, t, y[0]) / N:.3f}.")
    tai_csv(pd.DataFrame({"t": t, "S": y[0], "I": y[1], "R": y[2]}), "sir_can_thiep.csv", key="ct_csv")
    st.subheader("2. Miễn dịch lý tưởng trước dịch")
    st.markdown("Giả thiết: miễn dịch hoàn toàn, bền vững; người được miễn dịch chọn **ngẫu nhiên**; trộn đều.")
    p = st.slider("Tỉ lệ đã miễn dịch p (%)", 0, 95, 50, key="ct_p") / 100
    R0 = beta / gamma
    S0v = (1 - p) * (N - I0)
    st.write(f"𝓡₀ = {R0:.3f}; p_c = max(0, 1 − 1/𝓡₀) = {models.nguong_mien_dich(R0) * 100:.2f}%. Với p = {p * 100:.0f}%: "
             f"𝓡_eff(0) = {R0 * S0v / N:.3f} → " + ("I **tăng** ban đầu." if R0 * S0v / N > 1 else "I **không tăng** ban đầu."))
    st.subheader("3. Mở rộng SEIR")
    st.markdown("$E$: đã nhiễm nhưng **chưa có khả năng lây**; $1/\\sigma$: thời gian tiềm ẩn trung bình (tốc độ chuyển "
                "không đổi) — không đồng nhất với thời gian ủ bệnh.")
    sig_inv = st.slider("1/σ (tuần)", 0.1, 4.0, 1.0, 0.1, key="ct_sig")
    seir = solve_ivp(models.seir_rhs(beta, 1 / sig_inv, gamma, N), [0, 80], [S0, 0, I0, 0], method="DOP853",
                     rtol=1e-10, atol=1e-9, dense_output=True)
    sol, _ = models.sir_giai(S0, I0, N, beta, gamma, 80)
    tt = np.linspace(0, 80, 2000)
    hinh(lambda ax: (ax.plot(tt, sol.sol(tt)[1], "k-", label="SIR: I"), ax.plot(tt, seir.sol(tt)[2], "C3--", label="SEIR: I"),
                     ax.plot(tt, seir.sol(tt)[1], "C0:", label="SEIR: E"), ax.set_xlabel("t (tuần)"), ax.set_ylabel("số người"),
                     ax.legend(fontsize=8)))
    con = seir.sol(80)[1] + seir.sol(80)[2]
    st.write(f"S(80): SIR {sol.sol(80)[0]:.3f}, SEIR {seir.sol(80)[0]:.3f}; SEIR còn E + I = {con:.3g} tại t = 80.")
    if con < 1e-2:
        st.success("Dịch SEIR đã kết thúc trong khoảng khảo sát: cùng quy mô cuối với SIR, khác động học (VD32).")
    else:
        st.warning("Dịch SEIR chưa kết thúc tại t = 80: chưa thể so sánh quy mô cuối.")
    nhan_mo_phong()
