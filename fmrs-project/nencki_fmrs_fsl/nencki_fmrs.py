
from fsl_mrs.utils import mrs_io
from fsl_mrs.utils import plotting as plot
import pandas as pd
from fsl_mrs.utils import fitting
import fsl_mrs.dynamic as dyn
import numpy as np
import os
from fsl_mrs.utils.preproc import nifti_mrs_proc as proc
#from fsl_mrs.utils.misc import parse_metab_groups


#basic_location - directory to basis set
basis_location = 'fslbasis'


voxel = 'wat3T_4/VWFA'


#data - preprocessed data prepared for dynamic fitting
data = mrs_io.read_FID(voxel + '/fsl_mrs_preproc_fmrs/phased.nii.gz')
design_matrix = pd.read_csv(voxel + '/fsl_suma_r.csv', header=None)

#average data for fitting and inspection
avg_data = proc.average(data,'DIM_DYN')

#do the average fit
mrs0 = avg_data.mrs(basis_file=basis_location)
# Check that the basis has the right phase/frequency convention
mrs0.check_FID(repair=True) #added K.
mrs0.check_Basis(repair=True)

# Select our fitting options
Fitargs = {'ppmlim': (0.0, 6.5),
           'baseline_order': 0,
            'model': 'lorentzian'}

# Run the fitting
res = fitting.fit_FSLModel(mrs0,**Fitargs)

# Plot the result
fig_avgfit = plot.plot_fit(mrs0, res)


# ALl the data this time
mrslist = data.mrs(basis_file=basis_location)
# Check that the basis has the right phase/frequency convention
#for mrs in mrslist:
#    mrs.check_Basis(repair=True)


dobj = dyn.dynMRS(
        mrslist,
        design_matrix,
        config_file='fmrs_model-test.py',
        rescale=True,
        **Fitargs)


dres = dobj.fit()


dres_mean = dobj.fit_mean_spectrum()


#320 metab
list_of_averages = np.arange(0, 160) #TODO automatic size detetion


fig_dynfit = plot.plotly_dynMRS(mrslist, dres.reslist, list_of_averages) #add ,ppmlim=(0, 7) for water


fig_fitmap = dres.plot_mapped()




directory = os.getcwd()
print(directory)
folder = "results"
path = os.path.join(directory, voxel, folder)
print(path)
if not os.path.exists(directory):
    os.mkdir(path)

#figures
fig_avgfit.savefig(path + '/avgfit.png')
fig_dynfit.write_html(path + '/dynfit.html')
fig_fitmap.savefig(path + '/fitmap.png')


dres.cov_free.to_csv(path + '/dyn_cov.csv')


dres._data.to_csv(path + '/dyn_results.csv')


dres._dyn.save(path + '/dynmrs_obj')


pd.concat((dres.mean_free, dres.std_free), axis=1, keys=['mean', 'sd'])\
            .to_csv(path + '/free_parameters.csv')


dres._init_x.to_csv(path + '/init_results.csv')


pd.concat((dres.dataframe_mapped, dres.std_mapped), keys=['mean', 'std'], axis=0)\
            .T\
            .reorder_levels([1, 0], axis=1)\
            .sort_index(axis=1, level=0)\
            .to_csv(path + '/mapped_parameters.csv')

