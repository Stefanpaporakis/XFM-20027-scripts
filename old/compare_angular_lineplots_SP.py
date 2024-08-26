

#This script compares angular lineplots WITHIN H5 files over a number of patterns,
#not chunks. It will tell you if you sample is changing within H5 files


#If you set h5file to "sums", it will sum the individual H5 file so you can
#then tell the difference BETWEEN H5 files. Need to first run it over each
#H5 file and there a and b sets first to do so.





import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys
import glob
import pathlib 


maia_start = 138009

group = sys.argv[1]
run = int(sys.argv[2])
h5file = sys.argv[3]
ab = sys.argv[4] #a or b
qslice = int(sys.argv[5])



maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)

path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr/H5_{h5file}/"
if h5file == 'sums':
    #files = sorted(glob.glob(path+"*H*.npy"))
    files = sorted(glob.glob(path+"*H" "*_"+ab+"*.npy"))
    slist = []
    for i, filename in enumerate(files):
        fname= filename.split('/')[-1]
        runnumf = fname.split('_sum')[-2]
        profile = np.load(filename)
       # print("shape is", profile.shape)
        slist.append(profile)
        plt.plot(np.arange(0,360,2), profile[qslice,qslice,:]+i*0.2, label = runnumf)
        plt.legend()
    plt.title(group+"_"+str(run)+"_Summed_"+ab+"_h5 files")
    full_out= f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr/H5_sums/"
    fullcorr = sum(slist)
    np.save(full_out+str(maia_num)+"_"+str(run)+"_nstart400_"+ab+"_full_correlation_sum",fullcorr)
    plt.show()
    exit()
else: 
    split_path = path.split('corr/')[-1]
    removelast = split_path.split('/')[-2]
    files = sorted(glob.glob(path+"*_"+ab+"*.npy"))

    dlist = []
    for i in files:
        profile = np.load(i)
        #print("shape is", profile.shape)
        dlist.append(profile)

    plist = []
    plt.figure()
    plt.title(str(group)+"_"+str(run)+"_"+"H"+h5file)
    for i, (data,file_) in enumerate(zip(dlist,files)):
        fname= file_.split('/')[-1]
        runnumf = fname.split('_correlation')[-2]
        plt.plot(np.arange(0,360,2), data[qslice,qslice,:]+i*0.2, label=runnumf)
        plt.legend()
        plist.append(data)
    sumout = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr/H5_sums/"
    plt.figure() 
    Sum = sum(plist)
    np.save(sumout +"H"+h5file+"_"+ab+"_sum",Sum)
    plt.plot(np.arange(0,360,2), Sum[qslice,qslice,:]) 
    plt.title(str(group)+"_"+str(run)+"_"+"H"+h5file+"_sum")
    plt.ylabel("Intensity (arb units)")
    plt.xlabel(r'q (nm$^{-1}$)')
#plt.yscale("log"))
#plt.legend(plist, files)
    plt.draw()
    plt.show()    
