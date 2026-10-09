"""QA: trích khung hình ở 35%, 70% và cuối mỗi video, ghép thành một tờ ảnh để kiểm tra bằng mắt;
in thời lượng, độ phân giải của từng video.
Chạy:  python kiem_tra_khung.py <thư mục video> <tệp ảnh ra>"""
import glob
import os
import sys

import av
from PIL import Image, ImageDraw

thu_muc, ra = sys.argv[1], sys.argv[2]
hang = []
for f in sorted(glob.glob(os.path.join(thu_muc, "C*.mp4"))):
    with av.open(f) as c:
        s = c.streams.video[0]
        khung = [fr.to_image() for fr in c.decode(s)]
    tl = len(khung) / float(s.average_rate)
    print(f"{os.path.basename(f)}: {tl:.1f} s, {s.width}x{s.height}, {float(s.average_rate):.0f} khung/s")
    chon = [khung[int(len(khung) * p)] for p in (0.35, 0.7)] + [khung[-1]]
    hang.append((os.path.basename(f), [k.resize((427, 240)) for k in chon]))
anh = Image.new("RGB", (3 * 427, len(hang) * 254), "white")
v = ImageDraw.Draw(anh)
for i, (ten, ks) in enumerate(hang):
    v.text((4, i * 254), ten, fill="red")
    for j, k in enumerate(ks):
        anh.paste(k, (j * 427, i * 254 + 14))
anh.save(ra)
