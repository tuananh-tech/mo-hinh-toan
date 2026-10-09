"""Tiện ích giao diện dùng chung của website. Toán học nằm trong hoc_lieu/mhtoan; tệp này không chứa công thức mô hình.

Nguyên tắc an toàn: website KHÔNG thực thi mã do người dùng nhập; tệp CSV tải lên chỉ được đọc như dữ liệu số,
xử lý trên máy chạy ứng dụng, không gửi ra ngoài.
"""
from __future__ import annotations

import io
import json
import os
import sys
import zipfile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

THU_MUC_APP = os.path.dirname(os.path.abspath(__file__))
THU_MUC_HOC_LIEU = THU_MUC_APP
if THU_MUC_HOC_LIEU not in sys.path:
    sys.path.insert(0, THU_MUC_HOC_LIEU)

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mhtoan import analysis, data, he_tuyen_tinh, models, solvers  # noqa: E402,F401

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.grid": True,
                     "grid.color": "0.88", "lines.linewidth": 1.6, "mathtext.fontset": "dejavusans"})

DON_VI_THOI_GIAN = {"giờ": 1.0, "ngày": 24.0, "tuần": 168.0, "năm": 8766.0}


# ------------------------------------------------------------------ hiển thị chung
def chu_trinh(buoc: str):
    """Vị trí trong luồng: dự đoán → thay tham số → quan sát → giải thích → kiểm chứng."""
    cac_buoc = ["1. Dự đoán", "2. Thay tham số", "3. Quan sát", "4. Giải thích", "5. Kiểm chứng"]
    st.markdown(" → ".join(f"**{b}**" if b.startswith(buoc) else b for b in cac_buoc))


def nhan_mo_phong():
    st.caption("Kết quả là **mô phỏng/xấp xỉ** của mô hình toán học (Python, module `mhtoan`), không phải số liệu "
               "quan sát, trừ khi được ghi rõ là dữ liệu quan sát có nguồn. Website không chạy MATLAB; mã MATLAB "
               "tương ứng được cung cấp để tải và chạy riêng.")


def hinh(ve, kich_thuoc=(6.4, 3.6)):
    """Vẽ bằng ve(ax) rồi hiển thị; trả về bytes PNG để tải xuống."""
    fig, ax = plt.subplots(figsize=kich_thuoc)
    ve(ax)
    fig.tight_layout()
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    return buf.getvalue()


def tai_csv(df: pd.DataFrame, ten_tep: str, mo_ta="Tải dữ liệu (CSV)", key=None):
    st.download_button(mo_ta, df.to_csv(index=False).encode("utf-8"), file_name=ten_tep, mime="text/csv",
                       key=key or f"csv_{ten_tep}")


def tai_hinh(png: bytes, ten_tep: str, key=None):
    st.download_button("Tải hình (PNG)", png, file_name=ten_tep, mime="image/png", key=key or f"png_{ten_tep}")


def bao_loi_an_toan(ham, *args, thong_bao="Không tính được", **kwargs):
    """Gọi một hàm tính toán; nếu lỗi (tham số ngoài miền, solver không hội tụ, dữ liệu sai) thì hiện thông báo
    rõ ràng thay vì làm hỏng trang. Trả về None khi lỗi."""
    try:
        return ham(*args, **kwargs)
    except (ValueError, ArithmeticError, analysis.DuLieuKhongHopLe, solvers.KhongHoiTu, RuntimeError) as e:
        st.error(f"{thong_bao}: {e}")
        return None


# ------------------------------------------------------------------ tệp và học liệu
def doc_tep(*duong_dan, che_do="r"):
    p = os.path.join(THU_MUC_HOC_LIEU, *duong_dan)
    if not os.path.exists(p):
        return None
    with open(p, che_do, **({} if "b" in che_do else {"encoding": "utf-8"})) as fh:
        return fh.read()


def nut_tai_matlab(ten: str, key=None):
    noi_dung = doc_tep("matlab", ten)
    if noi_dung is None:
        st.warning(f"Không tìm thấy {ten}.")
        return
    st.download_button(f"Tải {ten}", noi_dung, file_name=ten, mime="text/plain", key=key or f"m_{ten}")


def zip_thu_muc(*duong_dan, duoi=(".m", ".md", ".csv")) -> bytes:
    goc = os.path.join(THU_MUC_HOC_LIEU, *duong_dan)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for ten in sorted(os.listdir(goc)):
            if ten.endswith(duoi):
                z.write(os.path.join(goc, ten), ten)
    return buf.getvalue()


@st.cache_data
def danh_muc_vi_du() -> dict:
    """Danh mục VD (mã → tiêu đề, mức) sinh từ Phụ lục A bằng hoc_lieu/scripts/kho_vi_du.py."""
    s = doc_tep("ket_qua", "danh_muc_vd.json")
    return json.loads(s) if s else {}


@st.cache_data
def so_lieu_vi_du() -> dict:
    s = doc_tep("ket_qua", "kho_vi_du.json")
    return json.loads(s) if s else {}


@st.cache_data
def thong_tin_video() -> dict:
    s = doc_tep("video", "thong_tin_video.json")
    return json.loads(s) if s else {}


