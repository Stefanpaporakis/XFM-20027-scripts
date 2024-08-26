




#Dont use this one, old script for mapping intensity that didn't really work 
#but might have some good ideasin it for later

print("dont use this script")
#exit()






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

#######################################
#dont touch

maia_start = 138009

#Stuff for setting up the x and y axis to plot the well map
# X Axis steps
def generate_x_list(start,end,cycles):
    values = []
    for _ in range(cycles):
        values.extend(list(range(start,end+1)))
        values.extend(list(range(end,start-1,-1)))
    return values
 
 # Y Axis steps
def generate_y_axis_values(y_initial,x_steps,y_steps,iterations):
    y_values = []
    for _ in range(iterations):
        y_values.extend([y_initial]*x_steps)
        y_initial -=y_steps
    return y_values
    
def d_list_to_array( d_list, x_steps, iterations):
	d_arr = np.array(d_list).reshape( (x_steps,iterations) )
	d_arr[::2,:] = d_arr[::2,::-1]
	return d_arr
	
#############################################    
#do touch  
  
#Number of steps down and across:
y_steps = 0.004 #steps down the well (0.004)
x_steps = 250 #steps across the well (0.002)
iterations = 125#int(10) # how many times we step down the well
cycles = 63# int(62.5)#int(0.5*iterations) # how many times we step across the well

#X axis parameters:
x_step_init = 0 #Starting value of well profile
#x_step_final = 63  #At what value we turn around and go back

#Y axis parameters:
y_initial = 1 # top of the scan


group = '50MO_EtAN_P6_3H'
run = 490
maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)

d_list = []
raw_path = f"/data/xfm/20027/raw/eiger/{group}/{tag}/"
analysis_path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr/"

files = sorted(glob.glob(raw_path+"*_data*.h5"))
for i in files:
    h5 = h5py.File(i,'r')
    print(h5['/entry/data/data/'].keys())
    exit()
    d1 = np.array((h5['entry/data/data']), dtype = 'int')
    #print (d1.shape)
    d1[d1>4.29e9] = 0  #setting high pixel values to zero
    for j in range(d1.shape[0]):
        dsum = np.sum(d1[j,:,:])
        d_list.append(dsum)
print ("Appended data into list with length ",len(d_list))
print ("reshaping list to fit")

print( "Number of zero intensity points:", np.sum(np.array(d_list)==0))
d_list = d_list[:-3044] #34294-31250
print ("list is now of length", len(d_list))



#generate x and y lists
print("generating x and y axis")
y = generate_y_axis_values(y_initial, x_steps, y_steps, iterations)
x = generate_x_list(x_step_init,x_steps,cycles)
x = x[:-376] 
#x = x[:10000]
#y = y[:10000]

#for i in range(0,100,1):
    #d_list.append(i)

#check if x, y and data is the same length
if len(y)==len(x)==len(d_list):
    print("lengths are the same, plotting well map")
    #cs = plt.scatter(x,y,c = d_list,cmap = plt.cm.jet)
    d_arr = d_list_to_array( d_list, iterations, x_steps) #iterations)
    im = plt.imshow(d_arr)
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
    plt.show()
else:
    print("lengths aren't the same for x, y and data")
    print("y is ", len(y))
    print("x is ", len(x))
    print("data is ", len(d_list))
    exit()




