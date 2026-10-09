"""Sinh kich_ban.md từ video/thong_tin_video.json (mốc thời gian ghi lại khi kết xuất), để kịch bản luôn khớp video.
Chạy sau ket_xuat.py:  python sinh_kich_ban.py
"""
import json
import os

DAY = os.path.dirname(os.path.abspath(__file__))
KHO_KHAN = {
    "C1": "đạo hàm chỉ là công thức, không là tốc độ",
    "C2": "không tự lập được phương trình từ 'vào − ra'",
    "C3": "tin dự báo vì mô hình khớp tốt dữ liệu huấn luyện",
    "C4": "không đọc được tính ổn định từ dấu của f",
    "C5": "nhầm tốc độ chuyển ngăn với nguy cơ trên mỗi người",
    "C6": "cho rằng R0 > 1 thì dịch luôn bùng phát",
    "C7": "không thấy hình học và chi phí của một bước giải số",
    "C8": "đồng nhất 'bậc cao' với 'luôn tốt hơn'",
    "C9": "không liên hệ quỹ đạo pha với đồ thị x(t), y(t); vai trò của vectơ riêng",
}


def main():
    tt = json.load(open(os.path.join(DAY, "video", "thong_tin_video.json"), encoding="utf-8"))
    d = ["# Kịch bản chín hoạt cảnh Manim", "",
         "TỆP SINH TỰ ĐỘNG bởi `sinh_kich_ban.py` từ `video/thong_tin_video.json`. Mốc thời gian được ghi **trong khi "
         "kết xuất** (`canh.py`, lớp `CanhHocLieu`), nên khớp với video. Mọi số liệu trên màn hình được tính bằng "
         "`hoc_lieu/mhtoan`, cùng nguồn với đồ án.",
         "",
         "**Video không có âm thanh.** Lời thuyết minh chỉ có ở dạng phụ đề (`video/<Cảnh>.vi.srt`) và bản chép lời "
         "dưới đây; giảng viên có thể đọc hoặc thu âm riêng. Mỗi cảnh có một câu hỏi dừng (khung màu cam). Đây là "
         "thiết kế đề xuất, chưa được dùng trong lớp học thật.", "",
         "| Cảnh | Khó khăn học tập được nhắm tới | Thời lượng (s) | Câu hỏi dừng (s) | Bài tập / ví dụ liên quan |",
         "|---|---|---|---|---|"]
    for ma, v in tt.items():
        d.append(f"| {ma} | {KHO_KHAN.get(ma[:2], '')} | {v['thoi_luong']:.0f} | "
                 f"{', '.join(f'{c['t']:.1f}' for c in v['cau_hoi_dung'])} | {', '.join(v['bai_tap'])} |")
    for ma, v in tt.items():
        d += ["", f"## {ma[:2]}. {v['tieu_de']} ({v['thoi_luong']:.0f} giây)", "",
              f"- **Mục tiêu.** {v['muc_tieu']}"]
        for c in v["cau_hoi_dung"]:
            d.append(f"- **Câu hỏi dừng** (giây {c['t']:.1f}): {c['cau_hoi']} — *gợi ý:* {c['goi_y']}")
        d.append(f"- **Bài tập liên quan.** {', '.join(v['bai_tap'])}")
        d.append("- **Lời thuyết minh (phụ đề):**")
        for p in v["loi_thuyet_minh"]:
            d.append(f"  - [{p['t0']:.1f}–{p['t1']:.1f} s] {p['text']}")
    open(os.path.join(DAY, "kich_ban.md"), "w", encoding="utf-8", newline="\n").write("\n".join(d) + "\n")
    print(f"Đã ghi kich_ban.md ({len(tt)} cảnh)")


if __name__ == "__main__":
    main()
