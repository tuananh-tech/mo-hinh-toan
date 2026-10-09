"""Hướng dẫn giảng viên, nguồn và trạng thái kiểm chứng (đọc từ các báo cáo đã sinh, có ngày chạy)."""
import io
import json

import pandas as pd
import streamlit as st

from tien_ich import doc_tep

st.title("Giảng viên: hướng dẫn, nguồn và trạng thái kiểm chứng")
tab1, tab2, tab3 = st.tabs(["Hướng dẫn giảng viên", "Nguồn", "Trạng thái kiểm chứng"])
with tab1:
    st.markdown("""
**Tổ chức một buổi (90 phút)** theo sáu pha: P1 khởi động từ hiện tượng (10') → P2 hình thành mô hình (25') →
P3 giải và phân tích (20–25') → P4 diễn giải hoặc mô phỏng (10–20') → P5 kiểm định và phản biện (10–15') → P6 mở rộng (5–10').
Tiến trình chi tiết, phiếu học tập, đáp án, gợi ý theo mức và ma trận đánh giá: Phụ lục C của đồ án và tệp
`phieu_hoc_tap.pdf` (trang Tải xuống).

**Dùng website trên lớp.** Yêu cầu người học ghi dự đoán (bước 1 của mỗi bài, câu hỏi dự đoán trong bước Mô phỏng)
*trước* khi thay tham số. Dùng video ở pha P1 hoặc P5; dừng video tại câu hỏi dừng.

**Lỗi thường gặp cần chủ động tạo tình huống:**
- nhầm tốc độ của toàn quần thể với tốc độ tăng trưởng riêng; dùng $1+r$ thay cho $e^r$;
- trộn hai dạng viết logistic ($r$ với $k=r/K$); lấy giá trị lớn nhất quan sát làm $K$;
- gọi $\\beta S_0/(\\gamma N)$ là $\\mathcal R_0$; kết luận ``$\\mathcal R_0>1$ thì dịch luôn bùng phát'';
- so sánh số ca báo cáo với $I(t)$ thay vì số nhiễm mới;
- tin kết quả Euler bước lớn; ``sửa'' số âm bằng cách cắt về 0;
- kết luận tâm từ trị riêng thuần ảo của hệ phi tuyến.

**Rubric** bảy tiêu chí × bốn mức (Phụ lục C) là **công cụ đề xuất**, chưa được kiểm định độ tin cậy và độ giá trị.
Các bài giảng chưa được dạy thử; website không thu thập dữ liệu người học.
""")
with tab2:
    st.markdown("""
- F. R. Giordano, W. P. Fox, S. B. Horton, *A First Course in Mathematical Modeling*, 5th ed., Cengage, 2014 — dữ liệu nấm men
  (Bảng 11.1, tr. 466), dân số Hoa Kỳ (tr. 463), tình huống cúm (tr. 51–52, 564–565), hai loài (tr. 531–547).
- R. Pearl (1927), dữ liệu nấm men (trích qua Giordano).
- H. W. Hethcote, The mathematics of infectious diseases, *SIAM Review* 42 (2000) 599–653 — mô hình dịch cổ điển, $\\mathcal R_0$,
  định lý ngưỡng (tr. 602–612).
- R. L. Burden, J. D. Faires, *Numerical Analysis*, 9th ed., 2011 — Euler, Runge–Kutta, ổn định (Chương 5).
- D. G. Zill, *Differential Equations with Modeling Applications*, 12th ed., 2024 — hệ tuyến tính (Chương 8).
- J. Stewart, *Calculus*, 7th ed., 2012.
- Tài liệu MATLAB (ode45, ode15s, odeset), Streamlit, Manim Community (truy cập 10/2026).

Danh mục đầy đủ có số trang ở phần Tài liệu tham khảo của đồ án.
""")
with tab3:
    st.markdown("Bảng dưới đây **đọc từ các báo cáo đã sinh khi chạy kiểm thử** (không chạy lại khi mở trang).")
    tom_tat = doc_tep("matlab", "ket_qua_matlab", "tom_tat_chay.csv")
    kc = doc_tep("matlab", "ket_qua_matlab", "kiem_chung.csv")
    if kc:
        bang = pd.read_csv(io.StringIO(kc))
        st.markdown(f"**MATLAB** (R2025a, chạy thật): {int(bang['dat'].sum())}/{len(bang)} kiểm tra đạt.")
        st.dataframe(bang[["nhom", "ten", "gia_tri", "ky_vong", "dung_sai", "dat"]], hide_index=True)
    else:
        st.warning("Chưa có kết quả chạy MATLAB (ket_qua_matlab/kiem_chung.csv).")
    if tom_tat:
        st.dataframe(pd.read_csv(io.StringIO(tom_tat)), hide_index=True)
    py = doc_tep("ket_qua", "kiem_thu_python.json")
    if py:
        kq = json.loads(py)
        st.markdown(f"**Python** ({kq.get('thoi_diem', '')}): {kq.get('dat', 0)} đạt, {kq.get('khong_dat', 0)} không đạt.")
    td = doc_tep("ket_qua", "kiem_tra_trinh_duyet.json")
    if td:
        kq = json.loads(td)
        st.markdown(f"**Trình duyệt thật** ({kq.get('thoi_diem', '')}, {kq.get('trinh_duyet', '')}): "
                    f"{kq.get('so_trang_dat', 0)}/{kq.get('so_trang', 0)} trang hiển thị không lỗi ở hai cỡ màn hình.")
    st.markdown("""
**Chưa kiểm chứng:** hiệu quả sư phạm (chưa dạy thử); độ tin cậy, độ giá trị của rubric; thẩm định mô hình SIR với dữ liệu
dịch thật. Website chạy Python; MATLAB chỉ được chạy riêng (không tích hợp MATLAB Engine).
""")
