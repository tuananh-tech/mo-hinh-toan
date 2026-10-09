"""Hệ tuyến tính hệ số hằng y' = A y (đợt 3): nghiệm thực ứng với trị riêng phức,
chuỗi Jordan, ma trận mũ và kiểm tra bằng thế vào hệ (residual).

Quy ước: mọi vectơ là mảng 1 chiều; hệ đại số giải bằng np.linalg.solve (tương đương A\b),
ma trận mũ dùng scipy.linalg.expm; không dùng ma trận nghịch đảo để giải hệ.
"""
from __future__ import annotations

import numpy as np
from scipy.linalg import expm


def _ma_tran_vuong_thuc(A):
    """Ma trận vuông số THỰC hữu hạn (báo lỗi thay vì âm thầm bỏ phần ảo)."""
    A = np.asarray(A)
    if A.ndim != 2 or A.shape[0] != A.shape[1] or np.iscomplexobj(A) or not np.all(np.isfinite(A)):
        raise ValueError("A phải là ma trận vuông số thực hữu hạn.")
    return A.astype(float)


def residual(A, u, t, dt=1e-6):
    """max |u'(t) - A u(t)|, u' tính bằng sai phân trung tâm (dùng để kiểm tra nghiệm)."""
    du = (np.asarray(u(t + dt)) - np.asarray(u(t - dt))) / (2 * dt)
    return float(np.max(np.abs(du - np.asarray(A) @ np.asarray(u(t)))))


def nghiem_thuc_tu_tri_rieng_phuc(A):
    """Với A thực có trị riêng alpha ± i beta (beta > 0), vectơ riêng v = p + i q:
    trả về hai hàm u1 = e^{alpha t}(p cos bt - q sin bt), u2 = e^{alpha t}(p sin bt + q cos bt)."""
    A = _ma_tran_vuong_thuc(A)
    lam, V = np.linalg.eig(A)
    k = int(np.argmax(lam.imag))
    if lam[k].imag <= 0:
        raise ValueError("A không có trị riêng phức với phần ảo dương.")
    al, be = lam[k].real, lam[k].imag
    p, q = V[:, k].real, V[:, k].imag
    # điều kiện để u1, u2 là nghiệm: A p = al p - be q, A q = be p + al q (kiểm tra với dung sai tương đối)
    thang = max(1.0, np.linalg.norm(A, 1)) * max(np.max(np.abs(p)), np.max(np.abs(q)))
    pd = max(np.max(np.abs(A @ p - (al * p - be * q))), np.max(np.abs(A @ q - (be * p + al * q))))
    if pd > 1e-10 * thang:
        raise ValueError(f"Phần dư của cặp (p, q) quá lớn: {pd:.2e}")
    u1 = lambda t: np.exp(al * t) * (p * np.cos(be * t) - q * np.sin(be * t))  # noqa: E731
    u2 = lambda t: np.exp(al * t) * (p * np.sin(be * t) + q * np.cos(be * t))  # noqa: E731
    return {"alpha": float(al), "beta": float(be), "p": p, "q": q, "u1": u1, "u2": u2}


def chuoi_jordan_2(A, lam, v1):
    """Với (A - lam I) v1 = 0, tìm v2 thỏa (A - lam I) v2 = v1 (bình phương tối thiểu vì ma trận suy biến;
    kiểm tra phần dư bằng 0) và trả về nghiệm e^{lam t} v1, e^{lam t}(t v1 + v2)."""
    A = _ma_tran_vuong_thuc(A)
    v1 = np.asarray(v1)
    if v1.ndim != 1 or v1.size != A.shape[0] or np.iscomplexobj(v1) or not np.all(np.isfinite(v1)):
        raise ValueError(f"v1 phải là vectơ thực hữu hạn có {A.shape[0]} phần tử.")
    v1 = v1.astype(float)
    if np.max(np.abs(v1)) == 0:
        raise ValueError("v1 = 0 không phải vectơ riêng (vectơ riêng luôn khác 0).")
    B = A - lam * np.eye(len(v1))
    thang = max(1.0, np.linalg.norm(B, 1)) * np.max(np.abs(v1))   # dung sai TƯƠNG ĐỐI
    if np.max(np.abs(B @ v1)) > 1e-10 * thang:
        raise ValueError("v1 không phải vectơ riêng ứng với lam.")
    v2 = np.linalg.lstsq(B, v1, rcond=None)[0]
    if np.max(np.abs(B @ v2 - v1)) > 1e-10 * thang:
        raise ValueError("Không giải được (A - lam I) v2 = v1: lam có thể có đủ vectơ riêng.")
    return {"v2": v2, "u1": lambda t: np.exp(lam * t) * v1,
            "u2": lambda t: np.exp(lam * t) * (t * v1 + v2)}


def nghiem_ma_tran_mu(A, y0, t):
    """y(t) = expm(t A) y0."""
    return expm(t * np.asarray(A, float)) @ np.asarray(y0, float)


def he_so_bat_dinh_tuyen_tinh(A, g):
    """x' = A x + t g: nghiệm riêng x_p = t a + b với A a = -g, A b = a (giải bằng solve, không dùng nghịch đảo)."""
    A = np.asarray(A, float)
    a = np.linalg.solve(A, -np.asarray(g, float))
    b = np.linalg.solve(A, a)
    return a, b


def phan_loai_diem_can_bang_2x2(A, tol=1e-12) -> str:
    """Phân loại điểm cân bằng 0 của y' = A y (A thực 2x2, det A != 0) theo Bảng 2.x của đồ án."""
    A = np.asarray(A, float)
    tr, de = np.trace(A), np.linalg.det(A)
    if abs(de) < tol:
        raise ValueError("det A = 0: điểm cân bằng không cô lập, bảng không áp dụng.")
    if de < 0:
        return "yên ngựa"
    disc = tr ** 2 - 4 * de
    if abs(tr) < tol:
        return "tâm"
    huong = "hút" if tr < 0 else "đẩy"
    if disc < -tol:
        return f"tiêu điểm {huong}"
    if abs(disc) <= tol:
        hai_vecto = np.allclose(A, (tr / 2) * np.eye(2), atol=1e-12)
        return f"nút sao {huong}" if hai_vecto else f"nút suy biến {huong}"
    return f"nút {huong}"
