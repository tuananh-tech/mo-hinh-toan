"""Kết xuất chín cảnh, chép MP4 vào video/<Cảnh>.mp4 và sinh phụ đề + siêu dữ liệu cho website.
Chạy (trong thư mục này):  python ket_xuat.py            # chất lượng cao 1080p60
                           python ket_xuat.py --nhap     # bản nháp 480p15 (không chép vào video/)
                           python ket_xuat.py --chi-phu-de   # chỉ gom video/thong_tin/*.json thành phụ đề

Mỗi cảnh, khi kết xuất, ghi mốc thời gian thuyết minh và câu hỏi dừng vào video/thong_tin/<Cảnh>.json
(lớp CanhHocLieu trong canh.py). Script này gom chúng thành:
  - video/<Cảnh>.vi.srt         phụ đề tiếng Việt (video KHÔNG có âm thanh; phụ đề thay cho lời đọc);
  - video/thong_tin_video.json  tiêu đề, mục tiêu, thời lượng, câu hỏi dừng, bản chép lời, bài tập liên quan.
"""
import json
import os
import shutil
import subprocess
import sys

CANH = ["C1_TocDoTrungBinhDenDaoHam", "C2_CanBangSinhTu", "C3_MalthusNgoaiMienHieuLuc", "C4_LogisticDuongPha",
        "C5_SIRSoDoNgan", "C6_NguongDinhDich", "C7_MotBuocEulerHeunRK4", "C8_SaiSoVaOnDinh", "C9_MatPhangPha"]
DAY = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.join(DAY, "video")


def _moc(giay: float) -> str:
    ms = int(round(giay * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def gom_phu_de():
    tong = {}
    for c in CANH:
        p = os.path.join(VIDEO, "thong_tin", c + ".json")
        if not os.path.exists(p):
            print(f"[THIEU] {c}: chưa có thong_tin (cần kết xuất cảnh)")
            continue
        with open(p, encoding="utf-8") as fi:
            tt = json.load(fi)
        tong[c] = tt
        dong = []
        for i, d in enumerate(tt["loi_thuyet_minh"], 1):
            dong.append(f"{i}\n{_moc(d['t0'])} --> {_moc(d['t1'])}\n{d['text']}\n")
        with open(os.path.join(VIDEO, c + ".vi.srt"), "w", encoding="utf-8") as fo:
            fo.write("\n".join(dong))
    with open(os.path.join(VIDEO, "thong_tin_video.json"), "w", encoding="utf-8") as fo:
        json.dump(tong, fo, ensure_ascii=False, indent=1)
    print(f"Đã gom {len(tong)}/{len(CANH)} cảnh vào thong_tin_video.json và *.vi.srt")
    return len(tong) == len(CANH)


if __name__ == "__main__":
    if "--chi-phu-de" in sys.argv:
        sys.exit(0 if gom_phu_de() else 1)
    nhap = "--nhap" in sys.argv
    chon = [a for a in sys.argv[1:] if not a.startswith("--")] or CANH
    co, thu_muc = ("-ql", "480p15") if nhap else ("-qh", "1080p60")
    os.makedirs(VIDEO, exist_ok=True)
    loi = 0
    for c in chon:
        kq = subprocess.run([sys.executable, "-m", "manim", co, "--disable_caching", "canh.py", c], cwd=DAY,
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
        nguon = os.path.join(DAY, "media", "videos", "canh", thu_muc, c + ".mp4")
        if kq.returncode != 0 or not os.path.exists(nguon):
            loi += 1
            print(f"[LOI] {c}\n{kq.stderr[-2000:]}")
            continue
        if not nhap:
            shutil.copyfile(nguon, os.path.join(VIDEO, c + ".mp4"))
        print(f"[OK] {c}: {os.path.getsize(nguon) / 1e6:.2f} MB")
    gom_phu_de()
    sys.exit(1 if loi else 0)
