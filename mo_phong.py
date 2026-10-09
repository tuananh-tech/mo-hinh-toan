"""Phần mô phỏng tương tác của từng bài học (tab "Mô phỏng"). Mọi tính toán gọi module mhtoan."""
import numpy as np
import pandas as pd
import streamlit as st
from scipy.integrate import solve_ivp

from tien_ich import (analysis, bao_loi_an_toan, chu_trinh, data, doc_csv_tai_len, he_tuyen_tinh, hinh, models,
                      nhan_mo_phong, solvers, tai_csv, tai_hinh)


# ============================================================================ Bài 1
def mo_phong_bai1():
    ym = data.NAM_MEN
    st.markdown("#### A. Từ dữ liệu đến tốc độ")
    chu_trinh("1")
    du_doan = st.radio("Dự đoán: trong 5 giờ đầu, đại lượng nào gần như **không đổi**?",
                       ["Hiệu P(n+1) − P(n)", "Tỉ số P(n+1)/P(n)", "Cả hai", "Không đại lượng nào"], index=None, key="b1_dd")
    t, P = ym["t"][:5], ym["P"][:5]
    df = pd.DataFrame({"t (giờ)": t, "P": P, "hiệu P(n+1)−P(n)": np.append(np.diff(P), np.nan),
                       "tỉ số P(n+1)/P(n)": np.append(P[1:] / P[:-1], np.nan)})
    st.dataframe(df.style.format(precision=3), hide_index=True)
    if du_doan is not None:
        if du_doan == "Tỉ số P(n+1)/P(n)":
            st.success("Đúng: tỉ số dao động quanh 1,6 trong khi hiệu tăng dần — dấu hiệu của tăng trưởng mũ.")
        else:
            st.warning("So sánh lại: hiệu tăng từ 8,7 lên 23,9; tỉ số chỉ dao động quanh 1,6.")
    st.caption(f"Dữ liệu quan sát: {ym['nguon']}.")

    st.markdown("#### B. Mô hình Malthus với tham số có đơn vị")
    chu_trinh("2")
    c1, c2, c3 = st.columns(3)
    b = c1.number_input("b — tốc độ sinh riêng (năm⁻¹)", 0.0, 2.0, 0.035, 0.005, format="%.3f", key="b1_b")
    d = c2.number_input("d — tốc độ tử riêng (năm⁻¹)", 0.0, 2.0, 0.015, 0.005, format="%.3f", key="b1_d")
    P0 = c3.number_input("P₀ — quy mô ban đầu (cá thể)", 1.0, 1e10, 2.0e6, 1e5, format="%.0f", key="b1_P0")
    T = st.slider("Khoảng khảo sát (năm)", 1, 200, 50, key="b1_T")
    r = b - d
    tt = np.linspace(0, T, 400)
    chu_trinh("3")
    png = hinh(lambda ax: (ax.plot(tt, models.malthus_chinh_xac(tt, P0, r), "k-"), ax.set_xlabel("t (năm)"),
                           ax.set_ylabel("P(t) (cá thể)")))
    c1, c2, c3 = st.columns(3)
    c1.metric("r = b − d", f"{r:.4f} năm⁻¹ = {models.doi_don_vi_ty_le(r, 12):.5f} tháng⁻¹")
    if r > 0:
        c2.metric("Thời gian tăng gấp đôi", f"{models.thoi_gian_gap_doi(r):.2f} năm")
    elif r < 0:
        c2.metric("Thời gian bán hủy", f"{models.thoi_gian_ban_huy(r):.2f} năm")
    else:
        c2.metric("r = 0", "quần thể không đổi")
    c3.metric("Hệ số nhân sau 1 năm", f"e^r = {np.exp(r):.4f}")
    chu_trinh("4")
    st.markdown("Sau một năm quần thể nhân với $e^{r}$, **không** phải $1+r$: với $r=0{,}24$ năm$^{-1}$, "
                "$e^{0{,}24}\\approx1{,}2712$ (tăng $27{,}1\\%$, VD01).")
    tai_hinh(png, "malthus.png", key="b1_png")

    st.markdown("#### C. Đối chiếu dữ liệu và miền hiệu lực theo tiêu chí")
    chu_trinh("5")
    n_khop = st.slider("Số quan sát đầu dùng để khớp (huấn luyện)", 3, 19, 5, key="b1_n")
    nguong = st.slider("Tiêu chí sai số tương đối tối đa (%)", 1, 50, 10, key="b1_ng")
    td, Pd = ym["t"], ym["P"]
    m = analysis.khop_malthus_log(td[:n_khop], Pd[:n_khop])
    du = m["P0"] * np.exp(m["r"] * td)
    ss = analysis.sai_so_tuong_doi_phan_tram(du, Pd)
    vuot = [x for x, e in zip(td, np.abs(ss)) if e > nguong]

    def ve(ax):
        ax.plot(td, Pd, "ko", ms=3.5, label="dữ liệu quan sát")
        ax.plot(td, du, "C0-", label="Malthus (khớp trên phần huấn luyện)")
        ax.axvline(td[n_khop - 1], color="0.5", ls=":", label="hết phần huấn luyện")
        ax.set_yscale("log"); ax.set_xlabel("t (giờ)"); ax.set_ylabel("P (thang logarit)"); ax.legend(fontsize=8)
    hinh(ve)
    st.write(f"r ≈ {m['r']:.4f} giờ⁻¹, P₀ ≈ {m['P0']:.3f}. "
             + (f"Sai số vượt {nguong}% lần đầu tại t = {vuot[0]:g} giờ." if vuot else f"Sai số không vượt {nguong}%."))
    st.markdown("Trên thang logarit, Malthus là **đường thẳng**; dữ liệu cong xuống cho thấy giả thiết "
                "\"không giới hạn tài nguyên\" bị vi phạm. Miền hiệu lực phụ thuộc **tiêu chí** đã chọn (VD10).")
    tai_csv(pd.DataFrame({"t": td, "quan sat": Pd, "Malthus": du, "sai so %": ss}), "malthus_doi_chieu.csv", key="b1_csv")
    nhan_mo_phong()


