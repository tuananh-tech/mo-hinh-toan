function P = mh_logistic_chinh_xac(t, P0, r, K, t0)
%MH_LOGISTIC_CHINH_XAC  Nghiem P' = r P (1 - P/K), P(t0) = P0 > 0:
%   P(t) = K P0 / (P0 + (K - P0) exp(-r (t - t0))).  t co the la mang.
if nargin < 5, t0 = 0; end
if ~(P0 > 0 && K > 0), error('mh_logistic_chinh_xac:tham_so', 'Can P0 > 0, K > 0.'); end
P = K * P0 ./ (P0 + (K - P0) .* exp(-r .* (t - t0)));
end
