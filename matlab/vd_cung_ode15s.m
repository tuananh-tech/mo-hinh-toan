%VD_CUNG_ODE15S  Bai toan cung (Burden-Faires 5.11, tr. 348-349), VD40:
%   u' = A u + g(t), A = [9 24; -24 -51] (tri rieng -3, -39), u(0) = [4/3; 2/3].
%   So sanh ode45 (Runge-Kutta tuong minh (4,5), khong danh cho bai toan cung) voi
%   ode15s (NDF bac 1-5, danh cho bai toan cung) o CUNG dung sai. So buoc lay tu
%   sol.stats (KHONG dem so diem dau ra, vi ode45 mac dinh tinh them diem noi suy).
A = [9 24; -24 -51];
g = @(t) [5*cos(t) - sin(t)/3; -9*cos(t) + sin(t)/3];
f = @(t, u) A*u + g(t);
u0 = [4/3; 2/3];
chinh_xac = @(t) [2*exp(-3*t) - exp(-39*t) + cos(t)/3; -exp(-3*t) + 2*exp(-39*t) - cos(t)/3];
opts = odeset('RelTol', 1e-6, 'AbsTol', 1e-9);
s45 = ode45(f, [0 10], u0, opts);
s15 = ode15s(f, [0 10], u0, odeset(opts, 'Jacobian', A));
fprintf('Dung sai: RelTol = 1e-6, AbsTol = 1e-9\n');
fprintf('ode45 : %4d buoc thanh cong, %4d buoc that bai, %5d lan tinh f; sai so tai t=10: %.2e\n', ...
    s45.stats.nsteps, s45.stats.nfailed, s45.stats.nfevals, norm(s45.y(:, end) - chinh_xac(10), inf));
fprintf('ode15s: %4d buoc thanh cong, %4d buoc that bai, %5d lan tinh f; sai so tai t=10: %.2e\n', ...
    s15.stats.nsteps, s15.stats.nfailed, s15.stats.nfevals, norm(s15.y(:, end) - chinh_xac(10), inf));
fprintf('RK4 buoc co dinh h = 0.1 (z = -3.9 nam ngoai mien on dinh) tai t = 1:\n');
[~, Y] = mh_rk4(f, 0, u0, 0.1, 1);
disp(Y(end, :));   % bung no, xem Bang 5.22 cua Burden-Faires
