"""Chín cảnh hoạt hình (Manim Community 0.19) cho bài giảng mô hình toán học của đồ án.

Mọi số liệu được tính từ module hoc_lieu/mhtoan (dùng chung với đồ án, website và MATLAB).
Mỗi cảnh ghi lại (khi kết xuất) mốc thời gian của từng câu thuyết minh và từng câu hỏi dừng vào
video/thong_tin/<Cảnh>.json; ket_xuat.py dùng các mốc này để sinh phụ đề .srt và thong_tin_video.json.
Video KHÔNG có âm thanh: lời thuyết minh được cung cấp dưới dạng phụ đề và bản chép lời.

Kết xuất nháp:        python -m manim -ql canh.py C1_TocDoTrungBinhDenDaoHam
Kết xuất chất lượng:  python ket_xuat.py   (cả chín cảnh, chép vào video/)
"""
import json
import os
import sys

import numpy as np
from manim import (BLUE, DOWN, GRAY, GREEN, LEFT, ORANGE, RED, RIGHT, UL, UP, UR, WHITE, YELLOW,
                   Arrow, Axes, Create, DashedLine, Dot, FadeIn, FadeOut, Line, MathTex, NumberLine,
                   Rectangle, Scene, SurroundingRectangle, Text, Transform, ValueTracker, VGroup, Write,
                   always_redraw, config)

THU_MUC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(THU_MUC))
from mhtoan import analysis as A, data as D, he_tuyen_tinh as H, models as M, solvers as S  # noqa: E402

PHONG = "Arial"          # phông có đủ dấu tiếng Việt trên Windows (không có ký tự 𝓡, ₀: dùng "R0")
config.background_color = "#1e1e1e"


def chu(s, co=28, mau=WHITE):
    return Text(s, font=PHONG, font_size=co, color=mau)


def tieu_de(scene, s):
    t = chu(s, 34, YELLOW).to_edge(UP)
    scene.play(Write(t), run_time=1.2)
    return t


def cau_hoi_dung(scene, s, goi_y, giay=3.0):
    """Câu hỏi dừng: giảng viên tạm dừng video để người học dự đoán. Mốc thời gian được ghi lại."""
    scene.ghi_cau_hoi(s, goi_y)
    h = chu("Dừng lại: " + s, 26, ORANGE)
    h.to_edge(DOWN)
    # nền đặc che phần hình phía sau (nhãn trục) để câu hỏi luôn đọc được
    khung = SurroundingRectangle(h, color=ORANGE, buff=0.15, fill_color="#1e1e1e", fill_opacity=0.95)
    scene.play(FadeIn(khung), FadeIn(h))
    scene.wait(giay)
    scene.play(FadeOut(h), FadeOut(khung))


