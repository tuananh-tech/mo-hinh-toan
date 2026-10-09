function [t, Y, so_vong] = mh_euler_an(f, J, t0, y0, h, T, tol, maxit)
%MH_EULER_AN  Euler an: w_{n+1} = w_n + h f(t_{n+1}, w_{n+1}).
%   Moi buoc giai G(w) = w - w_n - h f(t_{n+1}, w) = 0 bang Newton voi
%   G'(w) = I - h J(t_{n+1}, w); J(t, y) la ma tran Jacobi cua f theo y.
if nargin < 7 || isempty(tol),   tol = 1e-12; end
if nargin < 8 || isempty(maxit), maxit = 50;  end
t = mh_luoi(t0, T, h);
y = mh_chuan_bi(f, t0, y0, 'mh_euler_an');
m = numel(y);
Y = zeros(numel(t), m);
Y(1, :) = y.';
so_vong = zeros(numel(t) - 1, 1);
for n = 1:numel(t) - 1
    tn1 = t(n + 1);
    yn = y;
    G  = @(w) w - yn - h * f(tn1, w);
    DG = @(w) eye(m) - h * J(tn1, w);
    [y, so_vong(n)] = mh_newton(G, DG, yn, tol, maxit);
    mh_kiem_huu_han(y, n, 'mh_euler_an');
    Y(n + 1, :) = y.';
end
end
