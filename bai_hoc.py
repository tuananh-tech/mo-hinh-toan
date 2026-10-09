"""Khung trình bày một bài học theo luồng thống nhất:
Hiện tượng → Kiến thức chuẩn bị → Giả thiết → Phương trình → Mô phỏng → Video → Ví dụ → Luyện tập → MATLAB → Giới hạn."""
import streamlit as st

from ngan_hang_bai_tap import BAI_TAP
from noi_dung import BAI_HOC
from tien_ich import danh_muc_vi_du, doc_tep, hien_bai_tap, hien_video, nut_tai_matlab, so_lieu_vi_du

# "1 · ..." (không dùng "1. ": Markdown biến thành danh sách; ký tự ①–⑩ không hiển thị trên mọi phông)
CAC_BUOC = [f"{i} · {ten}" for i, ten in enumerate(
    ["Hiện tượng", "Kiến thức chuẩn bị", "Giả thiết", "Phương trình", "Mô phỏng",
     "Video", "Ví dụ", "Luyện tập", "MATLAB", "Giới hạn"], start=1)]


def hien_thi_bai(ma: str, mo_phong):
    bai = BAI_HOC[ma]
    st.title(bai["ten"])
    st.caption(f"Tương ứng {bai['chuong']}. Học lần lượt các bước từ trái sang phải.")
    with st.expander("Mục tiêu bài học (đo được)", expanded=False):
        for m in bai["muc_tieu"]:
            st.markdown(f"- {m}")
    tabs = st.tabs(CAC_BUOC)
    with tabs[0]:
        st.markdown(bai["hien_tuong"])
        st.text_area("Dự đoán của em trước khi học (ghi lại để đối chiếu ở bước 10)", key=f"{ma}_du_doan", height=70)
    with tabs[1]:
        st.markdown(bai["kien_thuc"])
    with tabs[2]:
        st.markdown(bai["gia_thiet"])
        st.info("Mỗi giả thiết ứng với một số hạng của phương trình; khi mô hình không khớp dữ liệu, hãy truy ngược giả thiết.")
    with tabs[3]:
        st.markdown(bai["phuong_trinh"])
    with tabs[4]:
        mo_phong()
    with tabs[5]:
        for ma_video in bai["video"]:
            hien_video(ma_video)
    with tabs[6]:
        dm, so_lieu = danh_muc_vi_du(), so_lieu_vi_du()
        st.markdown("Lời giải đầy đủ (tình huống → mục tiêu → dữ liệu → giả thiết → lập mô hình → giải → kiểm tra → "
                    "diễn giải → giới hạn → mở rộng) ở **Phụ lục A** của đồ án. Số liệu dưới đây được tính lại bằng module chung.")
        for vd in bai["vi_du"]:
            tt = dm.get(vd, {})
            with st.expander(f"{vd} — {tt.get('tieu_de', '')} ({tt.get('muc', '')})"):
                if tt.get("tom_tat"):
                    st.markdown(tt["tom_tat"])
                if vd in so_lieu:
                    st.json(so_lieu[vd], expanded=False)
    with tabs[7]:
        muc = st.radio("Mức", ["Tất cả", "Cơ bản", "Vận dụng", "Mở rộng"], horizontal=True, key=f"{ma}_muc")
        for i, bt in enumerate(b for b in BAI_TAP if b["bai"] == ma):
            if muc == "Tất cả" or bt["muc"] == muc:
                hien_bai_tap(bt, key=f"{ma}_{bt['ma']}")
    with tabs[8]:
        st.markdown("Website chạy mô phỏng bằng **Python**; mã **MATLAB** dưới đây cài đặt cùng thuật toán và đã được chạy, "
                    "đối chiếu với Python trong MATLAB R2025a (xem trang *Giảng viên và kiểm chứng*). Tải về và chạy trong "
                    "MATLAB: đặt thư mục hiện hành là thư mục chứa mã.")
        for ten in bai["matlab"]:
            nut_tai_matlab(ten, key=f"{ma}_{ten}")
            ma_nguon = doc_tep("matlab", ten)
            if ma_nguon:
                with st.expander(f"Xem {ten}"):
                    st.code(ma_nguon, language="matlab")
    with tabs[9]:
        st.markdown(bai["gioi_han"])
        if st.session_state.get(f"{ma}_du_doan"):
            st.info(f"Dự đoán ban đầu của em: *{st.session_state[f'{ma}_du_doan']}* — dự đoán đó đúng ở điểm nào, sai ở điểm nào?")
