

#This script compares angular lineplots for fully correlated samples




import numpy as np
import matplotlib.pyplot as plt

#don't chage these
refnum, refrun = 138490, 481
#refnum, refrun = 120773, 178
# set data to plot here
analysis_path = "/data/xfm/20027/analysis/eiger/"


# CholPeg tlc4 - decreasing temp
#title = "CholPeg tlc4"
#runs = [455,492,498,510,528,534,546,576]
#groups = ["tlc4"]*len(runs)
#npat = [200]*len(runs)
#qline = [2.08]*len(runs)
#ab = ["b"]*len(runs)
#labels = [68,56,54,50,44,42,38,28]

# TriFPP tlc4 - decreasing temp
#title = "TriFPP tlc4"
#runs = [494,500,512,530,548]  #LC runs
#groups = ["tlc4"]*len(runs)
#npat = [200]*len(runs)
#qline = [3.15]*len(runs)
#qline2 = [3.15]*len(runs)
#ab = ["b"]*len(runs)
#labels = [56,54,50,44,38]

# DPPC heating series
#title = "50MO_EAN heating ang corr"
#runs = [453,462,471,480,489,498,507,516,525,534,543,552]  #LC runs
#groups = ["50MO_EAN_P6_2H"]*len(runs)
#ab = ["a","b"]*len(runs)
#labels = [30,35,40,45,50,52,54,56,58,60,65,70]

# DPPC cooling series
title = "50MO_EtAN heating ang corr"
runs = [i for i in range(453,561)]  #LC runs
groups = ["50MO_EAN_P6_2H"]*len(runs)
ab = ["a","b"]*len(runs)
labels = [runs]



dlist = []
for i, run in enumerate(runs):
    try: 
        group = groups[i]
        xfmno = refnum + run - refrun
        tag = str(xfmno)+"_"+str(run) 
        path = analysis_path+group+"/"+tag+"/corr/"
        data = np.load( path+tag+"_nstart400_"+ab[i]+"_correlation_sum.npy")
        print(data.shape)
        dlist.append(data)
    except FileNotFoundError:
        continue

plist = []
for i_data, data in enumerate(dlist):
    p, = plt.plot(np.arange(0,360,2), data[31,31,:]+0.1*i_data)
    plist.append(p)
plt.title(title)
plt.ylabel("Intensity (arb units)")
plt.xlabel(r'q (nm$^{-1}$)')
#plt.yscale("log")
legend_temps = 30,35,40,45,50,52,54,56,58,60,65,70
#legend_temps = 60,58,56,54,50,45,40,35
plt.legend(plist, legend_temps)
plt.draw()
plt.show()    
