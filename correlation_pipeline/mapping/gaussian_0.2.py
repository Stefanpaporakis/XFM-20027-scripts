import numpy as np
import matplotlib.pyplot as plt
import correlation_toolkit as ct
from scipy.optimize import curve_fit
from scipy.integrate import simps
from scipy.stats import norm
from numpy.polynomial.polynomial import polyfit
import sys


def process(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path):
	#load radpeakpos	
	dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	data = dl.load_radial_peak_position(init_path)
	return data

def gaussian(x, mu, sig, amp):
    return (amp * norm.pdf(x, mu, sig))
	
def best_fit(data,nbins,hplot):
	h,be = np.histogram(data,bins = nbins,density = True)
	bc = (be[:-1]+be[1:])/2
	properties,_ = curve_fit(gaussian,bc,h,p0 = guess)
	mu,sig,amp = properties
	print('mu is ',properties[0])
	print('sig is ',properties[1])
	print('amp is ', properties[2])
	#area gauss
	areag = amp*sig*np.sqrt(2*np.pi)
	areah = simps(h,bc)
	#percentage of each phase
	ia3d_perc = areah/areag
	ia3d_percent.append(ia3d_perc)
	print('ia3d % is '+str(ia3d_perc))
	x_gauss = np.linspace(data.min(), data.max(), 1000)
	y_gauss = gaussian(x_gauss, *properties)
	if hplot is True:
		plt.hist(data, bins=nbins, density=True)
		plt.plot(x_gauss, amp * norm.pdf(x_gauss, mu, sig),label = 'ia3d phase')
		plt.legend()
		plt.show()
	else:
		pass

def plotter(ia3d_percent,temp):
	print()
	ia3d_percent = np.array(ia3d_percent)
	temp = np.array(temp)
	intc,slope = polyfit(temp,ia3d_percent,1)
	plt.plot(temp,ia3d_percent, label = 'ia3d percentage')
	plt.plot(temp,intc+slope*temp, label = 'best fit '+str(round(slope,3)))
	print('gradient is ',slope)
	plt.legend()
	plt.xlim(0,100)
	plt.show()


	

	


##Config stuff (required for every script that uses the toolkit)##
maia_start = 138009
group = '75MO_W_P4_2H'
run = [381,383,384,385,386,387,388,389,390,391,392,393]#,384,385,386]
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


#specific params
nbins = 1000
guess = [1,1,1] #Guess mu, sig, amp
lower = 0
upper = 3
hplot = True
ia3d_percent = []
for i in run:
	#Init
	print()
	print('######## run '+str(i)+' ########')
	maia = maia_start + i
	tags = str(maia)+"_"+str(i)
	tag = str(tags)
	maia_num = str(maia)
	
	#load data and trim
	data = process(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path)
	data = [value for value in data if value is not None and value != 0]
	#data = [value for value in data if value>lower and value<upper]# restrict between params
	data = np.array(data)
	
	#make histograms and fit gaussians
	fit = best_fit(data,nbins,hplot)
	
#plot ia3d percentage
plot_perc = plotter(ia3d_percent,temp)


