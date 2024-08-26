import numpy as np
import matplotlib.pyplot as plt


# set data to plot here
analysis_path = "/data/xfm/20027/analysis/eiger"

# TriFPP tlc4 - decreasing temp
title = '75MO_W heating run 35-80C'
runs = [i for i in range(377, 382)]  #LC runs
groups = ["75MO_W_P4_2H"]*len(runs)
labels = runs



maia_num = 138009
dlist = []
for i, run in enumerate(runs):
    try:
        group = groups[i]
        tag = str(maia_num+run)+"_"+str(run) 
        path = analysis_path+"/"+group+"/"+tag+"/"+tag+'_sum_red.npy'
        data = np.load( path)
		#print(data.shape)
        dlist.append(data)
    except FileNotFoundError:
        continue
plist = []
for i_data, data in enumerate(dlist):
    p, = plt.plot(data[:,0],data[:,1]+100*i_data)
    plist.append(p)
plt.title(title)
plt.ylabel("Intensity (arb units)")
plt.xlabel(r'q (nm$^{-1}$)')
#plt.yscale("log")

#P6 heating and cooling legends
legend_temps = 35,37.3,48.3,52.3,55.9,59.2,62.1,64.7,67,68.9,74.5,77.6,79.9

#P3 heating and cooling legends
#legend_temps = 30,40,50,60,65,70,75
#legend_temps = 70,65,62.5,60,57.5,55,52.5,50,47.5,45,40,35,30

#No plate number heating and cooling legends
#legend_temps = 30,35,40,45,50,55,60
#legend_temps = 60,55,50,45,40,35,30
plt.legend(plist, legend_temps,loc = 'upper right')
plt.draw()
plt.show()    
