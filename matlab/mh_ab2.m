function [t, Y] = mh_ab2(f, t0, y0, h, T)
%MH_AB2  Adams-Bashforth hai buoc (Burden-Faires (5.33)):
%   w_{i+1} = w_i + h/2 (3 f(t_i, w_i) - f(t_{i-1}, w_{i-1})), i >= 1.
%   Gia tri khoi dong w_1 tinh bang Euler cai tien (cung bac hai).
t = mh_luoi(t0, T, h);
y = mh_chuan_bi(f, t0, y0, 'mh_ab2');
Y = zeros(numel(t), numel(y));
Y(1, :) = y.';
k1 = f(t(1), y);
k2 = f(t(1) + h, y + h * k1);
y = y + h / 2 * (k1 + k2);
Y(2, :) = y.';
f_cu = k1;
for i = 2:numel(t) - 1
    f_moi = f(t(i), y);
    y = y + h / 2 * (3 * f_moi - f_cu);
    f_cu = f_moi;
    mh_kiem_huu_han(y, i, 'mh_ab2');
    Y(i + 1, :) = y.';
end
end
