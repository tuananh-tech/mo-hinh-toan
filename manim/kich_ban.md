# Kịch bản chín hoạt cảnh Manim

TỆP SINH TỰ ĐỘNG bởi `sinh_kich_ban.py` từ `video/thong_tin_video.json`. Mốc thời gian được ghi **trong khi kết xuất** (`canh.py`, lớp `CanhHocLieu`), nên khớp với video. Mọi số liệu trên màn hình được tính bằng `hoc_lieu/mhtoan`, cùng nguồn với đồ án.

**Video không có âm thanh.** Lời thuyết minh chỉ có ở dạng phụ đề (`video/<Cảnh>.vi.srt`) và bản chép lời dưới đây; giảng viên có thể đọc hoặc thu âm riêng. Mỗi cảnh có một câu hỏi dừng (khung màu cam). Đây là thiết kế đề xuất, chưa được dùng trong lớp học thật.

| Cảnh | Khó khăn học tập được nhắm tới | Thời lượng (s) | Câu hỏi dừng (s) | Bài tập / ví dụ liên quan |
|---|---|---|---|---|
| C1_TocDoTrungBinhDenDaoHam | đạo hàm chỉ là công thức, không là tốc độ | 29 | 6.9 | B1.3, VD02 |
| C2_CanBangSinhTu | không tự lập được phương trình từ 'vào − ra' | 31 | 7.1 | B1.1, B1.2, VD07 |
| C3_MalthusNgoaiMienHieuLuc | tin dự báo vì mô hình khớp tốt dữ liệu huấn luyện | 27 | 5.9 | B1.4, B1.5, VD10 |
| C4_LogisticDuongPha | không đọc được tính ổn định từ dấu của f | 26 | 3.2 | B2.1, B2.2, VD15 |
| C5_SIRSoDoNgan | nhầm tốc độ chuyển ngăn với nguy cơ trên mỗi người | 25 | 6.8 | B3.1, B3.4, VD23 |
| C6_NguongDinhDich | cho rằng R0 > 1 thì dịch luôn bùng phát | 29 | 4.5 | B3.2, B3.3, VD24 |
| C7_MotBuocEulerHeunRK4 | không thấy hình học và chi phí của một bước giải số | 23 | 5.7 | S.1, VD33, VD34, VD35 |
| C8_SaiSoVaOnDinh | đồng nhất 'bậc cao' với 'luôn tốt hơn' | 35 | 2.2 | S.2, S.3, S.4, VD36, VD37 |
| C9_MatPhangPha | không liên hệ quỹ đạo pha với đồ thị x(t), y(t); vai trò của vectơ riêng | 36 | 21.0 | B4.1, B4.2, VD46 |

## C1. Từ tốc độ trung bình đến đạo hàm (29 giây)

- **Mục tiêu.** Hiểu đạo hàm là giới hạn của tốc độ thay đổi trung bình (hệ số góc cát tuyến → tiếp tuyến).
- **Câu hỏi dừng** (giây 6.9): khi Δt nhỏ dần, hệ số góc cát tuyến tiến tới đâu? — *gợi ý:* Tiến tới hệ số góc tiếp tuyến tại t = 6, tức đạo hàm P'(6) ≈ 74,4 đơn vị/giờ.
- **Bài tập liên quan.** B1.3, VD02
- **Lời thuyết minh (phụ đề):**
  - [0.0–5.9 s] Dữ liệu sinh khối nấm men theo giờ (Pearl 1927) và đường cong logistic khớp với dữ liệu.
  - [5.9–13.5 s] Trong bốn giờ kể từ giờ thứ sáu, sinh khối tăng trung bình khoảng 83 đơn vị mỗi giờ: đó là hệ số góc của cát tuyến.
  - [13.5–20.0 s] Thu hẹp khoảng thời gian: tốc độ trung bình thay đổi và ổn định quanh khoảng 74,4 đơn vị mỗi giờ.
  - [20.0–29.2 s] Giới hạn đó là tốc độ tức thời — đạo hàm của mô hình, hệ số góc của tiếp tuyến. Đạo hàm tính trên mô hình, không trên các điểm đo rời rạc.

## C2. Cân bằng sinh – tử (31 giây)

- **Mục tiêu.** Lập phương trình P' = (b − d)P từ nguyên lý 'thay đổi = vào − ra' và kiểm tra đơn vị.
- **Câu hỏi dừng** (giây 7.1): trong khoảng Δt, P thay đổi bao nhiêu? — *gợi ý:* P(t+Δt) − P(t) = bPΔt − dPΔt + o(Δt): vào trừ ra.
- **Bài tập liên quan.** B1.1, B1.2, VD07
- **Lời thuyết minh (phụ đề):**
  - [0.0–5.1 s] Một quần thể P(t): số cá thể sinh ra là dòng vào, số cá thể chết là dòng ra.
  - [5.1–12.1 s] Trong khoảng thời gian ngắn Δt, số sinh tỉ lệ với quy mô quần thể và với độ dài Δt; số tử cũng vậy.
  - [12.1–18.5 s] Hiệu của chúng là lượng thay đổi. Chia cho Δt và cho Δt tiến về 0, ta được phương trình vi phân.
  - [18.5–24.6 s] Kiểm tra đơn vị: r có đơn vị một trên thời gian, rP có đơn vị cá thể trên thời gian, như P'.
  - [24.6–31.1 s] Mô hình đúng trong phạm vi các giả thiết: b, d không đổi, không di cư, tài nguyên không giới hạn.

