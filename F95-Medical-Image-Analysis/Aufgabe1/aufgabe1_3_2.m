camlist = webcamlist;
cam = webcam(1);
%preview(cam);
x = 0;
%for i = 1:1:10
%    x = x+i;
%    cam.Zoom = i;
%    pause(1);
%end
bild = snapshot(cam);
imshow(bild);
imwrite(bild,'Pos1.bmp')
uiwait(msgbox('Drücken zum schließen der Vorschau'));
clear('cam');
