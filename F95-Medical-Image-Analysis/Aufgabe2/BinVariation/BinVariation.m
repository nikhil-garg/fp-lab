data = importdata('50.txt', ' ');
data1 = importdata('100.txt', ' ');
data2 = importdata('150.txt', ' ');
data3 = importdata('200.txt', ' ');
data4 = importdata('256.txt', ' ');
scale = data(:,2);

m = data(:,3);
m1 = data1(:,3);
m2 = data2(:,3);
m3 = data3(:,3);
m4 = data4(:,3);

figure
hold on
%yyaxis left
xlabel('Variation Translations-Parameter(3)')
title('Plot 05: MI Metrik bei Variation der Bins')
%Plot 01: CT/CT Parameter[0]
%Plot 02: CT/CT Parameter[3]
%Plot 03: CT/MR Parameter[0]
%Plot 04: CT/MR Parameter[3]

ylabel('Metrik 1: Mutual Information [a.u.]')
plot(scale, m)
plot(scale, m1)
plot(scale, m2)
plot(scale, m3)
plot(scale, m4)
%yyaxis right
%ylabel('Metrik')
%plot(scale, m2)

legend('50Bins','100 Bins','150 Bins','200 Bins', '256 Bins','Location','southwest')



