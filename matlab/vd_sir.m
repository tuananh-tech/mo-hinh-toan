%VD_SIR  Vi du VD23-VD32 (Phu luc A, muc A.4).  Chay: >> vd_sir
d = mh_du_lieu(); c = d.cum;
N = c.N; S0 = c.S0; I0 = c.I0; g = c.gamma; b = c.beta;

fprintf('--- VD23 tham so co dinh beta = %.3f ---\n', b);
pk = mh_sir_dinh_dich(S0, I0, N, b, g);
[t, Y, td, Id] = mh_sir_giai(S0, I0, N, b, g, 60);
fprintf('R0 = %.3f (2.345); Imax cong thuc = %.4f (212.2504); Imax su kien = %.4f tai t = %.4f (6.8485)\n', ...
    pk.R0, pk.I_max, Id, td);
fprintf('S_inf = %.4f (129.0805); S(60) ode45 = %.4f\n', mh_sir_quy_mo_cuoi(S0, I0, N, b, g), Y(end,1));
fprintf('bao toan: max|S+I+R-N| = %.2e\n', max(abs(sum(Y, 2) - N)));

fprintf('--- VD24 R0 > 1 nhung R0*S0/N < 1 ---\n');
pk = mh_sir_dinh_dich(400, 5, N, b, g);
fprintf('R_eff(0) = %.3f (0.938); co dinh noi tai: %d (0); S_inf = %.2f (359.62)\n', ...
    pk.R_eff_0, pk.noi_tai, mh_sir_quy_mo_cuoi(400, 5, N, b, g));

fprintf('--- VD25 ---\n');
pk = mh_sir_dinh_dich(9990, 10, 10000, 0.5, 0.2);
fprintf('Imax = %.1f (2338.8); S_inf = %.1f (1072.1)\n', pk.I_max, mh_sir_quy_mo_cuoi(9990, 10, 10000, 0.5, 0.2));

fprintf('--- VD27 so ca moi tuan 1 = S(0)-S(1) ---\n');
opts = odeset('RelTol', 1e-11, 'AbsTol', 1e-11*N);
[~, Y1] = ode45(mh_sir_rhs(b, g, N), [0 1], [S0; I0; 0], opts);
fprintf('ca moi = %.3f (10.639); I(1) = %.3f (11.055); R(1) = %.3f (4.584)\n', S0 - Y1(end,1), Y1(end,2), Y1(end,3));

fprintf('--- VD28 nguong mien dich max(0, 1-1/R0) ---\n');
for R0 = [2.345 1.9969 0.9]
    fprintf('R0 = %.4f: p_c = %.4f\n', R0, max(0, 1 - 1/R0));
end

fprintf('--- VD29, VD30 can thiep ---\n');
pk = mh_sir_dinh_dich(S0, I0, N, 0.6*b, g);
fprintf('giam beta 40%% tu dau: Imax = %.2f (50.14)\n', pk.I_max);
[tc_t, tc_Y] = mh_sir_can_thiep(S0, I0, N, b, 0.6*b, g, 5, 60);
[Imax, k] = max(tc_Y(:,2));
fprintf('can thiep tai t = 5: Imax = %.2f (150.07) tai t = %.2f (5.00); S(60) = %.2f (342.94)\n', Imax, tc_t(k), tc_Y(end,1));

fprintf('--- VD31 hieu chinh beta ---\n');
bE = ((9 - 5) + g*5)*N/(S0*5);
bC = mh_sir_hieu_chinh_beta(S0, I0, N, g, 1, 9);
fprintf('beta Euler = %.6f (1.407035); beta lien tuc = %.5f (1.19816); R0 = %.5f (1.99693)\n', bE, bC, bC/g);
[~, Ye] = mh_euler(mh_sir_rhs(bC, g, N), 0, [S0 I0 0], 1, 1);
fprintf('Euler h=1 voi beta lien tuc: I1 = %.3f (7.961)\n', Ye(end,2));

fprintf('--- VD32 SEIR (sigma = 1/tuan) ---\n');
seir = @(t, y) [-b*y(1)*y(3)/N; b*y(1)*y(3)/N - 1*y(2); 1*y(2) - g*y(3); g*y(3)];
[ts, Ys] = ode45(seir, linspace(0, 80, 80001), [S0; 0; I0; 0], opts);
[Imax, k] = max(Ys(:,3));
fprintf('SEIR: Imax = %.2f (131.01) tai t = %.2f (13.23); S(80) = %.3f (129.081)\n', Imax, ts(k), Ys(end,1));
