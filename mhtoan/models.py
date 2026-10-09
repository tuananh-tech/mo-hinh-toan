"""Các mô hình toán học của đồ án: vế phải, nghiệm giải tích và các đại
lượng đặc trưng. Mọi hàm kiểm tra miền tham số và báo lỗi rõ ràng thay vì
trả về kết quả vô nghĩa.
"""
from __future__ import annotations

import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


class ThamSoKhongHopLe(ValueError):
    """Tham số nằm ngoài miền có ý nghĩa của mô hình."""


def _yeu_cau(dieu_kien: bool, thong_bao: str) -> None:
    if not dieu_kien:
        raise ThamSoKhongHopLe(thong_bao)


# ============================================================================
# 1. MALTHUS  P' = r P
# ============================================================================
def malthus_rhs(r: float):
    return lambda t, P: r * P


def malthus_chinh_xac(t, P0: float, r: float, t0: float = 0.0):
    _yeu_cau(P0 > 0, "P0 phải dương")
    return P0 * np.exp(r * (np.asarray(t, float) - t0))


def thoi_gian_gap_doi(r: float) -> float:
    _yeu_cau(r > 0, "Chỉ định nghĩa thời gian tăng gấp đôi khi r > 0")
    return math.log(2.0) / r


def thoi_gian_ban_huy(r: float) -> float:
    _yeu_cau(r < 0, "Chỉ định nghĩa thời gian bán hủy khi r < 0")
    return math.log(2.0) / abs(r)


def doi_don_vi_ty_le(r: float, he_so: float) -> float:
    """Đổi r từ (đơn vị cũ)^-1 sang (đơn vị mới)^-1, với 1 đơn vị cũ = he_so đơn vị mới.
    Ví dụ: r theo năm^-1 sang tháng^-1: he_so = 12, kết quả r/12."""
    _yeu_cau(he_so > 0, "Hệ số đổi đơn vị phải dương")
    return r / he_so


# ============================================================================
# 2. LOGISTIC  P' = r P (1 - P/K)
# ============================================================================
def logistic_rhs(r: float, K: float):
    _yeu_cau(K > 0, "K phải dương")
    return lambda t, P: r * P * (1.0 - P / K)


def logistic_chinh_xac(t, P0: float, r: float, K: float, t0: float = 0.0):
    _yeu_cau(P0 > 0 and K > 0, "Cần P0 > 0, K > 0")
    t = np.asarray(t, float)
    return K * P0 / (P0 + (K - P0) * np.exp(-r * (t - t0)))


def logistic_t_uon(P0: float, r: float, K: float, t0: float = 0.0) -> float:
    """Thời điểm P = K/2. Chỉ có nghĩa khi 0 < P0 < K, r > 0.
    Nếu P0 > K/2 thì t* < t0 (điểm uốn đã xảy ra trước thời điểm đầu)."""
    _yeu_cau(0 < P0 < K and r > 0, "Cần 0 < P0 < K và r > 0")
    return t0 + math.log((K - P0) / P0) / r


def logistic_thoi_diem_dat(L: float, P0: float, r: float, K: float, t0: float = 0.0) -> float:
    """Thời điểm nghiệm logistic đạt mức L, với 0 < P0 < L < K."""
    _yeu_cau(0 < P0 < L < K and r > 0, "Cần 0 < P0 < L < K và r > 0")
    return t0 + math.log(L * (K - P0) / (P0 * (K - L))) / r


# ---------------------------------------------------------------------------
# Logistic có khai thác hằng số  P' = r P (1 - P/K) - H
# ---------------------------------------------------------------------------
def khai_thac_rhs(r: float, K: float, H: float):
    return lambda t, P: r * P * (1.0 - P / K) - H


