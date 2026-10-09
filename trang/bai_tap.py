"""Ngân hàng bài tập: lọc theo bài, mức, dạng kỹ năng."""
import streamlit as st

from ngan_hang_bai_tap import BAI_TAP, DANG
from tien_ich import hien_bai_tap

st.title("Ngân hàng bài tập")
st.markdown("Mỗi bài có **ba mức gợi ý** mở dần, đáp án và giải thích. Bài tính toán được chấm tự động bằng so sánh số "
            "với dung sai (đáp án tính bằng module chung). Câu hỏi mở hiện đáp án mẫu để tự đối chiếu.")
c1, c2, c3 = st.columns(3)
TEN_BAI = {"Tất cả": None, "Bài 1": "bai1", "Bài 2": "bai2", "Bài 3": "bai3", "Bài 4": "bai4", "Phương pháp số": "so"}
bai = TEN_BAI[c1.selectbox("Bài", list(TEN_BAI), key="nh_bai")]
muc = c2.selectbox("Mức", ["Tất cả", "Cơ bản", "Vận dụng", "Mở rộng"], key="nh_muc")
dang = c3.selectbox("Dạng kỹ năng", ["Tất cả"] + DANG, key="nh_dang")
loc = [b for b in BAI_TAP if (bai is None or b["bai"] == bai) and (muc == "Tất cả" or b["muc"] == muc)
       and (dang == "Tất cả" or b["dang"] == dang)]
st.caption(f"{len(loc)} bài tập.")
for bt in loc:
    hien_bai_tap(bt, key=f"nh_{bt['ma']}")
