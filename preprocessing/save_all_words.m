%% To save all the words
    clear; clc;
    % Directory where the the given images are stored
    data_dir = '/Users/mario/Developer/HWR-data/data/image-data/';
    
    % where to save the extracted words
    folder_save = '/Users/mario/Developer/HWR-data/results/word-seg';

    % get the images and the segmented parchments
    disp(['Reading images from path: ', data_dir])
    [imgs, ~] = read_images(data_dir);
    disp(['Done. ', num2str(length(imgs)), ' images were found'])
    imgs = {imgs{1}};
    parchment_only = [];
    for i = 1:length(imgs)
        disp(['Segmenting parchment for image ', num2str(i)]);
        parchment_only{i} = p_segment(imgs{i});
    end
    
    disp('Segmenting words')
    disp('----------------')
    for i = 1:size(parchment_only,2)
        disp(['Parchment #: ' num2str(i)])
        % get all the lines from parchment i
        cur_parchment = parchment_only{i};
        parchment_bin = binarization(cur_parchment, 121, 0.34, 'sauvola');
        bin_lines = line_segmentation2(parchment_bin, parchment_bin*255);
        disp(['   Detected lines: ' num2str(length(bin_lines))])
        for j = 1:size(bin_lines)
            disp(['   Line #: ' num2str(j)])
            % get all word positions from line j in parchment i 
            % line_cur needs to be a binarized line
            line_cur = bin_lines{j};
            rm_background = remove_background_cc(line_cur);
            rm_boundary_noise = remove_boundary_noise(rm_background);
            [r c] = size(rm_boundary_noise);
            add_padding = logical(ones(r,c+250));
            add_padding(:,125:c+124) = rm_boundary_noise; 
            word_positions = word_histogram(add_padding);
            word_start = word_positions(:,1);
            word_indx = word_start > 0;
            word_count = 1;
            disp(['       Detected words: ' num2str(length(word_indx))])
            for k = 1:length(word_indx)
                % save all the words 
                if word_indx(k)
                    baseFileName = sprintf('Parchment#%d_Line#%d_Word#%d.png', i,j,word_count);
                    fullFileName = fullfile(folder_save, baseFileName);
                    word_cur = add_padding(:, word_positions(k,1):word_positions(k,2));
                    imwrite(word_cur, fullFileName);
                    word_count = word_count + 1;
                end
            end
        end
    end

%%


