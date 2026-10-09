function [a, c, R2] = mh_hoi_quy(x, y)
%MH_HOI_QUY  Duong thang binh phuong toi thieu y = a x + c (cong thuc dong).
x = x(:); y = y(:);
xb = mean(x); yb = mean(y);
Sxx = sum((x - xb).^2);
if Sxx == 0, error('mh_hoi_quy:x', 'Cac x khong duoc dong thoi bang nhau.'); end
a = sum((x - xb) .* (y - yb)) / Sxx;
c = yb - a * xb;
R2 = 1 - sum((y - (a * x + c)).^2) / sum((y - yb).^2);
end
