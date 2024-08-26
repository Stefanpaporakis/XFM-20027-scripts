
import numpy as np
import matplotlib.cm as cm
import correlation_toolkit as ct
import matplotlib.pyplot as plt

##Config stuff (required for every script that uses the toolkit)##
maia_start = 138009
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
lower = [1.31,1.35,1.36,1.38,1.37,1.4,1.39,1.41,1.4,1.43,1.47,1.51]
upper = [1.43,1.45,1.48,1.5,1.52,1.53,1.52,1.51,1.56,1.58,1.66,1.64]
analysis = 'radial_peak_position.npy'

#script specific params
strt=0
nruns=12
c_vals = np.linspace(0,0.3,len(run))
colors = cm.PuOr(c_vals)[::-1]
plist = []
dlistC = []
labels = run

fl = ct.path_maker(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
tag = fl.file_finder(group,run)[0]


if reduced_corr == False:
	for tag,j in zip(tag,qslice):
		qslice = int(j)
		print(tag)
		dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
		#load corr data#
		corr = dl.load_correlation_data(init_path,qslice,width,angle_blur)
		dlistC.append(corr)
		
if reduced_corr == True:
	for tag,j,k,l,m in zip(tag,qslice,temp,lower,upper):
		qslice = int(j)
		lower = l
		upper = m
		print(tag,qslice,l,m)
		dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
		#load corr data#
		corr = dl.load_correlation_data(init_path,qslice,width,angle_blur)
		dlistC.append(corr)
	
	
for i, data in enumerate(dlistC[strt:strt+nruns]):
    p, = plt.plot(np.arange(0,360,2),data,color=colors[i])
    plist.append(p)
plt.ylabel("Correlation intensity (arb units)", fontsize=10)
plt.xlabel(r'theta (degrees)',fontsize=10)
plt.legend(plist, labels[strt:strt+nruns], loc = 'upper right') 
plt.draw()
plt.show()    
