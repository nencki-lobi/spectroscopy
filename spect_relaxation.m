%spect calibration

%water's relaxation
T1_GM=1820;
T2_GM=100;
T1_WM=1080;
T2_WM=70;
T1_CSF=4160;
T2_CSF=500;

%metabolite's relaxation
T1_M=1400;
T2_M=200;

%tissue types
f_GM=0.3;
f_WM=0.5;
f_CSF=0.2;

%water concentration
C_GM=35880;
C_WM=43300;
C_CSF=55556;

%acquisition
TR=1500;
TE=30;

r=@(t1,t2,tr,te) exp(-te/t2)*(1-exp(-tr/t1));

f=corr_fac(f_GM,f_WM,f_CSF,r(T1_GM,T2_GM,TR,TE),r(T1_WM,T2_WM,TR,TE),r(T1_CSF,T2_CSF,TR,TE),r(T1_M,T2_M,TR,TE),C_GM,C_WM,C_CSF);

%c=s_met/s_wat * N_wat/N_met * f
c=1/35880 * 2/1 * f;

function c=corr_fac(f_GM,f_WM,f_CSF,r_GM,r_WM,r_CSF,R_M,C_GM,C_WM,C_CSF)
c=(f_GM*r_GM*C_GM+f_WM*r_WM*C_WM+f_CSF*r_CSF*C_CSF) / (1-f_CSF) / R_M;
end