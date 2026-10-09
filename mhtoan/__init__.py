"""mhtoan -- module tính toán dùng chung cho đồ án
"Xây dựng bài giảng về mô hình toán học cho một số hiện tượng tự nhiên".

Mọi số liệu trong đồ án (bảng, hình), ứng dụng Streamlit và hoạt cảnh
Manim đều được tính từ module này, để bảo đảm cùng tham số, cùng quy ước.

Quy ước ký hiệu (thống nhất với đồ án):
    Malthus  : P' = r P
    Logistic : P' = r P (1 - P/K)
    Khai thác: P' = r P (1 - P/K) - H
    SIR      : S' = -beta S I / N,  I' = beta S I / N - gamma I,  R' = gamma I
    SEIR     : thêm E (đã nhiễm, chưa có khả năng lây), E' = beta S I/N - sigma E
"""
from . import data, models, solvers, analysis  # noqa: F401

__version__ = "1.0.0"
