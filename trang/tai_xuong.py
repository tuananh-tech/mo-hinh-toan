"""Tải xuống: phiếu học tập, dữ liệu, hình, mã MATLAB, module Python, video."""
import json
import os

import pandas as pd
import streamlit as st

from tien_ich import THU_MUC_HOC_LIEU, data, doc_tep, tai_csv, zip_thu_muc

st.title("Tải xuống")
st.subheader("Phiếu học tập")
pdf = doc_tep("phieu_hoc_tap", "phieu_hoc_tap.pdf", che_do="rb")
if pdf:
    st.download_button("Phiếu học tập, đáp án, hướng dẫn giảng viên, rubric (PDF)", pdf, file_name="phieu_hoc_tap.pdf",
                       mime="application/pdf", key="tx_pdf")
else:
    st.warning("Chưa có phieu_hoc_tap.pdf.")

st.subheader("Dữ liệu (có nguồn)")
ym = data.NAM_MEN
tai_csv(pd.DataFrame({"t_gio": ym["t"], "P": ym["P"]}), "nam_men_pearl1927.csv",
        "Sinh khối nấm men (quan sát; Pearl 1927 qua Giordano et al. 2014, Bảng 11.1)", key="tx_nm")
hk = data.DAN_SO_HOA_KY
tai_csv(pd.DataFrame({"nam": hk["nam"], "dan_so": hk["P"]}), "dan_so_hoa_ky.csv",
        "Dân số Hoa Kỳ 1970, 1990, 2000 (quan sát; qua Giordano et al. 2014, tr. 463)", key="tx_hk")
st.download_button("Tham số tình huống cúm giáo khoa (JSON)", json.dumps(
    {k: v for k, v in data.CUM_GIAO_KHOA.items()}, ensure_ascii=False, indent=1), file_name="tinh_huong_cum.json",
    mime="application/json", key="tx_cum")
kq = doc_tep("ket_qua", "kho_vi_du.json")
if kq:
    st.download_button("Số liệu tính lại của kho ví dụ (JSON)", kq, file_name="kho_vi_du.json", mime="application/json",
                       key="tx_vd")

st.subheader("Mã nguồn")
st.download_button("Toàn bộ mã MATLAB (ZIP)", zip_thu_muc("matlab"), file_name="ma_matlab.zip", mime="application/zip",
                   key="tx_m")
st.download_button("Module Python mhtoan (ZIP)", zip_thu_muc("mhtoan", duoi=(".py",)), file_name="mhtoan.zip",
                   mime="application/zip", key="tx_py")

st.subheader("Hình của đồ án")
thu_muc_hinh = os.path.join(os.path.dirname(THU_MUC_HOC_LIEU), "picture")
if os.path.isdir(thu_muc_hinh):
    for ten in sorted(os.listdir(thu_muc_hinh)):
        if ten.startswith("hinh_") and ten.endswith(".pdf"):
            with open(os.path.join(thu_muc_hinh, ten), "rb") as fh:
                st.download_button(f"{ten}", fh.read(), file_name=ten, mime="application/pdf", key=f"tx_{ten}")

st.subheader("Video")
thu_muc_video = os.path.join(THU_MUC_HOC_LIEU, "manim", "video")
if os.path.isdir(thu_muc_video):
    for ten in sorted(os.listdir(thu_muc_video)):
        if ten.endswith((".mp4", ".srt")):
            with open(os.path.join(thu_muc_video, ten), "rb") as fh:
                st.download_button(ten, fh.read(), file_name=ten, key=f"tx_{ten}")
