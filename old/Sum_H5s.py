

#This script sums the H5s from the product of "compare_angular_lineplots_SP.py"
#Won't work for the chunked data, but I don't think we need to have it for the
#chunked data


import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys
import glob
import pathlib


group = sys.argv[1]
run = int(sys.argv[2])
qslice = int(sys.argv[3])
maia_start = 138009


maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)

path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr/H5_sums/"
files = sorted(glob.glob(path+"*_nstart*.npy"))
dlist = []
for i in files:
    profile = np.load(i)
    #print("shape is", profile.shape)
    dlist.append(profile)
Sum = sum(dlist)
np.save(path+"correlation_sum",Sum)
#plt.plot(Sum)
plt.plot(np.arange(0,360,2), Sum [qslice,qslice,:]) 
plt.title(str(group)+"_"+str(run)+"_full_correlation")
plt.ylabel("Intensity (arb units)")
plt.xlabel(r'q (nm$^{-1}$)')
plt.show()