# ============================================================================ Bài 2
def mo_phong_bai2():
    st.markdown("#### A. Nghiệm và đường pha")
    chu_trinh("1")
    st.radio("Dự đoán: quần thể tăng nhanh nhất khi P bằng bao nhiêu?", ["K/4", "K/2", "K", "Khi P nhỏ nhất"],
             index=None, key="b2_dd")
    chu_trinh("2")
    c1, c2, c3 = st.columns(3)
    r = c1.slider("r (năm⁻¹)", 0.05, 2.0, 0.4, 0.05, key="b2_r")
    K = c2.slider("K (cá thể)", 50.0, 2000.0, 500.0, 50.0, key="b2_K")
    P0 = c3.slider("P₀ (cá thể)", 1.0, 2.5 * K, 20.0, 1.0, key="b2_P0")
    T = st.slider("Khoảng khảo sát (năm)", 1, 100, 30, key="b2_T")
    t = np.linspace(0, T, 500)
    Pt = models.logistic_chinh_xac(t, P0, r, K)
    chu_trinh("3")
    c1, c2 = st.columns(2)
    with c1:
        def ve1(ax):
            Pg = np.linspace(0, max(1.3 * K, 1.1 * P0), 300)
            ax.plot(Pg, r * Pg * (1 - Pg / K), "k-"); ax.axhline(0, color="k", lw=0.8)
            ax.plot([0, K], [0, 0], "ko"); ax.plot([K / 2], [r * K / 4], "C3^")
            ax.annotate("", xy=(0.7 * K, 0), xytext=(0.3 * K, 0), arrowprops=dict(arrowstyle="->", color="C0"))
            ax.annotate("", xy=(1.05 * K, 0), xytext=(1.25 * K, 0), arrowprops=dict(arrowstyle="->", color="C0"))
            ax.set_xlabel("P (cá thể)"); ax.set_ylabel("f(P) (cá thể/năm)"); ax.set_title("Đường pha")
        hinh(ve1, (5, 3.4))
    with c2:
        def ve2(ax):
            ax.plot(t, Pt, "k-"); ax.axhline(K, color="0.4", ls=":"); ax.axhline(K / 2, color="0.6", ls="--")
            ax.set_xlabel("t (năm)"); ax.set_ylabel("P(t) (cá thể)"); ax.set_title("Nghiệm chính xác")
        hinh(ve2, (5, 3.4))
    c1, c2 = st.columns(2)
    c1.metric("Tốc độ tăng lớn nhất rK/4", f"{r * K / 4:.2f} cá thể/năm")
    if 0 < P0 < K / 2:
        c2.metric("Thời điểm uốn t*", f"{models.logistic_t_uon(P0, r, K):.3f} năm")
    elif P0 > K:
        c2.info("P₀ > K: quần thể giảm về K, không có điểm uốn.")
    else:
        c2.info("P₀ ≥ K/2: điểm uốn không nằm trong t ≥ 0.")
    chu_trinh("4")
    st.markdown("$0$ không ổn định ($f'(0)=r>0$), $K$ ổn định tiệm cận ($f'(K)=-r<0$); tăng nhanh nhất tại $P=K/2$.")
    chu_trinh("5")
    _, Y = solvers.rk4(models.logistic_rhs(r, K), 0.0, [P0], T / 500, T)
    st.write(f"Kiểm chứng: RK4 với 500 bước khác nghiệm tường minh tối đa "
             f"{np.max(np.abs(Y[:, 0] - models.logistic_chinh_xac(np.linspace(0, T, 501), P0, r, K))):.2e} cá thể.")
    tai_csv(pd.DataFrame({"t (nam)": t, "P": Pt}), "logistic_nghiem.csv", key="b2_csv")

    st.markdown("#### B. Khai thác với sản lượng không đổi")
    st.markdown("$P'=rP(1-P/K)-H$. Mô phỏng **dừng** khi quần thể chạm 0 (tuyệt chủng); không cắt giá trị âm.")
    c1, c2, c3, c4 = st.columns(4)
    r2 = c1.number_input("r (năm⁻¹)", 0.05, 3.0, 0.5, 0.05, key="b2_r2")
    K2 = c2.number_input("K (tấn)", 10.0, 1e5, 1000.0, 10.0, key="b2_K2")
    H = c3.number_input("H (tấn/năm)", 0.0, 1e5, 100.0, 5.0, key="b2_H")
    P02 = c4.number_input("P₀ (tấn)", 0.1, 1e5, 800.0, 10.0, key="b2_P02")
    T2 = st.slider("Khoảng khảo sát (năm)", 1, 300, 60, key="b2_T2")
    cb = models.khai_thac_can_bang(r2, K2, H)
    st.write(f"Ngưỡng tới hạn rK/4 = {cb['H_toi_han']:.3f} tấn/năm → chế độ **{cb['truong_hop']}**.")
    for P_cb, loai in cb["can_bang"]:
        st.write(f"• Điểm cân bằng P = {P_cb:.3f} tấn: {loai}")
    if cb["truong_hop"] == "H = rK/4":
        st.info("f'(K/2) = 0: tiêu chuẩn đạo hàm không kết luận được; xét dấu f = −(r/K)(P − K/2)² ≤ 0: nửa ổn định (VD20).")
    kq = bao_loi_an_toan(models.khai_thac_mo_phong, r2, K2, H, P02, T2, thong_bao="Không mô phỏng được")
    if kq is not None:
        def ve_kt(ax):
            ax.plot(kq["t"], kq["P"], "k-"); ax.set_xlabel("t (năm)"); ax.set_ylabel("P (tấn)")
            for P_cb, _ in cb["can_bang"]:
                ax.axhline(P_cb, color="0.5", ls=":")
        hinh(ve_kt)
        if kq["t_tuyet_chung"] is not None:
            st.error(f"Quần thể chạm 0 tại t ≈ {kq['t_tuyet_chung']:.4f} năm; mô phỏng dừng tại đây.")
    nhan_mo_phong()


