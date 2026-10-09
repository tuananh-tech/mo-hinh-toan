"""Trang giới thiệu và lộ trình học."""
import streamlit as st

from noi_dung import BAI_HOC, LO_TRINH

st.title("Mô hình toán học cho một số hiện tượng tự nhiên")
st.markdown("""
Website học tập đi kèm đồ án thạc sĩ *Xây dựng bài giảng về mô hình toán học cho một số hiện tượng tự nhiên*.
Ba hiện tượng trung tâm: **tăng trưởng không giới hạn** (Malthus), **tăng trưởng có giới hạn** (logistic),
**lan truyền dịch bệnh** (SIR); bài mở rộng về **hệ phương trình vi phân và mặt phẳng pha**.

**Cách học mỗi bài.** Đi lần lượt qua mười bước:
*Hiện tượng → Kiến thức chuẩn bị → Giả thiết → Phương trình → Mô phỏng → Video → Ví dụ → Luyện tập → MATLAB → Giới hạn*.
Trong bước Mô phỏng, luôn **dự đoán trước** rồi mới thay tham số, quan sát, giải thích và **kiểm chứng**.
""")
st.subheader("Lộ trình cho người mới")
st.markdown(LO_TRINH)
st.subheader("Các bài học")
for ma, bai in BAI_HOC.items():
    with st.container(border=True):
        st.markdown(f"**{bai['ten']}** — {bai['chuong']}")
        st.markdown("\n".join(f"- {m}" for m in bai["muc_tieu"][:3]))
st.subheader("Điều cần biết")
st.markdown("""
* Mọi con số được tính bằng **cùng một module Python** (`hoc_lieu/mhtoan`) với đồ án, mã MATLAB và video.
* Website chạy mô phỏng bằng **Python**. Mã **MATLAB** cùng thuật toán được cung cấp để tải và chạy trong MATLAB;
  website **không** chạy MATLAB.
* Dữ liệu quan sát luôn ghi nguồn; tình huống cúm là **tình huống giáo khoa**, không phải số liệu một đợt dịch thật.
* Các bài giảng, bài tập, rubric và website là **thiết kế đề xuất**, chưa được dạy thử với người học.
* Website không cần đăng nhập, không lưu dữ liệu người dùng, không gửi dữ liệu ra ngoài; tệp CSV tải lên chỉ được đọc
  như số liệu.
""")
