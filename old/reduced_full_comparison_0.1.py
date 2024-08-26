import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys
import glob
import pathlib 
import csv


def load_reduced (path,analysis,lower,upper,tag):
    reduceda = np.load(path+analysis+"/"+str(lower)+'_'+str(upper)+"/reduced"+tag+"_nstart400_a_correlation_sum.npy")
    reducedb = np.load(path+analysis+"/"+str(lower)+'_'+str(upper)+"/reduced"+tag+"_nstart400_b_correlation_sum.npy")
    reduced_data = reduceda+reducedb
    return reduced_data

def load_full (path,analysis,lower,upper,tag):
    fulla = np.load(path+tag+"_nstart400_a_correlation_sum.npy")
    fullb = np.load(path+tag+"_nstart400_b_correlation_sum.npy")
    full_data = fulla+fullb
    return full_data

def plot_ang_corr(reduced,full,qslice,w,angle_blur,seperation):
    integrated_slice = np.sum(np.sum(reduced[qslice-w:qslice+w+1,qslice-w:qslice+w+1,:],0),0)
    tmp = integrated_slice*0.0
    for shift in range(-angle_blur,angle_blur+1): tmp += np.roll(integrated_slice,shift)
    integrated_slice = tmp
    f_integrated_slice = np.sum(np.sum(full[qslice-w:qslice+w+1,qslice-w:qslice+w+1,:],0),0)
    f_tmp = f_integrated_slice*0.0
    for shift in range(-angle_blur,angle_blur+1): f_tmp += np.roll(f_integrated_slice,shift)
    f_integrated_slice = f_tmp
    return integrated_slice, f_integrated_slice

def load_xy(run):
    xpix = []
    ypix = []
    xyfile = 138009+int(run)
    xy_path = f"/data/xfm/20027/analysis/xy/{xyfile}/"
    with open (xy_path+str(xyfile)+"-et-marker-stage-cv.csv", newline ='') as xy:
        xyreader = csv.reader(xy,delimiter = ',')
        for row in xyreader:
            xpix.append(row[5])
            ypix.append(row[6])
    return xpix,ypix

def load_well(path,group,tag,analysis,chunksize):
    well_list = []
    bool_list = []
    if path ==f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps{chunksize}/":
        path =f"/data/xfm/20027/analysis/eiger/{group}/{tag}/mapping_stuff/"
    if analysis == 'maxpeaks':
        analysis = 'max_value.npy'
    if analysis =='radpeakpos':
        analysis ='radial_peak_position.npy'
    if analysis =='intpeaks':
        analysis ='summed_intensity.npy'
    if analysis =='radpeakheight':
        analysis ='radial_peak_height.npy'
    well = np.load(path+analysis, allow_pickle=True)
    well[well == None] = 0
    for i in well:
        well_list.append(i)
    boolwell = (well>lower)*(well<upper)
    for i in boolwell:
        bool_list.append(i)
    return bool_list, well_list
    
def well_plot(wells,xy): 
    xpix = np.array(xy[0], dtype = 'int')
    ypix = np.array(xy[1], dtype = 'int')
    xmin = min(xpix)
    ymin = min(ypix)
    xmax = max(xpix)
    ymax = max(ypix)

    #check if x, y and data is the same length
    xlen = int(len(xpix))
    well_list  = wells[1][:xlen]
    bool_list = wells[0][:xlen]

    if len(ypix)==len(xpix)==len(well_list):
        #im = np.zeros((260,135))
        im = np.zeros((xmax-xmin+1,ymax-ymin+1))
        for x,y,d in zip(xpix,ypix,well_list):
            im[x-xmin,y-ymin] = d
 
    if len(ypix)==len(xpix)==len(bool_list):
        #im = np.zeros((260,135))
        imr = np.zeros((xmax-xmin+1,ymax-ymin+1))
        for x,y,e in zip(xpix,ypix,bool_list):
            imr[x-xmin,y-ymin] = e  


    
    else:
        print("lengths aren't the same for x, y and data")
        print("y is ", len(ypix))
        print("x is ", len(xpix))
        print("data is ", len(d_list))
        exit() 
    return im,imr
    
