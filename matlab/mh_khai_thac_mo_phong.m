function [t, P, t_tuyet_chung] = mh_khai_thac_mo_phong(r, K, H, P0, T)
%MH_KHAI_THAC_MO_PHONG  P' = r P (1 - P/K) - H tren [0, T]. Tich phan DUNG
%   lai khi P cham 0 (su kien tuyet chung, Events voi isterminal = 1), thay
%   vi tiep tuc sang gia tri am vo nghia. t_tuyet_chung = [] neu khong xay ra.
opts = odeset('RelTol', 1e-10, 'AbsTol', 1e-10, 'Events', @cham_khong);
[t, P, te] = ode45(@(t, p) r * p * (1 - p / K) - H, [0 T], P0, opts);
if isempty(te)
    t_tuyet_chung = [];
else
    t_tuyet_chung = te(1);
end
end

function [gia_tri, dung, huong] = cham_khong(~, p)
gia_tri = p;
dung = 1;
huong = -1;
end
