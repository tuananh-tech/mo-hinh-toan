function y = mh_chuan_bi(f, t0, y0, ten)
%MH_CHUAN_BI  Kiem tra dau vao chung cho cac ham giai so buoc co dinh.
%   y = mh_chuan_bi(f, t0, y0, ten) kiem tra:
%     - f la function handle;
%     - t0 la so thuc huu han;
%     - y0 la VECTO (hang hoac cot, KHONG phai ma tran) so thuc huu han, khac rong;
%     - f(t0, y0) tra ve VECTO COT so THUC huu han cung so phan tu voi y0.
%   Tra ve y0 dang vecto cot. Bao loi co thong bao (khong am tham lam phang
%   ma tran hay de vecto hang lan truyen thanh ma tran do mo rong ngam).
if ~isa(f, 'function_handle')
    error([ten ':f'], '%s: f phai la function handle dang @(t, y).', ten);
end
if ~(isnumeric(t0) && isscalar(t0) && isreal(t0) && isfinite(t0))
    error([ten ':t0'], '%s: t0 phai la so thuc huu han.', ten);
end
if ~(isnumeric(y0) && isvector(y0) && isreal(y0) && all(isfinite(y0)))
    error([ten ':y0'], ...
        '%s: dieu kien dau y0 phai la VECTO so thuc huu han (nhan duoc kich thuoc %s).', ...
        ten, mat2str(size(y0)));
end
y = y0(:);
f0 = f(t0, y);
if ~(isnumeric(f0) && iscolumn(f0) && numel(f0) == numel(y))
    error([ten ':kich_thuoc'], ...
        '%s: f(t, y) phai tra ve VECTO COT %d x 1 (nhan duoc kich thuoc %s).', ...
        ten, numel(y), mat2str(size(f0)));
end
if ~(isreal(f0) && all(isfinite(f0)))
    error([ten ':gia_tri'], '%s: f(t0, y0) phai la so THUC huu han (co so phuc, NaN hoac Inf).', ten);
end
end
