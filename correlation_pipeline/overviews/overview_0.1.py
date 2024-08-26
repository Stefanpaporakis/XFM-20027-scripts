import numpy as np
import matplotlib.pyplot as plt
import correlation_toolkit as ct


def process(run,temp,maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path):
	aspect = 125/250
	fl = ct.path_maker(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	for qslice,run,temp in zip(qslice,run,temp):
		qslice = int(qslice)	
		tag,maia_num = fl.file_finder(group,run)
		setup = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
		saxs,corr,sumd,maxd,radpp,radph = setup.load_all(init_path,qslice,width,angle_blur)
		pd = ct.plot_data(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path)
		fig,ax = plt.subplots(2,3,figsize = (10,5))
		a = ax[0,0].plot(saxs[:,0],saxs[:,1])
		ax[0,0].set_title('1-D profile')
		b = ax[1,0].plot(np.arange(0,360,2), corr)
		ax[1,0].set_title('angular correlation')
		c = ax[0,1].imshow(pd.sum_plot(sumd),origin = 'lower',aspect = aspect, clim = [16000,17200])
		ax[0,1].set_title('summed intensity')
		plt.colorbar(c,ax = ax[0,1])
		d = ax[1,1].imshow(pd.max_plot(maxd),origin = 'lower',aspect = aspect, clim = [0,30])
		ax[1,1].set_title('max value')
		plt.colorbar(d,ax = ax[1,1])
		e = ax[0,2].imshow(pd.rad_pos_plot(radpp),origin = 'lower',aspect = aspect, clim = [1,2])
		ax[0,2].set_title('radial peak position')
		plt.colorbar(e,ax = ax[0,2])
		f = ax[1,2].imshow(pd.rad_height_plot(radph),origin = 'lower',aspect = aspect, clim = [0,0.25])
		ax[1,2].set_title('radial peak height')
		plt.colorbar(f,ax = ax[1,2])
		plt.suptitle(str(temp)+chr(176),fontsize = 30)
		plt.show()
			
		
	
	
##Config stuff (required for every script that uses the toolkit)##
group = '75MO_W_P4_2H'
run = [381,383,384,385,386,387,388,389,390,391,392,393]#,384,385,386]
temp = [30,35,37.3, 48.3, 52.3, 55.9, 59.2, 62.1, 64.7, 67, 68.9, 74.5]#,79.6]
maia_num = []
tag = []
chunksize = 1
reduced_corr = False #reduced or full correlation data
init_path = f"/data/xfm/20027/analysis/"
qslice = [32,35,33,34,34,34,34,35,35,37,37,37]
angle_blur = 0
width = 0
lower = '_'
upper = '_'
analysis = '_'





process(run,temp,maia_num,group,tag,analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path)

exit()

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


