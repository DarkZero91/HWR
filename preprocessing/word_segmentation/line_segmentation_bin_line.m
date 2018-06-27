function seg = line_segmentation_bin_line(BW, R)
% LINE_SEGMENTATION segment hw lines based on baselines only (not gaps)
%
%       seg = line_segmentation2(BW, R)
%
%       INPUT
%       BW: Binary image (logical class)
%       R: Reference image
%
%       OUTPUT
%       seg: cell array of segmented lines in R

    %Fuse background with parchment
    bin_parch = BW;
    BW = remove_cc(BW);
    
    [BW, angle] = rotating_histogram(BW);
    [~, baselines, ~] = line_histogram2(BW);    
    
    R = imrotate(R, angle, 'nearest', 'crop');
    bin_parch = imrotate(bin_parch, angle, 'nearest', 'crop');
    
    assert(length(baselines) >= 2);
    
    seg = cell(length(baselines), 1);
    
    % Segment based on baseline
    for i = 1:length(baselines)
        l = baselines(i);
        
        % Reconstruction for including the ascenders (but no the 'descenders')
        upper_bound = max(1, l-10);
        lower_bound = min(size(BW, 1), l+0);

        S = BW;
        S(1:upper_bound, :) = 255;
        S(lower_bound:end, :) = 255;
        S = ~S;
        BW2 = BW;
%         BW2(lower_bound:end, :) = 255; %prevent reconstruction downwards
        S2 = imreconstruct(S, ~BW2);
        
        %find new bounds
        [rows, ~] = find(S2 == 1);
        rows = sort(rows);
        upper_bound = rows(1);
        lower_bound = rows(end);
    
        seg{i} = bin_parch(upper_bound:lower_bound, :);
    end
end