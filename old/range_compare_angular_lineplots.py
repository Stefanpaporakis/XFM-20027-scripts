

#This script integrates over a q range you select then plots the angular cor.
#Will not show accruate correlations if peak shifts greatly between runs



import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn as sns
#don't chage these
refnum, refrun = 138490, 481
# set data to plot here
analysis_path = "/data/xfm/20027/analysis/eiger/"

# MO:PILs heating series
title = "40DPPC_W heating ang corr"
runs = [i for i in range(100,1000)]  #LC runs
groups = ["40DPPC_W_P6_6H"]*len(runs)
ab = ["a","b"]*len(runs)
labels = [runs]

first = int(sys.argv[1])
last = int(sys.argv[2])

dlist = []
slist = []
for i, run in enumerate(runs):
    try: 
        group = groups[i]
        xfmno = refnum + run - refrun
        tag = str(xfmno)+"_"+str(run) 
        path = analysis_path+group+"/"+tag+"/corr/"
        data = np.load( path+tag+"_nstart400_"+ab[i]+"_correlation_sum.npy")
       # print(data.shape)
        range_q = sum(data[range(first,last),range(first,last),:])
        slist.append(range_q)
        #print(range_q.shape)
        dlist.append(data)
    except FileNotFoundError:
        continue   
plist = []
for i_data, range_q in enumerate(slist):
    p, = plt.plot(np.arange(0,360,2), range_q+10*i_data)
    plist.append(p)
plt.title(title)
plt.ylabel("Intensity (arb units)")
plt.xlabel(r'q (nm$^{-1}$)')
plt.yscale("log")
legend_temps = 30,35,40,45,50,52,54,56,58,60,65,70
#legend_temps = 65,60,58,56,54,50,45,40,35
plt.legend(plist, legend_temps, loc= "upper right")
plt.draw()
plt.show()    
