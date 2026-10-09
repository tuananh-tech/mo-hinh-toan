function d = mh_du_lieu()
%MH_DU_LIEU  Du lieu dung trong luan van (giong hoc_lieu/mhtoan/data.py).
%   d.nam_men   : sinh khoi nam men (quan sat), Pearl (1927), trich theo
%                 Giordano-Fox-Horton (2014), Bang 11.1, tr. 466.
%   d.dan_so    : dan so Hoa Ky (quan sat), Giordano et al. (2014), tr. 463.
%   d.cum       : tinh huong cum giao khoa, Giordano et al. (2014), tr. 50-52,
%                 564-565; quy doi beta = a*N cho dang chuan beta*S*I/N.
d.nam_men.t = (0:18)';
d.nam_men.P = [9.6 18.3 29.0 47.2 71.1 119.1 174.6 257.3 350.7 441.0 ...
               513.3 559.7 594.8 629.4 640.8 651.1 655.9 659.6 661.8]';
d.dan_so.nam = [1970; 1990; 2000];
d.dan_so.P   = [203211926; 248710000; 281400000];
d.cum.N = 1000; d.cum.S0 = 995; d.cum.I0 = 5; d.cum.R_bd = 0;
d.cum.a = 0.001407;            % (nguoi.tuan)^-1, dang a*S*I
d.cum.gamma = 0.6;             % tuan^-1
d.cum.beta = d.cum.a * d.cum.N;% 1.407 tuan^-1 (tham so co dinh)
d.cum.I_sau_1_tuan = 9;        % so nguoi DANG nhiem (prevalence)
end