def khai_thac_can_bang(r: float, K: float, H: float) -> dict:
    """Phân loại theo H so với ngưỡng rK/4 (Mục 3.3; VD19–VD21 ở Phụ lục A)."""
    _yeu_cau(r > 0 and K > 0 and H >= 0, "Cần r > 0, K > 0, H >= 0")
    Hc = r * K / 4.0
    tol = 1e-12 * max(1.0, Hc)
    if H < Hc - tol:
        d = math.sqrt(1.0 - H / Hc)
        P_thap, P_cao = K / 2 * (1 - d), K / 2 * (1 + d)
        return {"truong_hop": "H < rK/4", "H_toi_han": Hc,
                "can_bang": [(P_thap, "không ổn định"), (P_cao, "ổn định tiệm cận")]}
    if abs(H - Hc) <= tol:
        return {"truong_hop": "H = rK/4", "H_toi_han": Hc,
                "can_bang": [(K / 2, "nửa ổn định: hút từ bên phải, đẩy từ bên trái")]}
    return {"truong_hop": "H > rK/4", "H_toi_han": Hc, "can_bang": []}


def khai_thac_mo_phong(r, K, H, P0, T, rtol=1e-10, atol=1e-10, n_diem=400):
    """Giải P' = rP(1-P/K) - H trên [0, T]; DỪNG khi P chạm 0 (tuyệt chủng)
    thay vì tiếp tục tích phân sang giá trị âm vô nghĩa."""
    _yeu_cau(P0 >= 0 and T > 0, "Cần P0 >= 0, T > 0")

    def cham_khong(t, y):
        return y[0]
    cham_khong.terminal = True
    cham_khong.direction = -1
    sol = solve_ivp(lambda t, y: [r * y[0] * (1 - y[0] / K) - H], [0, T], [P0],
                    method="DOP853", rtol=rtol, atol=atol, events=cham_khong,
                    dense_output=True)
    t_end = sol.t[-1]
    t = np.linspace(0, t_end, n_diem)
    P = sol.sol(t)[0]
    t_tuyet_chung = sol.t_events[0][0] if len(sol.t_events[0]) else None
    return {"t": t, "P": P, "t_tuyet_chung": t_tuyet_chung}


# ============================================================================
# 3. SIR  S' = -beta S I/N, I' = beta S I/N - gamma I, R' = gamma I
# ============================================================================
def _kiem_tra_sir(S0, I0, N, beta, gamma, R_bd=None):
    _yeu_cau(N > 0 and beta >= 0 and gamma > 0, "Cần N > 0, beta >= 0, gamma > 0")
    _yeu_cau(S0 >= 0 and I0 >= 0, "Cần S0 >= 0, I0 >= 0")
    if R_bd is None:
        R_bd = N - S0 - I0
    _yeu_cau(R_bd >= -1e-9 * N, "Tổng S0 + I0 vượt quá N (R(0) < 0)")
    _yeu_cau(abs(S0 + I0 + R_bd - N) <= 1e-9 * N, "S0 + I0 + R(0) phải bằng N")
    return R_bd


def sir_rhs(beta: float, gamma: float, N: float):
    def f(t, y):
        S, I, R = y[0], y[1], y[2]
        inc = beta * S * I / N
        return np.array([-inc, inc - gamma * I, gamma * I])
    return f


def so_sinh_san_co_ban(beta: float, gamma: float) -> float:
    """R_0 = beta/gamma (dạng chuẩn beta S I/N)."""
    _yeu_cau(gamma > 0, "gamma phải dương")
    return beta / gamma


def so_sinh_san_hieu_dung(S, beta, gamma, N):
    """R_eff(t) = R_0 S(t)/N."""
    return so_sinh_san_co_ban(beta, gamma) * np.asarray(S, float) / N


def nguong_mien_dich(R0: float) -> float:
    """Ngưỡng miễn dịch cộng đồng lý tưởng max(0, 1 - 1/R0) (giả thiết:
    miễn dịch hoàn toàn, phân bố ngẫu nhiên, mô hình trộn đều)."""
    _yeu_cau(R0 > 0, "R0 phải dương")
    return max(0.0, 1.0 - 1.0 / R0)


