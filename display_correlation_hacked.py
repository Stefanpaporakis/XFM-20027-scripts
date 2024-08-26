import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys
from scipy.signal import find_peaks

group = sys.argv[1]
run = int(sys.argv[2])
maia_start = 138009

maia_num = maia_start + run


#npatterns = sys.argv[3]
#ab = sys.argv[4]



#dont change this
#refnum = 121019
#refrun = 424
#xfmno = refnum + run - refrun
#runtag = str(xfmno)+"_"+str(run)

#datapath = "/data/xfm/19545/analysis/eiger/"+group+"/"+runtag+"/corr/"
#fname = runtag+"_n"+str(npatterns)+"_"+ab+"_correlation_sum.npy"

#datapath = "/data/xfm/20027/analysis/eiger/75MO_W_8H/138054_45/corr/"
#fname = "120640_45_a_correlation_sum.npy"
#datapath =  "/data/xfm/20027/analysis/eiger/75MO_W_P2_1H/138104_95/corr/"
#fname = "138104_95_a_correlation_sum.npy"
#datapath =  "/data/xfm/20027/analysis/eiger/75MO_W_6H/138044_35/corr/"
#fname = "138044_35_a_correlation_sum.npy"
#datapath =  "/data/xfm/20027/analysis/eiger/calibration/138016_7/corr/"
#fname = "138016_7_a_correlation_sum.npy"
# datapath = "/data/xfm/20027/analysis/eiger/50DMPC_W_1H/138152_143/corr/"
# fname = "138152_143_a_correlation_sum.npy"


# datapath = "/data/xfm/20027/analysis/eiger/75MO_W_P2_1H/138104_95/corr/"
# fname = "138104_95_a_correlation_sum_bgsub.npy"

datapath = f"/data/xfm/20027/analysis/eiger/{group}/{maia_num}_{run}/corr_nps1/"
# fname = f"{maia_num}_{run}_a_correlation_sum_bgsub.npy"
fname = f"{maia_num}_{run}_nstart400_a_correlation_sum_bgsub.npy"
data = np.load(datapath+fname)

fname = f"{maia_num}_{run}_nstart400_b_correlation_sum_bgsub.npy"
dataB = np.load(datapath+fname)

sc, scl = 0.15, 0.15
rmax =  128 #128

if len(sys.argv)>3:
    rline = int(sys.argv[3])
else:
    rline = 35 #this is where you set the line to extract and plot separately
irline = int(data.shape[0]*rline/rmax)
w = 1
#print(data.shape)
#print( "angular lineplot is from rline ", rline)
#print(f'current qmax is {rmax} - set to qbmax-qbmin in this script if using a reduced q range ')

disp = np.zeros( (data.shape[0], data.shape[2]) )
dispB = np.zeros( (data.shape[0], data.shape[2]) )
dline = np.zeros( data.shape[2] )
dlineB = np.zeros( data.shape[2] )
tmp = data*0.
tmpB = data*0.
ith = 1 # this crops from the left
thmin = (ith/360)*data.shape[2]
for i in np.arange(data.shape[0]):
    for j in np.arange(data.shape[1]):
        tmp[i,j,:] = data[i,j,:] - 1*np.average(data[i,j,ith:-ith])
        tmpB[i,j,:] = dataB[i,j,:] - 1*np.average(dataB[i,j,ith:-ith])
pw = 0
for i in np.arange(data.shape[0]):
    disp[i,:] = tmp[i,i,:]*(i*i)**pw
    dline[:] = np.sum(np.sum(tmp[irline-w:irline+w+1,irline-w:irline+w+1,:]*(i*i)**pw,0),0)
    dispB[i,:] = tmpB[i,i,:]*(i*i)**pw
    dlineB[:] = np.sum(np.sum(tmpB[irline-w:irline+w+1,irline-w:irline+w+1,:]*(i*i)**pw,0),0)

ir1 = disp.shape[0]-0
rmaxnew = rmax*(ir1/data.shape[0])
ir = 0
rminnew = rmax*(ir/data.shape[0])
plt.imshow(disp[ir:ir1,ith:disp.shape[1]//1], origin='lower', extent=[thmin,180,rminnew,rmaxnew], aspect=2)
plt.clim([np.min(disp[ir:ir1,ith:disp.shape[1]//2])*scl,np.max(disp[ir:ir1,ith:disp.shape[1]//2])*sc])
plt.figure()
#plt.colorbar()
plt.title(fname)

#plot a line from q=q'
#plt.figure()
#p, = plt.plot(np.arange(0,360,2), dline )
#pB, = plt.plot(np.arange(0,360,2), dlineB )
#plt.legend([p,pB], ["a", "b"])
#plt.xlim([0,360])
#plt.title(fname)

#plt.figure()
#plt.plot( disp[:,0])
#plt.plot( dispB[:,0])
peak1 = find_peaks(disp[:,0],height = 2)
print (peak1[0])

plt.draw()
plt.show()
