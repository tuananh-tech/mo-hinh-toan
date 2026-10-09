function [t, Y, t_dinh, I_dinh] = mh_sir_giai(S0, I0, N, beta, gamma, T, R_bd)
%MH_SIR_GIAI  Nghiem tham chieu SIR bang ode45 voi dung sai nghiem ngat.
%   Kiem tra dau vao: N > 0; S0, I0 >= 0; beta >= 0; gamma > 0; T > 0. Neu
%   KHONG truyen R_bd thi R_bd = N - S0 - I0 (phai >= 0). Neu CO truyen R_bd
%   thi bat buoc S0 + I0 + R_bd = N (sai lech tuong doi <= 1e-9): ve phai dung
%   N trong beta*S*I/N, nen tong khac N lam mo hinh mau thuan.
%   Su kien dinh dich: S - N/R0 = 0 (huong giam), CHI dung khi co dinh noi
%   tai (I0 > 0 va R0*S0/N > 1). Neu khong co dinh noi tai, t_dinh = [] va cuc
%   dai cua I la I0 tai t = 0. Neu su kien khong xay ra trong [0, T], t_dinh = []
%   va co canh bao. Ghi chu: dung sai cua bo giai kiem soat sai so DIA PHUONG
%   uoc luong; luon doi chieu them voi I_max giai tich (mh_sir_dinh_dich).
la_so = @(x) isnumeric(x) && isscalar(x) && isreal(x) && isfinite(x);
if ~all(cellfun(la_so, {S0, I0, N, beta, gamma, T}))
    error('mh_sir_giai:dau_vao', 'S0, I0, N, beta, gamma, T phai la so thuc huu han.');
end
if ~(N > 0 && S0 >= 0 && I0 >= 0 && beta >= 0 && gamma > 0 && T > 0)
    error('mh_sir_giai:dau_vao', 'Can N > 0, S0 >= 0, I0 >= 0, beta >= 0, gamma > 0, T > 0.');
end
if nargin < 7 || isempty(R_bd)
    R_bd = N - S0 - I0;
    if R_bd < -1e-9 * N
        error('mh_sir_giai:tong', 'S0 + I0 = %g vuot qua N = %g.', S0 + I0, N);
    end
    R_bd = max(R_bd, 0);   % chi xoa sai so lam tron cap 1e-9 N, khong cat gia tri am that
else
    if ~(la_so(R_bd) && R_bd >= 0)
        error('mh_sir_giai:dau_vao', 'R_bd phai la so thuc khong am.');
    end
    if abs(S0 + I0 + R_bd - N) > 1e-9 * N
        error('mh_sir_giai:tong', 'S0 + I0 + R_bd = %g khac N = %g.', S0 + I0 + R_bd, N);
    end
end
R0 = beta / gamma;
co_dinh = (I0 > 0) && (R0 * S0 / N > 1);
opts = odeset('RelTol', 1e-10, 'AbsTol', 1e-10 * N);
if co_dinh
    opts = odeset(opts, 'Events', @(t, y) su_kien_dinh(t, y, N / R0));
end
[t, Y, te, ye] = ode45(mh_sir_rhs(beta, gamma, N), [0 T], [S0; I0; R_bd], opts);
t_dinh = []; I_dinh = [];
if co_dinh
    if isempty(te)
        warning('mh_sir_giai:chua_den_dinh', ...
            'Dinh dich chua xay ra trong [0, %g]; hay tang T.', T);
    else
        t_dinh = te(1); I_dinh = ye(1, 2);
    end
end
end

function [gia_tri, dung, huong] = su_kien_dinh(~, y, S_sao)
gia_tri = y(1) - S_sao;   % I' = 0 khi S = N/R0
dung = 0;                 % khong dung tich phan
huong = -1;               % S giam qua S*
end