def sir_dinh_dich(S0, I0, N, beta, gamma) -> dict:
    """Đỉnh của I(t) trên [0, inf). Nếu R0*S0/N <= 1 thì I giảm ngay từ đầu:
    cực đại đạt tại t = 0 (không có đỉnh nội tại)."""
    _kiem_tra_sir(S0, I0, N, beta, gamma)
    R0 = so_sinh_san_co_ban(beta, gamma)
    if I0 == 0:
        return {"noi_tai": False, "I_max": 0.0, "S_tai_dinh": S0, "ly_do": "I0 = 0: không có dịch"}
    if R0 * S0 / N <= 1.0:
        return {"noi_tai": False, "I_max": I0, "S_tai_dinh": S0,
                "ly_do": "R0*S0/N <= 1: I giảm ngay từ t = 0"}
    Ss = N / R0
    Imax = I0 + S0 - Ss - Ss * math.log(S0 / Ss)
    return {"noi_tai": True, "I_max": Imax, "S_tai_dinh": Ss, "ly_do": "R0*S0/N > 1"}


def sir_quy_mo_cuoi(S0, I0, N, beta, gamma, xtol=1e-12) -> float:
    """S_inf: nghiệm duy nhất trong (0, min(S0, N/R0)) của
        I0 + S0 - s + (N/R0) ln(s/S0) = 0.
    Nếu I0 = 0 thì không có lây nhiễm: S_inf = S0 (trả về trực tiếp, tránh
    chọn nghiệm sai nhánh)."""
    _kiem_tra_sir(S0, I0, N, beta, gamma)
    _yeu_cau(S0 > 0, "Cần S0 > 0")
    if I0 == 0:
        return float(S0)
    R0 = so_sinh_san_co_ban(beta, gamma)
    if R0 == 0:
        return float(S0)
    Ss = N / R0
    g = lambda s: I0 + S0 - s + Ss * math.log(s / S0)
    hi = min(S0, Ss)
    lo = hi
    for _ in range(2000):            # thu nhỏ cận dưới tới khi g đổi dấu
        lo *= 0.5
        if g(lo) < 0:
            break
    else:
        raise RuntimeError("Không tìm được ngoặc nghiệm cho S_inf")
    _yeu_cau(g(hi) > 0, "g(cận trên) phải dương; kiểm tra tham số")
    return brentq(g, lo, hi, xtol=xtol, rtol=4 * np.finfo(float).eps, maxiter=500)


def sir_giai(S0, I0, N, beta, gamma, T, t_eval=None, rtol=1e-11, atol=None,
             R_bd=None, phuong_phap="DOP853"):
    """Nghiệm tham chiếu (độ chính xác cao) của SIR trên [0, T]. Có sự kiện
    đỉnh dịch S = N/R0 (chỉ khi có đỉnh nội tại)."""
    R_bd = _kiem_tra_sir(S0, I0, N, beta, gamma, R_bd)
    if atol is None:
        atol = 1e-12 * N
    R0 = so_sinh_san_co_ban(beta, gamma)
    events = None
    if I0 > 0 and R0 * S0 / N > 1:
        def dinh(t, y):
            return y[0] - N / R0
        dinh.direction = -1
        events = dinh
    sol = solve_ivp(sir_rhs(beta, gamma, N), [0, T], [S0, I0, R_bd], method=phuong_phap,
                    rtol=rtol, atol=atol, t_eval=t_eval, dense_output=True, events=events)
    if not sol.success:
        raise RuntimeError("Bộ giải thất bại: " + sol.message)
    t_dinh = None
    if events is not None and len(sol.t_events[0]):
        t_dinh = float(sol.t_events[0][0])
    return sol, t_dinh


