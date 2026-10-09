function kq = mh_sir_dinh_dich(S0, I0, N, beta, gamma)
%MH_SIR_DINH_DICH  Dinh cua I(t) tren [0, inf) theo Dinh ly nguong.
%   Neu R0*S0/N <= 1 (hoac I0 = 0) thi KHONG co dinh noi tai: cuc dai dat
%   tai t = 0. Nguoc lai I_max = I0 + S0 - S* - S* ln(S0/S*), S* = N/R0.
R0 = beta / gamma;
kq.R0 = R0;
kq.R_eff_0 = R0 * S0 / N;
if I0 == 0 || R0 * S0 / N <= 1
    kq.noi_tai = false;
    kq.I_max = I0;
    kq.S_tai_dinh = S0;
else
    Ss = N / R0;
    kq.noi_tai = true;
    kq.I_max = I0 + S0 - Ss - Ss * log(S0 / Ss);
    kq.S_tai_dinh = Ss;
end
end
