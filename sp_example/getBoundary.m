function boundary = getBoundary(seg,sp)
% returns the boundary of an indicated sp.
% seg: an array of the same size as the original image, entries being sp
% indices
% sp: an integer specifying the superpixel for which to calculate the
% boundary

seg(seg~=sp) = 0;
bdTemp = gradient(seg);
bdTemp(bdTemp~=0) = 1;
[bdY,bdX] = find(bdTemp~=0);
boundary = [bdX,bdY];

