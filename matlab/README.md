# Mã MATLAB của đồ án

Mã MATLAB của các mô hình và phương pháp số trong đồ án thạc sĩ
*"Xây dựng bài giảng về mô hình toán học cho một số hiện tượng tự nhiên"*.
Các mã VDxx trùng với kho ví dụ ở Phụ lục A của đồ án, website Streamlit và video Manim.

## Trạng thái kiểm chứng

- **Đã chạy thật** trong MATLAB R2025a (25.1.0.2943329), Windows 11 (PCWIN64), chỉ MATLAB cơ bản, không toolbox.
- Ngày chạy: 03/10/2026. Lệnh `matlab -sd <thư mục> -batch "chay_tat_ca"`.
- Kết quả: 9/9 script chạy không lỗi, **78/78 kiểm tra đạt**, trong đó 31 kiểm tra đối chiếu MATLAB–Python trên cùng bài toán, lưới và dung sai.
- Nhật ký, bảng kết quả và hình nằm trong `ket_qua_matlab/`.
- Phần dùng Symbolic Math Toolbox (`dsolve` trong `vd_he_tuyen_tinh`) là **tùy chọn**. Trên máy chạy không có toolbox này nên phần đó được **bỏ qua**, và chương trình in rõ thông báo bỏ qua.
- Kết quả trên chỉ áp dụng cho phiên bản và nền tảng nêu ở đây. Phiên bản khác có thể cho số bước của `ode45`/`ode15s` hoặc kết quả `fminsearch` khác ở các chữ số cuối; các kiểm tra đã đặt dung sai cho điều này.

## Yêu cầu

- MATLAB cơ bản, R2020a trở lên. Mã dùng `exportgraphics`; nếu thiếu thì tự chuyển sang `print`. Các script có hàm cục bộ (có từ R2016b) và dùng `readtable` với tùy chọn `VariableNamingRule` (R2020b).
- Không cần toolbox. Symbolic Math Toolbox là tùy chọn.
- Để chạy nhóm kiểm tra J (đối chiếu Python), cần tệp `../ket_qua/doi_chieu_python.csv`. Tệp này đã được đưa kèm; sinh lại bằng `python hoc_lieu/scripts/xuat_doi_chieu_matlab.py`.

## Cách chạy

**Trong MATLAB:**

```matlab
cd hoc_lieu/matlab      % thư mục chứa tệp này
chay_tat_ca             % chạy mọi ví dụ, xuất hình, chạy bộ kiểm thử; ghi nhật ký
kiem_chung              % chỉ chạy bộ kiểm thử
```

**Từ dòng lệnh Windows** (không mở giao diện), trong thư mục `hoc_lieu\matlab`:

```
"C:\Program Files\MATLAB\R2025a\bin\matlab.exe" -sd "%CD%" -batch "chay_tat_ca"
```

Mã thoát khác 0 nếu có script lỗi hoặc có kiểm tra không đạt.

## Kết quả sinh ra (`ket_qua_matlab/`)

| Tệp | Nội dung |
|---|---|
| `nhat_ky_<thời gian>.txt` | Toàn bộ đầu ra (`diary`), gồm phiên bản MATLAB, sản phẩm cài đặt, thời gian |
| `tom_tat_chay.csv` | Từng script: trạng thái, số giây, thông báo lỗi |
| `kiem_chung.csv` | Từng kiểm tra: nhóm, tên, giá trị MATLAB, kỳ vọng, dung sai, kiểu so sánh, đạt/không đạt, ghi chú lỗi |
| `sir_euler_tham_chieu.png`, `bac_hoi_tu.png`, `hai_loai.png` | Hình do `vd_hinh` xuất |

## Bộ kiểm thử (`kiem_chung.m`)

