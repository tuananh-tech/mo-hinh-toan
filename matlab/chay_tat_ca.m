function chay_tat_ca()
%CHAY_TAT_CA  Chay toan bo vi du, hinh va bo kiem thu MATLAB cua do an; ghi nhat ky.
%   Cach chay (trong MATLAB, thu muc hien hanh la hoc_lieu/matlab):   >> chay_tat_ca
%   Hoac tu dong lenh (Windows), tu thu muc hoc_lieu/matlab:
%       matlab -sd "%CD%" -batch "chay_tat_ca"
%   Ket qua trong ket_qua_matlab/:
%     nhat_ky_<thoi gian>.txt  : toan bo dau ra (diary), kem phien ban MATLAB, toolbox, thoi gian
%     tom_tat_chay.csv         : tung script: trang thai, thoi gian chay, thong bao loi
%     kiem_chung.csv           : tung kiem tra: gia tri, ky vong, dung sai, dat/khong dat
%     *.png                    : hinh do vd_hinh xuat
%   Mot script loi KHONG dung ca qua trinh; neu co loi, lenh bao loi o cuoi (ma thoat khac 0).
thu_muc = fileparts(mfilename('fullpath'));
thu_muc_kq = fullfile(thu_muc, 'ket_qua_matlab');
if ~exist(thu_muc_kq, 'dir'), mkdir(thu_muc_kq); end
moc = char(datetime('now', 'Format', 'yyyyMMdd_HHmmss'));
tep_nhat_ky = fullfile(thu_muc_kq, ['nhat_ky_' moc '.txt']);
diary(tep_nhat_ky); diary on;
fprintf('=== CHAY_TAT_CA (%s) ===\n', char(datetime('now')));
fprintf('MATLAB %s | %s | %s\n', version, computer, thu_muc);
v = ver;
fprintf('San pham co san: %s\n', strjoin(arrayfun(@(x) [x.Name ' ' x.Version], v, 'UniformOutput', false), '; '));
fprintf('Symbolic Math Toolbox: %s (chi dung cho phan tuy chon cua vd_he_tuyen_tinh)\n\n', ...
    mat2str(~isempty(ver('symbolic'))));
cac_script = {'vd_giai_tich_malthus', 'vd_logistic', 'vd_sir', 'vd_phuong_phap_so', 'vd_cung_ode15s', ...
    'vd_he_tuyen_tinh', 'vd_mo_rong', 'vd_hinh', 'kiem_chung'};
TT = cell(numel(cac_script), 4);
for i = 1:numel(cac_script)
    fprintf('\n################ %s ################\n', cac_script{i});
    tic;
    try
        chay_mot(cac_script{i});
        TT(i, :) = {cac_script{i}, 'DAT', toc, ''};
    catch e
        TT(i, :) = {cac_script{i}, 'LOI', toc, e.message};
        fprintf(2, '[LOI] %s: %s\n', cac_script{i}, e.message);
    end
    close all force;
end
T = cell2table(TT, 'VariableNames', {'script', 'trang_thai', 'giay', 'thong_bao'});
writetable(T, fullfile(thu_muc_kq, 'tom_tat_chay.csv'));
fprintf('\n=== TOM TAT ===\n'); disp(T);
so_loi = sum(strcmp(T.trang_thai, 'LOI'));
fprintf('Nhat ky: %s\n', tep_nhat_ky);
diary off;
if so_loi > 0
    error('chay_tat_ca:loi', '%d script loi (xem tom_tat_chay.csv va nhat ky).', so_loi);
end

end

function chay_mot(ten)
% Chay script trong khong gian lam viec rieng de cac script khong anh huong nhau.
evalin('base', 'clear');
evalin('base', ten);
end
