function [v2, u1, u2] = mh_jordan2(A, lam, v1)
%MH_JORDAN2  Chuoi Jordan do dai 2: (A - lam I) v1 = 0, (A - lam I) v2 = v1;
%   nghiem e^{lam t} v1 va e^{lam t}(t v1 + v2).
%   Kiem tra: A vuong thuc huu han; lam so thuc; v1 la vecto KHAC 0 cung kich thuoc
%   (vecto rieng luon khac 0); (A - lam I) v1 = 0 voi dung sai tuong doi. Vi
%   (A - lam I) suy bien nen v2 duoc tim bang binh phuong toi thieu (pinv) roi
%   KIEM TRA phan du (A - lam I) v2 - v1 = 0 voi dung sai tuong doi; neu
%   khong dat (v1 khong thuoc anh cua A - lam I) thi bao loi.
if ~(isnumeric(A) && ismatrix(A) && size(A, 1) == size(A, 2) && isreal(A) && all(isfinite(A(:))))
    error('mh_jordan2:dau_vao', 'A phai la ma tran vuong so thuc huu han.');
end
if ~(isnumeric(lam) && isscalar(lam) && isreal(lam) && isfinite(lam))
    error('mh_jordan2:dau_vao', 'lam phai la so thuc huu han.');
end
n = size(A, 1);
if ~(isnumeric(v1) && isvector(v1) && numel(v1) == n && isreal(v1) && all(isfinite(v1)))
    error('mh_jordan2:dau_vao', 'v1 phai la vecto thuc huu han co %d phan tu.', n);
end
v1 = v1(:);
if norm(v1, inf) == 0
    error('mh_jordan2:vecto_khong', 'v1 = 0 khong phai vecto rieng (vecto rieng luon khac 0).');
end
B = A - lam * eye(n);
thang = max(1, norm(B, 1)) * norm(v1, inf);
if norm(B * v1, inf) > 1e-10 * thang
    error('mh_jordan2:vecto_rieng', 'v1 khong phai vecto rieng ung voi lam (phan du %.2e).', norm(B*v1, inf));
end
v2 = pinv(B) * v1;
if norm(B * v2 - v1, inf) > 1e-10 * thang
    error('mh_jordan2:khong_giai_duoc', ...
        'Khong giai duoc (A - lam I) v2 = v1 (phan du %.2e): lam co the co du vecto rieng.', norm(B*v2 - v1, inf));
end
u1 = @(t) exp(lam*t) * v1;
u2 = @(t) exp(lam*t) * (t*v1 + v2);
end
