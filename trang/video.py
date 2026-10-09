"""Tất cả video: mục tiêu, video kèm phụ đề, câu hỏi dừng có mốc thời gian, bản chép lời, bài tập liên quan."""
import streamlit as st

from tien_ich import hien_video, thong_tin_video

st.title("Video hoạt hình (Manim) và câu hỏi dừng")
st.markdown("Video **không có âm thanh**. Lời thuyết minh được cung cấp dưới dạng **phụ đề tiếng Việt** và bản chép lời; "
            "giảng viên có thể đọc hoặc thu âm riêng. Tại mỗi câu hỏi dừng, hãy dừng video và trả lời trước khi xem tiếp.")
tt = thong_tin_video()
if not tt:
    st.warning("Chưa có tệp thong_tin_video.json (sinh khi kết xuất video bằng hoc_lieu/manim/ket_xuat.py).")
for ma in sorted(tt):
    # khung có viền (không dùng expander: hien_video đã có expander bản chép lời, Streamlit cấm lồng expander)
    with st.container(border=True):
        st.caption(f"Thời lượng {tt[ma].get('thoi_luong', 0):.0f} s")
        hien_video(ma)
        if tt[ma].get("bai_tap"):
            st.markdown("**Bài tập liên quan:** " + ", ".join(tt[ma]["bai_tap"]))
