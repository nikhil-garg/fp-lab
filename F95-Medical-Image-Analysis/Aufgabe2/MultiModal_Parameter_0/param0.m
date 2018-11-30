data = importdata('256.txt', ' ');
scale = data(:,2);
m1 = data(:,3);
m2 = data(:,4);

figure
hold on
yyaxis left
xlabel('Parameter der Rotation [0]')
title('Plot 03: Multimodal CT/MR Variation Parameter[0]')
%Plot 01: CT/CT Parameter[0]
%Plot 02: CT/CT Parameter[3]
%Plot 03: CT/MR Parameter[0]
%Plot 04: CT/MR Parameter[3]

ylabel('Metrik 1: MU (Mutual Information)')
plot(scale, m1)

yyaxis right
ylabel('Metrik 2: MSD (Mean Squared Difference)')
plot(scale, m2)



