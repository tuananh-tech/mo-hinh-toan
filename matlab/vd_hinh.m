%VD_HINH  Xuat cac hinh minh hoa bang MATLAB vao ket_qua_matlab/ (PNG).
%   Chay duoc ca khi khong co man hinh (matlab -batch): hinh duoc tao an.
%   Dung exportgraphics (R2020a tro len); neu khong co thi dung print.
thu_muc_kq = fullfile(fileparts(mfilename('fullpath')), 'ket_qua_matlab');
if ~exist(thu_muc_kq, 'dir'), mkdir(thu_muc_kq); end

% 1. SIR: nghiem tham chieu (ode45) va Euler buoc lon
[t, Y] = mh_sir_giai(995, 5, 1000, 1.407, 0.6, 24);
[te, Ye] = mh_euler(mh_sir_rhs(1.407, 0.6, 1000), 0, [995 5 0], 1, 24);
fig = figure('Visible', 'off');
plot(t, Y(:, 2), 'k-', te, Ye(:, 2), 'ko--', 'LineWidth', 1.2);
xlabel('t (tuan)'); ylabel('I (so nguoi dang nhiem)');
legend('ode45 (tham chieu)', 'Euler h = 1 tuan', 'Location', 'northeast'); grid on;
title('SIR: beta = 1.407, gamma = 0.6, N = 1000');
luu_hinh(fig, fullfile(thu_muc_kq, 'sir_euler_tham_chieu.png'));

% 2. Bac hoi tu tren bai toan logistic (thang log-log)
fl = @(t, P) 0.55 * P .* (1 - P / 665); ex = mh_logistic_chinh_xac(10, 9.6, 0.55, 665);
hs = [1 0.5 0.25 0.125]; pp = {@mh_euler, @mh_heun, @mh_diem_giua, @mh_rk4};
ten = {'Euler', 'Heun', 'diem giua', 'RK4'}; kieu = {'ko-', 'ks--', 'k^:', 'kd-.'};
fig = figure('Visible', 'off');
for i = 1:4
    E = zeros(size(hs));
    for j = 1:numel(hs)
        [~, P] = pp{i}(fl, 0, 9.6, hs(j), 10); E(j) = abs(P(end) - ex);
    end
    loglog(hs, E, kieu{i}, 'LineWidth', 1.1); hold on;
end
xlabel('buoc h'); ylabel('sai so tai t = 10'); legend(ten, 'Location', 'southeast'); grid on;
title('Do doc tren thang log = bac hoi tu');
luu_hinh(fig, fullfile(thu_muc_kq, 'bac_hoi_tu.png'));

% 3. Mat phang pha: canh tranh va Lotka-Volterra
fig = figure('Visible', 'off');
subplot(1, 2, 1); hold on;
fc = mh_hai_loai_rhs("canh_tranh", 1, 1, 0.5, 0.5);
opts = odeset('RelTol', 1e-9, 'AbsTol', 1e-11);
for u0 = [0.4 0.3; 2.2 0.4; 0.3 2.0; 2.0 2.4]'
    [~, U] = ode45(fc, [0 6], u0, opts); U = U(all(U < 3.2, 2), :);
    plot(U(:, 1), U(:, 2), 'k-');
end
plot(1, 1, 'ko', 'MarkerFaceColor', 'k'); axis([0 3 0 3]); xlabel('x'); ylabel('y'); title('Canh tranh');
subplot(1, 2, 2); hold on;
fL = mh_hai_loai_rhs("thu_moi", 1, 0.5, 0.75, 0.25);
for x0 = [3.5 4.5 6 7.5]
    [~, U] = ode45(fL, [0 25], [x0; 2], odeset(opts, 'MaxStep', 0.05));
    plot(U(:, 1), U(:, 2), 'k-');
end
plot(3, 2, 'ko', 'MarkerFaceColor', 'k'); xlabel('x (con moi)'); ylabel('y (thu san moi)'); title('Lotka-Volterra');
luu_hinh(fig, fullfile(thu_muc_kq, 'hai_loai.png'));
fprintf('Da xuat 3 hinh vao %s\n', thu_muc_kq);

function luu_hinh(fig, tep)
if exist('exportgraphics', 'file')
    exportgraphics(fig, tep, 'Resolution', 150);
else
    print(fig, tep, '-dpng', '-r150');
end
close(fig);
end
