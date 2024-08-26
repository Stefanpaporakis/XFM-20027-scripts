import numpy as np
import matplotlib.pyplot as plt
import sys


#don't change these
#pa jul 21: too bad i'm changing it
# refnum, refrun = 99118, 43
maia_start = 138009

#
#this sets the range of theta bins to normalise over (it may need to be changed or tested)
# This can be changed to test the bg subtraction
# PA july 21: keeping this, but save path of bg subbed will just over write
th0,th1 = 10,170
# theta0 = str(th0)
# theta1 = str(th1) 

# some plotting parameters
iq = 33 #which q=q' to plot as a line
scl, sc =0.5, 0.05 #scale the color limits on the displayed image (0<sc,scl<=1)
offset = 0   #0 for q=q' plane; non-zero gives a parallel plane (don't worry about changing this)

# set up run and id numbers for the dataset
group = '75MO_W_P4_2H' #sys.argv[1]
run = 385 #int(sys.argv[2])
# xfmno = refnum + run - refrun
# dataid = str(xfmno)+"_"+str(run)
#dataid = "99528_453"
dataid = f'{maia_start+run}_{run}'

#load the correlation data
datapath =  "/data/xfm/20027/analysis/eiger/"+group+"/"+dataid+"/corr_nps1/"
fname = datapath+dataid+"_nstart400_a_correlation_sum.npy"
print(fname)
datain = np.load(fname)
print("Data shape", datain.shape)


# set up and load the background correlation data
bggroup = 'calibration' #sys.argv[3]
bgrun = 8 #int(sys.argv[4])
# bgxfmno = refnum + bgrun - refrun
# bgdataid = str(bgxfmno)+"_"+str(bgrun)

bgdataid = f'{maia_start+bgrun}_{bgrun}'
bpath = "/data/xfm/20027/analysis/eiger/"+bggroup+"/"+bgdataid+"/corr/"
bfname = bpath +bgdataid+"_a_correlation_sum.npy"
print(bfname)
bg = np.load(bfname)


#
# a normalized bg subtraction for each q & q'
#
data = datain*0.0
bgnorm = datain*0.0
for i in np.arange(data.shape[0]):
    for j in np.arange(data.shape[0]):
        norm = np.sum(datain[i,j,th0:th1])/np.sum(bg[i,j,th0:th1]) 
        bgnorm[i,j,:] = bg[i,j,:]*norm
        data[i,j,:] = datain[i,j,:]-bgnorm[i,j,:]
        # if (i==120) and (j==120):
            # print("norm",norm)			


#
# masking out ranges of q and theta that might have errors
#
# (better to do this with the masking/plotting scripts in pypadf)
#
#data[:,:,:5] = 0
#data[:,:,-5:] = 0
#data[:30,:30,:] = 0

# save the background subtracted correlation function
# np.save(fname[:-4]+"_bgsub_"+theta0+theta1+".npy", data )
#np.save(fname[:-4]+"_bgsub.npy", data )

#
# from here on its just display code
#
plt.plot( datain[iq,iq,:], label = 'normal' ) 
plt.plot( bgnorm[iq,iq,:], label = 'background' ) 
plt.plot( data[iq,iq,:], label = 'background sub' ) 
plt.legend(loc = 'upper right')
# now display a cross-section of the correlation volume
disp = np.zeros((data.shape[0],data.shape[2]))
for i in np.arange(data.shape[0]-offset):
        disp[i,:] = data[i,i+offset,:] - np.average(data[i,i+offset,:])
plt.figure()
plt.imshow( disp )
plt.clim([scl*np.min(disp), sc*np.max(disp)])
#plt.draw()
plt.show()


