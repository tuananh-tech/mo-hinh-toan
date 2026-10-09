%VD_MO_RONG  Vi du VD41-VD45, VD52-VD54 (Phu luc A).  Chay: >> vd_mo_rong
fprintf('--- VD41 lam nguoi Newton ---\n');
k = log(65/35)/10;
fprintf('k = %.5f (0.06190); t(40 do) = %.2f (23.69); T(30) = %.2f (35.15)\n', k, log(65/15)/k, 25 + 65*exp(-30*k));

fprintf('--- VD42 o nhiem ho ---\n');
V = 1e6; F = 2e4; cv = 5;
fprintf('Q* = %.0f g; V/F = %.0f ngay; t90 = %.1f ngay (115.1); Q(30) = %.0f g (2255942)\n', ...
    V*cv, V/F, V/F*log(10), V*cv*(1 - exp(-F*30/V)));

fprintf('--- VD43 ho chua ---\n');
q = 50; tau = 10; W3 = q*tau*(1 - exp(-3/tau));
fprintf('W(3) = %.2f (129.59); ra max = %.2f (12.96); W(10) = %.2f (64.35)\n', W3, W3/tau, W3*exp(-7/tau));

fprintf('--- VD44 dao dong, nang luong ---\n');
om = 2; fd = @(t, y) [y(2); -om^2*y(1)];
E = @(y) 0.5*y(2)^2 + 0.5*om^2*y(1)^2;
[~, Ye] = mh_euler(fd, 0, [1 0], 0.1, 10);
[~, Yr] = mh_rk4(fd, 0, [1 0], 0.1, 10);
fprintf('Euler: x(10) = %.3f (4.473), E = %.2f (101.01); RK4: x(10) = %.4f (0.4083), E = %.5f (1.99982)\n', ...
    Ye(end,1), E(Ye(end,:)), Yr(end,1), E(Yr(end,:)));

fprintf('--- VD45 Lotka-Volterra, dai luong bao toan ---\n');
a = 1; b = 0.5; m = 0.75; n = 0.25;
fl = @(t, u) [(a - b*u(2))*u(1); (-m + n*u(1))*u(2)];
Vf = @(u) n*u(1) - m*log(u(1)) + b*u(2) - a*log(u(2));
[~, Ye] = mh_euler(fl, 0, [4 1], 0.05, 20);
[~, Yr] = mh_rk4(fl, 0, [4 1], 0.05, 20);
fprintf('V(0) = %.5f (0.46028); Euler V(20) = %.4f (0.7243); RK4 V(20) = %.6f (0.460279)\n', ...
    Vf([4 1]), Vf(Ye(end,:)), Vf(Yr(end,:)));

fprintf('--- VD52 lieu thuoc lap lai (minh hoa toan hoc) ---\n');
kq = mh_thuoc(1, 0.2, 6, 5);
fprintf('R_5 = %.4f (0.4299); R = %.4f (0.4310); voi H = 10, L = 2: C0 = %g, T = %.3f gio (8.047)\n', ...
    kq.R_n, kq.R, 10 - 2, log(10/2)/0.2);

fprintf('--- VD53 quang duong phanh ---\n');
kq = mh_phanh(20, 5);
fprintf('t_dung = %.2f s (4); d = %.2f m (40); v(5) = %.2f (0: xe da dung, khong phai -5)\n', ...
    kq.t_dung, kq.quang_duong, kq.v(5));

fprintf('--- VD54 hai loai canh tranh: x = (1 - y)x, y = (0.5 - 0.5x)y ---\n');
J = [0 -1; -0.5 0];                              % ma tran Jacobi tai (1, 1)
fprintf('tri rieng tai (1,1): %s -> diem yen ngua\n', mat2str(eig(J)', 4));
f = mh_hai_loai_rhs("canh_tranh", 1, 1, 0.5, 0.5);
opts = odeset('RelTol', 1e-9, 'AbsTol', 1e-11, 'Events', @su_kien_ra_hop);
U0 = [0.4 0.3; 2.2 0.4; 0.3 2.0; 2.0 2.4];
for i = 1:size(U0, 1)
    [~, U] = ode45(f, [0 30], U0(i, :)', opts);
    fprintf('(%.1f, %.1f) -> (%.3f, %.3f)\n', U0(i, :), U(end, :));
end

function [gt, dung, huong] = su_kien_ra_hop(~, u)
gt = max(u) - 3.2; dung = 1; huong = 1;
end