## C3. Malthus ngoài miền hiệu lực (27 giây)

- **Mục tiêu.** Miền hiệu lực gắn với một tiêu chí sai số; khớp tốt trên dữ liệu huấn luyện chưa chắc dự báo tốt.
- **Câu hỏi dừng** (giây 5.9): mô hình này dự báo tốt đến giờ thứ mấy (sai số ≤ 10%)? — *gợi ý:* Đến giờ thứ 5 (sai số +3,7%); từ giờ thứ 6 sai số đã +16%.
- **Bài tập liên quan.** B1.4, B1.5, VD10
- **Lời thuyết minh (phụ đề):**
  - [0.0–3.9 s] Khớp mô hình Malthus trên năm giờ đầu của dữ liệu nấm men.
  - [3.9–10.9 s] Với năm giờ đầu, mô hình hàm mũ rất khớp.
  - [10.9–15.6 s] Khi dự báo xa hơn, sai số tăng có hệ thống: tài nguyên bắt đầu hạn chế.
  - [15.6–20.6 s] Nếu chấp nhận sai số tối đa 10%, mô hình này chỉ dùng được đến giờ thứ năm.
  - [20.6–27.0 s] Ở giờ thứ mười, dự báo gấp gần ba lần quan sát. Kết luận gắn với bộ dữ liệu và tiêu chí đã chọn.

## C4. Logistic: đường pha (26 giây)

- **Mục tiêu.** Đọc dấu của f(P) để biết chiều biến thiên; xác định cân bằng và tính ổn định qua f'.
- **Câu hỏi dừng** (giây 3.2): ở đâu P tăng, ở đâu P giảm? — *gợi ý:* P tăng khi f(P) > 0 (0 < P < K), giảm khi f(P) < 0 (P > K).
- **Bài tập liên quan.** B2.1, B2.2, VD15
- **Lời thuyết minh (phụ đề):**
  - [0.0–8.2 s] Đồ thị vế phải f(P) = rP(1 − P/K) với r = 1, K = 100.
  - [8.2–11.9 s] Ở đâu f dương, quần thể tăng; ở đâu f âm, quần thể giảm.
  - [11.9–20.2 s] Điểm 0 không ổn định vì f'(0) = r dương; điểm K ổn định tiệm cận vì f'(K) = −r âm. Mọi nghiệm xuất phát dương đều tiến về K.
  - [20.2–26.2 s] Đỉnh của f tại P = K/2: quần thể tăng nhanh nhất khi đạt một nửa sức chứa, với tốc độ rK/4.

## C5. Mô hình SIR: sơ đồ ngăn (25 giây)

- **Mục tiêu.** Đọc sơ đồ ngăn thành hệ phương trình; tốc độ chuyển ngăn; bảo toàn S + I + R.
- **Câu hỏi dừng** (giây 6.8): tổng S + I + R thay đổi thế nào theo thời gian? — *gợi ý:* Không đổi: dòng ra khỏi S bằng dòng vào I, dòng ra khỏi I bằng dòng vào R.
- **Bài tập liên quan.** B3.1, B3.4, VD23
- **Lời thuyết minh (phụ đề):**
  - [0.0–4.8 s] Cộng đồng được chia thành ba ngăn: cảm nhiễm S, đang nhiễm I, loại ra R.
  - [4.8–12.0 s] Mỗi mũi tên là một tốc độ chuyển ngăn, tính bằng người trên tuần; nguy cơ trên mỗi người cảm nhiễm là β·I/N.
  - [12.0–18.5 s] Dòng ra khỏi S bằng dòng vào I; dòng ra khỏi I bằng dòng vào R. Vì vậy tổng S + I + R không đổi.
  - [18.5–25.4 s] Với tham số cố định của tình huống giáo khoa, số người đang nhiễm đạt đỉnh khoảng 212 người ở tuần 6,85.

## C6. Ngưỡng dịch: R_eff = R0·S/N (29 giây)

