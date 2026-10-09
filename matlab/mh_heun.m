function [t, Y] = mh_heun(f, t0, y0, h, T)
%MH_HEUN  Euler cai tien (Heun, hinh thang tuong minh; "Modified Euler" cua
%   Burden-Faires):  k1 = f(t_n, y_n), k2 = f(t_n + h, y_n + h k1),
%   y_{n+1} = y_n + h/2 (k1 + k2).  Xem mh_euler ve quy uoc dau vao/ra.
t = mh_luoi(t0, T, h);
y = mh_chuan_bi(f, t0, y0, 'mh_heun');
Y = zeros(numel(t), numel(y));
Y(1, :) = y.';
for n = 1:numel(t) - 1
    k1 = f(t(n), y);
    k2 = f(t(n) + h, y + h * k1);
    y = y + h / 2 * (k1 + k2);
    mh_kiem_huu_han(y, n, 'mh_heun');
    Y(n + 1, :) = y.';
end
end