class CanhHocLieu(Scene):
    """Cảnh có ghi mốc thời gian thuyết minh (phụ đề) và câu hỏi dừng."""
    TIEU_DE = ""
    MUC_TIEU = ""
    BAI_TAP = []

    def setup(self):
        self._phu_de, self._cau_hoi = [], []

    KY_TU_MOI_GIAY = 15.0   # tốc độ đọc phụ đề; mỗi câu hiện ít nhất max(2,5 s, độ dài/15) giây

    def _du_thoi_gian_doc(self):
        """Chờ thêm (giữ nguyên khung hình) nếu câu phụ đề đang hiện chưa đủ thời gian để đọc."""
        if self._phu_de and self._phu_de[-1]["t1"] is None:
            d = self._phu_de[-1]
            can = max(2.5, len(d["text"]) / self.KY_TU_MOI_GIAY)
            thieu = d["t0"] + can - self.renderer.time
            if thieu > 0.05:
                self.wait(thieu)
            d["t1"] = self.renderer.time

    def noi(self, van_ban):
        """Bắt đầu một câu thuyết minh tại thời điểm hiện tại của cảnh (kết thúc câu trước)."""
        self._du_thoi_gian_doc()
        t = self.renderer.time
        self._phu_de.append({"t0": t, "t1": None, "text": van_ban})

    def ghi_cau_hoi(self, cau_hoi, goi_y):
        self._cau_hoi.append({"t": self.renderer.time, "cau_hoi": cau_hoi, "goi_y": goi_y})

    def tear_down(self):
        self._du_thoi_gian_doc()
        t = self.renderer.time
        thu_muc = os.path.join(THU_MUC, "video", "thong_tin")
        os.makedirs(thu_muc, exist_ok=True)
        with open(os.path.join(thu_muc, f"{type(self).__name__}.json"), "w", encoding="utf-8") as fo:
            json.dump({"tieu_de": self.TIEU_DE, "muc_tieu": self.MUC_TIEU, "bai_tap": self.BAI_TAP,
                       "thoi_luong": t, "loi_thuyet_minh": self._phu_de, "cau_hoi_dung": self._cau_hoi},
                      fo, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------------------
class C1_TocDoTrungBinhDenDaoHam(CanhHocLieu):
    TIEU_DE = "Từ tốc độ trung bình đến đạo hàm"
    MUC_TIEU = "Hiểu đạo hàm là giới hạn của tốc độ thay đổi trung bình (hệ số góc cát tuyến → tiếp tuyến)."
    BAI_TAP = ["B1.3", "VD02"]

    def construct(self):
        self.noi("Dữ liệu sinh khối nấm men theo giờ (Pearl 1927) và đường cong logistic khớp với dữ liệu.")
        tieu_de(self, self.TIEU_DE)
        nm = D.NAM_MEN
        r, K, P0 = 0.55, 665.0, 9.6
        P = lambda t: float(M.logistic_chinh_xac(t, P0, r, K))  # noqa: E731
        ax = Axes(x_range=[0, 18, 2], y_range=[0, 700, 100], x_length=9, y_length=5,
                  axis_config={"include_numbers": True, "font_size": 20}).shift(DOWN * 0.3)
        nhan = VGroup(chu("t (giờ)", 22).next_to(ax.x_axis, RIGHT, buff=0.15),
                      chu("P (sinh khối)", 22).next_to(ax.y_axis, UP, buff=0.1))
        diem = VGroup(*[Dot(ax.c2p(t, p), radius=0.05, color=BLUE) for t, p in zip(nm["t"], nm["P"])])
        self.play(Create(ax), FadeIn(nhan), FadeIn(diem))
        duong = ax.plot(P, x_range=[0, 18], color=GREEN)
        self.play(Create(duong))
        t0 = 6.0
        dt = ValueTracker(4.0)

        def cat_tuyen():
            t1 = t0 + dt.get_value()
            k = (P(t1) - P(t0)) / (t1 - t0)
            return ax.plot(lambda x: P(t0) + k * (x - t0), x_range=[t0 - 2.5, min(t1 + 2.5, 18)], color=YELLOW)

        ct = always_redraw(cat_tuyen)
        d0 = Dot(ax.c2p(t0, P(t0)), color=RED)
        d1 = always_redraw(lambda: Dot(ax.c2p(t0 + dt.get_value(), P(t0 + dt.get_value())), color=RED))
        ct_so = always_redraw(lambda: MathTex(
            r"\frac{\Delta P}{\Delta t}=" + f"{(P(t0 + dt.get_value()) - P(t0)) / dt.get_value():.2f}".replace(".", "{,}"),
            font_size=34).to_corner(UR).shift(DOWN * 0.9))
        self.noi("Trong bốn giờ kể từ giờ thứ sáu, sinh khối tăng trung bình khoảng 83 đơn vị mỗi giờ: "
                 "đó là hệ số góc của cát tuyến.")
        self.play(FadeIn(d0), FadeIn(d1), Create(ct), FadeIn(ct_so))
        cau_hoi_dung(self, "khi Δt nhỏ dần, hệ số góc cát tuyến tiến tới đâu?",
                     "Tiến tới hệ số góc tiếp tuyến tại t = 6, tức đạo hàm P'(6) ≈ 74,4 đơn vị/giờ.")
        self.noi("Thu hẹp khoảng thời gian: tốc độ trung bình thay đổi và ổn định quanh khoảng 74,4 đơn vị mỗi giờ.")
        self.play(dt.animate.set_value(0.02), run_time=5)
        dao_ham = r * P(t0) * (1 - P(t0) / K)
        kq = MathTex(r"P'(6)=rP\left(1-\frac{P}{K}\right)\approx " + f"{dao_ham:.2f}".replace(".", "{,}"),
                     font_size=34).to_corner(UR).shift(DOWN * 1.9)
        self.noi("Giới hạn đó là tốc độ tức thời — đạo hàm của mô hình, hệ số góc của tiếp tuyến. "
                 "Đạo hàm tính trên mô hình, không trên các điểm đo rời rạc.")
        self.play(Write(kq))
        self.wait(2)


# ---------------------------------------------------------------------------
class C2_CanBangSinhTu(CanhHocLieu):
    TIEU_DE = "Cân bằng sinh – tử"
    MUC_TIEU = "Lập phương trình P' = (b − d)P từ nguyên lý 'thay đổi = vào − ra' và kiểm tra đơn vị."
    BAI_TAP = ["B1.1", "B1.2", "VD07"]

    def construct(self):
        self.noi("Một quần thể P(t): số cá thể sinh ra là dòng vào, số cá thể chết là dòng ra.")
        tieu_de(self, self.TIEU_DE)
        hop = Rectangle(width=3, height=1.6, color=BLUE)
        ten = MathTex("P(t)", font_size=48).move_to(hop)
        vao = Arrow(LEFT * 5.5, hop.get_left(), color=GREEN, buff=0.1)
        ra = Arrow(hop.get_right(), RIGHT * 5.5, color=RED, buff=0.1)
        nv = VGroup(chu("sinh:", 28, GREEN), MathTex(r"bP\,\Delta t", font_size=34, color=GREEN))
        nv.arrange(RIGHT).next_to(vao, UP)
        nr = VGroup(chu("tử:", 28, RED), MathTex(r"dP\,\Delta t", font_size=34, color=RED))
        nr.arrange(RIGHT).next_to(ra, UP)
        self.play(Create(hop), Write(ten))
        self.noi("Trong khoảng thời gian ngắn Δt, số sinh tỉ lệ với quy mô quần thể và với độ dài Δt; số tử cũng vậy.")
        self.play(Create(vao), Write(nv))
        self.play(Create(ra), Write(nr))
        cau_hoi_dung(self, "trong khoảng Δt, P thay đổi bao nhiêu?",
                     "P(t+Δt) − P(t) = bPΔt − dPΔt + o(Δt): vào trừ ra.")
        self.noi("Hiệu của chúng là lượng thay đổi. Chia cho Δt và cho Δt tiến về 0, ta được phương trình vi phân.")
        b1 = MathTex(r"P(t+\Delta t)-P(t)=bP\,\Delta t-dP\,\Delta t+o(\Delta t)", font_size=38).shift(DOWN * 1.8)
        self.play(Write(b1))
        b2 = MathTex(r"\frac{dP}{dt}=(b-d)P=rP", font_size=44).shift(DOWN * 1.8)
        self.wait(1)
        self.play(Transform(b1, b2))
        self.noi("Kiểm tra đơn vị: r có đơn vị một trên thời gian, rP có đơn vị cá thể trên thời gian, như P'.")
        dv = chu("Kiểm tra đơn vị: [r] = 1/thời gian, [rP] = cá thể/thời gian", 24, GRAY).shift(DOWN * 2.9)
        self.play(FadeIn(dv))
        self.noi("Mô hình đúng trong phạm vi các giả thiết: b, d không đổi, không di cư, tài nguyên không giới hạn.")
        gia_thiet = chu("Giả thiết: b, d không đổi; không di cư; tài nguyên không giới hạn", 24, YELLOW)
        gia_thiet.shift(UP * 2.0)
        self.play(FadeIn(gia_thiet))
        self.wait(2)


# ---------------------------------------------------------------------------
class C3_MalthusNgoaiMienHieuLuc(CanhHocLieu):
    TIEU_DE = "Malthus ngoài miền hiệu lực"
    MUC_TIEU = "Miền hiệu lực gắn với một tiêu chí sai số; khớp tốt trên dữ liệu huấn luyện chưa chắc dự báo tốt."
    BAI_TAP = ["B1.4", "B1.5", "VD10"]

    def construct(self):
        self.noi("Khớp mô hình Malthus trên năm giờ đầu của dữ liệu nấm men.")
        tieu_de(self, self.TIEU_DE)
        nm = D.NAM_MEN
        t, P = nm["t"], nm["P"]
        k = A.khop_malthus_log(t[:5], P[:5])
        du_bao = lambda x: float(k["P0"] * np.exp(k["r"] * x))  # noqa: E731
        ax = Axes(x_range=[0, 12, 2], y_range=[0, 1600, 400], x_length=9, y_length=4.4,
                  axis_config={"include_numbers": True, "font_size": 20}).shift(DOWN * 0.3)
        self.play(Create(ax))
        diem = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=BLUE) for a, b in zip(t[:11], P[:11])])
        self.play(FadeIn(diem[:5]))
        mo_ta = MathTex(r"P(t)\approx" + f"{k['P0']:.2f}".replace(".", "{,}") + r"\,e^{" +
                        f"{k['r']:.3f}".replace(".", "{,}") + r"t}", font_size=34).to_corner(UL).shift(DOWN * 0.9)
        cong = ax.plot(du_bao, x_range=[0, 4], color=GREEN)
        self.noi("Với năm giờ đầu, mô hình hàm mũ rất khớp.")
        self.play(Create(cong), Write(mo_ta))
        cau_hoi_dung(self, "mô hình này dự báo tốt đến giờ thứ mấy (sai số ≤ 10%)?",
                     "Đến giờ thứ 5 (sai số +3,7%); từ giờ thứ 6 sai số đã +16%.")
        self.noi("Khi dự báo xa hơn, sai số tăng có hệ thống: tài nguyên bắt đầu hạn chế.")
        cong2 = ax.plot(du_bao, x_range=[4, 10.6], color=GREEN)
        self.play(FadeIn(diem[5:]), Create(cong2), run_time=3)
        ss = A.sai_so_tuong_doi_phan_tram(np.array([du_bao(x) for x in t[:11]]), P[:11])
        vuot = int(np.argmax(np.abs(ss[5:]) > 10)) + 5
        vach = DashedLine(ax.c2p(vuot, 0), ax.c2p(vuot, 1600), color=RED)
        ghi = chu(f"từ t = {vuot} giờ: sai số {ss[vuot]:+.0f}% > 10%", 24, RED).move_to(ax.c2p(3.4, 1350))
        self.noi("Nếu chấp nhận sai số tối đa 10%, mô hình này chỉ dùng được đến giờ thứ năm.")
        self.play(Create(vach), FadeIn(ghi))
        cuoi = chu(f"t = 10: dự báo {du_bao(10):.0f}, quan sát {P[10]:.1f}  (gấp {du_bao(10) / P[10]:.2f} lần)".replace(".", ","),
                   24, YELLOW)
        cuoi.to_edge(DOWN, buff=0.1)
        self.noi("Ở giờ thứ mười, dự báo gấp gần ba lần quan sát. Kết luận gắn với bộ dữ liệu và tiêu chí đã chọn.")
        self.play(FadeIn(cuoi))
        self.wait(2)


