import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

# Load the data
init = pd.read_csv('init_results.csv') # replace 'filename.csv' with your file name

# Extract column conc_Glu for measurements from 0 to the end
init_glx = init[['conc_NAA','conc_NAAG']].astype(float)
init_glx=init_glx.mean(1)
print(init_glx)
print(init_glx.shape)

# Load your data file
fit = pd.read_csv('mapped_parameters.csv',index_col=0)

# Extract row that contains "conc_Glu"
fit_glu = fit.loc[['conc_NAA','conc_NAAG']].astype(float)
fit_glx=fit_glu.mean(0)[::2]
print(fit_glx.shape)

plt.figure(figsize=(20,3))
plt.scatter(range(len(init_glx)), init_glx, color='blue',s=5) # Plot the first vector as blue points
plt.plot(range(len(fit_glx)),fit_glx.values,color = 'red') # Plot the second vector as a line

plt.show()

# Save the figure
#plt.savefig('dynfit_glu.png', bbox_inches='tight')

