%VD_HE_TUYEN_TINH  Vi du VD46-VD51 (Phu luc A): he tuyen tinh he so hang.
%   Moi nghiem duoc KIEM TRA bang the vao he (phan du) va doi chieu voi expm.
%   Gia tri trong ngoac la gia tri Python (hoc_lieu/mhtoan).  Chay: >> vd_he_tuyen_tinh
phan_du = @(A, u, t) norm((u(t + 1e-6) - u(t - 1e-6)) / 2e-6 - A * u(t), inf);

fprintf('--- VD46 tri rieng phuc: A = [1 -5; 1 -1] ---\n');
A = [1 -5; 1 -1];
[u1, u2, al, be] = mh_nghiem_phuc(A);
fprintf('alpha = %.3g, beta = %.3g (0, 2); phan du u1 = %.1e, u2 = %.1e\n', al, be, ...
    phan_du(A, u1, 0.3), phan_du(A, u2, 0.3));
c = [u1(0) u2(0)] \ [1; 0];                    % giai he 2x2 bang A\b, khong dung inv
u = @(t) c(1)*u1(t) + c(2)*u2(t);
fprintf('|u(1.3) - expm(1.3 A) y0| = %.1e\n', norm(u(1.3) - expm(1.3*A)*[1; 0], inf));

fprintf('--- VD47 chuoi Jordan: A = [3 1; -1 1], lambda = 2 (boi dai so 2, boi hinh hoc 1) ---\n');
A = [3 1; -1 1];
[v2, ~, w2] = mh_jordan2(A, 2, [1; -1]);
fprintf('v2 = [%.3g %.3g]; phan du e^{2t}(t v1 + v2) = %.1e; rank(A - 2I) = %d\n', v2, ...
    phan_du(A, w2, 0.4), rank(A - 2*eye(2)));

fprintf('--- VD48 he so bat dinh: x'' = [1 2; 3 2] x + t [2; -4] ---\n');
A = [1 2; 3 2]; g = [2; -4];
a = A \ (-g); b = A \ a;
fprintf('a = [%.4g %.4g] (3, -2.5); b = [%.4g %.4g] (-2.75, 2.875)\n', a, b);
xp = @(t) t*a + b;
fprintf('phan du nghiem rieng = %.1e\n', norm(a - (A*xp(0.7) + 0.7*g), inf));

fprintf('--- VD49 bien thien hang so: x'' = [-5 1; 4 -2] x + e^{2t} [6; -1] ---\n');
A = [-5 1; 4 -2]; g = @(t) exp(2*t)*[6; -1];
xp = @(t) exp(2*t)*[23/24; 17/24];
d = (xp(0.7 + 1e-6) - xp(0.7 - 1e-6)) / 2e-6;
fprintf('tri rieng: %s; phan du x_p = %.1e\n', mat2str(sort(eig(A))', 4), norm(d - A*xp(0.7) - g(0.7), inf));
y0 = xp(0);
yt = expm(1*A)*y0 + integral(@(s) expm((1 - s)*A)*g(s), 0, 1, 'ArrayValued', true, ...
    'RelTol', 1e-12, 'AbsTol', 1e-14);
fprintf('|expm + tich phan - x_p(1)| = %.1e\n', norm(yt - xp(1), inf));

fprintf('--- VD50 khu bien: x'' = 3x - 2y, y'' = 2x - y, (x, y)(0) = (1, 0) ---\n');
A = [3 -2; 2 -1];
x = @(t) (1 + 2*t).*exp(t); y = @(t) (2*t).*exp(t);       % c1 = 1, c2 = 2
fprintf('|(x, y)(0.8) - expm(0.8 A) y0| = %.1e\n', norm([x(0.8); y(0.8)] - expm(0.8*A)*[1; 0], inf));

fprintf('--- VD51 RK4 va Euler cho x'' = x - 4y, y'' = -x + y, (1, 0) ---\n');
A = [1 -4; -1 1]; f = @(t, w) A*w;
h = 0.2; w0 = [1; 0];
K1 = h*f(0, w0); K2 = h*f(h/2, w0 + K1/2); K3 = h*f(h/2, w0 + K2/2); K4 = h*f(h, w0 + K3);
fprintf('K1 = [%g %g], K2 = [%g %g], K3 = [%g %g], K4 = [%g %g]\n', K1, K2, K3, K4);
[~, Yr] = mh_rk4(f, 0, w0, 0.2, 0.2);
[~, Ye] = mh_euler(f, 0, w0, 0.1, 0.2);
fprintf('RK4: (%.10f, %.10f) (1.3200666667, -0.2506666667); Euler h=0.1: (%.4f, %.4f) (1.25, -0.22)\n', ...
    Yr(end, :), Ye(end, :));
fprintf('dung (expm): (%.10f, %.10f) (1.3204247767, -0.2508470118)\n', expm(0.2*A)*w0);

fprintf('--- Phan tuy chon: Symbolic Math Toolbox ---\n');
if ~isempty(ver('symbolic')) && license('test', 'Symbolic_Toolbox')
    syms xs(t) ys(t)
    Sol = dsolve([diff(xs) == xs - 4*ys, diff(ys) == -xs + ys], [xs(0) == 1, ys(0) == 0]);
    disp(simplify([Sol.xs; Sol.ys]));
else
    fprintf('Khong co Symbolic Math Toolbox: BO QUA phan dsolve (khong anh huong cac kiem tra).\n');
end