# ---------------------------------------------------------------------------
class C4_LogisticDuongPha(CanhHocLieu):
    TIEU_DE = "Logistic: đường pha"
    MUC_TIEU = "Đọc dấu của f(P) để biết chiều biến thiên; xác định cân bằng và tính ổn định qua f'."
    BAI_TAP = ["B2.1", "B2.2", "VD15"]

    def construct(self):
        self.noi("Đồ thị vế phải f(P) = rP(1 − P/K) với r = 1, K = 100.")
        tieu_de(self, self.TIEU_DE)
        r, K = 1.0, 100.0
        ax = Axes(x_range=[-10, 130, 20], y_range=[-15, 30, 10], x_length=8, y_length=3.6,
                  axis_config={"include_numbers": True, "font_size": 18}).shift(UP * 0.6)
        f = lambda P: r * P * (1 - P / K)  # noqa: E731
        pt = MathTex(r"f(P)=rP\left(1-\frac{P}{K}\right)", font_size=34).to_corner(UR).shift(DOWN * 0.9)
        self.play(Create(ax), Write(pt))
        self.play(Create(ax.plot(f, x_range=[-10, 125], color=GREEN)))
        cau_hoi_dung(self, "ở đâu P tăng, ở đâu P giảm?",
                     "P tăng khi f(P) > 0 (0 < P < K), giảm khi f(P) < 0 (P > K).")
        self.noi("Ở đâu f dương, quần thể tăng; ở đâu f âm, quần thể giảm.")
        dt = NumberLine(x_range=[-10, 130, 10], length=8, include_ticks=False).shift(DOWN * 2.2)
        self.play(Create(dt))
        p0 = Dot(dt.n2p(0), color=RED)
        pK = Dot(dt.n2p(K), color=BLUE)
        self.play(FadeIn(p0), FadeIn(pK), FadeIn(MathTex("0", font_size=28).next_to(p0, DOWN)),
                  FadeIn(MathTex("K", font_size=28).next_to(pK, DOWN)))
        mui = VGroup(Arrow(dt.n2p(30), dt.n2p(70), buff=0, color=YELLOW),
                     Arrow(dt.n2p(125), dt.n2p(105), buff=0, color=YELLOW),
                     Arrow(dt.n2p(-3), dt.n2p(-10), buff=0, color=YELLOW))
        self.play(Create(mui))
        self.noi("Điểm 0 không ổn định vì f'(0) = r dương; điểm K ổn định tiệm cận vì f'(K) = −r âm. "
                 "Mọi nghiệm xuất phát dương đều tiến về K.")
        nx = chu("0 không ổn định (f'(0) = r > 0);  K ổn định tiệm cận (f'(K) = −r < 0)", 24)
        nx.to_edge(DOWN, buff=0.15)
        self.play(FadeIn(nx))
        uon = Dot(ax.c2p(K / 2, f(K / 2)), color=ORANGE)
        ghi = VGroup(MathTex(r"P=K/2:", font_size=28, color=ORANGE), chu("P' lớn nhất", 22, ORANGE))
        ghi.arrange(RIGHT).next_to(uon, UP)
        self.noi("Đỉnh của f tại P = K/2: quần thể tăng nhanh nhất khi đạt một nửa sức chứa, với tốc độ rK/4.")
        self.play(FadeIn(uon), Write(ghi))
        self.wait(2)


