import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys
from scipy.signal import find_peaks


#don't chage these##########
refnum, refrun = 138490, 481
############################

dataset = "75MO_W_P4_2H"
runs = [i for i in range(380,394)]  #LC runs
groups = [dataset]*len(runs)
ab = ["a","b"]*len(runs)


#set tolerance of peak hunting
tol = 2

sc, scl = 0.15, 0.15
rmax =  128 #128
w = 0
rline = 35 
nstart = 400

datapath = f"/data/xfm/20027/analysis/eiger/"
outpath = f"/data/xfm/20027/analysis/eiger/{dataset}/"
open(outpath+'peak_list.txt', 'w+').close()


for i, run in enumerate(runs):
    try: 
        group = groups[i]
        xfmno = refnum + run - refrun
        tag = str(xfmno)+"_"+str(run) 
        #path = datapath+group+"/"+tag+"/corr/"
        #THIS PATH FOR CHUNKED DATA
        path = datapath+group+"/"+tag+"/corr_nps1/"
        #path = datapath+group+"/"+tag+"/corr/" #Bg run

#load A set
       # Afname = path+tag+"_nstart" +str(nstart)+"_a_correlation_sum.npy"
       # dataA = np.load(Afname)
        #load A set
        Afname = path+tag+"_nstart" +str(nstart)+"_a_correlation_sum.npy"
        #Afname = path+tag+"_a_correlation_sum.npy" # Bg run
        #print(Afname)
        dataA = np.load(Afname)

#load B set
        Bfname = path+tag+"_nstart" +str(nstart)+"_b_correlation_sum.npy"
        #Bfname = path+tag+"_b_correlation_sum.npy" # Bg run
        dataB = np.load(Bfname)
        
        irline = int(dataA.shape[0]*rline/rmax)
        dispA = np.zeros( (dataA.shape[0], dataA.shape[2]) )
        dispB = np.zeros( (dataB.shape[0], dataB.shape[2]) )
        dlineA = np.zeros( dataA.shape[2] )
        dlineB = np.zeros( dataB.shape[2] )
        tmpA = dataA*0.
        tmpB = dataB*0.
        ith = 1 # this crops from the left
        thmin = (ith/360)*dataA.shape[2]
        for i in np.arange(dataA.shape[0]):
            for j in np.arange(dataA.shape[1]):
                tmpA[i,j,:] = dataA[i,j,:] - 1*np.average(dataA[i,j,ith:-ith])

        for i in np.arange(dataB.shape[0]):
            for j in np.arange(dataB.shape[1]):
                tmpB[i,j,:] = dataB[i,j,:] - 1*np.average(dataB[i,j,ith:-ith])
        pw = 0
        for i in np.arange(dataA.shape[0]):
            dispA[i,:] = tmpA[i,i,:]*(i*i)**pw
            dlineA[:] = np.sum(np.sum(tmpA[irline-w:irline+w+1,irline-w:irline+w+1,:]*(i*i)**pw,0),0)
        for i in np.arange (dataB.shape[0]):
            dispB[i,:] = tmpB[i,i,:]*(i*i)**pw
            dlineB[:] = np.sum(np.sum(tmpB[irline-w:irline+w+1,irline-w:irline+w+1,:]*(i*i)**pw,0),0)
        ir1 = dispA.shape[0]-0
        ir2 = dispB.shape[0]-0
        rmaxnewA = rmax*(ir1/dataA.shape[0])
        rmaxnewB = rmax*(ir2/dataB.shape[0])
        ir = 0
        rminnewA = rmax*(ir/dataA.shape[0])
        rminnewB = rmax*(ir/dataB.shape[0])

        peak_A_list = []
        peak_B_list = []
        peaksA = find_peaks(dispA[:,0],height = tol)
        for peaks in peaksA[0]:
            peak_A_list.append(peaks)
        #print (peak_A_list)
        peaksB = find_peaks(dispB[:,0],height = tol)
        for peaks in peaksB[0]:
            peak_B_list.append(peaks)
        #print (peak_B_list)
        matches = str(set(peak_A_list).intersection(peak_B_list))
        with open(outpath+'peak_list.txt', 'a+') as found:
            matches = matches.replace("{","")
            matches = matches.replace("}","")
            string = (f'{group},{run},{matches}')
            print("run "+str(run)+" peaks at ",matches)
            found.write(string+'\n')
    except FileNotFoundError:
        continue
plt.plot( dispA[:,0])
plt.plot( dispB[:,0])
plt.draw()
plt.show()
