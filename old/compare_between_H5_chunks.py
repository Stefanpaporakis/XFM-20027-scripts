
#This script compares H5 chunks BETWEEN H5 files, you set the size of the chunk,
#then you can check if the correlations are the same between H5 files within the 
#same sample. E.g. If H1 chunk 10 looks the same as H2 chunk 10







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
chunksize = 1
h5file = sys.argv[1]
ab = sys.argv[2] #a or b
qslice = 32#int(sys.argv[3])
w=0
angle_blur = 0




maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)
path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps{chunksize}/H5_{h5file}/"
if h5file == 'sums':
    files = sorted(glob.glob(path+"*H*.npy"))
    #For seperate A set and B set, uncomment line below
    #files = sorted(glob.glob(path+"*H" "*_"+ab+"*.npy"))
    slist = []
    for i, filename in enumerate(files):
        fname= filename.split('/')[-1]
        runnumf = fname.split('_sum')[-1]
        #For seperate A set and B set, uncomment line below
        #runnumf = fname.split('_sum')[-2]
        profile = np.load(filename)
       # print("shape is", profile.shape)
        slist.append(profile)
        integrated_slice = np.sum(np.sum(profile[qslice-w:qslice+w+1,qslice-w:qslice+w+1,:],0),0)
        tmp = integrated_slice*0.0
        for shift in range(-angle_blur,angle_blur+1): tmp += np.roll(integrated_slice,shift)
        integrated_slice = tmp
        plt.plot(np.arange(0,360,2), integrated_slice+i*0.2, label = runnumf)
        plt.legend()
    plt.title(group+", "+str(run)+", width = "+str(w)+", Summed h5 files")
    full_out= f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps{chunksize}/H5_sums/"
    fullcorr = sum(slist)
    #np.save(full_out+str(maia_num)+"_"+str(run)+"_nstart400_"+ab+"_full_correlation_sum",fullcorr)
    plt.show()
    exit()
else: 
    split_path = path.split(f'corr_nps{chunksize}/')[-1]
    removelast = split_path.split('/')[-2]
    files = sorted(glob.glob(path+"*_"+ab+"*.npy"))
    print( "Number of files found:", len(files))

    dlist = []
    for i in files:
        profile = np.load(i)
        print("shape is", profile.shape)
        dlist.append(profile)

    plist = []
    plt.figure()
    plt.title(str(group)+" "+str(run)+" "+ab+" H"+h5file)
    for i, (data,file_) in enumerate(zip(dlist,files)):
        #print(i)
        fname= file_.split('/')[-1]
        runnumf = fname.split('_correlation')[-2]
        integrated_slice = np.sum(np.sum(data[qslice-w:qslice+w+1,qslice-w:qslice+w+1,:],0),0)
        tmp = integrated_slice*0.0
        for shift in range(-angle_blur,angle_blur+1): tmp += np.roll(integrated_slice,shift)
        integrated_slice = tmp
        plt.plot(np.arange(0,360,2), integrated_slice+i*0.2, label=runnumf)
        plt.legend()
        plist.append(data)
        if i==0:
             datasum = np.copy(data)
        else:
             datasum += data
    sumout = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps{chunksize}/H5_sums/"
    plt.figure() 
    Sum = sum(plist)
    #np.save(sumout +"H"+h5file+"_"+ab,datasum)
    plt.plot(np.arange(0,360,2), datasum[qslice,qslice,:]) 
    plt.title(str(group)+" "+str(run)+" "+ab+" H"+h5file+"_sum")
    plt.ylabel("Intensity (arb units)")
    plt.xlabel(r'q (nm$^{-1}$)')
#plt.yscale("log"))
#plt.legend(plist, files)
    plt.draw()
    plt.show()    