# ---------------------------------------------------------------------------
class C5_SIRSoDoNgan(CanhHocLieu):
    TIEU_DE = "Mô hình SIR: sơ đồ ngăn"
    MUC_TIEU = "Đọc sơ đồ ngăn thành hệ phương trình; tốc độ chuyển ngăn; bảo toàn S + I + R."
    BAI_TAP = ["B3.1", "B3.4", "VD23"]

    def construct(self):
        self.noi("Cộng đồng được chia thành ba ngăn: cảm nhiễm S, đang nhiễm I, loại ra R.")
        tieu_de(self, self.TIEU_DE)
        c = D.CUM_GIAO_KHOA
        hop = [Rectangle(width=1.6, height=1.1, color=m) for m in (BLUE, RED, GREEN)]
        for i, h in enumerate(hop):
            h.move_to(LEFT * 4 + RIGHT * 4 * i + UP * 1.6)
        ten = [MathTex(s, font_size=44).move_to(h) for s, h in zip("SIR", hop)]
        m1 = Arrow(hop[0].get_right(), hop[1].get_left(), buff=0.1)
        m2 = Arrow(hop[1].get_right(), hop[2].get_left(), buff=0.1)
        n1 = MathTex(r"\beta\frac{SI}{N}", font_size=34).next_to(m1, UP)
        n2 = MathTex(r"\gamma I", font_size=34).next_to(m2, UP)
        dv = chu("tốc độ chuyển ngăn (người/tuần)", 18, GRAY).next_to(VGroup(m1, m2), DOWN, buff=0.15)
        self.play(*[Create(h) for h in hop], *[Write(t) for t in ten])
        self.noi("Mỗi mũi tên là một tốc độ chuyển ngăn, tính bằng người trên tuần; nguy cơ trên mỗi người cảm nhiễm là β·I/N.")
        self.play(Create(m1), Write(n1), Create(m2), Write(n2), FadeIn(dv))
        y_nghia = chu("I: đang nhiễm và có khả năng lây;  1/γ: thời gian mắc bệnh trung bình", 22, GRAY)
        y_nghia.next_to(VGroup(*hop), DOWN, buff=0.6)
        self.play(FadeIn(y_nghia))
        cau_hoi_dung(self, "tổng S + I + R thay đổi thế nào theo thời gian?",
                     "Không đổi: dòng ra khỏi S bằng dòng vào I, dòng ra khỏi I bằng dòng vào R.")
        self.noi("Dòng ra khỏi S bằng dòng vào I; dòng ra khỏi I bằng dòng vào R. Vì vậy tổng S + I + R không đổi.")
        self.play(FadeOut(y_nghia))
        sol, td = M.sir_giai(c["S0"], c["I0"], c["N"], c["beta"], c["gamma"], 24)
        ax = Axes(x_range=[0, 24, 4], y_range=[0, 1000, 500], x_length=8, y_length=2.9,
                  axis_config={"include_numbers": True, "font_size": 18}).shift(DOWN * 1.7)
        self.play(Create(ax))
        for j, m in enumerate((BLUE, RED, GREEN)):
            self.play(Create(ax.plot(lambda x, j=j: float(sol.sol(x)[j]), x_range=[0, 24], color=m)), run_time=1.5)
        pk = M.sir_dinh_dich(c["S0"], c["I0"], c["N"], c["beta"], c["gamma"])
        ghi = chu(f"β = 1,407; γ = 0,6 (1/tuần): đỉnh I ≈ {pk['I_max']:.1f} người tại t ≈ {td:.2f} tuần".replace(".", ","),
                  22, YELLOW).to_edge(DOWN, buff=0.1)
        self.noi("Với tham số cố định của tình huống giáo khoa, số người đang nhiễm đạt đỉnh khoảng 212 người ở tuần 6,85.")
        self.play(FadeIn(ghi))
        self.wait(2)


