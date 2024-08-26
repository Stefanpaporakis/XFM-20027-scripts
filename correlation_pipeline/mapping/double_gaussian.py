import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit
import correlation_toolkit as ct

def process(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path):
	#load radpeakpos	
	dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	data = dl.load_radial_peak_position(init_path)
	return data
	

def gaussian(x, mu1, sigma1, amp1, mu2, sigma2, amp2):
    return (amp1 * norm.pdf(x, mu1, sigma1)) + (amp2 * norm.pdf(x, mu2, sigma2))
	
	
	
	

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
bins = 1000
guess = [1,1,1,1,1,1] # mean, std, amp for 2 gaussians

for i in (run):
	#Init
	maia = maia_start + i
	tags = str(maia)+"_"+str(i)
	tag = str(tags)
	maia_num = str(maia)
	#load data and trim
	data = process(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path)
	#print(len(data))
	data = [value for value in data if value is not None and value != 0]
	#print(len(data))
	data = np.array(data)
	h,be = np.histogram(data,bins = bins,density = True)
	bc = (be[:-1]+be[1:])/2
	properties,_ = curve_fit(gaussian,bc,h,p0 = guess)
	mu1,sig1,amp1,mu2,sig2,amp2 = properties
	#area of first gauss
	area_ia3d = amp1*sig1*np.sqrt(2*np.pi)
	#area of second gauss
	area_other = amp2*sig2*np.sqrt(2*np.pi)
	#total area
	area_total = area_ia3d+area_other
	#percentage of each phase
	ia3d_perc = area_ia3d/area_total*100
	other_perc = area_other/area_total*100
	# Output the percentages and means
	print('ia3d % is '+str(ia3d_perc)+', with mean at '+str(mu1))
	print('second phase % is '+str(other_perc)+', with mean at '+str(mu2))
	





	# Plot the histogram with the fitted Gaussian components
	x_gauss = np.linspace(data.min(), data.max(), 1000)
	y_gauss = gaussian(x_gauss, *properties)

	plt.hist(data, bins=bins, density=True)
	plt.plot(x_gauss, y_gauss)
	plt.plot(x_gauss, amp1 * norm.pdf(x_gauss, mu1, sig1))
	plt.plot(x_gauss, amp2 * norm.pdf(x_gauss, mu2, sig2))
	plt.legend(['Total Fit', 'ia3d gauss', 'other gauss'])
	plt.show()


