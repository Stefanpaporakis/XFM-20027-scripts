import numpy as np
import matplotlib.pyplot as plt
import csv
   
def load_data(analysis_path,qslice,angle_blur,width):
    summed_data = [] 
    max_data = [] 
    radpos_data = []
    radheight_data = [] 
    #saxs profile 
    saxs = np.load(analysis_path+tag+'_sum_red.npy')
    #Correlation
    fulla = np.load(analysis_path+"/corr_nps1/"+tag+"_nstart400_a_correlation_sum.npy")
    fullb = np.load(analysis_path+"/corr_nps1/"+tag+"_nstart400_b_correlation_sum.npy")
    full = fulla+fullb
    f_integrated_slice = np.sum(np.sum(full[qslice-width:qslice+width+1,qslice-width:qslice+width+1,:],0),0)
    f_tmp = f_integrated_slice*0.0
    for shift in range(-angle_blur,angle_blur+1): f_tmp += np.roll(f_integrated_slice,shift)
    f_integrated_slice = f_tmp
    
    #summed intensity
    summed = np.load(analysis_path+"/mapping_stuff/summed_intensity.npy",allow_pickle=True)
    for i in summed:
        summed_data.append(i)
    #max value
    maxed = np.load(analysis_path+"/mapping_stuff/max_value.npy",allow_pickle=True)
    for i in maxed:
        max_data.append(i)
    
    #rad peak position
    radposition = np.load(analysis_path+"/mapping_stuff/radial_peak_position.npy",allow_pickle=True)
    for i in radposition:
        radpos_data.append(i) 
    
    #rad peal height   
    radialheight = np.load(analysis_path+"/mapping_stuff/radial_peak_height.npy",allow_pickle=True)
    for i in radialheight:
        radheight_data.append(i)
    return saxs, f_integrated_slice,summed_data,max_data,radpos_data,radheight_data  

def read_xy():
    #load x and y points from csv file
    xpix = []
    ypix = []
    xy_path = f"/data/xfm/20027/analysis/xy/{xyfile}/"
    with open (xy_path+str(xyfile)+"-et-marker-stage-cv.csv", newline ='') as xy:
        xyreader = csv.reader(xy,delimiter = ',')
        for row in xyreader:
            xpix.append(row[5])
            ypix.append(row[6])
    return xpix,ypix

def data_trim(xy,load_all): 
    xpix = np.array(xy[0], dtype = 'int')
    ypix = np.array(xy[1], dtype = 'int')
    xmin = min(xpix)
    ymin = min(ypix)
    xmax = max(xpix)
    ymax = max(ypix)

    #check if x, y and data is the same length
    xlen = int(len(xpix))
    summed_data  = load_all[2][:xlen]
    max_data = load_all[3][:xlen]
    radpos_data = load_all[4][:xlen]
    radheight_data = load_all[5][:xlen]
    return summed_data,max_data,radpos_data,radheight_data,xmin,ymin,xmax,ymax

def sum_plot(xy,trim_all):
    xmin = trim_all[4]
    ymin = trim_all[5]
    xmax = trim_all[6]
    ymax = trim_all[7]
    image = np.zeros((xmax-xmin+1,ymax-ymin+1))
    for x,y,d in zip(xy[0],xy[1],trim_all[0]):
        image[int(x)-int(xmin),int(y)-int(ymin)] = d
    return image

def max_plot(xy,trim_all):
    xmin = trim_all[4]
    ymin = trim_all[5]
    xmax = trim_all[6]
    ymax = trim_all[7]
    image = np.zeros((xmax-xmin+1,ymax-ymin+1))
    for x,y,d in zip(xy[0],xy[1],trim_all[1]):
        image[int(x)-int(xmin),int(y)-int(ymin)] = d
    return image
    
def rad_pos_plot(xy,trim_all):
    xmin = trim_all[4]
    ymin = trim_all[5]
    xmax = trim_all[6]
    ymax = trim_all[7]
    image = np.zeros((xmax-xmin+1,ymax-ymin+1))
    for x,y,d in zip(xy[0],xy[1],trim_all[2]):
        image[int(x)-int(xmin),int(y)-int(ymin)] = d
    return image
    
def rad_height_plot(xy,trim_all):
    xmin = trim_all[4]
    ymin = trim_all[5]
    xmax = trim_all[6]
    ymax = trim_all[7]
    image = np.zeros((xmax-xmin+1,ymax-ymin+1))
    for x,y,d in zip(xy[0],xy[1],trim_all[3]):
        image[int(x)-int(xmin),int(y)-int(ymin)] = d
    return image




maia_start = 138009
group = '75MO_W_P4_2H'
run = 383
xyfile = int(maia_start)+int(run)
qslice = 32
angle_blur = 0
width = 0

maia_num = maia_start+run
tag = str(maia_num)+"_"+str(run)
analysis_path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"

load_all = load_data(analysis_path,qslice,angle_blur,width)
xy = read_xy()
trim_all = data_trim(xy,load_all)



saxs = load_all[0]
correlations = load_all[1]
summed_intensity = sum_plot(xy,trim_all)
max_value = max_plot(xy,trim_all)
radial_peak_position = rad_pos_plot(xy,trim_all)
radial_peak_height = rad_height_plot(xy,trim_all)



fig,ax = plt.subplots(2,3,figsize = (10,5))
aspect = 125/250
a = ax[0,0].plot(saxs[:,0],saxs[:,1])
ax[0,0].set_title('1-D profile')
b = ax[1,0].plot(np.arange(0,360,2), correlations)
ax[1,0].set_title('angular correlation')
c = ax[0,1].imshow(summed_intensity,origin = 'lower',aspect = aspect, clim = [16000,17200])
ax[0,1].set_title('summed intensity')
plt.colorbar(c,ax = ax[0,1])
d = ax[1,1].imshow(max_value,origin = 'lower',aspect = aspect, clim = [0,30])
ax[1,1].set_title('max value')
plt.colorbar(d,ax = ax[1,1])
e = ax[0,2].imshow(radial_peak_position,origin = 'lower',aspect = aspect, clim = [0,3])
ax[0,2].set_title('radial peak position')
plt.colorbar(e,ax = ax[0,2])
f = ax[1,2].imshow(radial_peak_height,origin = 'lower',aspect = aspect, clim = [0,0.25])
ax[1,2].set_title('radial peak height')
plt.colorbar(f,ax = ax[1,2])
plt.suptitle("52.3"+chr(176),fontsize = 30)
plt.show()


