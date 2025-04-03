close all

addpath(genpath('/Users/bkossows/Lokalne/MATLAB/FID-A'))

%% sampling frequency
TR=4;
F = 1/TR;           % 1/4s=0.25 Hz
f = F .* (0:(160-1))/160; % 0 to 0.25 Hz, 160 points
 

%design matrix
%load as desmatrix array
desmatrix=desmatrix-mean(desmatrix);
ft_desmatrix=abs(fft(desmatrix));

% block=repmat([0,0,0,0,2,2,2,2],1,20)-1;
% block_ft=abs(fft(block));

figure; plot(f, ft_desmatrix, 'LineWidth', 2);
xlabel('Frequency'); ylabel('Power')

%time series
path='wat3T_1/wzrokowa/fsl_mrs_preproc_fmrs'
out = io_loadspec_niimrs(fullfile(path,'phased.nii'));
plot(real(out.specs))

timeseries=sum(real(out.specs),1);
y=timeseries-mean(timeseries);
plot(y)

yf = fft(y);        % Fourier transform
mag = abs(yf);      % Signal magnitude (the real part)

figure; plot(f, mag, 'LineWidth', 2);
xlabel('Frequency'); ylabel('Power')

% figure; plot(f, mag, 'LineWidth', 2); hold on; 
% xlabel('Frequency'); ylabel('Power')
% set(gca, 'XLim', [0 0.1])  


% figure; plot(f, mag, f, block_ft/max(block_ft)*max(mag));
% xlabel('Frequency'); ylabel('Power')
% set(gca, 'XLim', [0 0.1])  

figure; [AX, H1, H2]=plotyy(f, mag, f, ft_desmatrix);
xlabel('Frequency'); ylabel('Power')
xlim(AX,[0,0.1]);
set(H1,'LineWidth',2); set(H2,'LineWidth',2)



figure; 
[mag, f] = periodogram(desmatrix(:,2:end), [], [], 1/TR);
mag = mag ./ max(mag); % normalize r and K magnitudes to same scale so we can see both
plot(f, mag, 'LineWidth', 1);
set(gca, 'XLim', [0 0.02])  
title('HP Filter')



[b dev stat] = glmfit(desmatrix(:,1), y);    % The intercept is added automatically as the first predictor
glm_table(stat, {'Task'});

[b dev stat] = glmfit(desmatrix(:,1:end-1), y);    % The intercept is added automatically as the first predictor
glm_table(stat);

plotyy(1:160,desmatrix,1:160,y)


%%magic

% create design matrices with intercepts to reconstruct fits
% glmfit adds the intercept first, so we will too.
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

timeseries_prplot(y', desmatrix, 1);
title('Partial residual plot for Task');
xlabel('Time (samples)');

timeseries_prplot(y',desmatrix, [2:11]);
title('Partial residual plot for HP Filter (drift)');
xlabel('Time (samples)');


set(gca, 'XLim', [0 0.12]); hold on
[mag, f] = periodogram(y, [], [], 1/TR);
plot(f, mag, 'LineWidth', 1, 'Color', 'k');
[mag, f] = periodogram(fit_task, [], [], 1/TR);
plot(f, mag, 'LineWidth', 1, 'Color', 'b');
[mag, f] = periodogram(fit_drift, [], [], 1/TR);
plot(f, mag, 'LineWidth', 1, 'Color', [.3 .5 .3]);
legend({'Data' 'Fit from task' 'Fit from HPfilter'})


t=out.t'*1000;
fid=abs(out.fids(:,1));
fitfun = @(a,b,c,x) a.*exp(-x./b)+c;
fo = fitoptions('Method','NonlinearLeastSquares','StartPoint',[0.01 100 100]);
[f,goodness] = fit( t, fid, fitfun,fo);
coeffs = coeffvalues(f);
figure; plot(f,t,fid)

fprintf("T2*=%gms\n",coeffs(2))

t2s=zeros(160,1);
for i=1:160
    t2s(i)=t2star(out.t'*1000,abs(out.fids(:,i)));
end

t2s=t2s-mean(t2s);
plotyy(1:160,t2s,1:160,y)

[b dev stat] = glmfit(desmatrix(:,1), t2s);    % The intercept is added automatically as the first predictor
glm_table(stat, {'Task'});
[b dev stat] = glmfit(desmatrix(:,1:end-1), t2s);    % The intercept is added automatically as the first predictor
glm_table(stat);




todo=spm_select(inf,'image')
for i=1:4
y=spec2timeseries(todo(i,1:end-2),2);
[b dev stat] = glmfit(desevent(:,1:end-1), y);
b(2)*100/b(1)
save([todo(i,1:end-6),'_stat'],'y','stat')
%glm_table(stat);
end



    err=err*100/value(i_ref);
    value=value*100/value(i_ref);

    bar([value(i_words),value(i_bacs)])
    errorbar2([value(i_words),value(i_bacs)],[err(i_words),err(i_bacs)])