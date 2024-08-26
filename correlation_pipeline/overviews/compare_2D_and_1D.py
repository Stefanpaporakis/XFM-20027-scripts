import numpy as np
import matplotlib.pyplot as plt
import correlation_toolkit as ct
import fluxfm
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
	full_leg = 'full'
	red_leg = 'restricted between '+str(lower)+' and '+str(upper)
	
	#1D and 2D
	full_2D_data = np.load(dl.load_saxs_path(init_path)+'summed_diffraction.npy')
	red_2D_data = np.load(dl.load_correlation_path(init_path)+analysis+'/'+str(lower)+'_'+str(upper)+'/reduced_diffraction.npy')
	full_one_d= frm_integration(full_2D_data)
	red_one_d = frm_integration(red_2D_data)

	#correlations
	
	
	
	
	fig,ax = plt.subplots(1,3)
	ax[0].plot(full_one_d[:,0],full_one_d[:,1], label = full_leg)
	ax[0].plot(red_one_d[:,0],red_one_d[:,1], label = red_leg)
	ax[0].legend()
	ax[1].imshow(full_2D_data)
	ax[1].set_title(full_leg)
	ax[2].imshow(red_2D_data)
	ax[2].set_title(red_leg)
	plt.show()
	
###Config stuf from correlation toolkit
temp = 37.3
maia_num = '_'
tag = '_'
chunksize = 1
reduced_corr = '_' #reduced or full correlation data
init_path = f"/data/xfm/20027/analysis/"
group = '75MO_W_P4_2H'
angle_blur = '_'
width = '_'
analysis = 'radpeakpos'


#Stuff we need to change per sample
qslice = 34
run = 383
lower = 1.35
upper = 1.45



fl = ct.path_maker(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
tag,maia_num = fl.file_finder(group,run)
dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)

process(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)





