function Sinf = mh_sir_quy_mo_cuoi(S0, I0, N, beta, gamma)
%MH_SIR_QUY_MO_CUOI  S_inf: nghiem DUY NHAT trong (0, min(S0, N/R0)) cua
%   g(s) = I0 + S0 - s + (N/R0) ln(s/S0) = 0   (phuong trinh quy mo cuoi).
%   Neu I0 = 0 thi khong co lay nhiem: S_inf = S0 (tra ve truc tiep, tranh
%   chon nghiem sai nhanh). Ngoac nghiem [lo, hi] duoc kiem tra dau truoc khi
%   goi fzero.
if I0 == 0 || beta == 0
    Sinf = S0;
    return
end
Ss = N / (beta / gamma);
g = @(s) I0 + S0 - s + Ss * log(s / S0);
hi = min(S0, Ss);
if ~(g(hi) > 0)
    error('mh_sir_quy_mo_cuoi:ngoac', 'g(can tren) phai duong; kiem tra tham so.');
end
lo = hi;
for k = 1:2000
    lo = lo / 2;
    if g(lo) < 0, break; end
end
if ~(g(lo) < 0)
    error('mh_sir_quy_mo_cuoi:ngoac', 'Khong tim duoc ngoac nghiem.');
end
Sinf = fzero(g, [lo, hi], optimset('TolX', 1e-12));
end
