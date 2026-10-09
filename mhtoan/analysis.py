"""Khớp mô hình với dữ liệu và đánh giá: hồi quy tuyến tính, tuyến tính hóa,
bình phương tối thiểu phi tuyến, thí nghiệm chia dữ liệu theo thời gian."""
from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares

from . import models


class DuLieuKhongHopLe(ValueError):
    pass


def kiem_tra_du_lieu(t, P, can_duong=True):
    t = np.asarray(t, float); P = np.asarray(P, float)
    if t.shape != P.shape or t.ndim != 1:
        raise DuLieuKhongHopLe("t và P phải là hai dãy cùng độ dài")
    if len(t) < 3:
        raise DuLieuKhongHopLe("Cần ít nhất 3 quan sát")
    if np.any(~np.isfinite(t)) or np.any(~np.isfinite(P)):
        raise DuLieuKhongHopLe("Dữ liệu có giá trị thiếu hoặc không hữu hạn")
    if np.any(np.diff(t) <= 0):
        raise DuLieuKhongHopLe("Thời gian phải tăng ngặt")
    if can_duong and np.any(P <= 0):
        raise DuLieuKhongHopLe("Quy mô quần thể phải dương (để lấy logarithm)")
    return t, P


def hoi_quy_tuyen_tinh(x, y) -> dict:
    """Đường thẳng bình phương tối thiểu y = a x + c (Mục 3.3, chứng minh ở Phụ lục B.2)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    xb, yb = x.mean(), y.mean()
    Sxx = np.sum((x - xb) ** 2)
    if Sxx == 0:
        raise DuLieuKhongHopLe("Các giá trị x không được đồng thời bằng nhau")
    a = np.sum((x - xb) * (y - yb)) / Sxx
    c = yb - a * xb
    yhat = a * x + c
    ss_res = np.sum((y - yhat) ** 2); ss_tot = np.sum((y - yb) ** 2)
    return {"a": a, "c": c, "R2": 1 - ss_res / ss_tot if ss_tot > 0 else np.nan,
            "phan_du": y - yhat}


def rmse(du_bao, quan_sat):
    d = np.asarray(du_bao, float) - np.asarray(quan_sat, float)
    return float(np.sqrt(np.mean(d ** 2)))


def sai_so_tuong_doi_phan_tram(du_bao, quan_sat):
    q = np.asarray(quan_sat, float)
    return (np.asarray(du_bao, float) - q) / q * 100


# --------------------------------------------------------------- Malthus
def khop_malthus_log(t, P) -> dict:
    """ln P = ln P0 + r t  (hồi quy trên thang logarithm)."""
    t, P = kiem_tra_du_lieu(t, P)
    h = hoi_quy_tuyen_tinh(t, np.log(P))
    return {"r": h["a"], "P0": float(np.exp(h["c"])), "R2_log": h["R2"]}


def khop_malthus_nls(t, P, p0=None) -> dict:
    """Bình phương tối thiểu trên thang gốc cho P = P0 exp(r t)."""
    t, P = kiem_tra_du_lieu(t, P)
    if p0 is None:
        m = khop_malthus_log(t, P); p0 = [m["P0"], m["r"]]
    res = least_squares(lambda p: p[0] * np.exp(p[1] * t) - P, p0,
                        bounds=([1e-12, -10], [np.inf, 10]), xtol=1e-14, ftol=1e-14)
    return {"P0": res.x[0], "r": res.x[1], "thanh_cong": res.success}


# --------------------------------------------------------------- Logistic
def khop_logistic_tuyen_tinh(t, P, K) -> dict:
    """Y = ln(P/(K-P)) = r t + c, c = -r t*. Cần K > max P."""
    t, P = kiem_tra_du_lieu(t, P)
    if K <= P.max():
        raise DuLieuKhongHopLe("K phải lớn hơn mọi quan sát để ln(P/(K-P)) xác định")
    h = hoi_quy_tuyen_tinh(t, np.log(P / (K - P)))
    return {"r": h["a"], "c": h["c"], "t_sao": -h["c"] / h["a"], "K": K, "R2_Y": h["R2"]}


def logistic_theo_t_sao(t, r, K, ts):
    return K / (1 + np.exp(-r * (np.asarray(t, float) - ts)))


def khop_logistic_nls(t, P, p0=None, K_max=None) -> dict:
    """Bình phương tối thiểu phi tuyến cho (r, K, t*); hàm mục tiêu
    sum (P_i - K/(1+exp(-r(t_i - t*))))^2; ràng buộc r > 0, K >= max P.
    Khởi tạo mặc định: r = 0.5, K = 1.2 max P, t* = trung vị t."""
    t, P = kiem_tra_du_lieu(t, P)
    if p0 is None:
        p0 = [0.5, 1.2 * P.max(), float(np.median(t))]
    hi_K = np.inf if K_max is None else K_max
    res = least_squares(lambda p: logistic_theo_t_sao(t, *p) - P, p0,
                        bounds=([1e-9, P.max(), -np.inf], [np.inf, hi_K, np.inf]),
                        xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=20000)
    r, K, ts = res.x
    # độ nhạy thô: ma trận Jacobi tại nghiệm -> sai số chuẩn xấp xỉ
    J = res.jac
    dof = max(1, len(t) - 3)
    s2 = 2 * res.cost / dof
    try:
        cov = np.linalg.inv(J.T @ J) * s2
        se = np.sqrt(np.diag(cov))
    except np.linalg.LinAlgError:
        se = np.full(3, np.nan)
    return {"r": r, "K": K, "t_sao": ts, "thanh_cong": bool(res.success),
            "cham_bien_K": bool(K_max is not None and abs(K - K_max) < 1e-6 * K_max),
            "sai_so_chuan": se, "khoi_tao": list(p0)}


def thi_nghiem_chia_thoi_gian(t, P, t_cat: float, p0_logistic=None) -> dict:
    """Huấn luyện trên t <= t_cat, kiểm tra trên t > t_cat.
    Mọi tham số (kể cả K) CHỈ ước lượng từ phần huấn luyện."""
    t, P = kiem_tra_du_lieu(t, P)
    tr = t <= t_cat; te = ~tr
    if tr.sum() < 3 or te.sum() < 1:
        raise DuLieuKhongHopLe("Cần >= 3 điểm huấn luyện và >= 1 điểm kiểm tra")
    m = khop_malthus_nls(t[tr], P[tr])
    pm = m["P0"] * np.exp(m["r"] * t)
    lg = khop_logistic_nls(t[tr], P[tr], p0=p0_logistic)
    pl = logistic_theo_t_sao(t, lg["r"], lg["K"], lg["t_sao"])
    return {"t_cat": t_cat, "malthus": m, "logistic": lg,
            "rmse_huan_luyen": {"malthus": rmse(pm[tr], P[tr]), "logistic": rmse(pl[tr], P[tr])},
            "rmse_kiem_tra": {"malthus": rmse(pm[te], P[te]), "logistic": rmse(pl[te], P[te])},
            "du_bao": {"malthus": pm, "logistic": pl}, "mask_huan_luyen": tr}


def bang_hoi_tu(phuong_phap, f, y_chinh_xac, t0, y0, T, cac_h):
    """Sai số |y(T) - y_N| với các bước h; trả về sai số và bậc thực nghiệm."""
    from .solvers import bac_hoi_tu_thuc_nghiem
    ss = []
    for h in cac_h:
        t, y = phuong_phap(f, t0, y0, h, T)
        ss.append(float(np.max(np.abs(y[-1] - np.atleast_1d(y_chinh_xac(T))))))
    return np.array(ss), bac_hoi_tu_thuc_nghiem(ss)
