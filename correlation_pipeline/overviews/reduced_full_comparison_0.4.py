import numpy as np
import matplotlib.pyplot as plt
import correlation_toolkit as ct
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator

def frm_integration(frame, unit="q_nm^-1", npt=2250):
        """
        Perform azimuthal integration of frame array
        :param frame: numpy array containing 2D intensity
        :param unit:
        :param npt:
        :return: two-col array of q & intensity.
        """
        #print("Debug - ", self.cam_length, self.pix_size, self.wavelength)
        ai = AzimuthalIntegrator()
        ai.setFit2D(directDist=0.64/1000,
                    centerX=517.0902,
                    centerY=543.7068,
                    pixelX=75e-6,
                    pixelY=75e-6)
        ai.wavelength = 0.67018e-10
        integrated_profile = ai.integrate1d(data=frame, npt=npt, unit=unit)
        return np.transpose(np.array(integrated_profile))

def process(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur):
	rwell = []
	
	#full data
	reduced_corr = False
	fdl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	fwell = fdl.load_radial_peak_position(init_path)
	fcorr = fdl.load_correlation_data(init_path,qslice,width,angle_blur)
	full_2D_data = np.load(fdl.load_saxs_path(init_path)+'summed_diffraction.npy')
	full_one_d= frm_integration(full_2D_data)


	#reduced  data
	reduced_corr = True
	rdl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	for i in fwell:
		rwell_data = np.where((i >=lower)and(i<=upper),i,0)
		rwell.append(rwell_data)
	rcorr = rdl.load_correlation_data(init_path,qslice,width,angle_blur)
	red_2D_data = np.load(rdl.load_correlation_path(init_path)+'_diffraction.npy')
	red_one_d = frm_integration(red_2D_data)
	return fwell, rwell, fcorr, rcorr,full_2D_data,red_2D_data,full_one_d,red_one_d





###Config stuf from correlation toolkit
maia_start = 138009
group = '75MO_W_P4_2H'
run = [381,383]#, 385, 387]#,384,385,386,387,388,389,390,391,392,393]#,384,385,386]
temp = [30,35]#,48.3,55.9]#, 37.3, 48.3, 52.3, 55.9, 59.2, 62.1, 64.7, 67, 68.9, 74.5]#,79.6]
maia_num = []
tag = []
chunksize = 1
reduced_corr = '_' #reduced or full correlation data
init_path = f"/data/xfm/20027/analysis/"
qslice = [32,35]#,33,34]#,35,33,33]
angle_blur = 0
width = 0
lower = [1.31, 1.35]#,1.38,1.4]
upper = [1.43,1.45,]#1.5,1.53]
analysis = 'radial_peak_position.npy'

#Script specific
aspect = 125/250

fl = ct.path_maker(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)

for qslice,lower,upper,run,temp in zip(qslice,lower,upper,run,temp):
	tag,maia_num = fl.file_finder(group,run)
	qslice = int(qslice)
	pd = ct.plot_data(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path)
	fwell, rwell, fcorr, rcorr,full_2D_data,red_2D_data,full_one_d,red_one_d = process(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	fig,ax = plt.subplots(2,3)#,figsize = (15,5))
	a = ax[0,0].imshow(pd.rad_pos_plot(fwell),origin = 'lower',aspect = aspect, clim = [lower,upper])
	plt.colorbar(a,ax = ax[0,0])
	ax[0,0].set_title('full')
	b = ax[0,1].imshow(pd.rad_pos_plot(rwell),vmin = lower, vmax = upper,origin = 'lower',aspect = aspect, clim = [lower,upper])
	plt.colorbar(b,ax = ax[0,1])
	ax[0,1].set_title('filtered '+str(lower)+" "+str(upper))
	ax[0,2].plot(np.arange(0,360,2),fcorr, label = 'full')
	ax[0,2].plot(np.arange(0,360,2),rcorr, label =str(lower)+" "+str(upper)+ ' filtered')
	ax[0,2].legend()
	ax[1,0].imshow(full_2D_data)
	ax[1,0].set_title('full')
	ax[1,1].imshow(red_2D_data)
	ax[1,1].set_title('filtered '+str(lower)+" "+str(upper))
	ax[1,2].plot(full_one_d[:,0],full_one_d[:,1], label ='full')
	ax[1,2].plot(red_one_d[:,0],red_one_d[:,1], label = 'filtered '+str(lower)+" "+str(upper))
	ax[1,2].legend()
	plt.suptitle("run "+str(run)+", "+str(temp)+chr(176)+' rad peak pos ',fontsize = 20)
	plt.show()
	


