function t = mh_luoi(t0, T, h)
%MH_LUOI  Luoi deu t_n = t0 + n*h, n = 0..N, voi t0 + N*h = T CHINH XAC.
%   t = mh_luoi(t0, T, h) tra ve VECTO COT. Neu (T - t0)/h khong nguyen
%   thi bao loi, khong am tham lam tron so buoc (tranh lech thoi diem cuoi).
la_so = @(x) isnumeric(x) && isscalar(x) && isreal(x) && isfinite(x);
if ~(la_so(t0) && la_so(T))
    error('mh_luoi:khoang', 't0 va T phai la so thuc huu han.');
end
if ~(la_so(h) && h > 0)
    error('mh_luoi:buoc', 'Buoc h phai la so thuc duong huu han.');
end
if ~(T > t0)
    error('mh_luoi:khoang', 'Can T > t0.');
end
N = round((T - t0) / h);
if N < 1 || abs(t0 + N*h - T) > 1e-9 * max(1, abs(T))
    error('mh_luoi:khong_chia_het', ...
        '(T - t0)/h = %.6g khong phai so nguyen; hay chon h chia het do dai khoang.', (T - t0)/h);
end
t = t0 + h * (0:N)';
end
