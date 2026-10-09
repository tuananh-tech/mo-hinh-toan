"""Dữ liệu dùng trong đồ án. Mỗi bộ dữ liệu ghi rõ nguồn và loại.

LOẠI DỮ LIỆU
    "quan_sat"  : số liệu đo/điều tra đã được công bố (có nguồn).
    "giao_khoa" : tình huống giáo khoa với tham số được chọn trong tài liệu.
    "minh_hoa"  : dữ liệu do đồ án tạo ra để minh họa phương pháp.
"""
import numpy as np

# ---------------------------------------------------------------------------
# Sinh khối nấm men (Pearl 1927), trích theo Giordano, Fox, Horton (2014),
# A First Course in Mathematical Modeling, 5th ed., Bảng 11.1, tr. 466.
# ---------------------------------------------------------------------------
NAM_MEN = {
    "loai": "quan_sat",
    "nguon": "Pearl (1927), Quart. Rev. Biol. 2:532-548; trích theo "
             "Giordano-Fox-Horton (2014), Bảng 11.1, tr. 466",
    "don_vi_t": "giờ",
    "don_vi_P": "đơn vị sinh khối (theo nguồn)",
    "t": np.arange(19.0),
    "P": np.array([9.6, 18.3, 29.0, 47.2, 71.1, 119.1, 174.6, 257.3, 350.7,
                   441.0, 513.3, 559.7, 594.8, 629.4, 640.8, 651.1, 655.9,
                   659.6, 661.8]),
}

# ---------------------------------------------------------------------------
# Dân số Hoa Kỳ theo điều tra dân số, trích theo Giordano et al. (2014), tr. 463.
# ---------------------------------------------------------------------------
DAN_SO_HOA_KY = {
    "loai": "quan_sat",
    "nguon": "Điều tra dân số Hoa Kỳ, trích theo Giordano-Fox-Horton (2014), tr. 463",
    "nam": np.array([1970.0, 1990.0, 2000.0]),
    "P": np.array([203_211_926.0, 248_710_000.0, 281_400_000.0]),
}

# ---------------------------------------------------------------------------
# Tình huống dịch cúm giáo khoa (Giordano et al. 2014, tr. 51-52 và 564-565).
# Tài liệu dùng dạng tác dụng khối lượng a*S*I; đồ án dùng dạng chuẩn
# beta*S*I/N với beta = a*N.
# ---------------------------------------------------------------------------
CUM_GIAO_KHOA = {
    "loai": "giao_khoa",
    "nguon": "Giordano-Fox-Horton (2014), tr. 51-52 (mô hình rời rạc) và tr. 564-565",
    "N": 1000.0,
    "S0": 995.0,
    "I0": 5.0,
    "R0_ban_dau": 0.0,          # R(0); KHÔNG phải số sinh sản cơ bản
    "a": 0.001407,              # (người.tuần)^-1, dạng a S I
    "gamma": 0.6,               # tuần^-1 (thời gian mắc bệnh trung bình 5/3 tuần)
    "I_sau_1_tuan": 9.0,        # số người đang nhiễm (prevalence) sau 1 tuần
    "don_vi_t": "tuần",
}
CUM_GIAO_KHOA["beta"] = CUM_GIAO_KHOA["a"] * CUM_GIAO_KHOA["N"]   # 1.407 tuần^-1
