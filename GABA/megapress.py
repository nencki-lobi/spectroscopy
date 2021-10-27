#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import suspect
import subprocess
import re
import sys
import os


pfile=sys.argv[1]
folder=os.path.dirname(os.path.abspath(pfile))
print(pfile)


data, wref = suspect.io.load_pfile(pfile)


# In[3]:


data.shape


# In[4]:


noise_points = 1024
noise = wref[:, :, -noise_points:]
noise = np.moveaxis(noise, -2, 0).reshape((8, -1))
plt.imshow(np.cov(noise).real)


# In[5]:


white_wref = suspect.processing.channel_combination.whiten(wref, noise)
white_data = suspect.processing.channel_combination.whiten(data, noise)
# just to demonstrate that this does remove all correlations
white_noise = white_data[:, :, :, -noise_points:]
white_noise = np.moveaxis(white_noise, -2, 0).reshape((8, -1))
plt.imshow(np.cov(white_noise).real)


# In[6]:


channel_weights = suspect.processing.channel_combination.svd_weighting(white_wref, axis=-2)


# In[7]:


cc_wref = suspect.processing.channel_combination.combine_channels(white_wref, channel_weights)
cc_data = suspect.processing.channel_combination.combine_channels(white_data, channel_weights)


# In[8]:


plt.plot(cc_wref.frequency_axis_ppm(), cc_data[0, 0].spectrum().real)
plt.plot(cc_wref.frequency_axis_ppm(), cc_data[0, 1].spectrum().real)
plt.xlim(plt.xlim()[::-1])


# In[9]:


def correct_frequency_sr(target):
    def correct_fid(fid):
        frequency_shift, phase_shift = suspect.processing.frequency_correction.spectral_registration(fid, target)
        return fid.adjust_frequency(-frequency_shift).adjust_phase(-phase_shift)
    return correct_fid


# In[10]:


sr_on = np.apply_along_axis(correct_frequency_sr(cc_data[0, 0]), 1, cc_data[0])
sr_off = np.apply_along_axis(correct_frequency_sr(cc_data[1, 0]), 1, cc_data[1])


# In[11]:


sr_wref = np.apply_along_axis(correct_frequency_sr(cc_wref[0]), 1, cc_wref)


# In[12]:


wref_final = np.mean(sr_wref, axis=0)


# In[13]:


on_final = np.mean(sr_on, axis=0)
off_final = np.mean(sr_off, axis=0)


# In[14]:


global_frequency_shift, global_phase_shift = suspect.processing.frequency_correction.spectral_registration(on_final,
                                                                                                               off_final)
off_final_corrected = off_final.adjust_frequency(global_frequency_shift).adjust_phase(global_phase_shift)

diff = on_final - off_final_corrected

#LCMODEL

params = {
    "FILBAS": "/home/jovyan/work/GABA/gamma_press_te68_3t_v1.basis",
    "key": 210387309,
    "OWNER": (pfile + " by Bartosz Kossowski, Nencki Institute"),
    "LCSV": 11,
    "LCOORD": 9,
    "LPRINT": 6,
    "ATTH2O": 1
}
suspect.io.lcmodel.write_all_files(os.path.join(folder,'lcmodel','off.RAW'), data=off_final_corrected, wref_data=wref_final, params=params)


# In[43]:


myinput = open(os.path.join(folder,'lcmodel','off_sl0.CONTROL'))
result = subprocess.run("/home/jovyan/.lcmodel/bin/lcmodel",stdin=myinput,stdout=subprocess.PIPE)
subprocess.run(["ps2pdf",os.path.join(folder,'lcmodel','off.PS'),os.path.join(folder,'lcmodel','off.PDF')])
#print(result.stdout.decode())
lprint=result.stdout.decode()


# In[44]:


fcalibs=re.findall(r'FCALIB\s*=\s*(.+)',lprint)
print(fcalibs)
fcalib=(float(fcalibs[1]))


# In[45]:


params = {
    "FILBAS": "/home/jovyan/work/GABA/mega-press.basis",
    "key": 210387309,
    "OWNER": (pfile + " by Bartosz Kossowski, Nencki Institute"),
    "SPTYPE": "mega-press-3",
    "NCOMBI": 17,
    "CHCOMB(2)": "GABA_A+GABA_B",
    "LCSV": 11,
    "LCOORD": 9,
    "FCALIB": fcalib*1e4,
    "ATTH2O": 1
    #"LPRINT": 6
}
suspect.io.lcmodel.write_all_files(os.path.join(folder,'lcmodel','diff.RAW'), data=diff, wref_data=wref_final, params=params)


# In[46]:


myinput = open(os.path.join(folder,'lcmodel','diff_sl0.CONTROL'))
result = subprocess.run("/home/jovyan/.lcmodel/bin/lcmodel",stdin=myinput,stdout=subprocess.PIPE)
subprocess.run(["ps2pdf",os.path.join(folder,'lcmodel','diff.PS'),os.path.join(folder,'lcmodel','diff.PDF')])






