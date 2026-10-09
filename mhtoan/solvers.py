"""Các phương pháp số cho y' = f(t, y), y(t0) = y0 (y là số hoặc vectơ).

Quy ước (giống đồ án, Mục 2.4, theo Burden--Faires 9th ed.):
  * lưới t_n = t0 + n h, n = 0..N, với T = t0 + N h CHÍNH XÁC (nếu (T-t0)/h
    không nguyên thì báo lỗi, không âm thầm làm tròn số bước);
  * mọi thành phần của hệ được cập nhật ĐỒNG THỜI từ cùng trạng thái y_n;
  * Heun = hình thang tường minh (B&F gọi là Modified Euler, tr. 286; một số sách gọi "Euler cải tiến");
    "điểm giữa" là phương pháp khác (B&F tr. 286);
  * phương pháp ẩn giải phương trình bước bằng Newton, kiểm tra phần dư và
    báo lỗi khi không hội tụ (không âm thầm nhận kết quả).
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp


class KhongHoiTu(RuntimeError):
    """Vòng lặp Newton của phương pháp ẩn không hội tụ."""


def luoi(t0: float, T: float, h: float) -> np.ndarray:
    if h <= 0:
        raise ValueError("Bước h phải dương")
    if T <= t0:
        raise ValueError("Cần T > t0")
    n = round((T - t0) / h)
    if n < 1 or abs(t0 + n * h - T) > 1e-9 * max(1.0, abs(T)):
        raise ValueError(f"(T - t0)/h = {(T - t0) / h:.6g} không phải số nguyên; "
                         "hãy chọn h chia hết độ dài khoảng")
    return t0 + h * np.arange(n + 1)


def _vecto_thuc(x, ten):
    """Chuyển thành vectơ 1 chiều số THỰC hữu hạn; báo lỗi (không âm thầm bỏ phần ảo hay làm phẳng ma trận)."""
    a = np.asarray(x)
    if a.ndim > 1:
        raise ValueError(f"{ten} phải là vectơ (số hoặc mảng 1 chiều), nhận được mảng hình {a.shape}")
    if np.iscomplexobj(a):
        raise ValueError(f"{ten} có giá trị phức")
    a = np.atleast_1d(a.astype(float))
    if not np.all(np.isfinite(a)):
        raise ValueError(f"{ten} có giá trị không hữu hạn (NaN hoặc Inf)")
    return a


def _chay(buoc, f, t0, y0, h, T):
    t = luoi(t0, T, h)
    y0 = _vecto_thuc(y0, "Điều kiện đầu y0")
    f0 = _vecto_thuc(f(t[0], y0), "f(t0, y0)")
    if f0.shape != y0.shape:
        raise ValueError(f"f(t, y) phải trả về vectơ cùng kích thước với y0 {y0.shape}, nhận được {f0.shape}")
    y = np.empty((len(t), y0.size))
    y[0] = y0
    for n in range(len(t) - 1):
        moi = np.asarray(buoc(f, t[n], y[n], h))
        if moi.shape != y0.shape or np.iscomplexobj(moi) or not np.all(np.isfinite(moi)):
            raise FloatingPointError(f"Nghiệm số không còn là vectơ thực hữu hạn tại bước {n + 1}; "
                                     "hãy giảm h hoặc dùng phương pháp ẩn")
        y[n + 1] = moi
    return t, y


# ---------------------------------------------------------------- một bước
def buoc_euler(f, t, y, h):
    return y + h * np.asarray(f(t, y), float)


def buoc_heun(f, t, y, h):
    k1 = np.asarray(f(t, y), float)
    k2 = np.asarray(f(t + h, y + h * k1), float)
    return y + h / 2 * (k1 + k2)


def buoc_diem_giua(f, t, y, h):
    k1 = np.asarray(f(t, y), float)
    return y + h * np.asarray(f(t + h / 2, y + h / 2 * k1), float)


def buoc_rk4(f, t, y, h):
    k1 = h * np.asarray(f(t, y), float)
    k2 = h * np.asarray(f(t + h / 2, y + k1 / 2), float)
    k3 = h * np.asarray(f(t + h / 2, y + k2 / 2), float)
    k4 = h * np.asarray(f(t + h, y + k3), float)
    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6


def euler(f, t0, y0, h, T):
    return _chay(buoc_euler, f, t0, y0, h, T)


def heun(f, t0, y0, h, T):
    return _chay(buoc_heun, f, t0, y0, h, T)


def diem_giua(f, t0, y0, h, T):
    return _chay(buoc_diem_giua, f, t0, y0, h, T)


def rk4(f, t0, y0, h, T):
    return _chay(buoc_rk4, f, t0, y0, h, T)


def taylor2(f, df, t0, y0, h, T):
    """Taylor bậc hai (B&F (5.17) với n = 2): y_{n+1} = y_n + h f + h^2/2 * df,
    trong đó df(t, y) = f_t + f_y f là đạo hàm toàn phần của f dọc nghiệm
    (người dùng cung cấp, với hệ thì f_y là ma trận Jacobi)."""
    def buoc(f_, t, y, h_):
        return y + h_ * np.asarray(f_(t, y), float) + h_ ** 2 / 2 * np.asarray(df(t, y), float)
    return _chay(buoc, f, t0, y0, h, T)


# ---------------------------------------------------------------- phương pháp ẩn
def _newton(G, J, w0, tol, maxit):
    w = np.array(w0, float)
    for k in range(1, maxit + 1):
        r = np.atleast_1d(G(w))
        Jw = np.atleast_2d(J(w))
        dw = np.linalg.solve(Jw, -r)
        w = w + dw
        if np.max(np.abs(dw)) <= tol * (1 + np.max(np.abs(w))):
            res = np.max(np.abs(np.atleast_1d(G(w))))
            if res <= 1e3 * tol * (1 + np.max(np.abs(w))):
                return w, k, res
    raise KhongHoiTu(f"Newton không hội tụ sau {maxit} vòng; phần dư cuối "
                     f"{np.max(np.abs(np.atleast_1d(G(w)))):.3e}")


def euler_an(f, jac, t0, y0, h, T, tol=1e-12, maxit=50):
    """Euler ẩn: w_{n+1} = w_n + h f(t_{n+1}, w_{n+1}); giải bằng Newton với
    G(w) = w - w_n - h f(t_{n+1}, w), G'(w) = I - h J(t_{n+1}, w)."""
    t = luoi(t0, T, h)
    y = np.empty((len(t), np.size(y0)))
    y[0] = _vecto_thuc(y0, "Điều kiện đầu y0")
    so_vong = []
    for n in range(len(t) - 1):
        tn1 = t[n + 1]
        G = lambda w: w - y[n] - h * np.asarray(f(tn1, w), float)
        J = lambda w: np.eye(y.shape[1]) - h * np.atleast_2d(jac(tn1, w))
        y[n + 1], k, _ = _newton(G, J, y[n], tol, maxit)
        so_vong.append(k)
    return t, y, so_vong


