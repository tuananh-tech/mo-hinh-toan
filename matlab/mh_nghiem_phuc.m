function [u1, u2, al, be] = mh_nghiem_phuc(A)
%MH_NGHIEM_PHUC  Hai nghiem THUC cua y' = A y ung voi tri rieng phuc alpha +- i beta
%   (Zill, Dinh ly 8.2.3, tr. 364): v = p + i q la vecto rieng ung voi alpha + i beta,
%   u1(t) = e^{alpha t}(p cos(beta t) - q sin(beta t)),
%   u2(t) = e^{alpha t}(p sin(beta t) + q cos(beta t)).
%   Yeu cau A la ma tran VUONG, THUC, huu han. Truoc khi tra ve, ham KIEM TRA
%   A p = alpha p - beta q va A q = beta p + alpha q (dieu kien de u1, u2 la nghiem)
%   voi dung sai tuong doi; neu khong dat thi bao loi.
if ~(isnumeric(A) && ismatrix(A) && size(A, 1) == size(A, 2) && isreal(A) && all(isfinite(A(:))))
    error('mh_nghiem_phuc:dau_vao', 'A phai la ma tran vuong so thuc huu han.');
end
[V, L] = eig(A);
lam = diag(L);
[~, k] = max(imag(lam));
if imag(lam(k)) <= 0
    error('mh_nghiem_phuc:khong_phuc', 'A khong co tri rieng phuc (phan ao duong).');
end
al = real(lam(k)); be = imag(lam(k));
p = real(V(:, k)); q = imag(V(:, k));
thang = max(1, norm(A, 1)) * max(norm(p, inf), norm(q, inf));
pd = max(norm(A*p - (al*p - be*q), inf), norm(A*q - (be*p + al*q), inf));
if pd > 1e-10 * thang
    error('mh_nghiem_phuc:phan_du', 'Phan du cua cap (p, q) qua lon: %.2e.', pd);
end
u1 = @(t) exp(al*t) * (p*cos(be*t) - q*sin(be*t));
u2 = @(t) exp(al*t) * (p*sin(be*t) + q*cos(be*t));
end
