import numpy as np
import matplotlib.pyplot as plt
import correlation_toolkit as ct
from scipy.stats import norm
from scipy.integrate import quad
import matplotlib.mlab as mlab
import sys


def process(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path):
	#load radpeakpos	
	dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	data = dl.load_radial_peak_position(init_path)
	return data
	
def best_fit(data,nbins):
	
	print('initial guess amp, mean and sigma.')
	ams_str = input()
	ams = ams_str.split()
	amp = float(ams[0])
	mu = float(ams[1])
	sig= float(ams[2])
	
	h,be= np.histogram(data,bins = nbins)
	centers = (be[:-1] + be[1:])/2
	data_ar = np.zeros(len(data))
	data_ar[:]=data
	#(mu,sig) = norm.fit(data_ar)
	fit = np.linspace(min(data_ar),max(data_ar))
	gauss = norm.pdf(fit,mu,sig)
	gauss = gauss*amp
	plt.plot(be[:-1],h)
	plt.plot(fit,gauss)
	#plt.xlim(1.3,1.45)
	plt.show()
	area = np.trapz(gauss,fit)
	print("area under curve is ", area)


	


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
nbins = 34000
lower = 1
upper = 2


for i in (run):
	#Init
	maia = maia_start + i
	tags = str(maia)+"_"+str(i)
	tag = str(tags)
	maia_num = str(maia)
	#load data and trim
	data = process(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path)
	data = [value for value in data if value>lower and value<upper]#trim data between upper and lower
	mean = np.mean(data)
	std = np.std(data)
	print("mean is ", mean)
	print("std is ", std)
	#make histogram and fit gaussian
	retry = True
	while retry:
		fit = best_fit(data,nbins)
		response = input('try again? (y/n)')
		if response != 'y':
			retry = False

