import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd

#don't chage these
refnum, refrun = 138490, 481
# set data to plot here
analysis_path = "/data/xfm/20027/analysis/eiger/"


#Init
title = "75MO_W_P4_2H"
runs = [387]#,383,384,385,386,387,388,389,390,391,392,393]  #LC runs
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
percent = 50
r_lower,r_upper = 0,2
bar_width =0.004 #rad peak pos
#bar_width =1 #max val
#bar_width =0.004 #rad peak pos
#bar_width =0.004 #rad peak pos




for i, run in enumerate(runs):
    try:
        group = groups[i]
        xfmno = refnum + run - refrun
        tag = str(xfmno)+"_"+str(run)
        path = analysis_path+group+"/"+tag+"/mapping_stuff/"
        data = np.load(path+analysis,allow_pickle = True)
        data[data==None]=0    
        data[data>r_upper] =0
        data[data<r_lower] = 0    #THIS IS TO FILTER OUTLIERS
        data = [value for value in data if value !=0]
        #data[data<0] =350
        #print("data min max", np.min(data), np.max(data))
        
        dlist.append(data)
        #dlist.append(data[:,0],q_data[:,1])
    except FileNotFoundError:
        continue



fig,axs = plt.subplots(1,1)
print("most common "+str(percent)+"%")
for i, j in enumerate(dlist):
    #ax = axs[i//3,i%3] # all the plots (4 by 3)  
    #ax = axs[i] #Plots on one row
    ax = axs # Single run plot
    #h, be = np.histogram(j,bins=34000,range = (r_lower,r_upper))
    if analysis == 'radial_peak_position.npy':
        ax.hist(j,bins =1000,range = (r_lower,r_upper),width = bar_width,label = 'full')
        data_series = pd.Series(j)
        threshold = np.percentile(data_series.value_counts(),100-percent)
        most_common_values = data_series[data_series.isin(data_series.value_counts()[data_series.value_counts() >=threshold].index)]  
        ax.hist(most_common_values,bins =1000,range = (r_lower,r_upper),width = bar_width,label = str(percent)+'%')
    else:        
        ax.hist(j,bins =r_upper,range = (r_lower,r_upper),width = bar_width,label = 'full')
        data_series = pd.Series(j)
        threshold = np.percentile(data_series.value_counts(),100-percent)
        most_common_values = data_series[data_series.isin(data_series.value_counts()[data_series.value_counts() >=threshold].index)]  
        ax.hist(most_common_values,bins =r_upper,range = (r_lower,r_upper),width = bar_width,label = str(percent)+'%')
    #ax.set_yscale('log')
    ax.axvline(x = min(most_common_values), color = 'r', linestyle = '--')
    ax.axvline(x = max(most_common_values), color = 'r', linestyle = '--')
    #print(min(most_common_values))
    #print(max(most_common_values))
    ax.set_title(str(runs[i]) + ", "+plot_titles[i]+chr(176),x = 0.5, y = 0.6)
    ax.legend(loc =  'upper right')
    print(str(runs[i]) + ", "+plot_titles[i]+chr(176)+", between "+str(min(most_common_values))+" and "+str(max(most_common_values)))
plt.suptitle(analysis[:-4])
plt.show()
