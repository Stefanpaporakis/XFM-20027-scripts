import numpy as np
import matplotlib.pyplot as plt
import csv

class path_maker:
    def __init__(self,maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur):
        self.maia_num = maia_num
        self.group = group
        self.tag = tag
        self.analysis = analysis
        self.chunksize = chunksize
        self.reduced_corr = reduced_corr
        self.lower = lower
        self.upper = upper
        self.qslice = qslice
        self.width = width
        self.angle_blur = angle_blur 
        
    def file_finder(self,group,run):
        maia_start = 138009
        maia = maia_start + run
        tags = str(maia)+"_"+str(run)
        tag = str(tags)
        maia_num = str(maia)
        print(tag)
        return tag, maia_num

			
  

        
    def load_correlation_path(self,init_path):
        corr_path = init_path+f"eiger/{self.group}/{self.tag}/corr_nps{self.chunksize}/"
        if self.reduced_corr == True:
            if self.analysis == 'max_value.npy':
                analysis = 'maxpeaks'
            if self.analysis == 'radial_peak_position.npy':
                analysis = 'radpeakpos'
            if self.analysis =='summed_intensity.npy':
                analysis ='intpeaks'
            if self.analysis =='radial_peak_height.npy':
                analysis ='radpeakheight'
            corr_path = corr_path+analysis+"/"+str(self.lower)+"_"+str(self.upper)+"/reduced"
        else:
            corr_path = corr_path 
        return corr_path
    
    def load_well_path (self, init_path):
        well_path = init_path+f"eiger/{self.group}/{self.tag}/mapping_stuff/"
        return well_path
        
    def load_xy_path (self, init_path):
        xy_path = init_path+f"/xy/{self.maia_num}/"
        return xy_path
        
    def load_saxs_path (self, init_path):
        saxs_path = init_path+f"eiger/{self.group}/{self.tag}/"
        return saxs_path
        

        
        
        
