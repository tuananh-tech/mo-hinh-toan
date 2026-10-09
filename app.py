"""Website học mô hình toán học cho một số hiện tượng tự nhiên (đi kèm đồ án thạc sĩ).

Chạy cục bộ (từ thư mục gốc của dự án):
    python -m pip install -r hoc_lieu/requirements.txt
    streamlit run hoc_lieu/streamlit_app/app.py
"""
import streamlit as st

st.set_page_config(page_title="Mô hình toán học cho hiện tượng tự nhiên", page_icon="📈", layout="wide")

trang = {
    "Bắt đầu": [st.Page("trang/trang_chu.py", title="Giới thiệu và lộ trình", icon="🏠", default=True)],
    "Bài học": [
        st.Page("trang/bai_1.py", title="Bài 1. Malthus", icon="1️⃣"),
        st.Page("trang/bai_2.py", title="Bài 2. Logistic", icon="2️⃣"),
        st.Page("trang/bai_3.py", title="Bài 3. SIR", icon="3️⃣"),
        st.Page("trang/bai_4.py", title="Bài 4. Hệ và mặt phẳng pha", icon="4️⃣"),
    ],
    "Công cụ": [
        st.Page("trang/cong_cu_so.py", title="So sánh phương pháp số", icon="🧮"),
        st.Page("trang/cong_cu_khop.py", title="Khớp mô hình với dữ liệu", icon="📊"),
        st.Page("trang/cong_cu_can_thiep.py", title="Can thiệp và SEIR", icon="💉"),
    ],
    "Tài nguyên": [
        st.Page("trang/video.py", title="Video và câu hỏi dừng", icon="🎬"),
        st.Page("trang/bai_tap.py", title="Ngân hàng bài tập", icon="✍️"),
        st.Page("trang/tai_xuong.py", title="Tải xuống", icon="⬇️"),
        st.Page("trang/giang_vien.py", title="Giảng viên và kiểm chứng", icon="🧑‍🏫"),
    ],
}

from pathlib import Path

tep_phieu = Path(__file__).resolve().parent / "phieu_hoc_tap.pdf"

if tep_phieu.is_file():
    st.sidebar.download_button(
        label="📄 Tải phiếu học tập (PDF)",
        data=tep_phieu.read_bytes(),
        file_name="phieu_hoc_tap.pdf",
        mime="application/pdf",
        key="tai_phieu_hoc_tap_sidebar",
    )
else:
    st.sidebar.warning("Không tìm thấy phieu_hoc_tap.pdf")
st.navigation(trang).run()
