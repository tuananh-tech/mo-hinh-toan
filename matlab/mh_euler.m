function [t, Y] = mh_euler(f, t0, y0, h, T)
%MH_EULER  Phuong phap Euler tuong minh  y_{n+1} = y_n + h f(t_n, y_n).
%   f   : ham @(t, y) tra ve VECTO COT cung kich thuoc voi y.
%   y0  : dieu kien dau (vecto hang hoac cot; duoc chuyen thanh cot).
%   Ket qua: t (cot, N+1 phan tu), Y (ma tran (N+1) x m, moi HANG la mot
%   trang thai). Moi thanh phan duoc cap nhat DONG THOI tu trang thai cu.
t = mh_luoi(t0, T, h);
y = mh_chuan_bi(f, t0, y0, 'mh_euler');
Y = zeros(numel(t), numel(y));
Y(1, :) = y.';
for n = 1:numel(t) - 1
    y = y + h * f(t(n), y);
    mh_kiem_huu_han(y, n, 'mh_euler');
    Y(n + 1, :) = y.';
end
end
