




# Filters between a range, gives x and y pixel value for each
# peak position, that way we can focus on certain areas for correlations



import fluxfm
import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys
import glob
import pathlib 
import h5py
import hdf5plugin
import csv

def h5info(total_length, individual_lengths):
    result = []
    h5start = 1
    for i in individual_lengths:
        for j in range(i):
            if len(result)<total_length:
                result.append(h5start)
            else:
                break
        h5start +=1
        if len(result) >=total_length:
            break
    return result      

def h5frame(individual_lengths):
    frame = []
    for frame_number,length in enumerate(individual_lengths, start = 0):
        for frame_position in range(1,length+1):
            frame.append(frame_position)
    return frame

def well_plot(bool_list,well_list,xpix,ypix): 
    xpix = np.array(xpix, dtype = 'int')
    ypix = np.array(ypix, dtype = 'int')
    xmin = min(xpix)
    ymin = min(ypix)
    xmax = max(xpix)
    ymax = max(ypix)

    #check if x, y and data is the same length
    xlen = int(len(xpix))
    well_list  = well_list[:xlen]
    bool_list = bool_list[:xlen]

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
    fig,ax = plt.subplots(1,2,figsize = (10,5))
    a = ax[0].imshow(im, origin = 'lower',aspect = 125/250,clim = [1,2])
    ax[0].set_title('full '+str(run)+" "+analysis[:-4])
    plt.colorbar(a,ax = ax[0])
    b = ax[1].imshow(imr, origin = 'lower',aspect = 125/250, clim = [0,1])
    ax[1].set_title('filtered '+str(run)+" "+analysis[:-4])
    plt.colorbar(b,ax = ax[1])
    #plt.show()





maia_start = 138009
group = '75MO_W_P4_2H'
run = 393
xyfile = 138009+int(run)
lower= 1.64
upper = 1.9



analysis = 'radial_peak_position.npy'
maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)
analysis_path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/mapping_stuff/"

#Load well and append all data to list, and tell you what the most common number is
well_list = []
well = np.load(analysis_path+analysis, allow_pickle=True)
#print(len(well))
well[well == None] = 0
unique,counts = np.unique(well,return_counts = True)
most_common = unique[np.argmax(counts)]
print("most common "+analysis[:-4]+" for entire well is",most_common)
for i in well:
    well_list.append(i)

bool_list  = []

#boolwell = well  # No filter
boolwell = (well>lower)*(well<upper)
#boolwell = (well>300)*(well<370)+(well>400)    #Ignore everything between 350-380
for i in boolwell:
    bool_list.append(i)

    
#Merge lists to only contain values where boolwell is true, and the most common value in the reduced dataset
filtered_list = []
filtered_well = [value for i, value in enumerate(well) if boolwell[i]]
unique,counts = np.unique(filtered_well,return_counts = True)
most_common = unique[np.argmax(counts)]
print("most common " +analysis[:-4]+" for filtered well is",most_common)
for i in filtered_well:
    filtered_list.append(i)



#load x and y points from csv file
xpix = []
ypix = []
xy_path = f"/data/xfm/20027/analysis/xy/{xyfile}/"
with open (xy_path+str(xyfile)+"-et-marker-stage-cv.csv", newline ='') as xy:
    xyreader = csv.reader(xy,delimiter = ',')
    for row in xyreader:
        xpix.append(row[5])
        ypix.append(row[6])

# save xy values to list if boolean is true
x_list = []
y_list = []
x_data = [value for i, value in enumerate(xpix) if boolwell[i]]
for i in x_data:
    x_list.append(i)
y_data = [value for i, value in enumerate(ypix) if boolwell[i]]
for i in y_data:
    y_list.append(i)


#make a list of vlaues that correspond to the h5 file size the crop for the 
#boolean values to get what h5 file each frame cam from
h5_list = []
frame_list = []
total_length = int(len(well)) #run 381
print("total frames is ", total_length)
print("reduced number of frames to ", len(filtered_list))
individual_lengths = [9999,9999,9999,total_length-30000]#run 381
h5data = h5info(total_length,individual_lengths)
frame_data = h5frame(individual_lengths)
h5data = [value for i, value in enumerate(h5data) if boolwell[i]]
for i in h5data:
    h5_list.append(i)
frame_data = [value for i, value in enumerate(frame_data) if boolwell[i]]
for i in frame_data:
    frame_list.append(i)


#make everything the same length
xlen = int(len(x_list))
filtered_list  = filtered_list[:xlen]
h5_list = h5_list[:xlen]
frame_list = frame_list[:xlen]
#print(len(h5_list))
#print (len(filtered_list))
#print(len(x_list))
#print(len(y_list))

plot = well_plot(bool_list,well_list,xpix,ypix)

cont = 'y'#input('save filtered x and y peaks for correlations? [y/n]')
if cont =='y':
#save to a file (.txt in this case)
    if analysis =='summed_intensity.npy':
        analysis_path = analysis_path+'/intpeaks/'
    if analysis == 'max_value.npy':
        analysis_path = analysis_path+'/maxpeaks/'
    if analysis =='radial_peak_position.npy':
        analysis_path = analysis_path+'/radpeakpos/'
    if analysis =='radial_peak_height.npy':
        analysis_path = analysis_path+'/radpeakheight/'
    if os.path.exists(analysis_path)==False:
          os.mkdir(analysis_path)
    with open(analysis_path+str(lower)+'_'+str(upper)+'_xy_peaks.txt', 'w') as f:
        f.write('peak\tx\ty\th5\tframe\n')
        for i in range(0,len(filtered_list)):
            f.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(str(filtered_list[i]),str(x_list[i]),str(y_list[i]),str(h5_list[i]),str(frame_list[i])))
    print('saved x and y peaks to ', analysis_path+str(lower)+'_'+str(upper))

if cont=='n':
    print('didnt save')
    exit()