# ============================================================================ Bài 3
def mo_phong_bai3():
    cum = data.CUM_GIAO_KHOA
    st.caption("Mặc định: tình huống giáo khoa (Giordano–Fox–Horton 2014), β = aN = 1,407 tuần⁻¹ là **tham số cố định** "
               "lấy từ tài liệu.")
    chu_trinh("1")
    st.radio("Dự đoán: dịch kết thúc vì sao?", ["Vì mọi người đều đã mắc bệnh", "Vì số người cảm nhiễm giảm dưới một ngưỡng",
                                               "Vì β giảm dần"], index=None, key="b3_dd")
    chu_trinh("2")
    c1, c2, c3, c4, c5 = st.columns(5)
    N = c1.number_input("N (người)", 10.0, 1e9, cum["N"], 10.0, format="%.0f", key="b3_N")
    S0 = c2.number_input("S(0) (người)", 0.0, 1e9, cum["S0"], 1.0, format="%.1f", key="b3_S0")
    I0 = c3.number_input("I(0) (người)", 0.0, 1e9, cum["I0"], 1.0, format="%.1f", key="b3_I0")
    beta = c4.number_input("β (tuần⁻¹)", 0.0, 50.0, cum["beta"], 0.01, format="%.4f", key="b3_beta")
    gamma = c5.number_input("γ (tuần⁻¹)", 0.01, 50.0, cum["gamma"], 0.01, format="%.3f", key="b3_gamma")
    T = st.slider("Khoảng khảo sát (tuần)", 1, 200, 30, key="b3_T")
    R_bd = N - S0 - I0
    if R_bd < -1e-9 * N:
        st.error(f"Tổng dân số sai: S(0) + I(0) = {S0 + I0:g} vượt N = {N:g}. Hãy sửa điều kiện đầu.")
        return
    st.write(f"R(0) = N − S(0) − I(0) = {R_bd:g} người")
    R0 = models.so_sinh_san_co_ban(beta, gamma)
    kq = bao_loi_an_toan(models.sir_giai, S0, I0, N, beta, gamma, T, thong_bao="Bộ giải không thành công")
    if kq is None:
        return
    sol, t_dinh = kq
    tt = np.linspace(0, T, 600)
    S, I, R = sol.sol(tt)
    pk = models.sir_dinh_dich(S0, I0, N, beta, gamma)
    chu_trinh("3")
    png = hinh(lambda ax: (ax.plot(tt, S, "C0-", label="S(t)"), ax.plot(tt, I, "C3-", label="I(t) (đang nhiễm)"),
                           ax.plot(tt, R, "C2-", label="R(t)"),
                           ax.axvline(t_dinh, color="0.5", ls=":", label="đỉnh dịch") if t_dinh is not None else None,
                           ax.set_xlabel("t (tuần)"), ax.set_ylabel("số người"), ax.legend(fontsize=8)))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("𝓡₀ = β/γ", f"{R0:.4f}")
    c2.metric("𝓡_eff(0) = 𝓡₀·S(0)/N", f"{R0 * S0 / N:.4f}")
    if pk["noi_tai"]:
        c3.metric("Đỉnh dịch (công thức)", f"{pk['I_max']:.3f} người")
        if t_dinh is not None:
            c4.metric("Thời điểm đỉnh", f"{t_dinh:.3f} tuần")
        else:
            c4.warning("Đỉnh chưa xảy ra trong khoảng khảo sát — tăng T.")
    else:
        c3.info("𝓡_eff(0) ≤ 1: I giảm ngay từ đầu; không có đỉnh nội tại, giá trị lớn nhất là I(0).")
    if I0 > 0 and S0 > 0:
        Sinf = models.sir_quy_mo_cuoi(S0, I0, N, beta, gamma)
        st.write(f"Quy mô cuối: S∞ ≈ {Sinf:.3f} người không bao giờ mắc; số nhiễm tích lũy I(0) + S(0) − S∞ ≈ "
                 f"{I0 + S0 - Sinf:.3f}. Ngưỡng miễn dịch lý tưởng max(0, 1 − 1/𝓡₀) = {models.nguong_mien_dich(R0) * 100:.2f}%.")
    chu_trinh("4")
    st.markdown("Khi $I>0$: $I'>0\\iff\\mathcal R_{\\mathrm{eff}}(t)>1$. Điều kiện tăng ban đầu là $\\mathcal R_0S_0/N>1$, "
                "**không** chỉ $\\mathcal R_0>1$. Dịch kết thúc khi vẫn còn $S_\\infty>0$ người cảm nhiễm.")
    chu_trinh("5")
    st.write(f"Bảo toàn: max|S+I+R−N| = {np.max(np.abs(S + I + R - N)):.2e}; không âm: min S = {S.min():.3g}, "
             f"min I = {I.min():.3g}.")
    if pk["noi_tai"] and t_dinh is not None:
        st.write(f"Đỉnh trên nghiệm số {float(sol.sol(t_dinh)[1]):.6f} so với công thức {pk['I_max']:.6f}.")
    tai_hinh(png, "sir.png", key="b3_png")

    st.markdown("#### Số đang nhiễm, số nhiễm mới và số nhiễm tích lũy")
    tuan = np.arange(1, int(T) + 1)
    ca_moi = np.array([models.sir_ca_moi(sol, k - 1, k) for k in tuan])
    I_cuoi = np.array([float(sol.sol(k)[1]) for k in tuan])

    def ve2(ax):
        ax.bar(tuan - 0.2, ca_moi, width=0.4, label="số nhiễm mới trong tuần = S(k−1) − S(k)")
        ax.bar(tuan + 0.2, I_cuoi, width=0.4, label="I cuối tuần (đang nhiễm)")
        ax.set_xlabel("tuần"); ax.set_ylabel("số người"); ax.legend(fontsize=8)
    hinh(ve2)
    st.caption("Số ca báo cáo theo tuần phải so với **số nhiễm mới**, không phải với I(t).")
    tai_csv(pd.DataFrame({"tuan": tuan, "nhiem moi": ca_moi, "I cuoi tuan": I_cuoi,
                          "nhiem tich luy": I0 + S0 - np.array([float(sol.sol(k)[0]) for k in tuan])}),
            "sir_ca_moi.csv", key="b3_csv")

    st.markdown("#### Mặt phẳng pha (S, I)")

    def ve3(ax):
        if I0 > 0 and S0 > 0 and R0 > 0:
            Ss = N / R0
            ss = np.linspace(max(S.min(), 1e-9), S0, 400)
            ax.plot(ss, I0 + S0 - Ss * np.log(S0) - ss + Ss * np.log(ss), "k-", label="tích phân đầu")
            ax.axvline(Ss, color="0.5", ls="--", label="$S=N/\\mathcal{R}_0$")
        ax.plot(S, I, "C3:", lw=2.5, label="quỹ đạo tính số")
        ax.set_xlim(0, N); ax.set_ylim(0, None); ax.set_xlabel("S"); ax.set_ylabel("I"); ax.legend(fontsize=8)
    hinh(ve3)

    st.markdown("#### Hiệu chỉnh β: một bước Euler hay nghiệm liên tục")
    I1 = st.number_input("Số người ĐANG nhiễm sau 1 tuần (dữ kiện)", 0.1, 1e6, 9.0, 0.5, key="b3_I1")
    if S0 > 0 and I0 > 0:
        bE = models.sir_beta_tu_mot_buoc_euler(S0, I0, I1, N, gamma, 1.0)
        bC = bao_loi_an_toan(models.sir_hieu_chinh_beta, S0, I0, N, gamma, 1.0, I1, khoang=(1e-6, 50.0),
                             thong_bao="Không hiệu chỉnh được (khoảng tìm không chứa nghiệm)")
        c1, c2 = st.columns(2)
        c1.write(f"β từ một bước Euler: {bE:.6f} tuần⁻¹ → nghiệm liên tục cho I(1) = "
                 f"{models.sir_I_tai(1.0, S0, I0, N, bE, gamma):.4f}")
        if bC is not None:
            c2.write(f"β hiệu chỉnh liên tục (Brent, dung sai 1e−12): {bC:.6f} tuần⁻¹, 𝓡₀ = {bC / gamma:.5f}")
    nhan_mo_phong()


