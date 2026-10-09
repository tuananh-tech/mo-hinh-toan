# Bộ học liệu số kèm đồ án thạc sĩ

Bộ học liệu đi kèm đồ án thạc sĩ *"Xây dựng bài giảng về mô hình Toán cho một số hiện tượng tự nhiên"*.
Mọi thành phần dùng chung **một** gói tính toán `mhtoan/`, nên các con số khớp nhau giữa văn bản đồ án, kho ví dụ (Phụ lục A), website, video và bài tập. Mã MATLAB là một cài đặt độc lập của cùng các thuật toán và được đối chiếu với Python.

Bài giảng, phiếu, rubric, website và video là **thiết kế đề xuất**. Chúng chưa được dạy thử, nên chưa có bằng chứng về hiệu quả sư phạm. Rubric là công cụ đề xuất, chưa được kiểm định.

## Cấu trúc và trạng thái kiểm chứng (lần chạy 03–04/10/2026)

| Thư mục / tệp | Nội dung | Trạng thái |
|---|---|---|
| `mhtoan/` | Mô hình (Malthus, logistic, khai thác, SIR, SEIR, thuốc, phanh, hai loài, dao động); phương pháp số (Euler, Heun, điểm giữa, Taylor 2, RK4, AB2, Euler ẩn, hình thang ẩn); khớp dữ liệu; hệ tuyến tính (`he_tuyen_tinh.py`) | 35 kiểm thử đạt |
| `streamlit_app/` | Website: `app.py` (điều hướng), `trang/` (12 trang), `bai_hoc.py`, `mo_phong.py`, `cong_cu.py`, `noi_dung.py`, `ngan_hang_bai_tap.py` (33 bài), `tien_ich.py` | AppTest 10/10; trình duyệt thật 24/24 (Chrome 154, 2 cỡ màn hình) |
| `manim/` | `canh.py` (9 cảnh), `ket_xuat.py`, `sinh_kich_ban.py`; `video/` gồm MP4 1080p60, phụ đề `.vi.srt`, `thong_tin_video.json`; `kich_ban.md` (sinh tự động) | Đã kết xuất, kiểm tra khung hình. **Không có âm thanh** |
| `matlab/` | 28 hàm `mh_*`, 8 script `vd_*`, `kiem_chung.m`, `chay_tat_ca.m`; kết quả trong `ket_qua_matlab/` | **Chạy thật** trên MATLAB R2025a: 9/9 script, 78/78 kiểm tra |
| `scripts/` | Sinh hình, số liệu, danh mục ví dụ (`danh_muc_vi_du.py`), mục bài luyện tập của Phụ lục A (`xuat_bai_tap_tex.py`), bảng kết quả MATLAB của Phụ lục D (`xuat_ket_qua_matlab_tex.py`), giá trị đối chiếu (`xuat_doi_chieu_matlab.py`), kiểm tra bản thảo cũ (`kiem_tra_main1.py`) | Đã chạy |
| `tests/` | `chay_kiem_tra.py` (chạy mọi `test_*`), `kiem_tra_trinh_duyet.py` (Chrome qua CDP) | Xem trên |
| `ket_qua/` | JSON/CSV kết quả, ảnh chụp trình duyệt (`trinh_duyet/`) | — |
| `phieu_hoc_tap/` | Bản in phiếu học tập (13 trang), dùng chung nguồn với Phụ lục C | Đã biên dịch |
| `_luu_tru/` | Website đợt 2 (`streamlit_dot2/`), kịch bản video đợt 2 | Lưu trữ, không dùng |

## Cài đặt và chạy (từ thư mục gốc của dự án)

```bash
python -m pip install -r hoc_lieu/requirements.txt

streamlit run hoc_lieu/streamlit_app/app.py        # website (mở từ trang chủ)
python hoc_lieu/tests/chay_kiem_tra.py             # 35 kiểm thử
# kiểm tra trình duyệt: chạy website ở cổng 8599 rồi
python hoc_lieu/tests/kiem_tra_trinh_duyet.py
cd hoc_lieu/manim && python ket_xuat.py && python sinh_kich_ban.py   # kết xuất lại video (cần LaTeX, ffmpeg)
```

MATLAB: `matlab -sd hoc_lieu/matlab -batch chay_tat_ca` (xem `matlab/README.md`).
Trên Windows, nếu gặp lỗi mã hóa khi in tiếng Việt, đặt `PYTHONIOENCODING=utf-8`.

**Website chạy Python, không chạy MATLAB.** Mã MATLAB được cung cấp để tải về. Website không thực thi mã của người dùng, không thu thập dữ liệu người học, và xử lý tệp CSV tải lên ngay trên máy chủ chạy website.

**Triển khai:** đặt cả thư mục `hoc_lieu/` lên một máy chủ Python với cùng `requirements.txt`, tệp khởi động `hoc_lieu/streamlit_app/app.py`. Việc triển khai công khai chưa được thực hiện. Đã biết: với Streamlit 1.37, nếu yêu cầu đầu tiên sau khi khởi động máy chủ là địa chỉ một trang con, hộp thoại "Page not found" có thể hiện ra (trang vẫn hiển thị đúng).

## Dữ liệu

Nguồn của từng bộ dữ liệu được ghi trong `mhtoan/data.py`:
- dữ liệu quan sát: nấm men (Pearl 1927) và dân số Hoa Kỳ, cả hai trích qua Giordano–Fox–Horton 2014;
- tình huống giáo khoa: dịch cúm, với β = 1,407 là tham số cố định lấy từ tài liệu;
- dữ liệu minh họa, ghi nhãn "minh họa" hoặc "mô phỏng". Không có dữ liệu thực nghiệm nào được tạo giả.