# ---------------------------------------------------------------------------
class C6_NguongDinhDich(CanhHocLieu):
    TIEU_DE = "Ngưỡng dịch: R_eff = R0·S/N"
    MUC_TIEU = "Điều kiện tăng ban đầu là R0·S(0)/N > 1, không chỉ R0 > 1; đỉnh dịch tại S = N/R0."
    BAI_TAP = ["B3.2", "B3.3", "VD24"]

    def construct(self):
        self.noi("Mặt phẳng pha (S, I) của mô hình SIR với R0 = 2,345.")
        tieu_de(self, self.TIEU_DE)
        c = D.CUM_GIAO_KHOA
        N, b, g, I0 = c["N"], c["beta"], c["gamma"], c["I0"]
        R0 = b / g
        ax = Axes(x_range=[0, 1000, 200], y_range=[0, 300, 100], x_length=8, y_length=4.2,
                  axis_config={"include_numbers": True, "font_size": 18}).shift(DOWN * 0.5)
        nhan = VGroup(MathTex("S", font_size=30).next_to(ax.x_axis, RIGHT),
                      MathTex("I", font_size=30).next_to(ax.y_axis, UP))
        self.play(Create(ax), FadeIn(nhan))
        Ss = N / R0
        vach = DashedLine(ax.c2p(Ss, 0), ax.c2p(Ss, 300), color=ORANGE)
        self.noi("Đường đứt nét S = N/R0: bên phải đường này, mỗi người bệnh lây cho hơn một người.")
        self.play(Create(vach), Write(MathTex(r"S=\frac{N}{\mathcal R_0}", font_size=30, color=ORANGE)
                                      .next_to(vach, UP, buff=0.05)))
        cau_hoi_dung(self, "bắt đầu với S(0) < N/R0 thì I tăng hay giảm?",
                     "Giảm ngay: R_eff(0) = R0·S(0)/N < 1, dù R0 > 1 (VD24).")
        for S0, m in ((995, RED), (700, YELLOW), (400, BLUE)):
            sol, _ = M.sir_giai(S0, I0, N, b, g, 60)
            tt = np.linspace(0, 60, 1500)
            y = sol.sol(tt)
            if S0 == 995:
                self.noi("Bắt đầu với 995 người cảm nhiễm: I tăng, đạt đỉnh đúng khi quỹ đạo cắt đường S = N/R0.")
            elif S0 == 400:
                self.noi("Bắt đầu với 400 người cảm nhiễm: R_eff ban đầu bằng 0,94, nhỏ hơn 1, nên I giảm ngay.")
            self.play(Create(ax.plot_line_graph(y[0], y[1], add_vertex_dots=False, line_color=m)), run_time=2)
            reff = R0 * S0 / N
            ghi = chu(f"S(0) = {S0}: R_eff(0) = {reff:.2f}".replace(".", ","), 22, m)
            ghi.to_corner(UR).shift(DOWN * (0.9 + 0.45 * [995, 700, 400].index(S0)))
            self.play(FadeIn(ghi))
        kl = chu("I tăng ban đầu khi và chỉ khi R0·S(0)/N > 1 (với I(0) > 0), không chỉ R0 > 1", 22, YELLOW).to_edge(DOWN, buff=0.15)
        self.noi("Cùng một bệnh, cùng R0, nhưng kết cục phụ thuộc số người còn cảm nhiễm. Dịch kết thúc khi vẫn còn người chưa mắc.")
        self.play(FadeIn(kl))
        self.wait(2)