# ============================================================================ Bài 4
MAU_MA_TRAN = {"Nút hút": [[-3.0, 1.0], [1.0, -3.0]], "Yên ngựa": [[1.0, 2.0], [2.0, 1.0]],
               "Tiêu điểm hút": [[-0.4, 1.0], [-1.0, -0.4]], "Tâm": [[0.0, 1.0], [-1.0, 0.0]],
               "Nút suy biến": [[-1.0, 1.0], [0.0, -1.0]], "Tự nhập": None}


def mo_phong_bai4():
    st.markdown("#### A. Hệ tuyến tính $\\mathbf y'=A\\mathbf y$: trị riêng, phân loại, chân dung pha")
    chu_trinh("1")
    st.radio("Dự đoán: với $A=\\begin{pmatrix}0&1\\\\-1&0\\end{pmatrix}$ quỹ đạo có dạng gì?",
             ["xoắn vào gốc", "đường tròn quanh gốc", "đi thẳng ra xa"], index=None, key="b4_dd")
    chu_trinh("2")
    mau = st.selectbox("Ma trận mẫu", list(MAU_MA_TRAN), key="b4_mau")
    A0 = MAU_MA_TRAN[mau] or [[0.0, 1.0], [-2.0, -0.5]]
    c = st.columns(4)
    a11 = c[0].number_input("a₁₁", -10.0, 10.0, A0[0][0], 0.1, key=f"b4_a11_{mau}")
    a12 = c[1].number_input("a₁₂", -10.0, 10.0, A0[0][1], 0.1, key=f"b4_a12_{mau}")
    a21 = c[2].number_input("a₂₁", -10.0, 10.0, A0[1][0], 0.1, key=f"b4_a21_{mau}")
    a22 = c[3].number_input("a₂₂", -10.0, 10.0, A0[1][1], 0.1, key=f"b4_a22_{mau}")
    A = np.array([[a11, a12], [a21, a22]])
    lam, V = np.linalg.eig(A)
    loai = bao_loi_an_toan(he_tuyen_tinh.phan_loai_diem_can_bang_2x2, A, thong_bao="Không phân loại được")
    chu_trinh("3")
    c1, c2 = st.columns(2)
    with c1:
        def ve(ax):
            for g in np.linspace(0, 2 * np.pi, 12, endpoint=False) + 0.13:
                y0 = 1.6 * np.array([np.cos(g), np.sin(g)])
                ts = np.linspace(-2, 2, 300) if loai == "yên ngựa" else np.linspace(0, 6, 300)
                Y = np.array([he_tuyen_tinh.nghiem_ma_tran_mu(A, y0 * (0.25 if loai == "yên ngựa" else 1), t) for t in ts])
                ax.plot(Y[:, 0], Y[:, 1], "k-", lw=0.8)
                k = len(ts) // 3
                ax.annotate("", xy=Y[k + 1], xytext=Y[k], arrowprops=dict(arrowstyle="->", color="k"))
            for j in range(2):
                if abs(lam[j].imag) < 1e-12:
                    v = V[:, j].real / np.linalg.norm(V[:, j].real)
                    ax.plot([-2 * v[0], 2 * v[0]], [-2 * v[1], 2 * v[1]], "C3--", lw=1)
            ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_aspect("equal"); ax.set_title(f"Chân dung pha: {loai}")
        hinh(ve, (4.6, 4.4))
    with c2:
        y0 = np.array([1.0, 0.5])
        ts = np.linspace(0, 6, 300)
        Y = np.array([he_tuyen_tinh.nghiem_ma_tran_mu(A, y0, t) for t in ts])
        hinh(lambda ax: (ax.plot(ts, Y[:, 0], "C0-", label="x(t)"), ax.plot(ts, Y[:, 1], "C3--", label="y(t)"),
                         ax.set_xlabel("t"), ax.legend(fontsize=8), ax.set_title("Theo thời gian, y(0) = (1; 0,5)")),
             (4.6, 4.4))
    st.write("Trị riêng: " + ", ".join(f"{z.real:.4g}" + (f" {z.imag:+.4g}i" if abs(z.imag) > 1e-12 else "") for z in lam)
             + f"; vết = {np.trace(A):.4g}, định thức = {np.linalg.det(A):.4g}.")
    chu_trinh("4")
    st.markdown("Hai hình là **hai cách nhìn cùng một nghiệm**: mặt phẳng pha bỏ trục thời gian, đồ thị bên phải giữ "
                "thời gian. Đường đứt nét đỏ là các vectơ riêng thực (nghiệm đi thẳng dọc theo chúng).")
    chu_trinh("5")
    if np.max(np.abs(lam.imag)) > 1e-12:
        r_ = he_tuyen_tinh.nghiem_thuc_tu_tri_rieng_phuc(A)
        st.write(f"Kiểm chứng nghiệm thực từ trị riêng phức: phần dư u₁ = {he_tuyen_tinh.residual(A, r_['u1'], 0.3):.1e}, "
                 f"u₂ = {he_tuyen_tinh.residual(A, r_['u2'], 0.3):.1e}.")
    sol = solve_ivp(lambda t, y: A @ y, [0, 2], [1.0, 0.5], rtol=1e-11, atol=1e-13)
    st.write(f"Kiểm chứng ma trận mũ: |expm(2A)y₀ − nghiệm bộ giải| = "
             f"{np.max(np.abs(he_tuyen_tinh.nghiem_ma_tran_mu(A, [1.0, 0.5], 2.0) - sol.y[:, -1])):.1e}.")

    st.markdown("#### B. Hai loài: cạnh tranh và thú – mồi")
    mh = st.radio("Mô hình", ["Cạnh tranh x' = (a − by)x, y' = (m − nx)y", "Thú – mồi x' = (a − by)x, y' = (−m + nx)y"],
                  key="b4_mh")
    c = st.columns(6)
    a = c[0].number_input("a", 0.01, 5.0, 1.0, 0.05, key="b4_a")
    bb = c[1].number_input("b", 0.01, 5.0, 1.0 if mh.startswith("Cạnh") else 0.5, 0.05, key=f"b4_b_{mh[:3]}")
    m = c[2].number_input("m", 0.01, 5.0, 0.5 if mh.startswith("Cạnh") else 0.75, 0.05, key=f"b4_m_{mh[:3]}")
    n = c[3].number_input("n", 0.01, 5.0, 0.5 if mh.startswith("Cạnh") else 0.25, 0.05, key=f"b4_n_{mh[:3]}")
    x0 = c[4].number_input("x(0)", 0.01, 50.0, 0.4 if mh.startswith("Cạnh") else 4.0, 0.1, key=f"b4_x0_{mh[:3]}")
    y0_ = c[5].number_input("y(0)", 0.01, 50.0, 0.3 if mh.startswith("Cạnh") else 1.0, 0.1, key=f"b4_y0_{mh[:3]}")
    f = models.canh_tranh_rhs(a, bb, m, n) if mh.startswith("Cạnh") else models.lotka_volterra_rhs(a, bb, m, n)
    can_bang = (m / n, a / bb)

    def ra_ngoai(t, u):
        return max(u[0], u[1]) - 20 * max(can_bang)
    ra_ngoai.terminal = True
    s = solve_ivp(f, [0, 60], [x0, y0_], method="DOP853", rtol=1e-10, atol=1e-12, max_step=0.05, events=ra_ngoai)
    J = (np.array([[0, -bb * can_bang[0]], [-n * can_bang[1], 0]]) if mh.startswith("Cạnh")
         else np.array([[0, -bb * can_bang[0]], [n * can_bang[1], 0]]))
    lamJ = np.linalg.eigvals(J)
    c1, c2 = st.columns(2)
    with c1:
        hinh(lambda ax: (ax.plot(s.y[0], s.y[1], "k-"), ax.plot(*can_bang, "C3o"), ax.set_xlabel("x"), ax.set_ylabel("y"),
                         ax.set_title("Mặt phẳng pha")), (4.6, 4.0))
    with c2:
        hinh(lambda ax: (ax.plot(s.t, s.y[0], "C0-", label="x"), ax.plot(s.t, s.y[1], "C3--", label="y"),
                         ax.set_xlabel("t"), ax.legend(fontsize=8), ax.set_title("Theo thời gian")), (4.6, 4.0))
    st.write(f"Điểm cân bằng trong: ({can_bang[0]:.4g}; {can_bang[1]:.4g}); trị riêng Jacobi tại đó: "
             + ", ".join(f"{z.real:.3g}{z.imag:+.3g}i" for z in lamJ) + ".")
    if mh.startswith("Cạnh"):
        st.info("Trị riêng trái dấu: yên ngựa. Đường phân cách (đa tạp ổn định) chia trạng thái đầu thành hai miền; "
                "trạng thái đầu nằm đúng trên đó tiến về điểm cùng tồn tại. Mô hình không có tự giới hạn nên loài thắng tăng "
                "không bị chặn (mô phỏng dừng khi ra khỏi khung).")
    else:
        V = [models.lotka_volterra_bat_bien(s.y[:, k], a, bb, m, n) for k in (0, -1)]
        st.info(f"Trị riêng thuần ảo: tuyến tính hóa **chưa** kết luận; kết luận quỹ đạo kín đến từ bất biến "
                f"V = nx − m ln x + by − a ln y (lệch sau mô phỏng: {abs(V[1] - V[0]):.1e}).")
    nhan_mo_phong()
