function [t, Y] = mh_taylor2(f, df, t0, y0, h, T)
%MH_TAYLOR2  Taylor bac hai (Burden-Faires (5.17), n = 2):
%   y_{n+1} = y_n + h f(t_n, y_n) + h^2/2 * df(t_n, y_n),
%   trong do df(t, y) = f_t + f_y f la dao ham toan phan cua f doc nghiem
%   (nguoi dung cung cap; voi he thi f_y la ma tran Jacobi).
t = mh_luoi(t0, T, h);
y = mh_chuan_bi(f, t0, y0, 'mh_taylor2');
Y = zeros(numel(t), numel(y));
Y(1, :) = y.';
for n = 1:numel(t) - 1
    y = y + h * f(t(n), y) + h^2 / 2 * df(t(n), y);
    mh_kiem_huu_han(y, n, 'mh_taylor2');
    Y(n + 1, :) = y.';
end
end
