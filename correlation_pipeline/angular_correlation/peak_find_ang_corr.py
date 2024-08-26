

import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys
import glob
import pathlib 
import scipy.signal as signal

maia_start = 138009

group = '75MO_W_P4_2H'
run = 381
qslice = 32
chunksize = 1 # set chunksize to 1 for full correlation just about
tol = 1e-19
w=0
angle_blur = 0
frame_start = 1
maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)


path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps{chunksize}/"
fulla = np.load(path+f"{tag}_nstart{str(frame_start)}_a_correlation_sum.npy")
fullb = np.load(path+f"{tag}_nstart{str(frame_start)}_b_correlation_sum.npy")

full = fulla+fullb
##full##
f_integrated_slice = np.sum(np.sum(full[qslice-w:qslice+w+1,qslice-w:qslice+w+1,:],0),0)
f_tmp = f_integrated_slice*0.0
for shift in range(-angle_blur,angle_blur+1): f_tmp += np.roll(f_integrated_slice,shift)
f_integrated_slice = f_tmp
plt.plot(np.arange(0,360,2), f_integrated_slice, label = 'full')
plt.draw()
plt.show()
peaks = []
ang_peaks = signal.find_peaks(f_integrated_slice, prominence = 1e-190, width = 0)
for i in ang_peaks[0]:
    peaks.append(i*2)
half = len(peaks)//2
peaks = peaks[:half+1]
print("angular correlation peaks are ",peaks)

    
