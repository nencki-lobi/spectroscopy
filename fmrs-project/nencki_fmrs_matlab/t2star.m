function val=t2star(t,y)
fitfun = @(a,b,c,x) a.*exp(-x./b)+c;
fo = fitoptions('Method','NonlinearLeastSquares','StartPoint',[0.01 100 100]);
warning off
[f,goodness] = fit( t, y, fitfun,fo);
warning on
coeffs = coeffvalues(f);
val=coeffs(2);
end
