function [t, Y, so_vong] = mh_hinh_thang_an(f, J, t0, y0, h, T, tol, maxit)
%MH_HINH_THANG_AN  Hinh thang an (Burden-Faires (5.68)-(5.69)):
%   w_{n+1} = w_n + h/2 [f(t_n, w_n) + f(t_{n+1}, w_{n+1})], giai bang Newton.
if nargin < 7 || isempty(tol),   tol = 1e-12; end
if nargin < 8 || isempty(maxit), maxit = 50;  end
t = mh_luoi(t0, T, h);
y = mh_chuan_bi(f, t0, y0, 'mh_hinh_thang_an');
m = numel(y);
Y = zeros(numel(t), m);
Y(1, :) = y.';
so_vong = zeros(numel(t) - 1, 1);
for n = 1:numel(t) - 1
    tn = t(n); tn1 = t(n + 1);
    yn = y;
    fn = f(tn, yn);
    G  = @(w) w - yn - h / 2 * (fn + f(tn1, w));
    DG = @(w) eye(m) - h / 2 * J(tn1, w);
    [y, so_vong(n)] = mh_newton(G, DG, yn, tol, maxit);
    mh_kiem_huu_han(y, n, 'mh_hinh_thang_an');
    Y(n + 1, :) = y.';
end
end