def hien_video(ma: str):
    """Video + phụ đề (.srt, nếu có) + bản chép lời + câu hỏi dừng (mốc thời gian lấy khi kết xuất)."""
    tt = thong_tin_video().get(ma, {})
    st.markdown(f"**{ma[:3].rstrip('_')}. {tt.get('tieu_de', ma)}**")
    tep = os.path.join(THU_MUC_HOC_LIEU, "video", f"{ma}.mp4")
    srt = os.path.join(THU_MUC_HOC_LIEU, "video", f"{ma}.vi.srt")
    if os.path.exists(tep):
        st.video(tep, subtitles={"Tiếng Việt": srt} if os.path.exists(srt) else None)
    else:
        st.warning("Chưa có video đã kết xuất cho cảnh này (xem hoc_lieu/manim/README.md).")
        return
    if tt.get("muc_tieu"):
        st.caption("Mục tiêu: " + tt["muc_tieu"])
    for c in tt.get("cau_hoi_dung", []):
        st.markdown(f"⏸ **{c['t']:.0f} s** — {c['cau_hoi']}  \n*Gợi ý trả lời:* {c.get('goi_y', '')}")
    if tt.get("loi_thuyet_minh"):
        with st.expander("Bản chép lời thuyết minh (video không có âm thanh; phụ đề hiển thị cùng nội dung)"):
            for doan in tt["loi_thuyet_minh"]:
                st.markdown(f"[{doan['t0']:.0f}–{doan['t1']:.0f} s] {doan['text']}")


# ------------------------------------------------------------------ bài tập
def hien_bai_tap(bt: dict, key: str):
    """Một bài tập: đề, gợi ý mở dần ba mức, ô trả lời, chấm (số/chọn), đáp án và giải thích."""
    with st.container(border=True):
        st.markdown(f"**[{bt['ma']}] · {bt['muc']} · {bt['dang']}**  \n{bt['de']}")
        k_goi_y = f"goi_y_{key}"
        so_muc = st.session_state.get(k_goi_y, 0)
        for i in range(so_muc):
            st.info(f"Gợi ý mức {i + 1}: {bt['goi_y'][i]}")
        c1, c2 = st.columns([1, 3])
        if so_muc < len(bt["goi_y"]) and c1.button(f"Gợi ý mức {so_muc + 1}", key=f"nut_{key}"):
            st.session_state[k_goi_y] = so_muc + 1
            st.rerun()
        if bt["loai"] == "so":
            tl = c2.number_input("Câu trả lời", value=None, format="%.6f", key=f"tl_{key}")
            if tl is not None:
                dung = abs(tl - bt["dap_an"]()) <= bt["dung_sai"]
                (st.success if dung else st.error)("Đúng." if dung else "Chưa đúng — xem gợi ý từng mức rồi thử lại.")
        elif bt["loai"] == "chon":
            tl = c2.radio("Chọn một phương án", bt["lua_chon"], index=None, key=f"tl_{key}")
            if tl is not None:
                dung = bt["lua_chon"].index(tl) == bt["dap_an"]
                (st.success if dung else st.error)("Đúng." if dung else "Chưa đúng — xem gợi ý từng mức rồi thử lại.")
        else:
            c2.text_area("Câu trả lời của em (tự đối chiếu với đáp án mẫu)", key=f"tl_{key}", height=80)
        with st.expander("Đáp án và giải thích"):
            if bt["loai"] == "so":
                st.markdown(f"Đáp án: **{bt['dap_an']():.6g}** (dung sai ±{bt['dung_sai']:g}).")
            elif bt["loai"] == "chon":
                st.markdown(f"Đáp án: **{bt['lua_chon'][bt['dap_an']]}**")
            else:
                st.markdown(f"Đáp án mẫu: {bt['dap_an']}")
            for buoc in bt.get("giai_thich", []):
                st.markdown(f"- {buoc}")


# ------------------------------------------------------------------ dữ liệu tải lên
def doc_csv_tai_len(tep, cot_t="t", cot_P="P"):
    """Đọc CSV của người dùng như DỮ LIỆU (không thực thi gì); kiểm tra: đúng cột, không thiếu giá trị, là số,
    t tăng ngặt, P > 0, ít nhất 3 điểm. Báo lỗi analysis.DuLieuKhongHopLe kèm lý do cụ thể."""
    try:
        df = pd.read_csv(tep)
    except Exception as e:  # noqa: BLE001 - mọi lỗi đọc tệp đều trả về thông báo dữ liệu không hợp lệ
        raise analysis.DuLieuKhongHopLe(f"không đọc được tệp CSV ({e})") from e
    thieu = [c for c in (cot_t, cot_P) if c not in df.columns]
    if thieu:
        raise analysis.DuLieuKhongHopLe(f"thiếu cột {', '.join(thieu)} (cần đúng hai cột '{cot_t}', '{cot_P}')")
    if df[[cot_t, cot_P]].isna().any().any():
        raise analysis.DuLieuKhongHopLe("có ô trống (dữ liệu thiếu); hãy bỏ hoặc bổ sung các dòng đó")
    t = pd.to_numeric(df[cot_t], errors="coerce").to_numpy(float)
    P = pd.to_numeric(df[cot_P], errors="coerce").to_numpy(float)
    if np.isnan(t).any() or np.isnan(P).any():
        raise analysis.DuLieuKhongHopLe("có giá trị không phải số (ví dụ dấu phẩy thập phân '1,5' thay vì '1.5')")
    if len(t) < 3:
        raise analysis.DuLieuKhongHopLe("cần ít nhất 3 quan sát")
    return analysis.kiem_tra_du_lieu(t, P)