def sir_ca_moi(sol, a, b):
    """Số ca nhiễm mới trong [a, b] = tích phân của incidence beta S I/N
    = S(a) - S(b) (vì S' = -incidence). Khác với số đang nhiễm I(t)."""
    return float(sol.sol(a)[0] - sol.sol(b)[0])


def sir_can_thiep(S0, I0, N, beta1, beta2, gamma, tc, T, n_diem=600):
    """Can thiệp tại thời điểm tc: beta1 trên [0, tc], beta2 trên [tc, T].
    Tích phân từng giai đoạn, truyền đúng trạng thái tại tc."""
    _yeu_cau(0 <= tc <= T, "Cần 0 <= tc <= T")
    R_bd = _kiem_tra_sir(S0, I0, N, beta1, gamma)
    t1 = np.linspace(0, tc, max(2, int(n_diem * tc / T) if T > 0 else 2))
    y = np.array([S0, I0, R_bd], float)
    ts, ys = [], []
    if tc > 0:
        s1 = solve_ivp(sir_rhs(beta1, gamma, N), [0, tc], y, method="DOP853",
                       rtol=1e-11, atol=1e-12 * N, t_eval=t1)
        ts.append(s1.t); ys.append(s1.y); y = s1.y[:, -1]
    t2 = np.linspace(tc, T, max(2, n_diem - (len(t1) if tc > 0 else 0)))
    s2 = solve_ivp(sir_rhs(beta2, gamma, N), [tc, T], y, method="DOP853",
                   rtol=1e-11, atol=1e-12 * N, t_eval=t2)
    ts.append(s2.t); ys.append(s2.y)
    return np.concatenate(ts), np.concatenate(ys, axis=1)


def sir_beta_tu_mot_buoc_euler(S0, I0, I1, N, gamma, h=1.0):
    """beta sao cho MỘT bước Euler bước h đưa I0 thành I1:
    I1 = I0 + h (beta S0 I0/N - gamma I0)."""
    _yeu_cau(S0 > 0 and I0 > 0 and h > 0, "Cần S0, I0, h dương")
    return ((I1 - I0) / h + gamma * I0) * N / (S0 * I0)


def sir_I_tai(t, S0, I0, N, beta, gamma):
    sol, _ = sir_giai(S0, I0, N, beta, gamma, max(t, 1e-12), rtol=1e-12)
    return float(sol.sol(t)[1])


def sir_hieu_chinh_beta(S0, I0, N, gamma, t_quan_sat, I_quan_sat,
                        khoang=(1e-6, 20.0), xtol=1e-12):
    """beta sao cho NGHIỆM LIÊN TỤC thỏa I(t_quan_sat) = I_quan_sat.
    Tìm nghiệm bằng Brent trên khoảng `khoang` (I(t) tăng ngặt theo beta)."""
    f = lambda b: sir_I_tai(t_quan_sat, S0, I0, N, b, gamma) - I_quan_sat
    lo, hi = khoang
    _yeu_cau(f(lo) < 0 < f(hi), "Khoảng tìm beta không chứa nghiệm")
    return brentq(f, lo, hi, xtol=xtol, rtol=1e-14, maxiter=300)


# ============================================================================
# 4. SEIR (mở rộng): E là nhóm đã nhiễm nhưng CHƯA có khả năng lây
# ============================================================================
def seir_rhs(beta, sigma, gamma, N):
    def f(t, y):
        S, E, I, R = y
        inc = beta * S * I / N
        return np.array([-inc, inc - sigma * E, sigma * E - gamma * I, gamma * I])
    return f


# ============================================================================
# 5. Các mô hình mở rộng dùng trong kho ví dụ
# ============================================================================
def lam_nguoi_newton_chinh_xac(t, T0, T_mt, k):
    """T' = -k (T - T_mt):  T(t) = T_mt + (T0 - T_mt) e^{-k t}."""
    return T_mt + (T0 - T_mt) * np.exp(-k * np.asarray(t, float))


