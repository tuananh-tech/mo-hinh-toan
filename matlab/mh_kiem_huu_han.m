function mh_kiem_huu_han(y, n, ten)
%MH_KIEM_HUU_HAN  Bao loi neu nghiem so tai buoc n khong con la vecto cot so
%   thuc huu han (thuong do mat on dinh: buoc h qua lon, bai toan cung; hoac do
%   ve phai sinh so phuc / doi kich thuoc).
if ~iscolumn(y)
    error([ten ':kich_thuoc'], '%s: trang thai tai buoc %d khong con la vecto cot (kich thuoc %s).', ...
        ten, n, mat2str(size(y)));
end
if ~(isreal(y) && all(isfinite(y)))
    error([ten ':khong_huu_han'], ...
        '%s: nghiem so khong con la so thuc huu han tai buoc %d; hay giam h hoac dung phuong phap an.', ten, n);
end
end
