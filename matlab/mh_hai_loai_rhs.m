function f = mh_hai_loai_rhs(loai, a, b, m, n)
%MH_HAI_LOAI_RHS  Ve phai cua mo hinh hai loai (Giordano 12.2, 12.3).
%   loai = "canh_tranh":  x' = (a - b y) x,  y' = (m - n x) y
%   loai = "thu_moi"   :  x' = (a - b y) x,  y' = (-m + n x) y   (Lotka-Volterra)
switch char(loai)
    case 'canh_tranh'
        f = @(t, u) [(a - b*u(2))*u(1); (m - n*u(1))*u(2)];
    case 'thu_moi'
        f = @(t, u) [(a - b*u(2))*u(1); (-m + n*u(1))*u(2)];
    otherwise
        error('mh_hai_loai_rhs:loai', 'loai phai la canh_tranh hoac thu_moi.');
end
end
