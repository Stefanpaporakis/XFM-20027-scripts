import correlation_toolkit as ct
import numpy as np
import matplotlib.pyplot as plt





##Config stuff (required for every script that uses the toolkit)##
maia_start = 138009 ### DONT TOUCH##
group = '75MO_W_P4_2H'
run = 383
temp = 52.3
maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)
chunksize = 1
reduced_corr = False #reduced or full correlation data
init_path = f"/data/xfm/20027/analysis/"
qslice = 32
angle_blur = 0
width = 0
lower = '_' 
upper = '_'
analysis = '_'

###params to play with:
metric = 'summed_intensity'
aspect = 125/250
clim = 	[16000,17200]


#load data#
dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
all_data = dl.load_all(init_path,qslice,width,angle_blur)

#plot data#
pd = ct.plot_data(maia_num, group,tag,analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path)
plt.imshow(pd.sum_plot(all_data[metric]),origin = 'lower',aspect = aspect, clim = clim)
plt.title(str(run)+', '+str(temp)+chr(176)+ ', '+str(metric))
plt.colorbar()
plt.show()
