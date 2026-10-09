"""Ngân hàng bài tập có gợi ý theo ba mức, đáp án và giải thích.

- Đáp án số được TÍNH bằng module mhtoan (không gõ tay), chấm bằng so sánh với dung sai — không dùng mô hình ngôn ngữ.
- Ba loại: "so" (nhập số), "chon" (chọn một phương án), "mo" (câu hỏi mở: hiện đáp án mẫu để tự đối chiếu).
- Dữ liệu trong bài tập: dữ liệu quan sát có nguồn (nấm men, dân số Hoa Kỳ), tình huống giáo khoa (cúm),
  hoặc dữ liệu MÔ PHỎNG được ghi rõ.
"""
import math

import numpy as np

from tien_ich import data, models, solvers

CUM = data.CUM_GIAO_KHOA


def _euler_y3():
    _, Y = solvers.euler(lambda t, y: 1 + y, 0.0, [1.0], 0.1, 0.3)
    return float(Y[-1, 0])


def _rk4_he_x1():
    A = np.array([[1.0, -4.0], [-1.0, 1.0]])
    _, Y = solvers.rk4(lambda t, y: A @ y, 0.0, [1.0, 0.0], 0.2, 0.2)
    return float(Y[-1, 0])


BAI_TAP = [
    # ------------------------------------------------------------------ Bài 1
    {"ma": "B1.1", "bai": "bai1", "muc": "Cơ bản", "dang": "tính toán", "loai": "so",
     "de": "Một quần thể có $b=0{,}035$ năm$^{-1}$, $d=0{,}015$ năm$^{-1}$. Thời gian tăng gấp đôi (năm)?",
     "goi_y": ["Mô hình Malthus dùng tốc độ tăng trưởng riêng **thuần**.", "$r=b-d$.", "$T_d=\\ln2/r$."],
     "dap_an": lambda: models.thoi_gian_gap_doi(0.035 - 0.015), "dung_sai": 0.01,
     "giai_thich": ["$r=0{,}02$ năm$^{-1}$.", "$T_d=0{,}6931/0{,}02\\approx34{,}66$ năm, không phụ thuộc $P_0$."]},
    {"ma": "B1.2", "bai": "bai1", "muc": "Cơ bản", "dang": "kiểm tra đơn vị", "loai": "chon",
     "de": "Mô hình nào **sai về thứ nguyên** nếu $P$ đo bằng cá thể, $t$ đo bằng năm, $r$ đo bằng năm$^{-1}$?",
     "lua_chon": ["$P'=rP$", "$P'=r+P$", "$P'=rP(1-P/K)$ với $K$ đo bằng cá thể", "$\\ln(P/P_0)=rt$"],
     "dap_an": 1,
     "goi_y": ["Hai số hạng được cộng phải cùng đơn vị.", "$[r]=\\text{năm}^{-1}$, $[P]=\\text{cá thể}$.",
               "So sánh đơn vị của $r$ và của $P$ trong phương án thứ hai."],
     "giai_thich": ["$r$ có đơn vị năm$^{-1}$, $P$ có đơn vị cá thể: không cộng được (VD03).",
                    "Các phương án còn lại có hai vế cùng đơn vị; $rt$ và $P/P_0$ không thứ nguyên."]},
    {"ma": "B1.3", "bai": "bai1", "muc": "Cơ bản", "dang": "tính toán", "loai": "so",
     "de": "$r=0{,}24$ năm$^{-1}$ (tăng trưởng liên tục). Sau 1 năm quần thể **nhân** với hệ số bao nhiêu?",
     "goi_y": ["$P(1)/P(0)=?$", "Dùng nghiệm $P_0e^{rt}$.", "Tính $e^{0{,}24}$."],
     "dap_an": lambda: math.exp(0.24), "dung_sai": 1e-4,
     "giai_thich": ["$e^{0{,}24}\\approx1{,}2712$: tăng khoảng $27{,}1\\%$, không phải $24\\%$ (VD01)."]},
    {"ma": "B1.4", "bai": "bai1", "muc": "Vận dụng", "dang": "đọc đồ thị", "loai": "chon",
     "de": "Vẽ $\\ln P$ theo $t$ cho dữ liệu nấm men $t=0,\\dots,18$. Điều nào **đúng**?",
     "lua_chon": ["Các điểm thẳng hàng trên toàn khoảng nên mô hình Malthus phù hợp suốt 18 giờ",
                  "Các điểm gần thẳng hàng ở vài giờ đầu rồi cong xuống: Malthus chỉ phù hợp giai đoạn đầu",
                  "Các điểm cong lên: tăng nhanh hơn hàm mũ",
                  "Không thể kết luận gì từ đồ thị $\\ln P$"],
     "dap_an": 1,
     "goi_y": ["Nếu $P=P_0e^{rt}$ thì $\\ln P$ là hàm gì của $t$?", "Xem độ dốc của $\\ln P$ ở đầu và cuối thí nghiệm.",
               "Tốc độ tăng tương đối giảm dần thì đồ thị $\\ln P$ thế nào?"],
     "giai_thich": ["Malthus ⇔ $\\ln P$ bậc nhất theo $t$.",
                    "Với nấm men, độ dốc giảm dần về 0: đồ thị cong xuống, Malthus chỉ phù hợp giai đoạn đầu (VD10)."]},
    {"ma": "B1.5", "bai": "bai1", "muc": "Vận dụng", "dang": "phản biện", "loai": "chon",
     "de": "Khớp Malthus trên $t=0..4$, dự báo $P(10)\\approx1469$ trong khi quan sát $513{,}3$. Nguyên nhân chính?",
     "lua_chon": ["Dữ liệu những giờ đầu đo kém chính xác", "Tính toán sai", "Giả thiết tài nguyên không giới hạn bị vi phạm",
                  "Chọn sai đơn vị thời gian"],
     "dap_an": 2,
     "goi_y": ["Sai số là ngẫu nhiên hay có hệ thống?", "Sai số tăng dần theo thời gian gợi ý điều gì?",
               "Giả thiết nào của Malthus kém hợp lý khi quần thể đã lớn?"],
     "giai_thich": ["Sai số tăng có hệ thống: sai số **mô hình**.", "Nguồn dữ liệu không cho biết sai số đo, nên không có cơ "
                    "sở để nói dữ liệu đầu kém chính xác; giả thiết 4 (không phụ thuộc mật độ) bị vi phạm."]},
    {"ma": "B1.6", "bai": "bai1", "muc": "Mở rộng", "dang": "tính toán", "loai": "so",
     "de": "Dân số Hoa Kỳ $203\\,211\\,926$ (1970), $248\\,710\\,000$ (1990). Ước lượng $r$ (năm$^{-1}$, 4 chữ số thập phân).",
     "goi_y": ["Dùng hai điểm.", "$r=\\frac{1}{t_2-t_1}\\ln\\frac{P_2}{P_1}$.", "$t_2-t_1=20$ năm."],
     "dap_an": lambda: math.log(248710000 / 203211926) / 20, "dung_sai": 1e-4,
     "giai_thich": ["$r\\approx0{,}0101$ năm$^{-1}$, $T_d\\approx68{,}6$ năm (VD06)."]},
    # ------------------------------------------------------------------ Bài 2
    {"ma": "B2.1", "bai": "bai2", "muc": "Cơ bản", "dang": "tính toán", "loai": "so",
     "de": "$P'=0{,}4P(1-P/500)$, $P(0)=20$ ($t$: năm). Thời điểm uốn $t^*$ (năm)?",
     "goi_y": ["Điểm uốn là lúc $P=K/2$.", "$t^*=\\frac1r\\ln\\frac{K-P_0}{P_0}$.", "$=\\ln(480/20)/0{,}4$."],
     "dap_an": lambda: models.logistic_t_uon(20, 0.4, 500), "dung_sai": 0.01,
     "giai_thich": ["$t^*=\\ln24/0{,}4\\approx7{,}945$ năm (VD13)."]},
    {"ma": "B2.2", "bai": "bai2", "muc": "Cơ bản", "dang": "tính toán", "loai": "so",
     "de": "Cùng mô hình: tốc độ tăng lớn nhất (cá thể/năm)?",
     "goi_y": ["$f(P)=rP(1-P/K)$ là tam thức bậc hai.", "Cực đại tại $P=K/2$.", "$f(K/2)=rK/4$."],
     "dap_an": lambda: 0.4 * 500 / 4, "dung_sai": 1e-6,
     "giai_thich": ["$rK/4=50$ cá thể/năm — có đơn vị cá thể/năm, không phải năm$^{-1}$."]},
    {"ma": "B2.3", "bai": "bai2", "muc": "Cơ bản", "dang": "kiểm tra đơn vị", "loai": "chon",
     "de": "Tài liệu viết $P'=kP(665-P)$ với $k\\approx8{,}271\\cdot10^{-4}$. Đưa về dạng $rP(1-P/K)$ thì $r=$?",
     "lua_chon": ["$8{,}271\\cdot10^{-4}$ giờ$^{-1}$", "$0{,}55$ giờ$^{-1}$", "$665$ giờ$^{-1}$", "$8{,}271\\cdot10^{-4}\\cdot665^2$"],
     "dap_an": 1,
     "goi_y": ["Khai triển $kP(K-P)=kK\\,P(1-P/K)$.", "Vậy $r=kK$.", "Kiểm tra đơn vị: $[k]=(\\text{đơn vị}\\cdot\\text{giờ})^{-1}$."],
     "giai_thich": ["$r=kK\\approx0{,}55$ giờ$^{-1}$.", "Dùng nhầm $8{,}271\\cdot10^{-4}$ làm $r$ cho mô hình gần như không tăng "
                    "(thời gian gấp đôi ban đầu khoảng 840 giờ)."]},
    {"ma": "B2.4", "bai": "bai2", "muc": "Vận dụng", "dang": "phát hiện giả thiết sai", "loai": "chon",
     "de": "Một nhóm lấy $K=661{,}8$ (giá trị lớn nhất quan sát) rồi tính $\\ln\\frac{P}{K-P}$. Vấn đề là gì?",
     "lua_chon": ["Không có vấn đề", "Tại $P=661{,}8$ phép biến đổi không xác định; và giá trị lớn nhất không đủ để xác định $K$",
                  "Phải dùng $\\ln P$ thay vì $\\ln\\frac{P}{K-P}$", "$K$ phải nhỏ hơn mọi quan sát"],
     "dap_an": 1,
     "goi_y": ["Phép biến đổi xác định khi nào?", "$K-P$ phải dương với **mọi** quan sát.",
               "Một quan sát lớn nhất cho biết $K\\ge?$"],
     "giai_thich": ["Cần $0<P_i<K$ với mọi $i$; $K=661{,}8$ làm mẫu số bằng 0.",
                    "Giá trị lớn nhất không xác định được $K$: với dữ liệu có sai số đo, một quan sát có thể vượt $K$; "
                    "với $P_0>K$ mọi quan sát đều lớn hơn $K$. $K$ phải được ước lượng (hoặc chọn trước và nêu rõ là lựa chọn)."]},
    {"ma": "B2.5", "bai": "bai2", "muc": "Vận dụng", "dang": "tính toán", "loai": "so",
     "de": "$r=0{,}5$ năm$^{-1}$, $K=1000$ tấn, khai thác $H=100$ tấn/năm. Điểm cân bằng **ổn định** (tấn)?",
     "goi_y": ["Giải $rP(1-P/K)=H$.", "$P_\\pm=\\frac K2\\bigl(1\\pm\\sqrt{1-4H/(rK)}\\bigr)$.", "Cân bằng nào có $f_H'<0$?"],
     "dap_an": lambda: models.khai_thac_can_bang(0.5, 1000, 100)["can_bang"][1][0], "dung_sai": 0.01,
     "giai_thich": ["$P_+\\approx723{,}61$ ổn định tiệm cận, $P_-\\approx276{,}39$ không ổn định (VD19)."]},
    {"ma": "B2.6", "bai": "bai2", "muc": "Mở rộng", "dang": "tính toán", "loai": "so",
     "de": "$H=rK/4=125$ ($r=0{,}5$, $K=1000$), $P_0=400$. Sau bao nhiêu năm quần thể chạm 0?",
     "goi_y": ["$f_H(P)=-\\frac rK(P-\\frac K2)^2$.", "Đặt $u=P-500$: $u'=-(r/K)u^2$.", "$1/u=1/u_0+(r/K)t$."],
     "dap_an": lambda: 16.0, "dung_sai": 1e-3,
     "giai_thich": ["$u_0=-100$; $P=0\\Leftrightarrow u=-500$: $-1/500=-1/100+0{,}0005t$ ⇒ $t=16$ năm (VD20).",
                    "Cân bằng $K/2$ nửa ổn định: hút từ phải, đẩy từ trái."]},
    {"ma": "B2.7", "bai": "bai2", "muc": "Mở rộng", "dang": "phản biện", "loai": "mo",
     "de": "Với dữ liệu nấm men chỉ đến $t=5$ giờ, thuật toán cho $K\\approx4{,}6\\cdot10^8$. Vì sao? Có nghĩa mô hình logistic sai không?",
     "goi_y": ["Ở giai đoạn đầu $P\\ll K$, $P'/P\\approx?$", "Hệ số góc $-r/K$ so với nhiễu dữ liệu.",
               "Phân biệt nhận diện cấu trúc và nhận diện thực hành."],
     "dap_an": "Dữ liệu trước điểm uốn gần như hàm mũ nên không chứa thông tin về $K$ (không nhận diện được trong thực hành: "
               "đổi điểm khởi tạo thì $K$ thu được đổi từ $4{,}4\\cdot10^8$ đến $6{,}4\\cdot10^8$); "
               "logistic suy biến thành Malthus. Điều này không chứng minh logistic sai: khi dữ liệu vượt điểm uốn "
               "($t_c\\ge9$), $K$ được ước lượng ổn định (Bảng chia dữ liệu, VD18).",
     "giai_thich": []},
    # ------------------------------------------------------------------ Bài 3
    {"ma": "B3.1", "bai": "bai3", "muc": "Cơ bản", "dang": "tính toán", "loai": "so",
     "de": "Tình huống cúm: $\\beta=1{,}407$, $\\gamma=0{,}6$ (tuần$^{-1}$), $S_0=995$, $I_0=5$, $N=1000$. Tính $I_{\\max}$.",
     "goi_y": ["Kiểm tra trước: có đỉnh nội tại không ($\\mathcal R_0S_0/N>1$?).", "$S^*=N/\\mathcal R_0$.",
               "$I_{\\max}=I_0+S_0-S^*-S^*\\ln(S_0/S^*)$."],
     "dap_an": lambda: models.sir_dinh_dich(995, 5, 1000, 1.407, 0.6)["I_max"], "dung_sai": 0.05,
     "giai_thich": ["$\\mathcal R_0=2{,}345$, $\\mathcal R_0S_0/N\\approx2{,}33>1$: có đỉnh.",
                    "$S^*\\approx426{,}44$; $I_{\\max}\\approx212{,}25$ người (VD23)."]},
    {"ma": "B3.2", "bai": "bai3", "muc": "Cơ bản", "dang": "phát hiện giả thiết sai", "loai": "chon",
     "de": "Một tài liệu viết: ``số sinh sản cơ bản là $R_0=\\beta S(0)/(\\gamma N)$; nếu $R_0<1$ dịch biến mất''. Nhận xét?",
     "lua_chon": ["Hoàn toàn đúng", "Đại lượng đó là $\\mathcal R_{\\mathrm{eff}}(0)$, không phải $\\mathcal R_0=\\beta/\\gamma$",
                  "Phải là $\\beta N/\\gamma$", "Phải là $\\gamma/\\beta$"],
     "dap_an": 1,
     "goi_y": ["$\\mathcal R_0$ định nghĩa trong cộng đồng **hoàn toàn** cảm nhiễm.", "Khi $S_0<N$, có thêm thừa số $S_0/N$.",
               "Tên đúng của $\\mathcal R_0S_0/N$ là gì?"],
     "giai_thich": ["Với $\\beta SI/N$: $\\mathcal R_0=\\beta/\\gamma$; $\\beta S_0/(\\gamma N)=\\mathcal R_{\\mathrm{eff}}(0)$.",
                    "Điều kiện $I$ tăng ban đầu là $\\mathcal R_{\\mathrm{eff}}(0)>1$; hai đại lượng chỉ trùng khi $S_0=N$."]},
    {"ma": "B3.3", "bai": "bai3", "muc": "Cơ bản", "dang": "tính toán", "loai": "so",
     "de": "$S_0=400$, $I_0=5$, $N=1000$, $\\beta=1{,}407$, $\\gamma=0{,}6$. Tính $\\mathcal R_{\\mathrm{eff}}(0)$. $I$ có tăng không?",
     "goi_y": ["$\\mathcal R_{\\mathrm{eff}}(0)=\\mathcal R_0S_0/N$.", "$\\mathcal R_0=2{,}345$.", "So sánh với 1."],
     "dap_an": lambda: 1.407 / 0.6 * 400 / 1000, "dung_sai": 1e-3,
     "giai_thich": ["$0{,}938<1$: $I$ giảm ngay dù $\\mathcal R_0>1$ (VD24)."]},
    {"ma": "B3.4", "bai": "bai3", "muc": "Vận dụng", "dang": "tính toán", "loai": "so",
     "de": "Trong tuần đầu của tình huống cúm, có bao nhiêu **ca nhiễm mới**? (2 chữ số thập phân)",
     "goi_y": ["Số ca mới khác số đang nhiễm $I(1)$.", "Số ca mới $=\\int_0^1\\beta SI/N\\,dt$.", "$=S(0)-S(1)$."],
     "dap_an": lambda: M_ca_moi_tuan_1(), "dung_sai": 0.01,
     "giai_thich": ["$S(0)-S(1)\\approx10{,}64$; trong khi $I(1)\\approx11{,}06$ và $R(1)\\approx4{,}58$; $5+10{,}64-4{,}58\\approx11{,}06$ (VD27)."]},
    {"ma": "B3.5", "bai": "bai3", "muc": "Vận dụng", "dang": "chọn bước lưới", "loai": "chon",
     "de": "Giải SIR cúm bằng Euler trên $[0,30]$ tuần. Bước nào **bảo đảm** $S_n,I_n>0$ theo điều kiện đủ $h\\beta<1$, $h\\gamma<1$?",
     "lua_chon": ["$h=3$", "$h=2$", "$h=1$", "$h=0{,}5$"],
     "dap_an": 3,
     "goi_y": ["$S_{n+1}=S_n(1-h\\beta I_n/N)$.", "Cần $h\\beta<1$ với $\\beta=1{,}407$.", "$1/1{,}407\\approx0{,}71$."],
     "giai_thich": ["Chỉ $h=0{,}5$ thỏa $h\\beta<1$ và $h\\gamma<1$.", "$h=2$ cho $\\min I\\approx-12{,}1$; $h=3$ cho $\\min S\\approx-101{,}5$ "
                    "(VD38). $h=1$ vi phạm điều kiện đủ dù trong ví dụ này không ra số âm."]},
    {"ma": "B3.6", "bai": "bai3", "muc": "Vận dụng", "dang": "đánh giá sai số", "loai": "chon",
     "de": "Euler $h=1$ cho đỉnh khoảng 251 người ở tuần 9; RK4 $h=0{,}5$ cho khoảng 212 ở tuần 7. Kết luận nào đúng?",
     "lua_chon": ["Dịch thật có đỉnh 251 người", "Sai lệch là sai số của phương pháp Euler bước lớn, không phải đặc điểm của dịch",
                  "RK4 sai vì bỏ sót đỉnh", "Hai phương pháp mô tả hai mô hình khác nhau"],
     "dap_an": 1,
     "goi_y": ["Kiểm chứng bằng công thức đỉnh dịch.", "Giảm $h$ của Euler thì đỉnh thay đổi thế nào?", "Công thức cho $I_{\\max}=?$"],
     "giai_thich": ["Công thức giải tích cho $I_{\\max}\\approx212{,}25$; Euler tiến về giá trị này khi $h$ giảm (216 với $h=0{,}1$)."]},
    {"ma": "B3.7", "bai": "bai3", "muc": "Mở rộng", "dang": "tính toán", "loai": "so",
     "de": "Hiệu chỉnh $\\beta$ để **nghiệm liên tục** cho $I(1)=9$ ($S_0=995$, $I_0=5$, $\\gamma=0{,}6$). $\\beta\\approx$? (4 chữ số thập phân)",
     "goi_y": ["Đây không phải một bước Euler.", "Giải $I(1;\\beta)=9$ bằng tìm nghiệm (Brent) với nghiệm tham chiếu.",
               "Dùng công cụ trong tab Mô phỏng của Bài 3."],
     "dap_an": lambda: models.sir_hieu_chinh_beta(995, 5, 1000, 0.6, 1.0, 9.0, khoang=(0.6, 3.0)), "dung_sai": 1e-4,
     "giai_thich": ["$\\beta_C\\approx1{,}1982$, $\\mathcal R_0\\approx1{,}997$; một bước Euler cho $1{,}4070$ (VD31).",
                    "Sai số rời rạc hóa xuất hiện ngay trong khâu ước lượng tham số."]},
    {"ma": "B3.8", "bai": "bai3", "muc": "Mở rộng", "dang": "phản biện", "loai": "mo",
     "de": "Một báo cáo kết luận: ``mô hình SIR đã được thẩm định vì khớp đúng dữ kiện $I(1)=9$''. Phản biện.",
     "goi_y": ["Bao nhiêu dữ kiện, bao nhiêu tham số được hiệu chỉnh?", "Thẩm định cần dữ liệu độc lập.",
               "Phân biệt kiểm chứng và thẩm định."],
     "dap_an": "Một tham số được chọn để khớp đúng một dữ kiện thì khớp là đương nhiên, không chứng minh gì về khả năng mô tả "
               "hiện tượng. Thẩm định đòi hỏi so sánh với dữ liệu không dùng để hiệu chỉnh (chuỗi ca bệnh theo thời gian, "
               "đã mô hình hóa quá trình báo cáo). Mô hình ở đây chỉ được kiểm chứng tính toán.",
     "giai_thich": []},
    {"ma": "B3.9", "bai": "bai3", "muc": "Vận dụng", "dang": "tính toán", "loai": "so",
     "de": "$\\mathcal R_0=0{,}9$. Ngưỡng miễn dịch lý tưởng $p_c$ (%)?",
     "goi_y": ["$p_c=\\max(0,1-1/\\mathcal R_0)$.", "$1-1/0{,}9$ âm.", "Tỉ lệ không thể âm."],
     "dap_an": lambda: 100 * models.nguong_mien_dich(0.9), "dung_sai": 1e-6,
     "giai_thich": ["$p_c=0$: không cần miễn dịch trước; giá trị âm không có nghĩa (VD28)."]},
    # ------------------------------------------------------------------ Bài 4
    {"ma": "B4.1", "bai": "bai4", "muc": "Cơ bản", "dang": "đọc đồ thị", "loai": "chon",
     "de": "Hệ $\\mathbf y'=A\\mathbf y$ với $A=\\begin{pmatrix}1&2\\\\2&1\\end{pmatrix}$. Gốc tọa độ là loại điểm cân bằng nào?",
     "lua_chon": ["nút hút", "yên ngựa", "tiêu điểm hút", "tâm"],
     "dap_an": 1,
     "goi_y": ["Tính $\\det A$.", "$\\det A=-3<0$.", "$\\det A<0$ ⇒ hai trị riêng trái dấu."],
     "giai_thich": ["Trị riêng $3$ và $-1$ trái dấu ⇒ yên ngựa, không ổn định."]},
    {"ma": "B4.2", "bai": "bai4", "muc": "Vận dụng", "dang": "phát hiện giả thiết sai", "loai": "chon",
     "de": "$A=\\begin{pmatrix}-1&0\\\\0&-1\\end{pmatrix}$ (trị riêng kép $-1$). Một bạn viết nghiệm $e^{-t}\\mathbf v_1$, $te^{-t}\\mathbf v_2$. Đúng không?",
     "lua_chon": ["Đúng", "Sai: có hai vectơ riêng độc lập nên nghiệm là $e^{-t}\\mathbf v_1$, $e^{-t}\\mathbf v_2$",
                  "Sai: phải là $e^{t}$", "Sai: hệ không có nghiệm"],
     "dap_an": 1,
     "goi_y": ["So sánh bội đại số và bội hình học.", "$A+I=0$ có không gian nghiệm bao nhiêu chiều?",
               "Chỉ cần chuỗi Jordan khi thiếu vectơ riêng."],
     "giai_thich": ["Bội hình học bằng 2 = bội đại số: $A$ chéo hóa được, không cần số hạng $te^{-t}$ (nút sao)."]},
    {"ma": "B4.3", "bai": "bai4", "muc": "Vận dụng", "dang": "tính toán", "loai": "so",
     "de": "RK4 một bước $h=0{,}2$ cho $x'=x-4y$, $y'=-x+y$, $(x_0,y_0)=(1,0)$. Tính $x_1$ (6 chữ số thập phân).",
     "goi_y": ["$\\mathbf K_1=h\\mathbf f(\\mathbf y_0)=(0{,}2;-0{,}2)$.", "$\\mathbf K_2=(0{,}3;-0{,}24)$, $\\mathbf K_3=(0{,}326;-0{,}254)$.",
               "$\\mathbf K_4=(0{,}4684;-0{,}316)$; $x_1=1+(K_1+2K_2+2K_3+K_4)_x/6$."],
     "dap_an": _rk4_he_x1, "dung_sai": 1e-6,
     "giai_thich": ["$x_1=1+1{,}9204/6\\approx1{,}320067$; nghiệm đúng $1{,}320425$ (khớp \\texttt{expm})."]},
    {"ma": "B4.4", "bai": "bai4", "muc": "Mở rộng", "dang": "phản biện", "loai": "chon",
     "de": "Tại một điểm cân bằng của hệ phi tuyến, ma trận Jacobi có trị riêng $\\pm i$. Kết luận nào đúng?",
     "lua_chon": ["Điểm đó là tâm", "Điểm đó ổn định tiệm cận", "Tuyến tính hóa chưa đủ để kết luận", "Điểm đó không ổn định"],
     "dap_an": 2,
     "goi_y": ["Tiêu chuẩn tuyến tính hóa có ba trường hợp.", "Trị riêng phần thực bằng 0 thuộc trường hợp nào?",
               "Xem phản ví dụ $x'=-y+x(x^2+y^2)$, $y'=x+y(x^2+y^2)$."],
     "giai_thich": ["Phần thực bằng 0: chưa kết luận. Phản ví dụ có Jacobi $\\pm i$ nhưng gốc không ổn định."]},
    {"ma": "B4.5", "bai": "bai4", "muc": "Mở rộng", "dang": "phản biện", "loai": "chon",
     "de": "Mô hình cạnh tranh $x'=(1-y)x$, $y'=(0{,}5-0{,}5x)y$. Phát biểu nào **đúng**?",
     "lua_chon": ["Mọi trạng thái đầu dương đều dẫn tới loại trừ một loài",
                  "Trạng thái đầu nằm trên đường phân cách tiến về điểm cùng tồn tại $(1,1)$",
                  "$(1,1)$ là nút hút", "Hai loài luôn cùng tồn tại"],
     "dap_an": 1,
     "goi_y": ["Tính Jacobi tại $(1,1)$.", "Trị riêng $\\pm0{,}707$: yên ngựa.", "Đa tạp ổn định của yên ngựa là gì?"],
     "giai_thich": ["$(1,1)$ là yên ngựa; đa tạp ổn định là đường phân cách; trên đó quỹ đạo tiến về $(1,1)$ (VD54)."]},
    # ------------------------------------------------------------------ Phương pháp số
    {"ma": "S.1", "bai": "so", "muc": "Cơ bản", "dang": "tính toán", "loai": "so",
     "de": "$y'=1+y$, $y(0)=1$, $h=0{,}1$. Giá trị Euler $y_3$?",
     "goi_y": ["$y_{n+1}=y_n+h(1+y_n)$.", "$y_1=1{,}2$.", "$y_2=1{,}42$."],
     "dap_an": _euler_y3, "dung_sai": 1e-6,
     "giai_thich": ["$y_3=1{,}42+0{,}1\\cdot2{,}42=1{,}662$; nghiệm đúng $1{,}699718$ (VD33)."]},
    {"ma": "S.2", "bai": "so", "muc": "Cơ bản", "dang": "đánh giá sai số", "loai": "chon",
     "de": "Giảm $h$ một nửa thì sai số toàn cục của RK4 (nghiệm đủ trơn) giảm khoảng bao nhiêu lần?",
     "lua_chon": ["2", "4", "8", "16"], "dap_an": 3,
     "goi_y": ["Sai số toàn cục RK4 là $O(h^p)$ với $p=?$", "$p=4$.", "$2^4=?$"],
     "giai_thich": ["$E(h/2)/E(h)\\approx2^{-4}$: giảm khoảng 16 lần; bảng đồ án đo được bậc $3{,}94$ (VD36)."]},
    {"ma": "S.3", "bai": "so", "muc": "Vận dụng", "dang": "chọn phương pháp", "loai": "chon",
     "de": "Bài toán $\\mathbf u'=\\bigl(\\begin{smallmatrix}9&24\\\\-24&-51\\end{smallmatrix}\\bigr)\\mathbf u+\\mathbf g(t)$ (trị riêng $-3$, $-39$). Nên dùng gì?",
     "lua_chon": ["Euler bước lớn", "RK4 bước $h=0{,}1$", "Bộ giải ẩn cho bài toán cứng (ví dụ ode15s)", "Không giải số được"],
     "dap_an": 2,
     "goi_y": ["Tính $z=h\\lambda$ với $\\lambda=-39$, $h=0{,}1$.", "$z=-3{,}9$ có nằm trong miền ổn định RK4?",
               "Biên trái của miền ổn định RK4 trên trục thực khoảng $-2{,}785$."],
     "giai_thich": ["Hệ cứng: RK4 với $h=0{,}1$ bùng nổ; phương pháp ẩn ổn định với bước lớn (VD40)."]},
    {"ma": "S.4", "bai": "so", "muc": "Vận dụng", "dang": "tính toán", "loai": "so",
     "de": "$y'=-30y$, $h=0{,}1$. Hệ số khuếch đại $Q$ của RK4?",
     "goi_y": ["$z=h\\lambda=-3$.", "$Q(z)=1+z+z^2/2+z^3/6+z^4/24$.", "Thay $z=-3$."],
     "dap_an": lambda: 1 - 3 + 4.5 - 4.5 + 81 / 24, "dung_sai": 1e-9,
     "giai_thich": ["$Q=1{,}375>1$ ⇒ nghiệm số tăng dù nghiệm đúng giảm về 0 (VD37)."]},
    {"ma": "S.5", "bai": "so", "muc": "Mở rộng", "dang": "phát hiện giả thiết sai", "loai": "chon",
     "de": "Tài liệu A ghi ``sai số địa phương của Euler là $O(h^2)$'', tài liệu B ghi ``$O(h)$''. Kết luận?",
     "lua_chon": ["A sai", "B sai", "Hai quy ước khác nhau: chưa chia $h$ ($O(h^2)$) và đã chia $h$ ($O(h)$)",
                  "Cả hai sai: là $O(h^3)$"],
     "dap_an": 2,
     "goi_y": ["So định nghĩa sai số địa phương của hai tài liệu.", "Burden–Faires chia cho $h$.", "Sai số toàn cục của Euler là bao nhiêu?"],
     "giai_thich": ["Sai số một bước chưa chia $h$: $O(h^2)$; sai số cắt cụt đã chia $h$: $O(h)$; toàn cục: $O(h)$."]},
    {"ma": "S.6", "bai": "so", "muc": "Mở rộng", "dang": "đánh giá sai số", "loai": "mo",
     "de": "Giải $x''+4x=0$, $x(0)=1$, $x'(0)=0$ bằng Euler $h=0{,}1$ đến $t=10$: năng lượng tăng từ 2 lên khoảng 101. "
           "Vì sao? Nên dùng tiêu chí kiểm chứng nào?",
     "goi_y": ["Viết ma trận một bước Euler cho hệ dao động.", "$E_{n+1}=(1+h^2\\omega^2)E_n$.", "So sánh với RK4."],
     "dap_an": "Euler nhân năng lượng với $1+h^2\\omega^2=1{,}04$ mỗi bước: $2\\cdot1{,}04^{100}\\approx101$. Không phương pháp tường minh "
               "nào bảo toàn chính xác; tiêu chí hợp lý là theo dõi trôi năng lượng khi giảm $h$ (RK4: trôi giảm theo $h^5$) (VD44).",
     "giai_thich": []},
]


def M_ca_moi_tuan_1():
    sol, _ = models.sir_giai(995, 5, 1000, 1.407, 0.6, 2)
    return models.sir_ca_moi(sol, 0, 1)


DANG = ["tính toán", "kiểm tra đơn vị", "đọc đồ thị", "phát hiện giả thiết sai", "chọn phương pháp", "chọn bước lưới",
        "đánh giá sai số", "phản biện"]