class data_loader(path_maker):
	
	
	def __init__(self,maia_num, group,tag,analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur):
		super().__init__(maia_num, group,tag,analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
		self.summed_data = [] 
		self.max_data = [] 
		self.radpos_data = []
		self.radheight_data = []
	

		
		
	def load_saxs_data(self,init_path):
		saxs_path = self.load_saxs_path(init_path)
		saxs = np.load(saxs_path+self.tag+'_sum_red.npy')
		return saxs
		
	def load_correlation_data(self,init_path,qslice,width,angle_blur):
		corr_path = self.load_correlation_path(init_path)
		fulla = np.load(self.load_correlation_path(init_path)+self.tag+"_nstart400_a_correlation_sum.npy")
		fullb = np.load(corr_path+self.tag+"_nstart400_b_correlation_sum.npy")
		full = fulla+fullb
		#bg subtraction#
		bg = np.load(init_path+f'eiger/calibration/138017_8/corr/138017_8_a_correlation_sum.npy')
		bg = bg +(np.load(init_path+f'eiger/calibration/138017_8/corr/138017_8_b_correlation_sum.npy'))
		for i,j in enumerate(np.arange(full.shape[0])):
			norm = np.sum(full[i,j])/np.sum(bg[i,j])
			full[i,j,:] = full[i,j,:]-bg[i,j,:]*norm
		f_integrated_slice = np.sum(np.sum(full[qslice-width:qslice+width+1,qslice-width:qslice+width+1,:],0),0)
		f_tmp = f_integrated_slice*0.0
		for shift in range(-angle_blur,angle_blur+1): f_tmp += np.roll(f_integrated_slice,shift)
		f_integrated_slice = f_tmp
		return f_integrated_slice
	
		
	def load_summed_intensity(self,init_path):
		summed = np.load(self.load_well_path(init_path)+"/summed_intensity.npy",allow_pickle=True)
		for i in summed:
			self.summed_data.append(i)
		trim = self.trim_wells_to_xy(init_path)
		self.summed_data = self.summed_data[:trim[0]]
		return self.summed_data
	    
	def load_max_value(self,init_path):	
		maxed = np.load(self.load_well_path(init_path)+"/max_value.npy",allow_pickle=True)
		for i in maxed:
			self.max_data.append(i)
		trim = self.trim_wells_to_xy(init_path)
		self.max_data = self.max_data[:trim[0]]
		return self.max_data
		
	def load_radial_peak_position(self,init_path):
		radposition = np.load(self.load_well_path(init_path)+"/radial_peak_position.npy",allow_pickle=True)
		radposition[radposition == None] = 0
		for i in radposition:
			self.radpos_data.append(i) 
		trim = self.trim_wells_to_xy(init_path)
		self.radpos_data = self.radpos_data[:trim[0]]
		return self.radpos_data
		
	def load_radial_peak_height(self,init_path):  
		radialheight = np.load(self.load_well_path(init_path)+"/radial_peak_height.npy",allow_pickle=True)
		for i in radialheight:
			self.radheight_data.append(i)
		trim = self.trim_wells_to_xy(init_path)
		self.radheight_data = self.radheight_data[:trim[0]]
		return self.radheight_data  
    
	def trim_wells_to_xy(self,init_path):
		xpix = []
		ypix = []
		xy_path = self.load_xy_path(init_path)
		with open (xy_path+str(self.maia_num)+"-et-marker-stage-cv.csv", newline ='') as xy:
			xyreader = csv.reader(xy,delimiter = ',')
			for row in xyreader:
				xpix.append(row[5])
				ypix.append(row[6])
		xpix = np.array(xpix,dtype = 'int')
		ypix = np.array(ypix,dtype = 'int')
		xmin = min(xpix)
		ymin = min(ypix)
		xmax = max(xpix)
		ymax = max(ypix)
		xlen = int(len(xpix))
		return xlen,xmin,xmax,ymin,ymax,xpix,ypix
		
	def load_all(self,init_path,qslice,width,angle_blur):
		saxsd = self.load_saxs_data(init_path)
		corrd = self.load_correlation_data(init_path,qslice,width,angle_blur)
		sumd = self.load_summed_intensity(init_path)
		maxd = self.load_max_value(init_path)
		radppd = self.load_radial_peak_position(init_path)
		radphd = self.load_radial_peak_height(init_path)
		return {'saxs':saxsd,'correlations':corrd,'summed_intensity':sumd,
		'max_value':maxd, 'radial_peak_position':radppd, 'radial_peak_height':radphd}
		
		
		
class plot_data(data_loader):
	def __init__(self,maia_num, group,tag,analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path):
		super().__init__(maia_num, group,tag,analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)	
		setup = self.trim_wells_to_xy(init_path)
		self.image = []
		self.xmin = setup[1]
		self.xmax = setup[2]
		self.ymin = setup[3]
		self.ymax = setup[4]
		self.xpix = setup[5]
		self.ypix = setup[6]
		
	def sum_plot(self,summed_intensity):
		image = np.zeros((self.xmax-self.xmin+1,self.ymax-self.ymin+1))
		for x,y,d in zip (self.xpix,self.ypix,summed_intensity):
			image[int(x)-int(self.xmin),int(y)-int(self.ymin)] = d
		return image
		   
	def max_plot(self,max_value):
		image = np.zeros((self.xmax-self.xmin+1,self.ymax-self.ymin+1))
		for x,y,d in zip (self.xpix,self.ypix,max_value):
			image[int(x)-int(self.xmin),int(y)-int(self.ymin)] = d
		return image

	def rad_pos_plot(self,radial_peak_position):
		image = np.zeros((self.xmax-self.xmin+1,self.ymax-self.ymin+1))
		for x,y,d in zip (self.xpix,self.ypix,radial_peak_position):
			image[int(x)-int(self.xmin),int(y)-int(self.ymin)] = d
		return image
		
		
	def rad_height_plot(self,radial_peak_height):
		image = np.zeros((self.xmax-self.xmin+1,self.ymax-self.ymin+1))
		for x,y,d in zip (self.xpix,self.ypix,radial_peak_height):
			image[int(x)-int(self.xmin),int(y)-int(self.ymin)] = d
		return image







