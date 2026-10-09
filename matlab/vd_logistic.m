%VD_LOGISTIC  Vi du VD13-VD22 (Phu luc A, muc A.3).  Chay: >> vd_logistic
d = mh_du_lieu();
r = 0.4; K = 500; P0 = 20;
fprintf('--- VD13 ---\n');
fprintf('t* = %.3f (7.945); rK/4 = %.1f (50); t90 = %.2f (13.44); P(5) = %.2f (117.70)\n', ...
    log((K-P0)/P0)/r, r*K/4, log(450*(K-P0)/(P0*(K-450)))/r, mh_logistic_chinh_xac(5, P0, r, K));

fprintf('--- VD14 ---\n');
fprintf('P(2) = %.2f (601.32); t(550) = %.3f (3.543)\n', mh_logistic_chinh_xac(2, 800, r, K), ...
    log(550*(K-800)/(800*(K-550)))/r);

fprintf('--- VD16 tuyen tinh hoa voi K = 665 ---\n');
[a, c, R2] = mh_hoi_quy(d.nam_men.t, log(d.nam_men.P ./ (665 - d.nam_men.P)));
fprintf('r = %.4f (0.5307); c = %.4f (-4.1636); t* = %.3f (7.846); R2 = %.4f (0.9996)\n', a, c, -c/a, R2);

fprintf('--- VD17 binh phuong toi thieu phi tuyen (fminsearch) ---\n');
[rr, KK, ts, e] = mh_khop_logistic(d.nam_men.t, d.nam_men.P, [0.5 794.16 9]);
fprintf('r = %.4f (0.5470); K = %.2f (663.02); t* = %.3f (7.808); RMSE = %.2f (3.20)\n', rr, KK, ts, e);

fprintf('--- VD18 chia du lieu theo thoi gian ---\n');
for tc = [7 9 11 13]
    tr = d.nam_men.t <= tc; te = ~tr;
    [rr, KK, ts] = mh_khop_logistic(d.nam_men.t(tr), d.nam_men.P(tr), [0.5 1.2*max(d.nam_men.P(tr)) 6]);
    Pd = KK ./ (1 + exp(-rr*(d.nam_men.t(te) - ts)));
    fprintf('t_c = %2d: K = %8.2f, RMSE kiem tra logistic = %8.2f\n', tc, KK, ...
        sqrt(mean((Pd - d.nam_men.P(te)).^2)));
end
fprintf('(ky vong K: 865.97, 721.43, 656.73, 659.21; RMSE: 142.51, 45.62, 5.98, 3.92)\n');

fprintf('--- VD19-VD21 khai thac ---\n');
[~, ~, te1] = mh_khai_thac_mo_phong(0.5, 1000, 100, 200, 60);
[~, ~, te2] = mh_khai_thac_mo_phong(0.5, 1000, 125, 400, 200);
[t3, P3, te3] = mh_khai_thac_mo_phong(0.5, 1000, 125, 600, 200);
[~, ~, te4] = mh_khai_thac_mo_phong(0.5, 1000, 150, 800, 100);
fprintf('H=100, P0=200: tuyet chung t = %.3f (4.304)\n', te1);
fprintf('H=125, P0=400: tuyet chung t = %.6f (16.000000)\n', te2);
fprintf('H=125, P0=600: P(200) = %.4f (509.0909); te rong: %d\n', P3(end), isempty(te3));
fprintf('H=150, P0=800: tuyet chung t = %.4f (18.6089)\n', te4);

fprintf('--- VD22 doi bien u = 1/P ---\n');
u = 1/K + (1/P0 - 1/K)*exp(-r*5);
fprintf('P(5) = %.4f (117.7012)\n', 1/u);
