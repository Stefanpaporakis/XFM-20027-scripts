import numpy as np
import glob
import h5py
import hdf5plugin
import matplotlib.pyplot as plt
import os
import pathlib
import correlation_toolkit as ct


def process(raw_path,dlist,all_data):
	for k, h5 in enumerate(sorted(glob.glob(raw_path+"*_data*.h5"))):
		with h5py.File(h5) as f:
			print('looking at ', h5)
			d = np.array(f['entry/data/data'])
			d[d>4.29e9] = 0
			full = d
			print('h5 shape is',d.shape)
			framemask = dlist[dlist[:,0]==k+1,1].astype(np.int)-1
			nframemask = framemask[(framemask >=0)&(framemask <d.shape[0])]
			d = d[nframemask,:,:]
			print("reduced h5 to ", d.shape)
			if all_data is None:
				all_data = np.sum(d,axis = 0)
				full_image = np.sum(full,axis = 0)
			else:
				all_data +=np.sum(d,axis = 0)
				full_image += np.sum(full,axis = 0)
	return full_image, all_data



group = '75MO_W_P4_2H'
run = [381,383,384,385,386,387,388,389,390,391,392,393]
temp = [30,35,37.3, 48.3, 52.3, 55.9, 59.2, 62.1, 64.7, 67, 68.9, 74.5]#,79.6]
lower = [1.31,1.35,1.36,1.38,1.37,1.4,1.39,1.41,1.4,1.43,1.47,1.51]
upper = [1.43,1.45,1.48,1.5,1.52,1.53,1.52,1.51,1.56,1.58,1.66,1.64]
maia_num = []
tag = []
chunksize = 1
reduced_corr = False #reduced or full correlation data
init_path = f"/data/xfm/20027/analysis/"
qslice = [32,35,33,34,34,34,34,35,35,37,37,37]
angle_blur = 0
width = 0
analysis = '_'





if int(len(run)) == int(len(lower)) ==  int(len(upper)):
	pass
else:
	print('cant run script, check you groups')
	print('run length ',len(run))
	print('lower length ', len(lower))
	print('upper length ', len(upper))
	exit()

fl = ct.path_maker(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)

for run,lower,upper in zip(run,lower,upper):
	all_data = None
	tag,maia_num = fl.file_finder(group,run)
	dlist = np.loadtxt(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/mapping_stuff/radpeakpos/{str(lower)}_{str(upper)}_xy_peaks.txt", skiprows=1, delimiter = '	')[:,3:]
	raw_path = f"/data/xfm/20027/raw/eiger/{group}/{tag}/"
	outpath = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps1/radpeakpos/{str(lower)}_{str(upper)}/"
	full_image, all_data = process(raw_path,dlist,all_data)
	plt.imshow(full_image)
	plt.savefig(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"+'summed_diffraction.png')
	plt.close()
	fig,ax = plt.subplots(1,2,figsize = (10,5))
	a = ax[0].imshow(full_image)
	ax[0].set_title('full diffraction image')
	b = ax[1].imshow(all_data)
	ax[1].set_title('reduced ')# + str(lower) + ', '+str(upper) = ' difraction image')
	image = plt.imshow(all_data)
	if os.path.exists(outpath)==False:
          os.mkdir(outpath)
	np.save(outpath+'reduced_diffraction.npy',all_data)
	np.save(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"+'summed_diffraction.npy',full_image)
	plt.savefig(outpath+'reduced_image.png')
	plt.close()

