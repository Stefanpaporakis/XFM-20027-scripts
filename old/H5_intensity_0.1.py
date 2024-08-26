

#This script calculates the intensity of a well from its given H5 files,
#X and Y positions are from /data/xfm/analysis/xy/group number/
#Will plot intensity map when finished, but use "show_well_map" to play around
#once done






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


maia_start = 138009


group = '75MO_W_P4_2H'
run = 383
maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)
xyfile = 138392

d_list = []
raw_path = f"/data/xfm/20027/raw/eiger/{group}/{tag}/"
analysis_path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"

#load x and y points from csv file
xpix = []
ypix = []
xy_path = f"/data/xfm/20027/analysis/xy/{xyfile}/"
with open (xy_path+str(xyfile)+"-et-marker-stage-cv.csv", newline ='') as xy:
    xyreader = csv.reader(xy,delimiter = ',')
    for row in xyreader:
        xpix.append(row[5])
        ypix.append(row[6])

print('xy file found and loaded')

files = sorted(glob.glob(raw_path+"*_data*.h5"))
for i in files:
    h5 = h5py.File(i,'r')
    #print(h5['/entry/data/data/Dataset/'].keys())
    d1 = np.array((h5['entry/data/data']), dtype = 'int')
    #print (d1.shape)
    d1[d1>4.29e9] = 0  #setting high pixel values to zero
    for j in range(d1.shape[0]):
        dsum = np.sum(d1[j,:,:])
        d_list.append(dsum)
print ("Appended data into list with length ",len(d_list))
print( "Number of zero intensity points:", np.sum(np.array(d_list)==0))

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
    plt.imshow(im, origin = 'lower', aspect = 135/260)
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
    np.save(analysis_path+'full_well_map.npy',im)
    plt.show()
    
else:
    print("lengths aren't the same for x, y and data")
    print("y is ", len(ypix))
    print("x is ", len(xpix))
    print("data is ", len(d_list))
    exit()




