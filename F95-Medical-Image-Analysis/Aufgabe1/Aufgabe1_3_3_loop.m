files = dir('*.bmp');
for file2 = files'
    ref_bild = rgb2gray(imread(file2.name));
%ref_bild = rgb2gray(imread('Pos1.bmp'));
    for file = files'
        bew_bild = rgb2gray(imread(file.name));
        [optimizer, metric] = imregconfig('monomodal');
        T = imregtform(bew_bild, ref_bild, 'translation', optimizer, metric);
        Rreferenz = imref2d(size(ref_bild)); 
        bild_transformiert = imwarp(bew_bild, T, 'OutputView', Rreferenz);
        %figure
        %bildpair = [bild_transformiert, ref_bild];
        %imshowpair(bildpair,'diff');
        %uiwait(msgbox(file.name));
        %imwrite(bild,)
        %imshowpair(bild_transformiert, ref_bild);
        %imwrite(obj, 'overlay.bmp')
        disp(['Matrix von ', file2.name, ' mit ',file.name]);
        T.T
    end
end
