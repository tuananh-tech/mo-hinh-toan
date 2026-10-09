%VD_GIAI_TICH_MALTHUS  Vi du VD01-VD12 (Phu luc A, muc A.1-A.2).
%   Chay:  >> vd_giai_tich_malthus
%   In ra cac so lieu de doi chieu voi luan van (cot "ky vong" lay tu
%   hoc_lieu/ket_qua/kho_vi_du.json, tinh doc lap bang Python).
d = mh_du_lieu();
fprintf('--- VD01 doi don vi ---\n');
fprintf('r/12 = %.4f (ky vong 0.0200); e^0.24 = %.4f (1.2712); ln 1.24 = %.4f (0.2151)\n', ...
    0.24/12, exp(0.24), log(1.24));

fprintf('--- VD04 tich luy ---\n');
fprintf('tich phan = %.2f (1556.93); tong trai = %.2f (1518.33)\n', ...
    120/0.05*(exp(0.5)-1), sum(120*exp(0.05*(0:9))));

fprintf('--- VD05 xap xi tuyen tinh ---\n');
for dt = [1 0.1 0.01]
    fprintf('dt = %5.2f: sai so tuong doi = %.5f %%\n', dt, (exp(0.5*dt)-(1+0.5*dt))/exp(0.5*dt)*100);
end

fprintf('--- VD06 dan so Hoa Ky ---\n');
r = log(d.dan_so.P(2)/d.dan_so.P(1))/20;
du = d.dan_so.P(2)*exp(0.01*10);
fprintf('r = %.6f (0.010102); P(2000) = %.0f (274867059); sai so = %.2f %% (-2.32)\n', ...
    r, du, (du - d.dan_so.P(3))/d.dan_so.P(3)*100);

fprintf('--- VD07, VD08, VD12 ---\n');
fprintf('T_d = %.2f nam (34.66); P(10) = %.0f (2442806)\n', log(2)/0.02, 2e6*exp(0.2));
k = log(2)/4; fprintf('k = %.4f (0.1733); t_1 = %.2f gio (17.29)\n', k, log(20)/k);
fprintf('t_1500 = %.2f nam (36.62)\n', log(3)/0.03);

fprintf('--- VD09 uoc luong r tren 5 diem dau ---\n');
t5 = d.nam_men.t(1:5); P5 = d.nam_men.P(1:5);
[a, c, R2] = mh_hoi_quy(t5, log(P5));
fprintf('hoi quy log: r = %.4f (0.4952), P0 = %.2f (10.39), R2 = %.4f (0.9932)\n', a, exp(c), R2);
fprintf('hai diem: r = %.4f (0.5006)\n', log(P5(5)/P5(1))/4);

fprintf('--- VD10 du bao ngoai mau ---\n');
for ti = [5 6 8 10]
    p = exp(c + a*ti);
    fprintf('t = %2d: du bao %8.1f, quan sat %6.1f, sai so %7.1f %%\n', ti, p, ...
        d.nam_men.P(ti+1), (p - d.nam_men.P(ti+1))/d.nam_men.P(ti+1)*100);
end

fprintf('--- VD11 roi rac -> lien tuc ---\n');
for dt = [1 0.5 0.1 0.01]
    fprintf('dt = %5.2f: (1 + r dt)^n = %.4f\n', dt, (1 + 0.5*dt)^round(4/dt));
end
fprintf('e^2 = %.4f\n', exp(2));
