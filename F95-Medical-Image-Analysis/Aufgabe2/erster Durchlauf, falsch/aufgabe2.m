data = importdata('04-ct-mr-param3.txt', ' ');
scale = data(:,2);
m1 = data(:,3);
m2 = data(:,4);

figure
hold on
yyaxis left
xlabel('Skalierungsfaktor')
title('Plot 04: CT/MR Parameter[3]')
%Plot 01: CT/CT Parameter[0]
%Plot 02: CT/CT Parameter[3]
%Plot 03: CT/MR Parameter[0]
%Plot 04: CT/MR Parameter[3]

ylabel('Metrik 1')
plot(scale, m1)

yyaxis right
ylabel('Metrik 2')
plot(scale, m2)