| Nhóm | Nội dung |
|---|---|
| A. Đầu vào | Lưới không chia hết; `f` trả về sai kích thước; nghiệm không hữu hạn; `y0` không hữu hạn. Mỗi trường hợp phải báo lỗi |
| B. Phần dư | Nghiệm logistic tường minh; nghiệm thực từ trị riêng phức; chuỗi Jordan; `expm` so với `ode45` |
| C. Bậc hội tụ | Euler 1, Heun 2, điểm giữa 2, RK4 4 (dung sai 0,15) |
| D. SIR | Bảo toàn $S+I+R$; không âm (RK4, $h=0{,}5$); phát hiện số âm của Euler $h=3$ (không cắt về 0); đỉnh dịch giải tích = `ode45`; $S_\infty$; trường hợp không có đỉnh nội tại; $I_0=0$ |
| E. Bất biến | Năng lượng Euler tăng đúng theo $(1+h^2\omega^2)^n$; trôi năng lượng RK4 tỉ lệ $h^5$; bất biến Lotka–Volterra |
| F. Độ nhạy | $I_{\max}$ tăng và $S_\infty$ giảm theo $\beta$; hiệu chỉnh $\beta$ liên tục |
| G. Khớp dữ liệu | Hồi quy tuyến tính hóa; bình phương tối thiểu phi tuyến (`fminsearch`) |
| H, I, K | Khai thác (ba chế độ, sự kiện $P=0$); Euler ẩn và hình thang ẩn với Newton; bài toán cứng (`ode15s` so với `ode45`) |
| J. MATLAB–Python | 31 đại lượng đọc từ `doi_chieu_python.csv`, mỗi đại lượng có dung sai và kiểu so sánh riêng |

## Quy ước lập trình

- Vế phải `f(t, y)` nhận và trả về **vectơ cột**. Đầu ra `Y` của các bộ giải là ma trận `(N+1) x m`, **mỗi hàng là một trạng thái**; mọi thành phần được cập nhật đồng thời.
- Mọi bộ giải bước cố định gọi `mh_chuan_bi` để kiểm tra đầu vào (`f` là function handle; `y0` hữu hạn; `f(t0, y0)` đúng kích thước) và gọi `mh_kiem_huu_han` sau mỗi bước. Khi nghiệm không còn hữu hạn, bộ giải báo lỗi có thông báo thay vì trả kết quả vô nghĩa.
- `mh_luoi` báo lỗi nếu `(T - t0)/h` không nguyên: bước cuối không bị âm thầm làm tròn.
- Hệ đại số được giải bằng `A \ b`, không dùng `inv(A) * b`. Ma trận mũ tính bằng `expm`. Chuỗi Jordan dùng `pinv` rồi kiểm tra phần dư.
- Phương pháp ẩn dùng Newton (`mh_newton`), kiểm tra cả số gia lẫn phần dư, **báo lỗi khi không hội tụ**.
- Không hàm nào "sửa" nghiệm bằng cách cắt giá trị âm về 0. Vận tốc trong `mh_phanh` bằng 0 sau thời điểm dừng vì đó là **mô hình** (xe đứng yên), không phải để che lỗi số.
- `ode45` là cặp Dormand–Prince (4,5) bước thích nghi, **không** phải RK4 cổ điển (`mh_rk4`). Số bước của `ode45`/`ode15s` lấy từ `sol.stats`, không đếm số điểm đầu ra.

## Danh mục tệp

| Tệp | Nội dung |
|---|---|
| `mh_luoi`, `mh_chuan_bi`, `mh_kiem_huu_han` | lưới đều; kiểm tra đầu vào; kiểm tra hữu hạn |
| `mh_euler`, `mh_heun`, `mh_diem_giua`, `mh_rk4`, `mh_taylor2`, `mh_ab2` | phương pháp tường minh (Heun = hình thang hiện) |
| `mh_euler_an`, `mh_hinh_thang_an`, `mh_newton` | phương pháp ẩn + Newton |
| `mh_du_lieu` | dữ liệu có nguồn (nấm men, dân số Hoa Kỳ, tình huống cúm) |
| `mh_sir_*` | SIR: vế phải, đỉnh dịch, quy mô cuối, nghiệm tham chiếu (Events), hiệu chỉnh β, can thiệp |
| `mh_logistic_chinh_xac`, `mh_khai_thac_mo_phong`, `mh_hoi_quy`, `mh_khop_logistic` | logistic, khai thác, khớp dữ liệu |
| `mh_nghiem_phuc`, `mh_jordan2` | hệ tuyến tính: trị riêng phức, chuỗi Jordan |
| `mh_thuoc`, `mh_phanh`, `mh_hai_loai_rhs` | liều thuốc (minh họa toán học), phanh, hai loài |
| `vd_*.m` | script ví dụ VD01–VD54 (`vd_hinh`: xuất hình) |
| `kiem_chung.m`, `chay_tat_ca.m` | bộ kiểm thử; chạy tất cả, có nhật ký |
