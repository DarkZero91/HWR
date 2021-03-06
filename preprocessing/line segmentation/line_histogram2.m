function [ H, baselines, gaps ] = line_histogram2( BW )
% LINE_HISTOGRAM2 Compute the number of black pixels per row
%
%       [ H, baselines, gaps ] = line_segmentation(BW)
%
%       INPUT
%       BW: Binary image (logical class).
%
%       OUTPUT
%       H: counts per row
%       baselines: rows of the maxima
%       gaps: rows of the minima

    H = size(BW,2) - sum(BW, 2);
    
    H = double(H);
    
    %smooth Histogram and find maxima
    H = smooth_signal(H, 30);
    [~, baselines] = findpeaks(H,'MinPeakProminence',15);
    %minima
    Hinv = H*-1;
    [~, gaps] = findpeaks(Hinv,'MinPeakProminence',60);
end

