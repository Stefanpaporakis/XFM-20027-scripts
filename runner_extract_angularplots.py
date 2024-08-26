import numpy as np
import matplotlib.pyplot as plt
import sys

#don't chage these
refnum, refrun = 138009, 0

# set data to plot here [UPDATE THIS]
analysis_path = "/data/xfm/20027/analysis/eiger/"

rmax = 11.31   #maximum q (r) value in the correlation function (padf)
rline = 3.15   #r value to extract lineplot for
rline2 = 3.15  #r' value to extract lineplot for
w = 5          # width in pixels to integrate (q/r)
pw = 0         # scale radial values by this power

group = sys.argv[1]
runstart = int(sys.argv[2])
if len(sys.argv)>4:
    runstop = int(sys.argv[3])
    ab = sys.argv[4]
else:
    runstop = runstart
    ab = sys.argv[3]



qlist = []
for i, run in enumerate(range(runstart,runstop+1,1)):
    xfmno = refnum + run - refrun
    tag = str(xfmno)+"_"+str(run) 
    path = analysis_path+group+"/"+'138054_45'+"/corr/"
    data = np.load( path+tag+"_"+ab+"_correlation_sum.npy")

    irline = int(data.shape[0]*rline/rmax)
    irline2 = int(data.shape[0]*rline2/rmax)
    disp = np.zeros( (data.shape[0], data.shape[2]) )
    dline = np.zeros( data.shape[2] )
    tmp = data*0.
    for ii in np.arange(data.shape[0]):
       for j in np.arange(data.shape[1]):
           tmp[ii,j,:] = data[ii,j,:] - 1*np.average(data[ii,j,:])
    
    for ii in np.arange(data.shape[0]):
         disp[ii,:] = tmp[ii,ii,:]*(ii*ii)**pw 
         dline[:] = np.sum(np.sum(tmp[irline-w:irline+w,irline2-w:irline2+w,:]*(ii*ii)**pw,0),0)
    np.save(path+tag+"_"+ab+"_qline%.2f"%rline+"_qline%.2f.npy"%rline2, dline)
    qlist.append(dline)

