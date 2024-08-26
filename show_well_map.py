


#This script plots an intensity map of the well, only works after you have run 
# "H5_intensity_0.1.py"








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


def well_plot(d_list,xpix,ypix): 
    xpix = np.array(xpix, dtype = 'int')
    ypix = np.array(ypix, dtype = 'int')
    xmin = min(xpix)
    ymin = min(ypix)
    xmax = max(xpix)
    ymax = max(ypix)

    #check if x, y and data is the same length
    xlen = int(len(xpix))
    d_list  = d_list[:xlen]
    print( "reshaped data to be ", len(d_list))

    if len(ypix)==len(xpix)==len(d_list):
        print("lengths are the same, plotting well map")
        #im = np.zeros((260,135))
        im = np.zeros((xmax-xmin+1,ymax-ymin+1))
        for x,y,d in zip(xpix,ypix,d_list):
            im[x-xmin,y-ymin] = d
        #plt.imshow(im, origin = 'lower', aspect = 135/260, clim = [scale_lower,scale_upper])
        plt.imshow(im, origin = 'lower', aspect = 260/135, clim = [scale_lower,scale_upper])
        plt.colorbar()
        fig = plt.gcf()
        ax  = plt.gca()
   
        class EventHandler:
          def __init__(self):
            fig.canvas.mpl_connect('button_press_event', self.onpress)

          def onpress(self, event):
            if event.inaxes!=ax:
                return
            xi, yi = (int(round(n)) for n in (event.xdata, event.ydata))
            value = im.get_array()[xi,yi]
            color = im.cmap(im.norm(value))
            print(xi,yi,value,color)

        handler = EventHandler()
   
        plt.title(analysis[:-4])
        plt.show()
    
    else:
        print("lengths aren't the same for x, y and data")
        print("y is ", len(ypix))
        print("x is ", len(xpix))
        print("data is ", len(d_list))
        exit()  


maia_start = 138009
group = '75MO_W_P4_2H'
run = 378
xyfile = 138387
scale_lower = 300
scale_upper = 400


#analysis = 'radial_peak_height.npy'
#analysis = 'max_value.npy'
analysis = 'radial_peak_position.npy'
#analysis = 'summed_intensity.npy'




maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)
d_list = []
analysis_path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/mapping_stuff/"
well = np.load(analysis_path+analysis, allow_pickle=True)
for i in well:
    d_list.append(i)

#load x and y points from csv file
xpix = []
ypix = []
xy_path = f"/data/xfm/20027/analysis/xy/{xyfile}/"
with open (xy_path+str(xyfile)+"-et-marker-stage-cv.csv", newline ='') as xy:
    xyreader = csv.reader(xy,delimiter = ',')
    for row in xyreader:
        xpix.append(row[6])
        ypix.append(row[5])

plot = well_plot(d_list,xpix,ypix)

