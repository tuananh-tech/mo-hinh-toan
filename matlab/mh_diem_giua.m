function [t, Y] = mh_diem_giua(f, t0, y0, h, T)
%MH_DIEM_GIUA  Phuong phap diem giua (Burden-Faires tr. 286):
%   y_{n+1} = y_n + h f(t_n + h/2, y_n + h/2 f(t_n, y_n)).
%   Day KHONG phai phuong phap Heun/Euler cai tien.
t = mh_luoi(t0, T, h);
y = mh_chuan_bi(f, t0, y0, 'mh_diem_giua');
Y = zeros(numel(t), numel(y));
Y(1, :) = y.';
for n = 1:numel(t) - 1
    k1 = f(t(n), y);
    y = y + h * f(t(n) + h / 2, y + h / 2 * k1);
    mh_kiem_huu_han(y, n, 'mh_diem_giua');
    Y(n + 1, :) = y.';
end
end