- **Mục tiêu.** Điều kiện tăng ban đầu là R0·S(0)/N > 1, không chỉ R0 > 1; đỉnh dịch tại S = N/R0.
- **Câu hỏi dừng** (giây 4.5): bắt đầu với S(0) < N/R0 thì I tăng hay giảm? — *gợi ý:* Giảm ngay: R_eff(0) = R0·S(0)/N < 1, dù R0 > 1 (VD24).
- **Bài tập liên quan.** B3.2, B3.3, VD24
- **Lời thuyết minh (phụ đề):**
  - [0.0–3.5 s] Mặt phẳng pha (S, I) của mô hình SIR với R0 = 2,345.
  - [3.5–9.5 s] Đường đứt nét S = N/R0: bên phải đường này, mỗi người bệnh lây cho hơn một người.
  - [9.5–15.5 s] Bắt đầu với 995 người cảm nhiễm: I tăng, đạt đỉnh đúng khi quỹ đạo cắt đường S = N/R0.
  - [15.5–21.1 s] Bắt đầu với 400 người cảm nhiễm: R_eff ban đầu bằng 0,94, nhỏ hơn 1, nên I giảm ngay.
  - [21.1–28.7 s] Cùng một bệnh, cùng R0, nhưng kết cục phụ thuộc số người còn cảm nhiễm. Dịch kết thúc khi vẫn còn người chưa mắc.

## C7. Một bước: Euler, Heun, RK4 (23 giây)

- **Mục tiêu.** Thấy hình học của một bước giải số và chi phí (số lần tính f) của mỗi phương pháp.
- **Câu hỏi dừng** (giây 5.7): điểm Euler nằm trên hay dưới nghiệm đúng? Vì sao? — *gợi ý:* Dưới: nghiệm đang cong lên (lõm lên) nên tiếp tuyến ở đầu bước nằm dưới đường cong.
- **Bài tập liên quan.** S.1, VD33, VD34, VD35
- **Lời thuyết minh (phụ đề):**
  - [0.0–4.7 s] Một bước h = 2 giờ cho mô hình logistic nấm men, xuất phát từ P0 = 9,6.
  - [4.7–10.7 s] Euler đi theo tiếp tuyến tại đầu bước.
  - [10.7–16.9 s] Heun lấy trung bình hệ số góc ở hai đầu bước; RK4 dùng bốn hệ số góc với trọng số 1, 2, 2, 1.
  - [16.9–23.2 s] Chính xác hơn nhưng mỗi bước tốn nhiều phép tính hơn: Euler một, Heun hai, RK4 bốn lần tính f.

## C8. Sai số và ổn định (35 giây)

- **Mục tiêu.** Đọc bậc hội tụ từ độ dốc trên thang log; phân biệt độ chính xác với ổn định tuyệt đối.
- **Câu hỏi dừng** (giây 2.2): khi h giảm một nửa, sai số RK4 giảm bao nhiêu lần? — *gợi ý:* Khoảng 2⁴ = 16 lần (bậc 4); độ dốc trên thang log bằng bậc.
- **Bài tập liên quan.** S.2, S.3, S.4, VD36, VD37
- **Lời thuyết minh (phụ đề):**
  - [0.0–7.2 s] Sai số tại t = 10 của bài toán logistic khi giảm bước h, vẽ trên thang logarit.
  - [7.2–14.8 s] Độ dốc của mỗi đường bằng bậc hội tụ: Euler khoảng 1, Heun khoảng 2, RK4 khoảng 4.
  - [14.8–20.3 s] Nhưng độ chính xác cao không cứu được một bước quá lớn. Xét y' = −30y với h = 0,1.
  - [20.3–25.6 s] Euler và RK4 đều bùng nổ trong khi nghiệm đúng giảm về 0; Euler ẩn vẫn suy giảm.
  - [25.6–34.7 s] Nghiệm số chỉ suy giảm theo khi trị tuyệt đối của hệ số khuếch đại nhỏ hơn 1: ổn định tuyệt đối là một tính chất khác với bậc chính xác.

## C9. Mặt phẳng pha của hệ tuyến tính (36 giây)

- **Mục tiêu.** Liên hệ quỹ đạo trong mặt phẳng pha với đồ thị x(t), y(t); đọc vai trò của vectơ riêng ở điểm yên ngựa.
- **Câu hỏi dừng** (giây 21.0): bắt đầu đúng trên vectơ riêng (1; −1) thì quỹ đạo đi đâu? — *gợi ý:* Đi thẳng vào gốc dọc theo vectơ riêng ứng với λ = −1 (đa tạp ổn định).
- **Bài tập liên quan.** B4.1, B4.2, VD46
- **Lời thuyết minh (phụ đề):**
  - [0.0–6.5 s] Hệ x' = −0,4x + y, y' = −x − 0,4y. Bên trái: x(t) và y(t) theo thời gian. Bên phải: mặt phẳng pha.
  - [6.5–13.7 s] Mỗi điểm của mặt phẳng pha là một trạng thái (x, y); thời gian không hiện trên hình mà là chiều chuyển động.
  - [13.7–19.0 s] Trị riêng phức với phần thực âm: x và y dao động tắt dần, quỹ đạo xoắn vào gốc.
  - [19.0–26.0 s] Hệ thứ hai có trị riêng 3 và −1: điểm yên ngựa. Các đường đỏ là hai vectơ riêng.
  - [26.0–35.6 s] Xuất phát đúng trên vectơ riêng ứng với −1, nghiệm đi thẳng vào gốc. Lệch một chút, nghiệm tiến gần gốc rồi bị đẩy ra theo vectơ riêng ứng với 3.
