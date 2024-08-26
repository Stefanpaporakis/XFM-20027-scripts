
#This script compares full correlated H5 files. 
#Have to run compare_summed first



import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys
import glob
import pathlib 


maia_start = 138009
group = '75MO_W_P4_2H'
run = 381
qslice = 32 #int(sys.argv[1])
w=0
angle_blur = 0


maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)



path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"
files = sorted(glob.glob(path+"*correlation_sum.npy"))

for i,filename in enumerate(files):
    #fname= filename.split('nps')[-1]
    #fname = fname.split('_fullcorr')[-2]
    profile = np.load(filename)
    plt.plot(np.arange(0,360,2), profile[qslice,qslice,:]-i*8,) #label = fname) 
plt.title(group+", "+str(run)+" chunked full correlation")
plt.legend(loc=  'upper right')
plt.show()   


