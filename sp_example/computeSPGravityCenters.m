function spCoord = computeSPGravityCenters(Seg)
Labels = sort(setdiff(unique(Seg(:)),0));
spCoord = zeros(length(Labels),2);
for i = 1:length(Labels)
  [y,x] = find(Seg == Labels(i));
  spCoord(i,:) = [mean(x), mean(y)];
end