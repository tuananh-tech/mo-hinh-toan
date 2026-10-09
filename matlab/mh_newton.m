function [w, k, phan_du] = mh_newton(G, DG, w0, tol, maxit)
%MH_NEWTON  Giai G(w) = 0 bang Newton, xuat phat tu w0 (vecto cot).
%   Dung khi ca so gia va phan du deu nho hon dung sai. Neu sau maxit vong
%   chua thoa man thi BAO LOI (khong am tham nhan ket qua).
w = w0(:);
for k = 1:maxit
    r = G(w);
    dw = -(DG(w) \ r);
    w = w + dw;
    phan_du = norm(G(w), inf);
    if norm(dw, inf) <= tol * (1 + norm(w, inf)) && phan_du <= 1e3 * tol * (1 + norm(w, inf))
        return
    end
end
error('mh_newton:khong_hoi_tu', ...
    'Newton khong hoi tu sau %d vong; phan du cuoi %.3e.', maxit, phan_du);
end
