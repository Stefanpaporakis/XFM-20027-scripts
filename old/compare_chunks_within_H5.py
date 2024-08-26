


#Name of this script is self explanitory

import sys
import numpy as np
import matplotlib.pyplot as plt

#don't chage these

maia_start = 138009


group = '75MO_W_P2_1H'
run = 95
qslice = int(sys.argv[1])
maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)
analysis_path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"
nstart = 1

#runs = [i for i in range(1,50)]  #LC runs
runs = [1,2,5,20,50]#These are your chunk sizes
ab = ["a","b"]*len(runs)
labels = runs



dlist = []
for i, run in enumerate(runs):
    try: 
        path = analysis_path+"corr_nps"+str(run)+"/"
        print(path)
        data = np.load(path+str(tag)+"_nstart" +str(nstart)+"_a_correlation_sum.npy")
        dlist.append(data)
        print(data.shape)
    except FileNotFoundError:
        continue
plist = []
for i_data, data in enumerate(dlist):
    p, = plt.plot(np.arange(0,360,2), data[qslice,qslice,:])#+2*i_data)
    plist.append(p)
#plt.title(title)
plt.ylabel("Intensity (arb units)")
plt.xlabel(r'q (nm$^{-1}$)')
plt.yscale("log")
legend = labels
plt.legend(plist,legend)
plt.draw()
plt.show()    
