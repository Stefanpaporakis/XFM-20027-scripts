import numpy as np
import matplotlib.pyplot as plt
import correlation_toolkit as ct
from scipy.optimize import curve_fit
from scipy.stats import norm
import sys

def fit(data,amp,mu,sigma):
	return 34000*norm.pdf(data,loc = 1.35,scale = 2)

def process(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path):
	#load radpeakpos	
	dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	data = dl.load_radial_peak_position(init_path)
	return data


##Config stuff (required for every script that uses the toolkit)##
maia_start = 138009
group = '75MO_W_P4_2H'
run = [381]#,381,383,384,385,386,387,388,389,390,391,392,393]#,384,385,386]
temp = [30]#,35, 37.3, 48.3, 52.3, 55.9, 59.2, 62.1, 64.7, 67, 68.9, 74.5]#,79.6]
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
amp = 34000
sig = 55
mu = 1.35

for i in (run):
	phase_fraction = []
	maia = maia_start + i
	tags = str(maia)+"_"+str(i)
	tag = str(tags)
	maia_num = str(maia)
	data = process(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path)
	#data = [value for value in data if value>1 and value<2]
	hist,left = np.histogram(data,bins=1000)
	print(hist.mean())
	print(hist.std())
	
	#move bins to centre
	centers = left[:-1] +(left[1] - left[0])
	
	p1,_ = curve_fit(fit,centers, hist)
	
	fig,ax = plt.subplots()
	ax.hist(data,bins = 34000)
	x = np.linspace(left[0],left[-1],34000)
	data_fit = fit(x,*p1)
	ax.plot(x,data_fit)
	plt.show()