def hinh_thang_an(f, jac, t0, y0, h, T, tol=1e-12, maxit=50):
    """Hình thang ẩn (B&F (5.68), tr. 351), Newton như (5.69), tr. 352."""
    t = luoi(t0, T, h)
    y = np.empty((len(t), np.size(y0)))
    y[0] = _vecto_thuc(y0, "Điều kiện đầu y0")
    so_vong = []
    for n in range(len(t) - 1):
        tn, tn1 = t[n], t[n + 1]
        fn = np.asarray(f(tn, y[n]), float)
        G = lambda w: w - y[n] - h / 2 * (fn + np.asarray(f(tn1, w), float))
        J = lambda w: np.eye(y.shape[1]) - h / 2 * np.atleast_2d(jac(tn1, w))
        y[n + 1], k, _ = _newton(G, J, y[n], tol, maxit)
        so_vong.append(k)
    return t, y, so_vong


# ---------------------------------------------------------------- đa bước
def adams_bashforth2(f, t0, y0, h, T):
    """AB2 (B&F (5.33), tr. 307): w_{i+1} = w_i + h/2 (3 f_i - f_{i-1}).
    Giá trị khởi động w_1 tính bằng Heun (bậc 2) để không làm giảm bậc."""
    t = luoi(t0, T, h)
    y = np.empty((len(t), np.size(y0)))
    y[0] = _vecto_thuc(y0, "Điều kiện đầu y0")
    y[1] = buoc_heun(f, t[0], y[0], h)
    f_cu = np.asarray(f(t[0], y[0]), float)
    for i in range(1, len(t) - 1):
        f_moi = np.asarray(f(t[i], y[i]), float)
        y[i + 1] = y[i] + h / 2 * (3 * f_moi - f_cu)
        f_cu = f_moi
    return t, y


# ---------------------------------------------------------------- tham chiếu
def nghiem_tham_chieu(f, t_span, y0, t_eval=None, rtol=1e-12, atol=1e-12):
    """Nghiệm có độ chính xác cao (DOP853, bước thích nghi) dùng làm chuẩn so sánh.
    Dung sai bộ giải KHÔNG tự bảo đảm số chữ số đúng cho mọi đầu ra; đồ án
    luôn đối chiếu thêm với nghiệm/quan hệ giải tích khi có."""
    sol = solve_ivp(f, t_span, np.atleast_1d(np.asarray(y0, float)), method="DOP853",
                    rtol=rtol, atol=atol, t_eval=t_eval, dense_output=True)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol


# ---------------------------------------------------------------- ổn định
HE_SO_KHUECH_DAI = {
    "Euler": lambda z: 1 + z,
    "Heun": lambda z: 1 + z + z ** 2 / 2,
    "Điểm giữa": lambda z: 1 + z + z ** 2 / 2,
    "RK4": lambda z: 1 + z + z ** 2 / 2 + z ** 3 / 6 + z ** 4 / 24,
    "Euler ẩn": lambda z: 1 / (1 - z),
    "Hình thang ẩn": lambda z: (1 + z / 2) / (1 - z / 2),
}
"""Q(z), z = h*lambda: khi áp dụng cho y' = lambda y thì w_{n+1} = Q(z) w_n
(B&F (5.66), tr. 350)."""


def bac_hoi_tu_thuc_nghiem(sai_so):
    """p ~ log2(E(h)/E(h/2)) cho dãy sai số ứng với h, h/2, h/4, ..."""
    e = np.asarray(sai_so, float)
    return np.log2(e[:-1] / e[1:])