# ---------------------------------------------------------------------------
class C7_MotBuocEulerHeunRK4(CanhHocLieu):
    TIEU_DE = "Một bước: Euler, Heun, RK4"
    MUC_TIEU = "Thấy hình học của một bước giải số và chi phí (số lần tính f) của mỗi phương pháp."
    BAI_TAP = ["S.1", "VD33", "VD34", "VD35"]

    def construct(self):
        self.noi("Một bước h = 2 giờ cho mô hình logistic nấm men, xuất phát từ P0 = 9,6.")
        tieu_de(self, self.TIEU_DE)
        r, K, P0, h = 0.55, 665.0, 9.6, 2.0
        f = M.logistic_rhs(r, K)
        ex = lambda t: float(M.logistic_chinh_xac(t, P0, r, K))  # noqa: E731
        ax = Axes(x_range=[0, 2.5, 0.5], y_range=[0, 40, 10], x_length=6.5, y_length=4.4,
                  axis_config={"include_numbers": True, "font_size": 18}).shift(DOWN * 0.5 + RIGHT * 2.3)
        self.play(Create(ax), Create(ax.plot(ex, x_range=[0, 2.4], color=GREEN)))
        d0 = Dot(ax.c2p(0, P0))
        self.play(FadeIn(d0))
        k1 = float(f(0, np.array([P0]))[0])
        tt = Line(ax.c2p(0, P0), ax.c2p(h, P0 + h * k1), color=YELLOW)
        self.noi("Euler đi theo tiếp tuyến tại đầu bước.")
        self.play(Create(tt))
        cau_hoi_dung(self, "điểm Euler nằm trên hay dưới nghiệm đúng? Vì sao?",
                     "Dưới: nghiệm đang cong lên (lõm lên) nên tiếp tuyến ở đầu bước nằm dưới đường cong.")
        kq = {"Euler": S.buoc_euler(f, 0.0, np.array([P0]), h)[0],
              "Heun": S.buoc_heun(f, 0.0, np.array([P0]), h)[0],
              "RK4": S.buoc_rk4(f, 0.0, np.array([P0]), h)[0]}
        mau = {"Euler": YELLOW, "Heun": BLUE, "RK4": RED}
        self.noi("Heun lấy trung bình hệ số góc ở hai đầu bước; RK4 dùng bốn hệ số góc với trọng số 1, 2, 2, 1.")
        for i, (ten, y) in enumerate(kq.items()):
            d = Dot(ax.c2p(h, y), color=mau[ten], radius=0.08)
            g = chu(f"{ten}: {y:.3f}   (sai số {abs(y - ex(h)):.3f})".replace(".", ","), 22, mau[ten])
            g.to_corner(UL).shift(DOWN * (0.9 + 0.45 * i))
            self.play(FadeIn(d), FadeIn(g))
        dung = chu(f"Nghiệm đúng P(2) = {ex(h):.3f}".replace(".", ","), 22, GREEN).to_corner(UL).shift(DOWN * 2.25)
        self.play(FadeIn(dung))
        so_lan = chu("Số lần tính f mỗi bước: Euler 1, Heun 2, RK4 4", 22, GRAY).to_edge(DOWN, buff=0.15)
        self.noi("Chính xác hơn nhưng mỗi bước tốn nhiều phép tính hơn: Euler một, Heun hai, RK4 bốn lần tính f.")
        self.play(FadeIn(so_lan))
        self.wait(2)


