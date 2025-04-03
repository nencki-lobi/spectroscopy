function timeseries=spec2timeseries(file,method)
%function will read the nifti file using FID-A
%then You can choose to accumulate the whole spetrum (method=0) or
%calculate t2star of subsequent FIDs (method=2)

out = io_loadspec_niimrs(file);
pts=out.averages;

switch method
    case 0
        timeseries=sum(real(out.specs),1);
    case 1
         %not implemented
    case 2
        timeseries=zeros(pts,1);
        for i=1:pts
            timeseries(i)=t2star(out.t'*1000,abs(out.fids(:,i)));
        end
end

%if You are planning to run FFT remeber to demean Your data!
%timeseries=timeseries-mean(timeseries);
end