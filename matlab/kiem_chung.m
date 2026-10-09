%KIEM_CHUNG  Bo kiem thu MATLAB cua do an (co assertion va dung sai ro rang).
%   Chay:  >> kiem_chung
%   - Moi kiem tra co: nhom, ten, gia tri MATLAB, gia tri ky vong, dung sai, kieu so sanh.
%   - Mot kiem tra loi KHONG dung ca bo: loi duoc ghi vao cot ghi_chu, kiem tra tinh la KHONG DAT.
%   - Ket qua ghi vao ket_qua_matlab/kiem_chung.csv; neu co kiem tra khong dat thi bao loi o cuoi
%     (de lenh matlab -batch tra ve ma loi khac 0).
%   - Nhom J doi chieu MATLAB-Python tren CUNG bai toan, luoi, dung sai, doc tu
%     hoc_lieu/ket_qua/doi_chieu_python.csv (sinh bang hoc_lieu/scripts/xuat_doi_chieu_matlab.py).
thu_muc = fileparts(mfilename('fullpath'));
thu_muc_kq = fullfile(thu_muc, 'ket_qua_matlab');
if ~exist(thu_muc_kq, 'dir'), mkdir(thu_muc_kq); end
KQ = struct('nhom', {}, 'ten', {}, 'gia_tri', {}, 'ky_vong', {}, 'dung_sai', {}, 'kieu', {}, ...
    'dat', {}, 'ghi_chu', {});

% ---------------------------------------------------------------- A. dau vao
KQ = them(KQ, 'A dau vao', 'mh_luoi bao loi khi (T-t0)/h khong nguyen', @() co_loi(@() mh_luoi(0, 1, 0.3)), true, 0, 'dung');
KQ = them(KQ, 'A dau vao', 'mh_rk4 bao loi khi f tra sai kich thuoc', ...
    @() co_loi(@() mh_rk4(@(t, y) [y; y], 0, 1, 0.1, 1)), true, 0, 'dung');
KQ = them(KQ, 'A dau vao', 'mh_rk4 bao loi khi nghiem khong huu han', ...
    @() co_loi(@() mh_rk4(@(t, y) y ./ (t - 0.5), 0, 1, 0.25, 1)), true, 0, 'dung');
KQ = them(KQ, 'A dau vao', 'mh_euler bao loi khi y0 khong huu han', ...
    @() co_loi(@() mh_euler(@(t, y) y, 0, NaN, 0.1, 1)), true, 0, 'dung');
