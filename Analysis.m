clc; clear all; close all; 
filename1 = 'none_1.csv';
S1 = importdata(filename1, ',');
data_none = S1.data;
filename2 = 'swap_1.csv';
S2 = importdata(filename2, ',');
data_swap = S2.data;
% filename3 = 'expand_1.csv';
% S3 = importdata(filename3, ',');
% data_expand = S3.data;
t_value = zeros(1,8);
samp = zeros(1,8);

for x = 10:10:80
data_none_new = data_none(1:x, 6:end);
data_swap_new = data_swap(1:x, 5:end);
%data_expand = data_expand(1:x, 5:end);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                       %
% set y-value as needed: 1:80 2:90 3:95 %                              
%                                       %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

y = 1;

ts_none = data_none_new(:, y);
[N1 ~] = size(ts_none(ts_none>0));


ts_swap = data_swap_new(:, y);
[M1 ~] = size(ts_swap(ts_swap>0));

%ts_expand = data_expand(:, y);
%[M1 ~] = size(ts_expand(ts_expand>0));


mean_none = nanmean(ts_none);
mean_swap = nanmean(ts_swap);
% mean_expand = nanmean(ts_expand);

std_none = nanstd(ts_none);
std_swap = nanstd(ts_swap);
% std_expand = nanstd(ts_expand);

pooled_var_sq = ((N1-1)*(std_none^2) + (M1-1)*(std_swap^2))/(N1+M1-2);
%pooled_var_sq = ((N1-1)*(std_none^2) + (M1-1)*(std_expand^2))/(N1+M1-2);
SE = sqrt((pooled_var_sq)*((1/N1) + (1/M1)));
i = x/10;
samp(i) = x;
t_value(i) = (mean_none-mean_swap)/(SE);
dof = N1+M1 - 2;

end

plot(samp, t_value)
xlabel('# of samples')
ylabel('t-value')
title('# of samples vs t-value')