def tron_chat_chinh_xac(t, Q0, F, V, c_vao):
    """Q' = F c_vao - (F/V) Q:  Q(t) = V c_vao + (Q0 - V c_vao) e^{-F t / V}."""
    return V * c_vao + (Q0 - V * c_vao) * np.exp(-F * np.asarray(t, float) / V)


def ho_chua_chinh_xac(t, W0, q, tau):
    """W' = q - W/tau, q hằng:  W(t) = q tau + (W0 - q tau) e^{-t/tau}."""
    return q * tau + (W0 - q * tau) * np.exp(-np.asarray(t, float) / tau)


def dao_dong_rhs(omega):
    """x'' + omega^2 x = 0 viết thành hệ y = (x, v)."""
    return lambda t, y: np.array([y[1], -omega ** 2 * y[0]])


# ============================================================================
# 6. Mở rộng đợt 3: liều thuốc lặp lại, phanh, hai loài tương tác
# ============================================================================
def thuoc_nong_do_du(C0: float, k: float, T: float, n: int) -> float:
    """Nồng độ dư ngay trước liều thứ n+1 (mỗi liều tăng tức thời C0, C' = -kC giữa hai liều).

    R_n = C0 e^{-kT} (1 - e^{-nkT}) / (1 - e^{-kT}).  Minh họa toán học, KHÔNG phải hướng dẫn dùng thuốc.
    """
    _yeu_cau(C0 > 0 and k > 0 and T > 0 and n >= 1, "Cần C0, k, T > 0 và n >= 1.")
    q = np.exp(-k * T)
    return float(C0 * q * (1 - q ** n) / (1 - q))


def thuoc_nong_do_gioi_han(C0: float, k: float, T: float) -> float:
    """R = lim R_n = C0 / (e^{kT} - 1) (trạng thái ổn định)."""
    _yeu_cau(C0 > 0 and k > 0 and T > 0, "Cần C0, k, T > 0.")
    return float(C0 / np.expm1(k * T))


def thuoc_chu_ky(H: float, L: float, k: float) -> dict:
    """Ở trạng thái ổn định, nồng độ dao động giữa L và H: C0 = H - L, T = ln(H/L)/k."""
    _yeu_cau(0 < L < H and k > 0, "Cần 0 < L < H và k > 0.")
    return {"C0": H - L, "T": float(np.log(H / L) / k)}


def phanh(v0: float, k: float) -> dict:
    """v' = -k (giảm tốc đều) CHỈ đến lúc dừng t_s = v0/k; quãng đường d = v0^2/(2k)."""
    _yeu_cau(v0 >= 0 and k > 0, "Cần v0 >= 0 và k > 0.")
    return {"t_dung": v0 / k, "quang_duong": v0 ** 2 / (2 * k)}


def phanh_van_toc(t, v0: float, k: float):
    """Vận tốc theo mô hình phanh: v0 - k t với t <= t_s, bằng 0 sau khi xe dừng (xe đứng yên)."""
    t = np.asarray(t, float)
    return np.where(t <= v0 / k, v0 - k * t, 0.0)


def canh_tranh_rhs(a, b, m, n):
    """Hai loài cạnh tranh (Giordano §12.2): x' = (a - b y) x,  y' = (m - n x) y."""
    return lambda t, u: np.array([(a - b * u[1]) * u[0], (m - n * u[0]) * u[1]])


def lotka_volterra_rhs(a, b, m, n):
    """Thú săn mồi - con mồi (Giordano §12.3): x' = (a - b y) x,  y' = (-m + n x) y."""
    return lambda t, u: np.array([(a - b * u[1]) * u[0], (-m + n * u[0]) * u[1]])


def lotka_volterra_bat_bien(u, a, b, m, n):
    """V(x, y) = n x - m ln x + b y - a ln y, hằng dọc theo nghiệm (x, y > 0)."""
    x, y = u
    return float(n * x - m * np.log(x) + b * y - a * np.log(y))
