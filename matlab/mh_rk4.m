function [t, Y] = mh_rk4(f, t0, y0, h, T)
%MH_RK4  Runge-Kutta bac bon co dien, buoc co dinh (Burden-Faires tr. 288):
%   k1 = h f(t_n, y_n),  k2 = h f(t_n + h/2, y_n + k1/2),
%   k3 = h f(t_n + h/2, y_n + k2/2),  k4 = h f(t_n + h, y_n + k3),
%   y_{n+1} = y_n + (k1 + 2 k2 + 2 k3 + k4)/6.
%   Luu y: ode45 cua MATLAB KHONG phai phuong phap nay (ode45 dung cap
%   Dormand-Prince (4,5) voi buoc thich nghi).
t = mh_luoi(t0, T, h);
y = mh_chuan_bi(f, t0, y0, 'mh_rk4');
Y = zeros(numel(t), numel(y));
Y(1, :) = y.';
for n = 1:numel(t) - 1
    k1 = h * f(t(n), y);
    k2 = h * f(t(n) + h / 2, y + k1 / 2);
    k3 = h * f(t(n) + h / 2, y + k2 / 2);
    k4 = h * f(t(n) + h, y + k3);
    y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
    mh_kiem_huu_han(y, n, 'mh_rk4');
    Y(n + 1, :) = y.';
end
end
