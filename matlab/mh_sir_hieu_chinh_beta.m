function beta = mh_sir_hieu_chinh_beta(S0, I0, N, gamma, t_qs, I_qs, khoang)
%MH_SIR_HIEU_CHINH_BETA  Tim beta sao cho NGHIEM LIEN TUC thoa I(t_qs) = I_qs
%   (I_qs la so nguoi DANG nhiem). I(t_qs; beta) tang theo beta nen dung
%   fzero tren khoang ngoac `khoang` (mac dinh [0.6, 3]); kiem tra doi dau
%   truoc. Moi lan danh gia giai SIR bang ode45 voi RelTol = 1e-12.
if nargin < 7 || isempty(khoang), khoang = [0.6, 3]; end
opts = odeset('RelTol', 1e-12, 'AbsTol', 1e-12 * N);
I_tai = @(b) gia_tri_I(b, S0, I0, N, gamma, t_qs, opts);
r = @(b) I_tai(b) - I_qs;
if ~(r(khoang(1)) < 0 && r(khoang(2)) > 0)
    error('mh_sir_hieu_chinh_beta:ngoac', 'Khoang tim beta khong chua nghiem.');
end
beta = fzero(r, khoang, optimset('TolX', 1e-12));
end

function I = gia_tri_I(b, S0, I0, N, gamma, t_qs, opts)
[~, Y] = ode45(mh_sir_rhs(b, gamma, N), [0 t_qs], [S0; I0; N - S0 - I0], opts);
I = Y(end, 2);
end
