"""Nội dung các bài học của website (văn bản, công thức, liên kết học liệu).

Chỉ chứa nội dung trình bày; mọi con số được TÍNH trong mo_phong.py / ngan_hang_bai_tap.py bằng module
mhtoan, dùng chung với đồ án, MATLAB và video. Ký hiệu thống nhất với Danh mục ký hiệu của đồ án.
"""

BAI_HOC = {
    "bai1": {
        "ten": "Bài 1. Tăng trưởng không giới hạn: mô hình Malthus",
        "chuong": "Mục 3.2 của đồ án",
        "muc_tieu": [
            "Thiết lập được $P'=rP$ từ cân bằng sinh–tử và nêu được các giả thiết.",
            "Giải được bằng tách biến và kiểm tra được nghiệm bằng đạo hàm.",
            "Ước lượng được $r$ (có đơn vị) từ hai điểm và từ đồ thị $(t,\\ln P)$.",
            "Chỉ ra được, có số liệu, khi nào mô hình không còn phù hợp (miền hiệu lực theo tiêu chí).",
        ],
        "hien_tuong": """
Một mẻ **nấm men** được nuôi trong môi trường giàu dinh dưỡng. Sinh khối đo theo giờ (dữ liệu thí nghiệm của
Pearl, 1927, trích theo Giordano–Fox–Horton 2014, Bảng 11.1) tăng rất nhanh trong vài giờ đầu.

**Câu hỏi:** sinh khối tăng theo quy luật nào? Có thể dự báo sinh khối sau 10 giờ không?
""",
        "kien_thuc": """
* **Tốc độ trung bình và đạo hàm.** $\\frac{\\Delta P}{\\Delta t}$ là hệ số góc cát tuyến; khi $\\Delta t\\to0$ nó tiến tới
  $P'(t)$, hệ số góc tiếp tuyến (video C1).
* **Tốc độ tuyệt đối và tương đối.** $P'$ (cá thể/giờ) khác $P'/P$ (giờ$^{-1}$, tính trên một cá thể).
* **Hàm mũ và logarit.** $P_0e^{rt}$ có tỉ số $P(t+\\tau)/P(t)=e^{r\\tau}$ không đổi; $\\ln P$ là hàm bậc nhất của $t$.
* **Kiểm tra đơn vị.** Đối số của $e^x$, $\\ln x$ phải không thứ nguyên: $rt$ không thứ nguyên nên $[r]=\\text{giờ}^{-1}$.
""",
        "gia_thiet": """
1. **Khép kín:** không nhập cư, xuất cư.
2. **Đồng nhất:** mọi cá thể như nhau (không xét tuổi, giới tính).
3. **Sinh, tử tỉ lệ với quy mô:** trong khoảng ngắn $\\Delta t$ có $bP\\Delta t+o(\\Delta t)$ cá thể sinh ra và
   $dP\\Delta t+o(\\Delta t)$ cá thể chết; $b,d$ hằng (đơn vị thời gian$^{-1}$).
4. **Không phụ thuộc mật độ:** tài nguyên đủ để $b$, $d$ không đổi khi quần thể tăng.
5. **Xấp xỉ liên tục:** $P(t)$ là hàm khả vi.
""",
        "phuong_trinh": r"""
Cân bằng trên $[t,t+\Delta t]$: $P(t+\Delta t)-P(t)=(b-d)P\Delta t+o(\Delta t)$. Chia cho $\Delta t$, cho $\Delta t\to0$:

$$P'(t)=rP(t),\qquad r=b-d,\qquad P(t_0)=P_0>0 .$$

Nghiệm (tách biến, kiểm tra bằng đạo hàm): $P(t)=P_0e^{r(t-t_0)}$; thời gian tăng gấp đôi $T_d=\ln2/r$ (khi $r>0$),
không phụ thuộc $P_0$. Lấy logarit: $\ln P=\ln P_0+r(t-t_0)$, nên $r$ là hệ số góc của đường thẳng qua các điểm
$(t_i,\ln P_i)$; từ hai quan sát, $r=\frac{1}{t_2-t_1}\ln\frac{P_2}{P_1}$.
""",
        "video": ["C1_TocDoTrungBinhDenDaoHam", "C2_CanBangSinhTu", "C3_MalthusNgoaiMienHieuLuc"],
        "vi_du": ["VD01", "VD02", "VD06", "VD07", "VD09", "VD10", "VD11", "VD12"],
        "matlab": ["vd_giai_tich_malthus.m", "mh_euler.m", "mh_hoi_quy.m"],
        "gioi_han": """
* **Miền hiệu lực theo tiêu chí:** khớp trên $t=0,\\dots,4$ giờ, mô hình chỉ đạt sai số tương đối $\\le10\\%$ đến
  $t=5$ giờ; tại $t=10$ dự báo khoảng $1469$ so với quan sát $513{,}3$ (VD10).
* **Sai số có hệ thống** (tăng dần theo thời gian) là dấu hiệu của sai số **mô hình** — giả thiết 4 bị vi phạm —
  không phải dữ liệu đo kém.
* Không xét cấu trúc tuổi, di cư; tham số hằng; mô hình tất định nên không mô tả dao động ngẫu nhiên khi quần thể nhỏ.
* Dân số Hoa Kỳ: dự báo tốt sau 10 năm (sai số $-2{,}3\\%$) nhưng phi lý sau 300 năm.
""",
    },
    "bai2": {
        "ten": "Bài 2. Tăng trưởng có giới hạn: mô hình logistic",
        "chuong": "Mục 3.3 của đồ án",
        "muc_tieu": [
            "Phát hiện được giả thiết logistic từ dữ liệu (tốc độ tăng tương đối giảm gần tuyến tính).",
            "Xác định được hai điểm cân bằng và tính ổn định bằng đường pha.",
            "Tính được thời điểm uốn $t^*$ và tốc độ tăng lớn nhất $rK/4$, có đơn vị.",
            "Ước lượng được tham số và đánh giá được trên thang gốc, trong mẫu và ngoài mẫu.",
            "Giải thích được vì sao dữ liệu giai đoạn đầu không xác định được $K$.",
        ],
        "hien_tuong": """
Dự báo của Bài 1 sai gần ba lần sau 10 giờ. Toàn bộ dữ liệu nấm men (0–18 giờ) có dạng **chữ S**: tăng nhanh, chậm dần,
rồi gần như dừng quanh 660 đơn vị.

**Câu hỏi:** tốc độ tăng *tương đối* thay đổi thế nào khi sinh khối tăng? Dùng phát hiện đó để xây dựng mô hình tốt hơn.
""",
        "kien_thuc": """
* Bài 1 (tốc độ tương đối, hàm mũ, logarit).
* **Đường pha** của phương trình tự trị $y'=f(y)$: điểm cân bằng $f(y^*)=0$; dấu của $f$ cho chiều biến thiên;
  $f'(y^*)<0$ ⇒ ổn định tiệm cận, $f'(y^*)>0$ ⇒ không ổn định, $f'(y^*)=0$ ⇒ chưa kết luận.
* **Đạo hàm cấp hai, điểm uốn:** $y''=f'(y)f(y)$.
* **Phân tích phân thức:** $\\frac{1}{P(K-P)}=\\frac1K\\bigl(\\frac1P+\\frac1{K-P}\\bigr)$.
""",
        "gia_thiet": """
Giữ các giả thiết 1, 2, 5 của Bài 1; thay giả thiết 3–4 bằng:

* **Tốc độ tăng tương đối giảm tuyến tính theo quy mô:** $\\frac{P'}{P}=r\\bigl(1-\\frac PK\\bigr)$ — gần $r$ khi $P\\ll K$,
  bằng 0 khi $P=K$, âm khi $P>K$. Đây là **quyết định mô hình hóa** đơn giản nhất phù hợp dữ liệu, không phải định luật.
* $K$ là **sức chứa** (cùng đơn vị với $P$), $r$ là tốc độ tăng nội tại (thời gian$^{-1}$).
""",
        "phuong_trinh": r"""
$$P'=rP\Bigl(1-\frac PK\Bigr),\qquad P(t_0)=P_0>0 .$$

* Nếu tài liệu viết $P'=kP(K-P)$ thì $r=kK$; $[k]=(\text{cá thể}\cdot\text{thời gian})^{-1}$ khác $[r]=\text{thời gian}^{-1}$.
* Cân bằng $0$ (không ổn định) và $K$ (ổn định tiệm cận); tăng nhanh nhất khi $P=K/2$ với tốc độ $rK/4$.
* Nghiệm: $P(t)=\dfrac{KP_0}{P_0+(K-P_0)e^{-r(t-t_0)}}$; nếu $0<P_0<K/2$, $t^*=t_0+\frac1r\ln\frac{K-P_0}{P_0}$.
* Tuyến tính hóa (chỉ khi $0<P_i<K$ với **mọi** quan sát): $\ln\frac{P}{K-P}=rt-rt^*$.
""",
        "video": ["C4_LogisticDuongPha"],
        "vi_du": ["VD13", "VD14", "VD15", "VD16", "VD17", "VD18", "VD19", "VD20", "VD21", "VD22"],
        "matlab": ["vd_logistic.m", "mh_logistic_chinh_xac.m", "mh_khop_logistic.m", "mh_khai_thac_mo_phong.m"],
        "gioi_han": """
* $K=665$ được chọn khi nhìn **toàn bộ** dữ liệu ⇒ sai số tính trên chính dữ liệu đó là sai số **trong mẫu**.
  Giá trị quan sát lớn nhất (661,8) **không đủ** để xác định $K$; ngay cả $K>\\max P_i$ chỉ đúng với quỹ đạo tăng
  quan sát không sai số (dữ liệu có nhiễu có thể vượt $K$; quỹ đạo giảm từ $P_0>K$ luôn nằm trên $K$).
* **Nhận diện:** về cấu trúc, $r$ và $K$ xác định được từ toàn bộ quỹ đạo không nhiễu; trong thực hành, dữ liệu chỉ
  ở giai đoạn đầu ($t_c=5$) không xác định được $K$ (thuật toán đẩy $K$ ra rất lớn).
* Dạng bậc nhất của $P'/P$ là giả thiết đơn giản nhất; $K$ có thể thay đổi; không có độ trễ.
* Khai thác: khi quần thể chạm 0, mô phỏng **dừng** — không có ``dân số âm''.
""",
    },
    "bai3": {
        "ten": "Bài 3. Lan truyền dịch bệnh: mô hình SIR",
        "chuong": "Mục 3.4 của đồ án",
        "muc_tieu": [
            "Lập được hệ SIR từ sơ đồ ngăn và chứng minh được bảo toàn $S+I+R=N$.",
            "Xây dựng được $\\mathcal R_0=\\beta/\\gamma$ và phát biểu đúng điều kiện tăng ban đầu $\\mathcal R_0S_0/N>1$.",
            "Phân biệt được số đang nhiễm $I(t)$, tốc độ nhiễm mới, số nhiễm mới trong một khoảng và số nhiễm tích lũy.",
            "Giải số được bằng Euler và RK4, kiểm chứng được bằng công thức đỉnh dịch.",
            "Phân biệt được sai số mô hình với sai số của phương pháp số.",
        ],
        "hien_tuong": """
Một ký túc xá $1000$ sinh viên; ban đầu $5$ người mắc cúm; thời gian mắc bệnh trung bình $5/3$ tuần; sau một tuần có
$9$ người **đang** mắc (tình huống giáo khoa của Giordano–Fox–Horton 2014, không phải số liệu một đợt dịch thật).

**Câu hỏi:** dịch đạt đỉnh khi nào, với bao nhiêu người bệnh cùng lúc? Có phải cuối cùng ai cũng mắc bệnh?
Cần miễn dịch trước cho bao nhiêu sinh viên?
""",
        "kien_thuc": """
* **Hệ phương trình vi phân**, không gian trạng thái (với SIR sau khi khử $R=N-S-I$: mặt phẳng $(S,I)$), quỹ đạo.
* **Nguyên lý cân bằng** cho từng ngăn: tốc độ thay đổi = vào − ra.
* **Tích phân như tích lũy:** số ca mới trong $[a,b]$ là $\\int_a^b\\beta SI/N\\,dt=S(a)-S(b)$.
* **Phương pháp số:** Euler, Heun, RK4 cho hệ; kiểm chứng bằng giảm bước, bảo toàn, không âm.
""",
        "gia_thiet": """
1. Cộng đồng khép kín, đợt dịch ngắn (bỏ qua sinh tử khác).
2. Ba nhóm $S$ (cảm nhiễm), $I$ (đang nhiễm, **có khả năng lây**), $R$ (loại ra); không có thời kỳ tiềm ẩn.
3. **Trộn đều:** mỗi người có trung bình $\\beta$ tiếp xúc đủ để lây mỗi đơn vị thời gian.
4. Mỗi người bệnh rời nhóm $I$ với cường độ $\\gamma$ (thời gian mắc bệnh trung bình $1/\\gamma$).
5. Miễn dịch bền vững trong thời gian xét.
""",
        "phuong_trinh": r"""
$$S'=-\beta\frac{SI}{N},\qquad I'=\beta\frac{SI}{N}-\gamma I,\qquad R'=\gamma I,\qquad S+I+R=N .$$

* Nhãn trên sơ đồ ngăn: $\beta SI/N$ và $\gamma I$ là **tốc độ chuyển ngăn** (người/thời gian); nguy cơ trên **mỗi**
  người cảm nhiễm là $\beta I/N$.
* $\mathcal R_0=\beta/\gamma$; $\mathcal R_{\mathrm{eff}}(t)=\mathcal R_0S(t)/N$; $I'=\gamma I(\mathcal R_{\mathrm{eff}}-1)$.
* Khi $I_0>0$: $I$ **tăng ban đầu** khi và chỉ khi $\mathcal R_0S_0/N>1$ (không chỉ $\mathcal R_0>1$).
* Nếu có đỉnh nội tại: đỉnh khi $S=S^*=N/\mathcal R_0$, $I_{\max}=I_0+S_0-S^*-S^*\ln\frac{S_0}{S^*}$.
  Nếu $\mathcal R_0S_0/N\le1$: $I$ giảm ngay, giá trị lớn nhất là $I_0$.
* Dạng $aSI$ của một số tài liệu tương ứng $\beta=aN$; $\beta S_0/(\gamma N)$ là $\mathcal R_{\mathrm{eff}}(0)$, **không** phải $\mathcal R_0$.
""",
        "video": ["C5_SIRSoDoNgan", "C6_NguongDinhDich"],
        "vi_du": ["VD23", "VD24", "VD25", "VD26", "VD27", "VD28", "VD29", "VD30", "VD31", "VD32"],
        "matlab": ["vd_sir.m", "mh_sir_rhs.m", "mh_sir_giai.m", "mh_sir_dinh_dich.m", "mh_sir_hieu_chinh_beta.m"],
        "gioi_han": """
* $\\beta=1{,}407$ là **tham số cố định** lấy từ tài liệu (ước lượng bằng một bước Euler). Hiệu chỉnh nghiệm liên tục với
  cùng dữ kiện cho $\\beta\\approx1{,}198$, $\\mathcal R_0\\approx1{,}997$.
* Mô hình đã được **kiểm chứng tính toán**, **chưa được thẩm định** bằng dữ liệu dịch thật.
* Trộn đều, thời gian mắc bệnh phân bố mũ, tham số hằng, không có thời kỳ tiềm ẩn (SEIR là mở rộng).
* Tất định: khi số người bệnh nhỏ, $I=0{,}4$ người không có nghĩa thực tế.
* Số ca báo cáo theo tuần phải so với **số ca mới**, không phải $I(t)$.
""",
    },
    "bai4": {
        "ten": "Bài 4 (mở rộng). Hệ phương trình vi phân và mặt phẳng pha",
        "chuong": "Mục 2.3, 3.5 của đồ án",
        "muc_tieu": [
            "Phân biệt được không gian trạng thái, không gian mở rộng chứa thời gian và trường vectơ.",
            "Tìm được trị riêng, vectơ riêng và phân loại được điểm cân bằng của hệ tuyến tính $2\\times2$.",
            "Viết được hai nghiệm thực khi trị riêng phức và nghiệm từ chuỗi Jordan khi thiếu vectơ riêng.",
            "Dùng đúng tiêu chuẩn tuyến tính hóa và biết khi nào nó không đủ để kết luận.",
            "Đọc được mặt phẳng pha của mô hình hai loài (đường phân cách, quỹ đạo kín).",
        ],
        "hien_tuong": """
Hai loài cá cùng ăn một nguồn thức ăn; tôm nhỏ và cá voi trong quan hệ con mồi – thú săn mồi. Mỗi loài thay đổi theo
thời gian và **ảnh hưởng lẫn nhau**, nên cần một **hệ** phương trình.

**Câu hỏi:** từ một trạng thái ban đầu, hai quần thể tiến tới đâu? Có cùng tồn tại được không?
""",
        "kien_thuc": """
* Ma trận, định thức, **trị riêng** $\\det(A-\\lambda I)=0$ và **vectơ riêng** $(A-\\lambda I)\\mathbf v=\\mathbf 0$, $\\mathbf v\\ne\\mathbf 0$.
* Số phức, công thức Euler $e^{i\\beta t}=\\cos\\beta t+i\\sin\\beta t$.
* Bài 2 (điểm cân bằng, ổn định một chiều).
""",
        "gia_thiet": """
* Hệ tự trị $\\mathbf y'=\\mathbf f(\\mathbf y)$ với $\\mathbf f$ khả vi liên tục (bảo đảm tồn tại, duy nhất địa phương):
  khi đó hai quỹ đạo khác nhau không cắt nhau, và quỹ đạo không tới điểm cân bằng sau thời gian hữu hạn.
* Mô hình hai loài: tốc độ tăng riêng của mỗi loài phụ thuộc tuyến tính vào loài kia (giả thiết đơn giản nhất).
""",
        "phuong_trinh": r"""
* **Hệ tuyến tính** $\mathbf y'=A\mathbf y$: nghiệm $e^{tA}\mathbf y_0$. Trị riêng thực phân biệt: $\sum c_ie^{\lambda_it}\mathbf v_i$.
  Trị riêng phức $\alpha\pm i\beta$, $\mathbf v=\mathbf p+i\mathbf q$: $e^{\alpha t}(\mathbf p\cos\beta t-\mathbf q\sin\beta t)$,
  $e^{\alpha t}(\mathbf p\sin\beta t+\mathbf q\cos\beta t)$. Chuỗi Jordan $(A-\lambda I)\mathbf v_2=\mathbf v_1$:
  $e^{\lambda t}\mathbf v_1$, $e^{\lambda t}(t\mathbf v_1+\mathbf v_2)$.
* **Tuyến tính hóa** tại $\mathbf y^*$ với ma trận Jacobi $J$: mọi trị riêng phần thực âm ⇒ ổn định tiệm cận cục bộ;
  có trị riêng phần thực dương ⇒ không ổn định; còn lại (gồm thuần ảo) ⇒ **chưa kết luận**.
* Cạnh tranh: $x'=(a-by)x$, $y'=(m-nx)y$. Thú – mồi (Lotka–Volterra): $x'=(a-by)x$, $y'=(-m+nx)y$,
  bất biến $nx-m\ln x+by-a\ln y$.
""",
        "video": ["C9_MatPhangPha"],
        "vi_du": ["VD45", "VD46", "VD47", "VD48", "VD49", "VD50", "VD51", "VD54"],
        "matlab": ["vd_he_tuyen_tinh.m", "mh_nghiem_phuc.m", "mh_jordan2.m", "mh_hai_loai_rhs.m"],
        "gioi_han": """
* Phân loại theo trị riêng chỉ chắc chắn cho hệ **tuyến tính**; với hệ phi tuyến, trị riêng thuần ảo không đủ kết luận có tâm.
* Mô hình cạnh tranh: **không** phải mọi trạng thái đầu đều dẫn tới loại trừ — trạng thái trên đường phân cách tiến về
  điểm cùng tồn tại; mô hình không có tự giới hạn nên loài thắng tăng không bị chặn.
* Lotka–Volterra: dao động phụ thuộc điều kiện đầu, rất nhạy với thay đổi cấu trúc mô hình.
""",
    },
}

LO_TRINH = """
| Bước | Người mới (đường cơ bản) | Đường nâng cao |
|---|---|---|
| 1 | Bài 1: Malthus (tab Hiện tượng → Mô phỏng → Luyện tập mức cơ bản) | Bài 1 đầy đủ + ví dụ VD09, VD10 |
| 2 | Bài 2: Logistic (đường pha, nghiệm, tuyến tính hóa) | + Công cụ khớp dữ liệu: chia dữ liệu theo thời gian, tính nhận diện $K$ |
| 3 | Bài 3: SIR (sơ đồ ngăn, ngưỡng, mô phỏng Euler/RK4) | + hiệu chỉnh $\\beta$, can thiệp, SEIR |
| 4 | Công cụ phương pháp số (sai số khi giảm $h$) | + ổn định tuyệt đối, bài toán cứng |
| 5 | — | Bài 4: hệ tuyến tính, mặt phẳng pha, hai loài |
"""
