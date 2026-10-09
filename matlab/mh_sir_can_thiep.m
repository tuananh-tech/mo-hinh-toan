function [t, Y] = mh_sir_can_thiep(S0, I0, N, beta1, beta2, gamma, tc, T)
%MH_SIR_CAN_THIEP  Can thiep tai thoi diem tc: beta1 tren [0, tc], beta2 tren
%   [tc, T]. Tich phan TUNG GIAI DOAN, trang thai tai tc duoc truyen lam
%   dieu kien dau cho giai doan sau (khong ap beta2 cho qua khu).
if ~(tc >= 0 && tc <= T), error('mh_sir_can_thiep:tc', 'Can 0 <= tc <= T.'); end
opts = odeset('RelTol', 1e-10, 'AbsTol', 1e-10 * N);
y0 = [S0; I0; N - S0 - I0];
t = []; Y = [];
if tc > 0
    [t1, Y1] = ode45(mh_sir_rhs(beta1, gamma, N), [0 tc], y0, opts);
    t = t1; Y = Y1; y0 = Y1(end, :)';
end
[t2, Y2] = ode45(mh_sir_rhs(beta2, gamma, N), [tc T], y0, opts);
if tc > 0
    t2 = t2(2:end); Y2 = Y2(2:end, :);   % bo diem tc trung lap
end
t = [t; t2]; Y = [Y; Y2];
end
