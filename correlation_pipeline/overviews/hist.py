import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#don't chage these
refnum, refrun = 138490, 481
# set data to plot here
analysis_path = "/data/xfm/20027/analysis/eiger/"


#Init
title = "75MO_W_P4_2H"
runs = [381,383,384,385,386,387,388,389,390,391,392,393]  #LC runs
groups = [title]*len(runs)
labels = [runs]
#Which one to plot
#analysis = 'max_value.npy'
#analysis = 'summed_intensity.npy'
analysis = 'radial_peak_position.npy'
#analysis = 'radial_peak_height.npy'
dlist = []
c_vals = np.linspace(0,0.3,len(runs))
colors = cm.PuOr(c_vals)[::-1]
plot_titles = ["35","37.3","48.3","52.3","55.9","59.2",
"62.1","64.7","67","68.9","74.5","77.6","79.9"]
percent = 20
crop = True
r_lower,r_upper = 1,2


for i, run in enumerate(runs):
    try:
        group = groups[i]
        xfmno = refnum + run - refrun
        tag = str(xfmno)+"_"+str(run)
        path = analysis_path+group+"/"+tag+"/mapping_stuff/"
        data = np.load(path+analysis,allow_pickle = True)
        data[data==None]=0    
        #data[data>600] =0    #THIS IS TO FILTER OUTLIERS
        #data[data<0] =350
        #print("data min max", np.min(data), np.max(data))
        
        dlist.append(data)
        #dlist.append(data[:,0],q_data[:,1])
    except FileNotFoundError:
        continue



fig,axs = plt.subplots(4,3)
for i, j in enumerate(dlist):
    ax = axs[i//3,i%3] # all the plots (4 by 3)  
    #ax = axs[i] #Plots on one row
   # ax = axs # Single run plot
    if crop == True:
        h, be = np.histogram(j,bins=34000,range = (r_lower,r_upper))
    else:
        h, be = np.histogram(j,bins=34000)
    ax.plot(be[:-1],h)
    ax.set_title(str(runs[i]) + ", "+plot_titles[i]+chr(176),x = 0.5, y = 0.6)
plt.suptitle(analysis[:-4])
plt.show()
exit()

plt.figure()
print(str(analysis[:-4])+', '+str(percent)+'%')
for i, j in enumerate(dlist):
    counter = 0
    counter = counter+i
    h, be = np.histogram(j,bins=34000)
    ch = 0
    ch_array = h*0
    for i in range(1,h.shape[0]):
        ch += h[i]
        ch_array[i] = ch
    below = np.where(ch_array/np.max(ch_array)<percent/100)
    above = np.where(ch_array/min(k for k in ch_array if k>0)<percent/100)
    #print(np.min(ch_array))
    #exit()
    i_thresh = below[0][-1]
    j_thresh = above[0][-1]
    plt.plot(be[:-1],ch_array/np.max(ch_array),color=colors[counter],label = str(runs[counter])+', '+str(round(be[i_thresh],3))+' ('+plot_titles[counter]+chr(176)+')')
    plt.plot(be[i_thresh],percent/100,color = colors[counter],marker = 'D')
    plt.plot(be[j_thresh],percent/100,color = colors[counter],marker = 'D')
    if crop == True:
        plt.xlim(r_lower,r_upper)
    plt.legend()
    plt.title(str(analysis[:-4])+', '+str(percent)+'%')
    print(str(runs[counter])+' threshold =',be[i_thresh])
    print(be[j_thresh])
plt.show()
    

    




