# ---------------------------------------------------------------------------
class C8_SaiSoVaOnDinh(CanhHocLieu):
    TIEU_DE = "Sai số và ổn định"
    MUC_TIEU = "Đọc bậc hội tụ từ độ dốc trên thang log; phân biệt độ chính xác với ổn định tuyệt đối."
    BAI_TAP = ["S.2", "S.3", "S.4", "VD36", "VD37"]

    def construct(self):
        self.noi("Sai số tại t = 10 của bài toán logistic khi giảm bước h, vẽ trên thang logarit.")
        tit = tieu_de(self, self.TIEU_DE)
        f = M.logistic_rhs(0.55, 665.0)
        ex = lambda t: M.logistic_chinh_xac(t, 9.6, 0.55, 665.0)  # noqa: E731
        hs = [1.0, 0.5, 0.25, 0.125]
        ax = Axes(x_range=[-1, 0.2, 0.2], y_range=[-5, 2.5, 1], x_length=6, y_length=4.2,
                  axis_config={"include_numbers": True, "font_size": 16}).shift(LEFT * 2.6 + DOWN * 0.5)
        nh = VGroup(MathTex(r"\log_{10}h", font_size=26).next_to(ax.x_axis, RIGHT, buff=0.1),
                    MathTex(r"\log_{10}E(h)", font_size=26).next_to(ax.y_axis, UP, buff=0.05).shift(RIGHT * 0.9))
        self.play(Create(ax), FadeIn(nh))
        cau_hoi_dung(self, "khi h giảm một nửa, sai số RK4 giảm bao nhiêu lần?",
                     "Khoảng 2⁴ = 16 lần (bậc 4); độ dốc trên thang log bằng bậc.")
        self.noi("Độ dốc của mỗi đường bằng bậc hội tụ: Euler khoảng 1, Heun khoảng 2, RK4 khoảng 4.")
        for pp, m, ten in ((S.euler, YELLOW, "Euler"), (S.heun, BLUE, "Heun"), (S.rk4, RED, "RK4")):
            e, p = A.bang_hoi_tu(pp, f, ex, 0.0, [9.6], 10.0, hs)
            x, y = np.log10(hs), np.log10(e)
            self.play(Create(ax.plot_line_graph(x, y, line_color=m, vertex_dot_style={"color": m})), run_time=1.2)
            g = chu(f"{ten}: bậc ≈ {p[-1]:.2f}".replace(".", ","), 20, m)
            g.next_to(ax, RIGHT, buff=0.3).shift(UP * (1.2 - 0.5 * ["Euler", "Heun", "RK4"].index(ten)))
            self.play(FadeIn(g))
        self.wait(1.0)
        self._du_thoi_gian_doc()
        self.clear()
        self.add(tit)
        self.noi("Nhưng độ chính xác cao không cứu được một bước quá lớn. Xét y' = −30y với h = 0,1.")
        pt = MathTex(r"y'=-30y,\quad y(0)=\tfrac13,\quad h=0{,}1\ (z=h\lambda=-3)", font_size=34).shift(UP * 2.2)
        self.play(Write(pt))
        hang = []
        for i, (ten, Q) in enumerate((("Euler", S.HE_SO_KHUECH_DAI["Euler"]), ("RK4", S.HE_SO_KHUECH_DAI["RK4"]))):
            q = Q(-3.0)
            hang.append(chu(f"{ten}: Q(−3) = {q:g};  y(1,5) = {(1 / 3) * q ** 15:.3g}".replace(".", ",").replace("-", "−").replace("e+04", "·10⁴"), 26,
                            RED).shift(UP * (1.0 - 0.6 * i)))
        jac = lambda t, y: np.array([[-30.0]])  # noqa: E731
        _, y_an, _ = S.euler_an(lambda t, y: -30 * y, jac, 0.0, [1 / 3], 0.1, 1.5)
        hang.append(chu(f"Euler ẩn: Q(−3) = 1/(1+3) = 0,25;  y(1,5) = {y_an[-1, 0]:.2g}".replace(".", ",").replace("e-10", "·10⁻¹⁰"), 26, GREEN)
                    .shift(UP * -0.2))
        self.noi("Euler và RK4 đều bùng nổ trong khi nghiệm đúng giảm về 0; Euler ẩn vẫn suy giảm.")
        for g in hang:
            self.play(FadeIn(g))
        kl = chu("Nghiệm đúng giảm về 0; phương pháp chỉ suy giảm theo khi |Q(hλ)| < 1", 24, YELLOW).shift(DOWN * 1.6)
        self.noi("Nghiệm số chỉ suy giảm theo khi trị tuyệt đối của hệ số khuếch đại nhỏ hơn 1: ổn định tuyệt đối "
                 "là một tính chất khác với bậc chính xác.")
        self.play(FadeIn(kl))
        self.wait(2.5)


