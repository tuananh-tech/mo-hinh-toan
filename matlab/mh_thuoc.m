function kq = mh_thuoc(C0, k, T, n)
%MH_THUOC  Lieu thuoc lap lai (MINH HOA TOAN HOC, khong phai huong dan dung thuoc).
%   Giua hai lieu C' = -k C; moi T gio mot lieu lam nong do tang TUC THOI them C0.
%   kq.R_n  : nong do du ngay truoc lieu thu n+1 = C0 e^{-kT}(1 - e^{-nkT})/(1 - e^{-kT})
%   kq.R    : gioi han (trang thai on dinh) = C0/(e^{kT} - 1)
if ~(C0 > 0 && k > 0 && T > 0 && n >= 1 && n == fix(n))
    error('mh_thuoc:dau_vao', 'Can C0, k, T > 0 va n nguyen >= 1.');
end
q = exp(-k * T);
kq.R_n = C0 * q * (1 - q^n) / (1 - q);
kq.R = C0 / expm1(k * T);
end
