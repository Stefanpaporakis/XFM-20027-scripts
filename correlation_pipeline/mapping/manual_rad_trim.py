import numpy as np
import matplotlib.pyplot as plt
import correlation_toolkit as ct
import sys


def reduction(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path, aspect):
	#load radpeakpos
	dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	data = dl.load_radial_peak_position(init_path)
	
	
	#make histogram and map
	pd = ct.plot_data(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path)
	
	fig,ax = plt.subplots(1,2)
	fig.subplots_adjust(top = 0.6)
	a = ax[0].hist(data,bins =1000,range = (1,2),width = 0.004)
	ax[0].set_title('histogram')
	b = ax[1].imshow(pd.rad_pos_plot(data),origin = 'lower',aspect = aspect, clim = [1,2])
	ax[1].set_title('radial peak position map')
	plt.colorbar(b,ax = ax[1])
	plt.suptitle(i)
	plt.show()
	
	print('trim to? (lower,upper)')
	lower,upper = input().split()
	lower = float(lower)
	upper = float(upper)
	#reduce data by upper and lower
	booldata = [j if lower<=j<=upper else 0 for j in data] 

	#plot reduced data
	
	fig,ax = plt.subplots(1,2)
	fig.subplots_adjust(top = 0.6)
	a = ax[0].hist(booldata,bins =1000,range = (1,2),width = 0.004)
	ax[0].set_title('reduced histogram')
	b = ax[1].imshow(pd.rad_pos_plot(booldata),origin = 'lower',aspect = aspect, clim = [lower,upper])
	ax[1].set_title('reduced radial peak position map')
	plt.colorbar(b,ax = ax[1])
	plt.suptitle(i)
	plt.show()
	
	redata = np.nonzero(booldata)[0]
	print('data reduced from '+str(len(data))+ ' to ' + str(len(redata)))
	fraction = (len(redata)/len(data))*100
	return fraction
	


##Config stuff (required for every script that uses the toolkit)##
maia_start = 138009
group = '75MO_W_P4_2H'
run = [390,391,392,393]#,384,385,386]
temp = [30,35, 37.3, 48.3, 52.3, 55.9, 59.2, 62.1, 64.7, 67, 68.9, 74.5]#,79.6]
maia_num = []
tag = []
chunksize = 1
reduced_corr = False #reduced or full correlation data
init_path = f"/data/xfm/20027/analysis/"
qslice = []
angle_blur = []
width = []
lower = '_' 
upper = '_'
analysis = '_'




aspect = 125/250
ia3d_percent = []
for i in (run):
	phase_fraction = []
	maia = maia_start + i
	tags = str(maia)+"_"+str(i)
	tag = str(tags)
	maia_num = str(maia)
	
	#Rety loop (if you want to trim differently)
	retry = True
	while retry:
		process = reduction(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path, aspect)
		response = input('try again? (y/n)')
		if response != 'y':
			retry = False
			ia3d_percent.append(str(process))
	print('moving on to next dataset')
	
with open (init_path+f'eiger/{group}/fraction.txt', 'w') as f:
	string = (f'{run},{temp},{ia3d_percent}')
	f.write(string+'\n') 
ia3d_percent= [eval(k) for k in ia3d_percent]
plt.plot(temp,ia3d_percent)
plt.xlim(0,100)
plt.xlabel('temp')
plt.ylabel('ia3d percentage')
plt.show()

	
