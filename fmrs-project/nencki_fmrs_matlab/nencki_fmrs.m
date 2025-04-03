close all

addpath(genpath('/Users/bkossows/Lokalne/MATLAB/FID-A'))

todo=spm_select(inf,'image') %select all nii files eg. phased.nii

% Load design matrix using GUI as a 'desmatrix' of a type 'Numeric Matrix'.

for i=1:4
y=spec2timeseries(todo(i,1:end-2),2);
[b dev stat] = glmfit(desmatrix(:,1:end-1), y);
fprintf('First beta change for %s is:\n %g%%\n',todo(i,:),b(2)*100/b(1));
stat_table=glm_table(stat); %this function is from CanlabCore repo
writetable(stat_table,[todo(i,1:end-6),'_stat'])
end

Xfull = [ones(160,1) desmatrix(:,1:end-1)]; 
Xi = [ones(160,1) desmatrix(:,1)];  
Ki = [ones(160,1) desmatrix(:,2:end-1)];  
fit = Xfull * stat.beta;
fit_task = Xi * stat.beta(1:2);
fit_drift = Ki * stat.beta([1 3:end]);
figure; 
subplot(1, 2, 1); hold on;
plot(y, 'k')
plot(fit, 'b', 'LineWidth', 2)
legend({'Data' 'Fitted (full model)'})
subplot(1, 2, 2); hold on;
plot(fit_drift, 'Color', [.3 .5 .3], 'LineWidth', 2)
plot(fit_task, 'b', 'LineWidth', 2)
legend({'Partial fit (task)' 'Partial fit (HP Filter)'})