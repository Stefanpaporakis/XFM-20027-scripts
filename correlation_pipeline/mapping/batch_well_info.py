

#X and Y positions are from /data/xfm/analysis/xy/group number/
#Will caclulate intesntiy, peak height, radial peak pos, r, max val for each frame






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
from scipy.signal import find_peaks
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator


def frm_integration(frame, unit="q_nm^-1", npt=2250):
        """
        Perform azimuthal integration of frame array
        :param frame: numpy array containing 2D intensity
        :param unit:
        :param npt:
        :return: two-col array of q & intensity.
        """
        #print("Debug - ", self.cam_length, self.pix_size, self.wavelength)
        ai = AzimuthalIntegrator()
        ai.setFit2D(directDist=0.64/1000,
                    centerX=517.0902,
                    centerY=543.7068,
                    pixelX=75e-6,
                    pixelY=75e-6)
        ai.wavelength = 0.67018e-10
        integrated_profile = ai.integrate1d(data=frame, npt=npt, unit=unit)
        return np.transpose(np.array(integrated_profile))
def well_plot(d_list,xpix,ypix): 
    print ("Appended data into list with length ",len(d_list))
    print( "Number of zero points:", np.sum(np.array(d_list)==0))

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
        #np.save(analysis_path+'full_well_map.npy',im)
        plt.show()
    
    else:
        print("lengths aren't the same for x, y and data")
        print("y is ", len(ypix))
        print("x is ", len(xpix))
        print("data is ", len(d_list))
        exit()  
def sum_intensity(d):
    summed_data = np.sum(d)
    return summed_data
def max_val(d):
    maximum = np.max(d)
    #if maximum>100:   #Turn these on if there are outliers in max
     #   maximum = 0
    return maximum
def peak_info(d):
        max_peak_height = None
        max_peak_position = None
        max_peak_position_q = None
        one_d_slice = frm_integration(d)
        #print(type(one_d_slice), one_d_slice.shape)
        peaks, properties = find_peaks(one_d_slice[:1500,1])
        if peaks.size>0:
            peak_heights = one_d_slice[peaks,1]
            max_peak_idx = np.argmax(peak_heights)
            max_peak_height = peak_heights[max_peak_idx]
            max_peak_position = peaks[max_peak_idx] 
            max_peak_position_q = one_d_slice[max_peak_position,0]
        return max_peak_height, max_peak_position, max_peak_position_q
    
    
#don't chage these##########
refnum, refrun = 138490, 481
############################

dataset = "75MO_W_P4_2H"
runs = [i for i in range(377,379)]  #LC runs
groups = [dataset]*len(runs)



for i, run in enumerate(runs):
    summed_intensity_list = []
    max_value_list = []
    max_peak_position_list = []
    max_peak_height_list = []
    try: 
        group = groups[i]
        xfmno = refnum + run - refrun
        tag = str(xfmno)+"_"+str(run)
        
        raw_path = f"/data/xfm/20027/raw/eiger/{group}/{tag}/"
        analysis_path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"
        files = sorted(glob.glob(raw_path+"*_data*.h5"))
        for i in files:
            h5 = h5py.File(i,'r')
    #print(h5['/entry/data/data/Dataset/'].keys())
            d1 = np.array((h5['entry/data/data']), dtype = 'int')
            print (d1.shape)
            
            d1[d1>4.29e9] = 0  #setting high pixel values to zero
                 
            #SUMMED INTENSITY# REMEMBER TO UNHASH THE SAVE FILE AT THE END!!!!!
            #for j in range(d1.shape[0]):
             #   #if j%100==0:print(j)
              #  dsum = sum_intensity(d1[j,:,:]) #sums intensites
               # summed_intensity_list.append(dsum)
            #print('finished summed intensities, starting max values')
            
            #MAX VALUE#
            #for j in range(d1.shape[0]):
             #   #if j%100==0:print(j)
              #  dmax = max_val(d1[j,:,:])# finds the max value for each frame
               # max_value_list.append(dmax)
            #print('finished max values, starting radial peak info')
             
            #RADIAL PEAK INFO#
            for j in range(d1.shape[0]):
                if j%100==0:print(j)
                max_peak_height, max_peak_positions, max_peak_position_q = peak_info(d1[j,:,:])
                #dintegral_plot = peak_info(d1[j,:,:])
                max_peak_position_list.append(max_peak_position_q)
                max_peak_height_list.append(max_peak_height)
            print('peak info finished, saving data')
            
        pathlib.Path(analysis_path+'/mapping_stuff/').mkdir(parents = True,exist_ok = True)
        #np.save(analysis_path+'/mapping_stuff/'+'summed_intensity',np.array(summed_intensity_list))
        #np.save(analysis_path+'/mapping_stuff/'+'max_value',np.array(max_value_list))
        np.save(analysis_path+'/mapping_stuff/'+'radial_peak_position',np.array(max_peak_position_list))
        #np.save(analysis_path+'/mapping_stuff/'+'radial_peak_height',np.array(max_peak_height_list))
        #plot = well_plot(d_list,xpix,ypix) #plots well map of chosen parameters
    
    except FileNotFoundError:
        continue






