function kq = mh_phanh(v0, k)
%MH_PHANH  Giam toc deu v' = -k (k > 0) CHI den luc dung t_s = v0/k.
%   kq.t_dung = v0/k; kq.quang_duong = v0^2/(2k);
%   kq.v = @(t) van toc theo mo hinh (bang 0 sau khi xe dung, khong am).
if ~(v0 >= 0 && k > 0)
    error('mh_phanh:dau_vao', 'Can v0 >= 0 va k > 0.');
end
kq.t_dung = v0 / k;
kq.quang_duong = v0^2 / (2 * k);
kq.v = @(t) max(v0 - k * t, 0);
end
