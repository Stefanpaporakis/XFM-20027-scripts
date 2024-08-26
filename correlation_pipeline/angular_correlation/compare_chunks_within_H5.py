


#Name of this script is self explanitory

import sys
import numpy as np
import matplotlib.pyplot as plt

#don't chage these

maia_start = 138009


group = '75MO_W_P2_1H'
run = 95
H5 = 2
nstart = 400
qslice = 32
maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)
analysis_path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"


#runs = [i for i in range(1,50)]  #LC runs
runs = [1,2,5,20,50]#These are your chunk sizes
ab = ["a","b"]*len(runs)
labels = runs



dlist = []
for i, run in enumerate(runs):
    try: 
        path = analysis_path+"corr_nps"+str(run)+"/"
        data = np.load(path+str(tag)+"_nstart" +str(nstart)+"_h5file"+str(H5)+"_a_correlation_sum.npy")
        print(data.shape)
        dlist.append(data)
    except FileNotFoundError:
        continue
plist = []
for i_data, data in enumerate(dlist):
    p, = plt.plot(np.arange(0,360,2), data[qslice,qslice,:]+0.2*i_data)
    plist.append(p)
plt.title("h5 "+str(H5)+" comparison of chunksizes")
plt.ylabel("Intensity (arb units)")
plt.xlabel(r'q (nm$^{-1}$)')
#plt.yscale("log")
legend = labels
plt.legend(plist,legend, title = "chunksize")
plt.draw()
plt.show()    
