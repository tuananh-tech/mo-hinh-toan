function [r, K, ts, rmse] = mh_khop_logistic(t, P, p0)
%MH_KHOP_LOGISTIC  Binh phuong toi thieu phi tuyen cho P = K/(1+exp(-r(t-ts))):
%   cuc tieu hoa  Phi = sum_i (P_i - K/(1+exp(-r(t_i - ts))))^2.
%   CHI dung MATLAB co ban (fminsearch). Rang buoc r > 0, K > max(P) duoc
%   bao dam bang doi bien r = exp(u1), K = max(P) + exp(u2), ts = u3.
%   p0 = [r0, K0, ts0] (can K0 > max(P)). Neu co Optimization Toolbox, co
%   the dung lsqcurvefit voi rang buoc bien de doi chieu.
t = t(:); P = P(:);
Pmax = max(P);
if nargin < 3 || isempty(p0), p0 = [0.5, 1.2 * Pmax, median(t)]; end
if p0(2) <= Pmax, error('mh_khop_logistic:K0', 'Can K0 > max(P).'); end
du_bao = @(u) (Pmax + exp(u(2))) ./ (1 + exp(-exp(u(1)) .* (t - u(3))));
phi = @(u) sum((du_bao(u) - P).^2);
u0 = [log(p0(1)), log(p0(2) - Pmax), p0(3)];
opt = optimset('TolX', 1e-12, 'TolFun', 1e-12, 'MaxFunEvals', 1e5, 'MaxIter', 1e5);
u = fminsearch(phi, u0, opt);
u = fminsearch(phi, u, opt);      % khoi dong lai mot lan de chac hoi tu
r = exp(u(1)); K = Pmax + exp(u(2)); ts = u(3);
rmse = sqrt(phi(u) / numel(t));
end