def plots(get_well_data,get_ang_corr_data,seperation,analysis,lower,upper,qslice,temp):
    fig,ax = plt.subplots(1,3,figsize = (15,5))
    a = ax[0].imshow(get_well_data[0], origin = 'lower',aspect = 125/250, clim = [lower,upper])
    ax[0].set_title('full '+analysis)
    plt.colorbar(a,ax = ax[0])
    b = ax[1].imshow(get_well_data[1], origin = 'lower',aspect = 125/250)
    ax[1].set_title('filtered '+str(lower)+" "+str(upper)+" "+analysis)
    plt.colorbar(b,ax = ax[1])
    ax[2].plot(np.arange(0,360,2), get_ang_corr_data[0]+seperation, label =analysis+" "+ str(lower)+" "+str(upper)+ ' filtered')
    ax[2].plot(np.arange(0,360,2), get_ang_corr_data[1]+seperation, label = 'full')
    ax[2].set_title("qslice = "+str(qslice)+' angular correlations')
    ax[2].legend()
    plt.suptitle("run "+str(run)+", "+str(temp)+chr(176),fontsize = 20)
    plt.show()

def bg_sub (maia_start,full,reduced):
	th0 = 0
	th1 = 180
	bggroup = 'calibration'
	bgrun = 8 
	bgdataid = f'{maia_start+bgrun}_{bgrun}'
	bpath = "/data/xfm/20027/analysis/eiger/"+bggroup+"/"+bgdataid+"/corr/"
	bfname = bpath +bgdataid+"_a_correlation_sum.npy"
	bg = np.load(bfname)
	full_data = full*0.0
	full_bgnorm = full*0.0
	red_data = reduced*0.0
	red_bgnorm = reduced*0.0
	for i in np.arange(full_data.shape[0]):
		for j in np.arange(full_data.shape[0]):
			norm = np.sum(full[i,j,th0:th1])/np.sum(bg[i,j,th0:th1]) 
			full_bgnorm[i,j,:] = bg[i,j,:]*norm
			full_data[i,j,:] = full[i,j,:]-full_bgnorm[i,j,:]
	for i in np.arange(red_data.shape[0]):
		for j in np.arange(red_data.shape[0]):
			norm = np.sum(reduced[i,j,th0:th1])/np.sum(bg[i,j,th0:th1]) 
			red_bgnorm[i,j,:] = bg[i,j,:]*norm
			red_data[i,j,:] = reduced[i,j,:]-red_bgnorm[i,j,:]
	return full_data,red_data

def plot_bg_sub_ang_corr(bg_reduced,bg_full,qslice,w,angle_blur,seperation):
	integrated_slice = np.sum(np.sum(bg_reduced[qslice-w:qslice+w+1,qslice-w:qslice+w+1,:],0),0)
	tmp = integrated_slice*0.0
	for shift in range(-angle_blur,angle_blur+1): tmp += np.roll(integrated_slice,shift)
	integrated_slice = tmp
	f_integrated_slice = np.sum(np.sum(bg_full[qslice-w:qslice+w+1,qslice-w:qslice+w+1,:],0),0)
	f_tmp = f_integrated_slice*0.0
	for shift in range(-angle_blur,angle_blur+1): f_tmp += np.roll(f_integrated_slice,shift)
	f_integrated_slice = f_tmp
	return integrated_slice, f_integrated_slice

###main script here##
maia_start = 138009
group = '75MO_W_P4_2H'
run = 383
temp = 37.3
qslice = 35
chunksize = 1 # set chunksize to 1 for full correlation just about
w=0
angle_blur = 0
seperation = 0
maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)
analysis = 'radpeakpos'
#analysis = 'intpeaks'
#analysis = 'maxpeaks'

#381
lower = 1.35
upper = 1.45
#383
#lower =1.35
#upper =1.45

#385
#lower = 1.38
#upper = 1.5

#387
#lower = 1.4
#upper = 1.53
#lower = 1.53
#upper = 2


path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps{chunksize}/"
subtract_bg = True


reduced= load_reduced(path,analysis,lower,upper,tag)
full = load_full(path,analysis,lower,upper,tag)
if subtract_bg == True:
	bg_corr = bg_sub (maia_start,full,reduced)
	bg_reduced  = bg_corr[0]
	bg_full = bg_corr[1]
	get_ang_corr_data = plot_bg_sub_ang_corr(bg_reduced,bg_full,qslice,w,angle_blur,seperation)
	wells = load_well(path,group,tag,analysis,chunksize)
	xy = load_xy(run)
	get_well_data = well_plot(wells,xy)
	plot_all = plots(get_well_data,get_ang_corr_data,seperation,analysis,lower,upper,qslice,temp)
else:
	get_ang_corr_data = plot_ang_corr(reduced,full,qslice,w,angle_blur,seperation)
	wells = load_well(path,group,tag,analysis,chunksize)
	xy = load_xy(run)
	get_well_data = well_plot(wells,xy)
	plot_all = plots(get_well_data,get_ang_corr_data,seperation,analysis,lower,upper,qslice,temp)