% Dot 4 (phan bien): cac loi da duoc gop y o ban truoc
KQ = them(KQ, 'A dau vao', 'mh_euler bao loi khi f tra VECTO HANG (khong de mo rong ngam thanh ma tran)', ...
    @() co_ma_loi(@() mh_euler(@(t, y) y.', 0, [1; 2], 0.1, 1), 'mh_euler:kich_thuoc'), true, 0, 'dung');
KQ = them(KQ, 'A dau vao', 'mh_rk4 bao loi khi y0 la MA TRAN (khong am tham lam phang)', ...
    @() co_ma_loi(@() mh_rk4(@(t, y) -y, 0, eye(2), 0.1, 1), 'mh_rk4:y0'), true, 0, 'dung');
KQ = them(KQ, 'A dau vao', 'mh_euler bao loi khi f sinh so PHUC', ...
    @() co_ma_loi(@() mh_euler(@(t, y) sqrt(-y), 0, 1, 0.1, 1), 'mh_euler:gia_tri'), true, 0, 'dung');
KQ = them(KQ, 'A dau vao', 'mh_luoi bao loi khi h phuc hoac Inf', ...
    @() co_ma_loi(@() mh_luoi(0, 1, 0.1 + 0.1i), 'mh_luoi:buoc') && co_ma_loi(@() mh_luoi(0, 1, Inf), 'mh_luoi:buoc'), true, 0, 'dung');
KQ = them(KQ, 'A dau vao', 'mh_sir_giai bao loi khi S0 + I0 + R_bd khac N', ...
    @() co_ma_loi(@() mh_sir_giai(990, 5, 1000, 1.407, 0.6, 10, 50), 'mh_sir_giai:tong'), true, 0, 'dung');
KQ = them(KQ, 'A dau vao', 'mh_sir_giai chap nhan R_bd dung tong (995 + 5 + 0 = N)', ...
    @() ~co_loi(@() mh_sir_giai(995, 5, 1000, 1.407, 0.6, 10, 0)), true, 0, 'dung');
KQ = them(KQ, 'A dau vao', 'mh_jordan2 bao loi khi v1 = 0 (vecto rieng luon khac 0)', ...
    @() co_ma_loi(@() mh_jordan2([3 1; -1 1], 2, [0; 0]), 'mh_jordan2:vecto_khong'), true, 0, 'dung');
KQ = them(KQ, 'A dau vao', 'mh_jordan2 bao loi khi lam co du vecto rieng (A = 2I)', ...
    @() co_ma_loi(@() mh_jordan2(2 * eye(2), 2, [1; 0]), 'mh_jordan2:khong_giai_duoc'), true, 0, 'dung');
KQ = them(KQ, 'A dau vao', 'mh_nghiem_phuc bao loi voi ma tran phuc', ...
    @() co_ma_loi(@() mh_nghiem_phuc([1 1i; -1 1]), 'mh_nghiem_phuc:dau_vao'), true, 0, 'dung');

% ---------------------------------------------------------------- B. nghiem giai tich, phan du
r = 0.55; K = 665; P0 = 9.6;
fl = @(t, P) r * P .* (1 - P / K);
KQ = them(KQ, 'B phan du', 'phan du nghiem logistic tuong minh', ...
    @() max(abs(((mh_logistic_chinh_xac((1:18) + 1e-6, P0, r, K) - mh_logistic_chinh_xac((1:18) - 1e-6, P0, r, K)) / 2e-6) ...
    - fl(0, mh_logistic_chinh_xac(1:18, P0, r, K))) ./ fl(0, mh_logistic_chinh_xac(1:18, P0, r, K))), 0, 1e-6, 'tuyet_doi');
A = [1 -5; 1 -1]; [u1, u2] = mh_nghiem_phuc(A);
KQ = them(KQ, 'B phan du', 'tri rieng phuc: phan du u1', @() phan_du(A, u1, 0.3), 0, 1e-7, 'tuyet_doi');
KQ = them(KQ, 'B phan du', 'tri rieng phuc: phan du u2', @() phan_du(A, u2, 0.3), 0, 1e-7, 'tuyet_doi');
A = [3 1; -1 1]; [~, ~, w2] = mh_jordan2(A, 2, [1; -1]);
KQ = them(KQ, 'B phan du', 'chuoi Jordan: phan du e^{2t}(t v1 + v2)', @() phan_du(A, w2, 0.4), 0, 1e-6, 'tuyet_doi');
A = [1 -4; -1 1];
KQ = them(KQ, 'B phan du', 'expm so voi ode45 (he tuyen tinh, t = 1)', @() sai_so_expm_ode45(A), 0, 1e-8, 'tuyet_doi');

% ---------------------------------------------------------------- C. bac hoi tu
pp = {@mh_euler, @mh_heun, @mh_diem_giua, @mh_rk4}; bac = [1 2 2 4];
for i = 1:4
    KQ = them(KQ, 'C bac hoi tu', sprintf('bac thuc nghiem %s (h = 0.25 -> 0.125)', func2str(pp{i})), ...
        @() bac_thuc_nghiem(pp{i}, fl, P0, r, K), bac(i), 0.15, 'tuyet_doi');
end

% ---------------------------------------------------------------- D. SIR
fs = mh_sir_rhs(1.407, 0.6, 1000);
KQ = them(KQ, 'D SIR', 'Euler h=0.5 bao toan S+I+R', @() lech_tong(@mh_euler, fs, 0.5, 24), 0, 1e-9, 'tuyet_doi');
KQ = them(KQ, 'D SIR', 'RK4 h=0.5 bao toan S+I+R', @() lech_tong(@mh_rk4, fs, 0.5, 24), 0, 1e-9, 'tuyet_doi');
KQ = them(KQ, 'D SIR', 'RK4 h=0.5 khong am (min S, I > 0)', @() min_thanh_phan(@mh_rk4, fs, 0.5, 24) > 0, true, 0, 'dung');
KQ = them(KQ, 'D SIR', 'Euler h=3 tren [0,30]: phat hien S am (khong cat ve 0)', ...
    @() min_thanh_phan(@mh_euler, fs, 3, 30) < 0, true, 0, 'dung');
pk = mh_sir_dinh_dich(995, 5, 1000, 1.407, 0.6);
KQ = them(KQ, 'D SIR', 'I_max giai tich', @() pk.I_max, 212.2503795, 1e-6, 'tuong_doi');
KQ = them(KQ, 'D SIR', 'dinh ode45 trung I_max giai tich', @() dinh_ode45(), pk.I_max, 1e-6, 'tuong_doi');
Sinf = mh_sir_quy_mo_cuoi(995, 5, 1000, 1.407, 0.6);
KQ = them(KQ, 'D SIR', 'S_inf (fzero)', @() Sinf, 129.0805498, 1e-8, 'tuong_doi');
KQ = them(KQ, 'D SIR', 'S(80) cua ode45 trung S_inf', @() S80_ode45(), Sinf, 1e-5, 'tuong_doi');
KQ = them(KQ, 'D SIR', 'R0*S0/N <= 1 => khong co dinh noi tai', @() ~mh_sir_dinh_dich(400, 5, 1000, 1.407, 0.6).noi_tai, true, 0, 'dung');
KQ = them(KQ, 'D SIR', 'I0 = 0 => S_inf = S0', @() mh_sir_quy_mo_cuoi(995, 0, 1000, 1.407, 0.6), 995, 0, 'tuyet_doi');

% ---------------------------------------------------------------- E. nang luong, bat bien
om = 2; fd = @(t, y) [y(2); -om^2 * y(1)]; E = @(y) 0.5 * y(2)^2 + 0.5 * om^2 * y(1)^2;
KQ = them(KQ, 'E bat bien', 'Euler: E_n = (1 + h^2 w^2)^n E_0 (h = 0.1, n = 100)', ...
    @() nang_luong(@mh_euler, fd, E, 0.1), 2 * (1 + 0.04)^100, 1e-10, 'tuong_doi');
KQ = them(KQ, 'E bat bien', 'RK4: troi nang luong giam ~ h^5 (ti so khi chia doi h)', ...
    @() abs(nang_luong(@mh_rk4, fd, E, 0.1) - 2) / abs(nang_luong(@mh_rk4, fd, E, 0.05) - 2), 32, 0.2, 'tuong_doi');
fL = mh_hai_loai_rhs("thu_moi", 1, 0.5, 0.75, 0.25);
VL = @(u) 0.25 * u(1) - 0.75 * log(u(1)) + 0.5 * u(2) - log(u(2));
KQ = them(KQ, 'E bat bien', 'Lotka-Volterra: RK4 giu bat bien V (h = 0.05, T = 20)', ...
    @() bat_bien(@mh_rk4, fL, VL), 0, 1e-5, 'tuyet_doi');
KQ = them(KQ, 'E bat bien', 'Lotka-Volterra: Euler lam lech V dang ke', @() bat_bien(@mh_euler, fL, VL) > 0.1, true, 0, 'dung');

% ---------------------------------------------------------------- F. do nhay tham so
Im = @(b) mh_sir_dinh_dich(995, 5, 1000, b, 0.6).I_max;
KQ = them(KQ, 'F do nhay', 'I_max tang theo beta (1.3 < 1.407 < 1.5)', @() Im(1.3) < Im(1.407) && Im(1.407) < Im(1.5), true, 0, 'dung');
KQ = them(KQ, 'F do nhay', 'S_inf giam theo beta', ...
    @() mh_sir_quy_mo_cuoi(995, 5, 1000, 1.5, 0.6) < mh_sir_quy_mo_cuoi(995, 5, 1000, 1.3, 0.6), true, 0, 'dung');
KQ = them(KQ, 'F do nhay', 'beta lien tuc (fzero + ode45)', @() mh_sir_hieu_chinh_beta(995, 5, 1000, 0.6, 1, 9), 1.19815655, 1e-7, 'tuong_doi');

% ---------------------------------------------------------------- G. khop du lieu
d = mh_du_lieu();
KQ = them(KQ, 'G khop du lieu', 'hoi quy ln(P/(665-P)): he so goc r', ...
    @() mh_hoi_quy(d.nam_men.t, log(d.nam_men.P ./ (665 - d.nam_men.P))), 0.530674663, 1e-8, 'tuong_doi');
KQ = them(KQ, 'G khop du lieu', 'NLS (fminsearch): K', @() khop_K(d), 663.0220, 5e-4, 'tuong_doi');

% ---------------------------------------------------------------- H. khai thac, I. phuong phap an, K. bai toan cung
KQ = them(KQ, 'H khai thac', 'H = rK/4, P0 = 400: tuyet chung tai t = 16', @() t_tuyet_chung(125, 400, 200), 16, 1e-6, 'tuyet_doi');
KQ = them(KQ, 'H khai thac', 'H > rK/4: tuyet chung tai t = 18.60888', @() t_tuyet_chung(150, 800, 100), 18.6088797528, 1e-7, 'tuong_doi');
KQ = them(KQ, 'H khai thac', 'H < rK/4, P0 > P_-: tien ve P_+ (khong tuyet chung)', @() tien_ve_P_cong(), true, 0, 'dung');
KQ = them(KQ, 'I phuong phap an', 'Euler an: y_15 = (1/4)^15/3', @() euler_an_y15(), (1/3) * 0.25^15, 1e-12, 'tuong_doi');
KQ = them(KQ, 'I phuong phap an', 'Hinh thang an: y_15 = (-0.2)^15/3', @() hinh_thang_an_y15(), (1/3) * (-0.2)^15, 1e-12, 'tuong_doi');
KQ = them(KQ, 'K bai toan cung', 'ode15s it buoc hon ode45, ca hai sai so < 1e-5', @() cung_ok(), true, 0, 'dung');

% ---------------------------------------------------------------- J. doi chieu MATLAB - Python
tep = fullfile(thu_muc, '..', 'ket_qua', 'doi_chieu_python.csv');
if exist(tep, 'file')
    B = readtable(tep, 'TextType', 'string', 'Delimiter', ',', 'VariableNamingRule', 'preserve');
    for i = 1:height(B)
        ten = char(B.ten(i));
        KQ = them(KQ, 'J MATLAB-Python', ten, @() gia_tri_matlab(ten), double(B.gia_tri(i)), double(B.dung_sai(i)), char(B.kieu(i)));
    end
else
    KQ = them(KQ, 'J MATLAB-Python', 'co tep doi_chieu_python.csv', @() false, true, 0, 'dung');
end

% ---------------------------------------------------------------- tong ket
T = struct2table(KQ);
writetable(T, fullfile(thu_muc_kq, 'kiem_chung.csv'));
so_dat = sum([KQ.dat]); so_kt = numel(KQ);
fprintf('\nKET QUA: %d/%d kiem tra dat. Bang chi tiet: %s\n', so_dat, so_kt, fullfile(thu_muc_kq, 'kiem_chung.csv'));
if so_dat < so_kt
    error('kiem_chung:that_bai', '%d kiem tra KHONG DAT (xem cot ghi_chu trong kiem_chung.csv).', so_kt - so_dat);
end

% ================================================================ ham cuc bo
function KQ = them(KQ, nhom, ten, ham, ky_vong, dung_sai, kieu)
ghi_chu = '';
try
    v = ham();
    switch kieu
        case 'dung',      dat = isequal(logical(v), logical(ky_vong));
        case 'tuyet_doi', dat = abs(v - ky_vong) <= dung_sai;
        case 'tuong_doi', dat = abs(v - ky_vong) <= dung_sai * max(abs(ky_vong), eps);
        otherwise, error('kiem_chung:kieu', 'Kieu so sanh khong hop le: %s', kieu);
    end
catch e
    v = NaN; dat = false; ghi_chu = e.message;
end
KQ(end + 1) = struct('nhom', nhom, 'ten', ten, 'gia_tri', double(v), 'ky_vong', double(ky_vong), ...
    'dung_sai', dung_sai, 'kieu', kieu, 'dat', dat, 'ghi_chu', ghi_chu);
nhan = {'[KHONG DAT]', '[DAT]      '};
fprintf('%s %-16s %-60s MATLAB = %-16.10g ky vong = %-16.10g %s\n', nhan{dat + 1}, nhom, ten, double(v), double(ky_vong), ghi_chu);
end

function b = co_loi(ham)
b = false;
try, ham(); catch, b = true; end
end

function b = co_ma_loi(ham, ma)
%CO_MA_LOI  true neu ham() bao loi DUNG ma dinh danh 'ma' (khong chap nhan loi bat ky).
b = false;
try
    ham();
catch loi
    b = strcmp(loi.identifier, ma);
end
end

function e = phan_du(A, u, t)
e = norm((u(t + 1e-6) - u(t - 1e-6)) / 2e-6 - A * u(t), inf);
end

function e = sai_so_expm_ode45(A)
[~, Y] = ode45(@(t, y) A * y, [0 1], [1; 0], odeset('RelTol', 1e-12, 'AbsTol', 1e-14));
e = norm(Y(end, :)' - expm(A) * [1; 0], inf);
end

function p = bac_thuc_nghiem(pp, fl, P0, r, K)
ex = mh_logistic_chinh_xac(10, P0, r, K);
[~, Y1] = pp(fl, 0, P0, 0.25, 10); [~, Y2] = pp(fl, 0, P0, 0.125, 10);
p = log2(abs(Y1(end) - ex) / abs(Y2(end) - ex));
end

function e = lech_tong(pp, fs, h, T)
[~, Y] = pp(fs, 0, [995 5 0], h, T); e = max(abs(sum(Y, 2) - 1000));
end

function m = min_thanh_phan(pp, fs, h, T)
[~, Y] = pp(fs, 0, [995 5 0], h, T); m = min(min(Y(:, 1:2)));
end

function I = dinh_ode45()
[~, ~, ~, I] = mh_sir_giai(995, 5, 1000, 1.407, 0.6, 80);
end

function S = S80_ode45()
[~, Y] = mh_sir_giai(995, 5, 1000, 1.407, 0.6, 80); S = Y(end, 1);
end

function En = nang_luong(pp, fd, E, h)
[~, Y] = pp(fd, 0, [1 0], h, 10); En = E(Y(end, :));
end

function e = bat_bien(pp, fL, VL)
[~, Y] = pp(fL, 0, [4 1], 0.05, 20); e = abs(VL(Y(end, :)) - VL([4 1]));
end

function Kv = khop_K(d)
[~, Kv] = mh_khop_logistic(d.nam_men.t, d.nam_men.P);
end

function te = t_tuyet_chung(H, P0, T)
[~, ~, te] = mh_khai_thac_mo_phong(0.5, 1000, H, P0, T);
end

function ok = tien_ve_P_cong()
H = 100; r = 0.5; K = 1000;
Pc = K / 2 * (1 + sqrt(1 - 4 * H / (r * K)));
[~, P, te] = mh_khai_thac_mo_phong(r, K, H, 300, 200);
ok = isempty(te) && abs(P(end) - Pc) < 1e-3;
end

function y = euler_an_y15()
[~, Y] = mh_euler_an(@(t, y) -30 * y, @(t, y) -30, 0, 1/3, 0.1, 1.5); y = Y(end);
end

function y = hinh_thang_an_y15()
[~, Y] = mh_hinh_thang_an(@(t, y) -30 * y, @(t, y) -30, 0, 1/3, 0.1, 1.5); y = Y(end);
end

function ok = cung_ok()
A = [9 24; -24 -51];
f = @(t, u) A * u + [5 * cos(t) - sin(t) / 3; -9 * cos(t) + sin(t) / 3];
ex = [2 * exp(-30) - exp(-390) + cos(10) / 3; -exp(-30) + 2 * exp(-390) - cos(10) / 3];
o = odeset('RelTol', 1e-6, 'AbsTol', 1e-9);
s45 = ode45(f, [0 10], [4/3; 2/3], o);
s15 = ode15s(f, [0 10], [4/3; 2/3], odeset(o, 'Jacobian', A));
ok = s15.stats.nsteps < s45.stats.nsteps && norm(s45.y(:, end) - ex, inf) < 1e-5 && norm(s15.y(:, end) - ex, inf) < 1e-5;
end

function v = gia_tri_matlab(ten)
%GIA_TRI_MATLAB  Tinh lai bang MATLAB dai luong mang ten 'ten' trong doi_chieu_python.csv.
fl = @(t, P) 0.55 * P .* (1 - P / 665);
fs = mh_sir_rhs(1.407, 0.6, 1000);
switch ten
    case 'logistic_euler_P10_h025',     [~, Y] = mh_euler(fl, 0, 9.6, 0.25, 10); v = Y(end);
    case 'logistic_heun_P10_h025',      [~, Y] = mh_heun(fl, 0, 9.6, 0.25, 10); v = Y(end);
    case 'logistic_diem_giua_P10_h025', [~, Y] = mh_diem_giua(fl, 0, 9.6, 0.25, 10); v = Y(end);
    case 'logistic_rk4_P10_h025',       [~, Y] = mh_rk4(fl, 0, 9.6, 0.25, 10); v = Y(end);
    case 'logistic_chinh_xac_P10',      v = mh_logistic_chinh_xac(10, 9.6, 0.55, 665);
    case 'sir_rk4_S24_h05',             [~, Y] = mh_rk4(fs, 0, [995 5 0], 0.5, 24); v = Y(end, 1);
    case 'sir_rk4_maxI_h05',            [~, Y] = mh_rk4(fs, 0, [995 5 0], 0.5, 24); v = max(Y(:, 2));
    case 'sir_euler_maxI_h1',           [~, Y] = mh_euler(fs, 0, [995 5 0], 1, 24); v = max(Y(:, 2));
    case 'sir_euler_minI_h2_T30',       [~, Y] = mh_euler(fs, 0, [995 5 0], 2, 30); v = min(Y(:, 2));
    case 'sir_Imax_giai_tich',          v = mh_sir_dinh_dich(995, 5, 1000, 1.407, 0.6).I_max;
    case 'sir_S_inf',                   v = mh_sir_quy_mo_cuoi(995, 5, 1000, 1.407, 0.6);
    case 'sir_t_dinh_ode',              [~, ~, v] = mh_sir_giai(995, 5, 1000, 1.407, 0.6, 80);
    case 'sir_beta_lien_tuc',           v = mh_sir_hieu_chinh_beta(995, 5, 1000, 0.6, 1, 9);
    case 'sir_beta_euler',              v = ((9 - 5) + 0.6 * 5) / (995 * 5 / 1000);
    case 'seir_Imax'
        f4 = @(t, y) [-1.407*y(1)*y(3)/1000; 1.407*y(1)*y(3)/1000 - y(2); y(2) - 0.6*y(3); 0.6*y(3)];
        s = ode45(f4, [0 80], [995; 0; 5; 0], odeset('RelTol', 1e-11, 'AbsTol', 1e-9));
        v = max(deval(s, linspace(0, 80, 160001), 3));
    case {'he_rk4_x1', 'he_rk4_y1'}
        [~, Y] = mh_rk4(@(t, w) [1 -4; -1 1] * w, 0, [1 0], 0.2, 0.2);
        v = Y(end, 1 + strcmp(ten, 'he_rk4_y1'));
    case {'he_expm_x', 'he_expm_y'}
        e = expm(0.2 * [1 -4; -1 1]) * [1; 0]; v = e(1 + strcmp(ten, 'he_expm_y'));
    case {'hsbd_b1', 'hsbd_b2'}
        A = [1 2; 3 2]; a = A \ [-2; 4]; b = A \ a; v = b(1 + strcmp(ten, 'hsbd_b2'));
    case 'nam_men_hoi_quy_r'
        d = mh_du_lieu(); v = mh_hoi_quy(d.nam_men.t, log(d.nam_men.P ./ (665 - d.nam_men.P)));
    case 'nam_men_nls_r'
        d = mh_du_lieu(); v = mh_khop_logistic(d.nam_men.t, d.nam_men.P);
    case 'nam_men_nls_K'
        d = mh_du_lieu(); [~, v] = mh_khop_logistic(d.nam_men.t, d.nam_men.P);
    case 'khai_thac_t_tuyet_chung',     [~, ~, v] = mh_khai_thac_mo_phong(0.5, 1000, 150, 800, 100);
    case {'dao_dong_euler_E10', 'dao_dong_rk4_E10'}
        fd = @(t, y) [y(2); -4 * y(1)];
        if strcmp(ten, 'dao_dong_euler_E10'), [~, Y] = mh_euler(fd, 0, [1 0], 0.1, 10);
        else, [~, Y] = mh_rk4(fd, 0, [1 0], 0.1, 10); end
        v = 0.5 * Y(end, 2)^2 + 2 * Y(end, 1)^2;
    case 'lotka_rk4_V20'
        [~, Y] = mh_rk4(mh_hai_loai_rhs("thu_moi", 1, 0.5, 0.75, 0.25), 0, [4 1], 0.05, 20);
        u = Y(end, :); v = 0.25 * u(1) - 0.75 * log(u(1)) + 0.5 * u(2) - log(u(2));
    case 'thuoc_R_gioi_han',            v = mh_thuoc(1, 0.2, 6, 1).R;
    case 'thuoc_T_chu_ky',              v = log(10 / 2) / 0.2;
    case 'phanh_quang_duong',           v = mh_phanh(20, 5).quang_duong;
    otherwise
        error('kiem_chung:ten', 'Chua co cach tinh MATLAB cho "%s".', ten);
end
end