# ---------------------------------------------------------------------------
class C9_MatPhangPha(CanhHocLieu):
    TIEU_DE = "Mặt phẳng pha của hệ tuyến tính"
    MUC_TIEU = ("Liên hệ quỹ đạo trong mặt phẳng pha với đồ thị x(t), y(t); đọc vai trò của vectơ riêng "
                "ở điểm yên ngựa.")
    BAI_TAP = ["B4.1", "B4.2", "VD46"]

    def construct(self):
        self.noi("Hệ x' = −0,4x + y, y' = −x − 0,4y. Bên trái: x(t) và y(t) theo thời gian. Bên phải: mặt phẳng pha.")
        tit = tieu_de(self, self.TIEU_DE)
        A1 = np.array([[-0.4, 1.0], [-1.0, -0.4]])
        y0 = np.array([1.6, 0.0])
        T = 8.0
        ax_t = Axes(x_range=[0, T, 2], y_range=[-1.6, 1.6, 0.8], x_length=5.2, y_length=3.4,
                    axis_config={"include_numbers": True, "font_size": 16}).shift(LEFT * 3.3 + DOWN * 0.6)
        ax_p = Axes(x_range=[-1.8, 1.8, 0.6], y_range=[-1.8, 1.8, 0.6], x_length=3.8, y_length=3.8,
                    axis_config={"include_numbers": False}).shift(RIGHT * 3.4 + DOWN * 0.6)
        nhan = VGroup(MathTex("t", font_size=26).next_to(ax_t.x_axis, RIGHT, buff=0.1),
                      MathTex("x", font_size=26).next_to(ax_p.x_axis, RIGHT, buff=0.1),
                      MathTex("y", font_size=26).next_to(ax_p.y_axis, UP, buff=0.05))
        self.play(Create(ax_t), Create(ax_p), FadeIn(nhan))
        tg = ValueTracker(0.0)
        nghiem = lambda t: H.nghiem_ma_tran_mu(A1, y0, t)  # noqa: E731
        duong_x = always_redraw(lambda: ax_t.plot(lambda s: float(nghiem(s)[0]), x_range=[0, max(tg.get_value(), 1e-3)],
                                                  color=BLUE))
        duong_y = always_redraw(lambda: ax_t.plot(lambda s: float(nghiem(s)[1]), x_range=[0, max(tg.get_value(), 1e-3)],
                                                  color=RED))
        quy_dao = always_redraw(lambda: ax_p.plot_line_graph(
            [float(nghiem(s)[0]) for s in np.linspace(0, max(tg.get_value(), 1e-3), 120)],
            [float(nghiem(s)[1]) for s in np.linspace(0, max(tg.get_value(), 1e-3), 120)],
            add_vertex_dots=False, line_color=YELLOW))
        cham = always_redraw(lambda: Dot(ax_p.c2p(*nghiem(tg.get_value())), color=WHITE, radius=0.07))
        chu_giai = VGroup(MathTex("x(t)", font_size=26, color=BLUE), MathTex("y(t)", font_size=26, color=RED))
        chu_giai.arrange(RIGHT, buff=0.4).next_to(ax_t, UP, buff=0.1)
        self.play(FadeIn(chu_giai))
        self.add(duong_x, duong_y, quy_dao, cham)
        self.noi("Mỗi điểm của mặt phẳng pha là một trạng thái (x, y); thời gian không hiện trên hình mà là chiều chuyển động.")
        self.play(tg.animate.set_value(T), run_time=6)
        chu_thich = chu("trị riêng −0,4 ± i: xoắn vào gốc (tiêu điểm hút)", 22, GRAY).to_edge(DOWN, buff=0.2)
        self.noi("Trị riêng phức với phần thực âm: x và y dao động tắt dần, quỹ đạo xoắn vào gốc.")
        self.play(FadeIn(chu_thich))
        self.wait(1.0)
        self._du_thoi_gian_doc()
        self.clear()
        self.add(tit)
        A2 = np.array([[1.0, 2.0], [2.0, 1.0]])
        ax2 = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=5.0, y_length=5.0,
                   axis_config={"include_numbers": False}).shift(DOWN * 0.5)
        self.noi("Hệ thứ hai có trị riêng 3 và −1: điểm yên ngựa. Các đường đỏ là hai vectơ riêng.")
        self.play(Create(ax2))
        v_on_dinh = VGroup(DashedLine(ax2.c2p(-2, 2), ax2.c2p(2, -2), color=RED))
        v_khong = VGroup(DashedLine(ax2.c2p(-2, -2), ax2.c2p(2, 2), color=RED))
        nhan_v = VGroup(MathTex(r"\lambda=-1", font_size=28, color=RED).next_to(ax2.c2p(-2, 2), RIGHT, buff=0.1),
                        MathTex(r"\lambda=3", font_size=28, color=RED).next_to(ax2.c2p(2, 2), RIGHT, buff=0.1))
        self.play(Create(v_on_dinh), Create(v_khong), FadeIn(nhan_v))
        cau_hoi_dung(self, "bắt đầu đúng trên vectơ riêng (1; −1) thì quỹ đạo đi đâu?",
                     "Đi thẳng vào gốc dọc theo vectơ riêng ứng với λ = −1 (đa tạp ổn định).")
        self.noi("Xuất phát đúng trên vectơ riêng ứng với −1, nghiệm đi thẳng vào gốc. Lệch một chút, nghiệm tiến gần gốc "
                 "rồi bị đẩy ra theo vectơ riêng ứng với 3.")
        for x0, mau in ((1.8, GREEN), (1.7, YELLOW), (1.9, BLUE)):
            y_bd = -1.8 if mau == GREEN else (-1.6 if mau == YELLOW else -2.0)
            ts = np.linspace(0, 2.2, 200)
            Y = np.array([H.nghiem_ma_tran_mu(A2, [x0, y_bd], t) for t in ts])
            Y = Y[np.all(np.abs(Y) < 2.2, axis=1)]
            self.add(Dot(ax2.c2p(x0, y_bd), color=mau, radius=0.06))
            self.play(Create(ax2.plot_line_graph(Y[:, 0], Y[:, 1], add_vertex_dots=False, line_color=mau)), run_time=1.5)
        kl = chu("Yên ngựa: không ổn định; vectơ riêng ứng với λ < 0 là đường đi vào gốc", 22, YELLOW).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(kl))
        self.wait(2)
