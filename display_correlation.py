import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys

group = sys.argv[1]
run = int(sys.argv[2])
npatterns = sys.argv[3]
ab = sys.argv[4]



#dont change this
refnum = 138390
refrun = 381
xfmno = refnum + run - refrun
runtag = str(xfmno)+"_"+str(run)

datapath = "/data/xfm/20027/analysis/eiger/"+group+"/"+runtag+"/corr_nps1/"
fname = runtag+"_nstart"+str(npatterns)+"_"+ab+"_correlation_sum.npy"
data = np.load(datapath+fname)


sc, scl = 0.05, 0.05
rmax = 11.31
rline = 2.08 #CholPeg
#rline = 3.15
irline = int(data.shape[0]*rline/rmax)
w = 2

disp = np.zeros( (data.shape[0], data.shape[2]) )
dline = np.zeros( data.shape[2] )
tmp = data*0.
for i in np.arange(data.shape[0]):
   for j in np.arange(data.shape[1]):
       tmp[i,j,:] = data[i,j,:] - 1*np.average(data[i,j,:])
pw = 0
for i in np.arange(data.shape[0]):
     disp[i,:] = tmp[i,i,:]*(i*i)**pw 
     dline[:] = np.sum(np.sum(tmp[irline-w:irline+w,irline-w:irline+w,:]*(i*i)**pw,0),0)

ir1 = 512
rmaxnew = rmax*(ir1/data.shape[0])
ir = 10
rminnew = rmax*(ir/data.shape[0])
plt.imshow(disp[ir:ir1,:disp.shape[1]//2], origin='lower', extent=[0,180,rminnew,rmaxnew], aspect=9)
plt.clim([np.min(disp[ir:ir1,ir:ir1])*scl,np.max(disp[ir:ir1,ir:ir1])*sc])
#plt.figure()
plt.colorbar()
plt.title(fname)

#plot a line from q=q'
plt.figure()
plt.plot(np.arange(0,360,2), dline )
plt.xlim([0,360])
plt.title(fname)
"""
plt.figure()
disp2 = data[:,:,90]*np.outer(np.arange(data.shape[0]),np.arange(data.shape[1]))**2
plt.imshow( disp2[ir:ir1,ir:ir1], origin='lower', extent=[0,rmaxnew,0,rmaxnew], aspect=1)
plt.title( "Const theta" )
plt.clim([np.min(disp2[ir:ir1,ir:ir1])*scl,np.max(disp2[ir:ir1,ir:ir1])*sc])

plt.figure()
rprime = 7
irp = int(data.shape[0]*rprime/rmax)
disp3 = data[irp,:,:]*np.outer(np.arange(data.shape[0]),np.ones(data.shape[2]))**2
plt.imshow( disp3[ir:ir1,:disp3.shape[1]//2], origin='lower', extent=[0,180,0,rmaxnew], aspect=9)
plt.title( "r not eq rprime" )
plt.clim([np.min(disp3[ir:ir1,:])*scl,np.max(disp3[ir:ir1,:])*sc])
"""
plt.draw()
plt.show()
