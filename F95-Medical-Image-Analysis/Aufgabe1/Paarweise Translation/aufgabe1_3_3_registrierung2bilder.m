fix_bild = rgb2gray(imread('Pos1.bmp'));
bew_bild = rgb2gray(imread('Pos5.bmp'));

[optimizer, metric] = imregconfig('monomodal');
T = imregtform(bew_bild, fix_bild, 'translation', optimizer, metric);
Rreferenz = imref2d(size(fix_bild)); 
bild_transformiert = imwarp(bew_bild, T, 'OutputView', Rreferenz);
figure

imshowpair(bild_transformiert, fix_bild);
uiwait(msgbox('OK'));
imshow(fix_bild);
uiwait(msgbox('OK'));
imshow(bew_bild);
uiwait(msgbox('OK'));
imshow(bild_transformiert);
optimizer
metric
T.T