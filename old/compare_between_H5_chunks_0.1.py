import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys
import glob
import pathlib 



def find_folders(datapath,file_filter):
    folders = []
    for folder_name in os.listdir(datapath):
        folder_path = os.path.join(datapath,folder_name)
        if os.path.isdir(folder_path) and file_filter in folder_name:
            folders.append(folder_path)
    return (folders)
    
def find_files(folders):
    files = []
    for file_name in folders:
        file_path = sorted(glob.glob(file_name+"/*nstart400_h5*.npy"))
        files.append(file_path)
    return files
 
 

        
def load_data (files):
    data_list = []
    all_titles = []
    all_runs = []
    for i, data in enumerate(files): 
        plot_list = []
        title_list = []
        runnum_list = []
        for j, values in enumerate(data):
            title = values.split('/')[-2]
            title = title.split('corr_nps')[+1]
            title_list.append(title)
            fname= values.split('/')[-1]
            runnumf = fname.split('_correlation')[-2]
            runnumf = runnumf.split('400_')[+1]
            runnum_list.append(runnumf)
            profile = np.load(values)
            integrated_slice = np.sum(np.sum(profile[qslice-w:qslice+w+1,qslice-w:qslice+w+1,:],0),0)
            tmp = integrated_slice*0.0
            for shift in range(-angle_blur,angle_blur+1): tmp += np.roll(integrated_slice,shift)
            integrated_slice = tmp 
            #plots = plt.plot(np.arange(0,360,2), integrated_slice+j*0.2,label = runnumf)
            plot_list.append(integrated_slice)
        data_list.append(plot_list)
        all_titles.append(title_list)
        all_runs.append(runnum_list)
        #plt.title(title)
        #plt.legend()
        #plt.show()
    return data_list,all_titles,all_runs
    #return all_titles
    #return all_runs


maia_start = 138009

group = '75MO_W_P4_2H'
run = 381
maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)

qslice = 32
w=0
angle_blur = 0
datapath = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"
file_filter = 'corr_nps'

folders = find_folders(datapath,file_filter)
files = find_files(folders)
profiles,titles,runner  = load_data(files)
fig,axs = plt.subplots(2,3)
print(len(profiles[0][0]))

for i,(ax, profile) in enumerate (zip(axs.flatten(), profiles)):
    for j, line in enumerate(profile):
        ax.plot(np.arange(0,360,2), profiles[i][j]+j*0.2,)
        ax.legend(runner[i], loc = 'upper right')
    ax.set_title("chunksize "+titles[i][0])
plt.suptitle(group+" "+str(run)+" chunksize comparison")
plt.show()

    



   
