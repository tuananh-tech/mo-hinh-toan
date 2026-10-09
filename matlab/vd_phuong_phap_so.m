%VD_PHUONG_PHAP_SO  Vi du VD33-VD40 (Phu luc A, muc A.5).  Chay: >> vd_phuong_phap_so
f = @(t, y) 1 + y;
fprintf('--- VD33-VD35 y'' = 1 + y, y(0) = 1, h = 0.1 ---\n');
[~, Ye] = mh_euler(f, 0, 1, 0.1, 0.3);
[~, Yh] = mh_heun(f, 0, 1, 0.1, 0.3);
[~, Ym] = mh_diem_giua(f, 0, 1, 0.1, 0.3);
[~, Yr] = mh_rk4(f, 0, 1, 0.1, 0.3);
disp([Ye Yh Ym Yr 2*exp((0:0.1:0.3)') - 1]);   % cot: Euler Heun Diem giua RK4 Chinh xac

fprintf('--- VD36 bac hoi tu tren bai toan logistic ---\n');
r = 0.55; K = 665; P0 = 9.6;
fl = @(t, P) r * P .* (1 - P / K);
ex = mh_logistic_chinh_xac(10, P0, r, K);
pp = {@mh_euler, @mh_heun, @mh_diem_giua, @mh_rk4};
ten = {'Euler', 'Heun', 'Diem giua', 'RK4'};
hs = [1 0.5 0.25 0.125];
for i = 1:4
    E = zeros(size(hs));
    for j = 1:numel(hs)
        [~, Y] = pp{i}(fl, 0, P0, hs(j), 10);
        E(j) = abs(Y(end) - ex);
    end
    fprintf('%-9s sai so: %s | bac: %s\n', ten{i}, mat2str(E, 4), mat2str(log2(E(1:end-1)./E(2:end)), 3));
end
fprintf('(ky vong bac cuoi: 1.06, 1.95, 1.94, 3.94)\n');

fprintf('--- VD37 on dinh tuyet doi, y'' = -30 y, h = 0.1 ---\n');
z = -3;
Q = [1+z, 1+z+z^2/2, 1+z+z^2/2+z^3/6+z^4/24, 1/(1-z), (1+z/2)/(1-z/2)];
disp(Q);   % ky vong: -2  2.5  1.375  0.25  -0.2
[~, Yi, nv] = mh_euler_an(@(t, y) -30*y, @(t, y) -30, 0, 1/3, 0.1, 1.5);
fprintf('Euler an: y(1.5) = %.4e (3.1044e-10), so vong Newton toi da = %d\n', Yi(end), max(nv));

fprintf('--- VD38 Euler SIR buoc lon ---\n');
fs = mh_sir_rhs(1.407, 0.6, 1000);
for h = [0.5 1 2 3]
    [~, Y] = mh_euler(fs, 0, [995 5 0], h, 30);
    fprintf('h = %.1f: min S = %9.3f, min I = %9.3f, max|tong-1000| = %.1e\n', h, min(Y(:,1)), min(Y(:,2)), max(abs(sum(Y,2)-1000)));
end

fprintf('--- VD39 Taylor bac hai, mot buoc h = 1 ---\n');
df = @(t, P) r * (1 - 2*P/K) .* fl(t, P);
[~, Yt] = mh_taylor2(fl, df, 0, P0, 1, 1);
fprintf('Taylor2 = %.3f (16.193); chinh xac = %.3f (16.465)\n', Yt(end), mh_logistic_chinh_xac(1, P0, r, K));

fprintf('--- VD40 AB2 so voi Heun ---\n');
for h = [0.5 0.25 0.125]
    [~, Ya] = mh_ab2(fl, 0, P0, h, 10);
    [~, Yh] = mh_heun(fl, 0, P0, h, 10);
    fprintf('h = %.3f: AB2 %.3f, Heun %.3f\n', h, abs(Ya(end)-ex), abs(Yh(end)-ex));
end
fprintf('(ky vong: 2.334/4.040, 0.690/1.070, 0.186/0.276)\n');
