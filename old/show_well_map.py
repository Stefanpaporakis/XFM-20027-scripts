
import numpy as np
import matplotlib.pyplot as plt
import glob
import pathlib 
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
        plt.imshow(im, origin = 'lower',aspect = 84/260, clim = [scale_lower,scale_upper])
        #plt.imshow(im, origin = 'lower', aspect = 260/135, clim = [scale_lower,scale_upper])
        plt.colorbar()
        fig = plt.gcf()
        ax  = plt.gca()   
        plt.title(str(run)+" "+analysis[:-4])
        plt.show()
    
    else:
        print("lengths aren't the same for x, y and data")
        print("y is ", len(ypix))
        print("x is ", len(xpix))
        print("data is ", len(d_list))
        exit()  


maia_start = 138009
group = '75MO_W_P4_2H'
run = 383
xyfile = int(maia_start)+int(run)
#scale_lower =0
#scale_upper =100  #Standard for max val
#scale_lower = 16000
#scale_upper = 18500 #Standard for summed intensity
scale_lower = 300
scale_upper = 400 #Standard for rad peak position
#scale_upper =1 #Standard for rad peak height
#scale_lower = 0



#analysis = 'radial_peak_height.npy'
#analysis = 'max_value.npy'
analysis = 'radial_peak_position.npy'
#analysis = 'summed_intensity.npy'




maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)
d_list = []
analysis_path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/mapping_stuff/"
well = np.load(analysis_path+analysis, allow_pickle=True)
print(well.shape)



for i in well:
    #if i>700:
     #   i = 0 #Filter outliers
    d_list.append(i)

#load x and y points from csv file
xpix = []
ypix = []
xy_path = f"/data/xfm/20027/analysis/xy/{xyfile}/"
with open (xy_path+str(xyfile)+"-et-marker-stage-cv.csv", newline ='') as xy:
    xyreader = csv.reader(xy,delimiter = ',')
    for row in xyreader:
        xpix.append(row[5])
        ypix.append(row[6])
plot = well_plot(d_list,xpix,ypix)


