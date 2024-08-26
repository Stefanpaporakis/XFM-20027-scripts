


#This script is an updated version to plot angular correlations of 
#different runs from the same sample/well. Before you plot, to get the
#correct qslice, first run "find_peaks_ang_corr.py"




import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn as sns
import matplotlib.cm as cm
#don't chage these
refnum, refrun = 138490, 481


########### temps and runs################################
dataset = "75MO_W_P4_2H"
analysis_path = "/data/xfm/20027/analysis/eiger/"
peaklist = np.loadtxt(f"/data/xfm/20027/analysis/eiger/{dataset}/"+'peak_list.txt', delimiter = ',', usecols = (1,2))
runs = []
peaks = []
for i in (peaklist[:,1]):
	peaks.append(int(i))
for i in (peaklist[:,0]):
	runs.append(int(i))



plot_title = "75MO_W_P4_2H"
temps = [35, 37.3, 48.3, 52.3, 55.9, 59.2, 62.1, 64.7, 67, 68.9,74.5, 77.6, 79.9]
groups = [dataset]*len(runs)
labels = runs



width = 0
rcen = np.array(peaks) #where peak is
r0s = rcen-width
r1s = rcen+width+1
rmin = 10

dlistC = []
bg = np.load(analysis_path+"calibration/138017_8/corr/138017_8_a_correlation_sum.npy")
bg = bg+(np.load(analysis_path+"calibration/138017_8/corr/138017_8_b_correlation_sum.npy"))


for i, run in enumerate (runs):
    group = groups[i]
    xfmno = refnum + run - refrun
    tag = str(xfmno)+"_"+str(run) 
    path = analysis_path+group+"/"+tag+"/corr_nps1/"
    dataA = np.load( path+tag+"_nstart400_a_correlation_sum.npy")
    dataB =  np.load( path+tag+"_nstart400_b_correlation_sum.npy")
    dataC = dataA+dataB
    
    #BG SUBTRACTION
    for j in np.arange(dataC.shape[0]):
        norm = np.sum(dataC[i,j])/np.sum(bg[i,j]) 
        dataC[i,j,:] = dataC[i,j,:]-bg[i,j,:]*norm
    dlistC.append(dataC)
    #print(data.shape)

nth = dlistC[0].shape[2]
thmax = 360
thvals = np.arange(nth)*thmax/nth

c_vals = np.linspace(0,0.3,len(runs))
colors = cm.PuOr(c_vals)[::-1]
plist = []
strt=0
nruns=1
for i, data in enumerate(dlistC[strt:strt+nruns]):
    tmp = np.average(data[r0s[strt+i]:r1s[strt+i],:,:],0)
    disp = np.average(tmp[r0s[strt+i]:r1s[strt+i],:],0)-i*4
    p, = plt.plot(thvals, disp,color=colors[i])
    plist.append(p)
plt.ylabel("Correlation intensity (arb units)", fontsize=10)
plt.xlabel(r'theta (degrees)',fontsize=10)
plt.legend(plist, labels[strt:strt+nruns], loc = 'upper right') 
plt.draw()
plt.show()    
