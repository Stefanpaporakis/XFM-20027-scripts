"""
correlation.py

Tools to calculate an angular intensity correlation function
from a directory of diffraction patterns

Classes:
    correlation

Functions:
    random_oddeven_index

"""

import os
import numpy as np
import multiprocessing as mp
import sys

#from padfpy import diffraction
#from padfpy import io
import fxstools.padfio as io
import fxstools.correlationTools as crtls
import time

# for debugging
# import matplotlib.pyplot as plt

def random_oddeven_index( npatterns, oddeven):
    """Random index between 0 and npatterns-1
       
    Parameters
    ----------
    npatterns : int
        number of diffraction patterns in dataset
    
    oddeven : int
        0 - return an even index
        1 - return an odd index 

    Returns
    -------
    m : int
        integer between 0 an npatterns-1
        integer can be odd or even according to the value of oddeven
    """

    m = np.int(np.random.rand() * npatterns/2)
    if oddeven==0:
        m = 2*m
    elif oddeven==1:
        m = 2*m+1
    if m >= npatterns: m = npatterns-1
    return m



#
# ----------------------------------------------------------------
# Calculate the correlation
#
#

class correlation:
    """ 
    Tools to calculate Angular intensity correlation functions 
    from a directory of diffraction patterns

    Attributes
    ----------
    path : str
        path to save output of the correlation calculation

    tag : str
        prefix for all output file names
        (used not to overwrite previous calculations)

    flist : list (str)
        list of file names (strings) for diffraction images
        including paths (used if fromlist is True)

    dps : numpy array (3 dimensions)
        array of diffraction patterns 
        (used if fromlist is False)

    fromlist : Bool
        if TRUE read diffraction patterns from flist,
        if FALSE use diffraction patterns from dps

    nx : int
`       number of rows in input diffraction array

    ny : int
        number of columns in input diffraction array


    nth : int
        number of angular samples
        must be the same in q-space and real-space

    wl : float
        wavelength of the incident beam. Units: metres

    nthreads : int
        number of CPU processes to use

    dz : float
        sample to detector distance. Units: metres

    pw : float
        width of detector pixel. Units: metres
    
    npatterns: int
        number of diffraction patterns to process

    nstart : int
        index of first diffraction pattern to process (default 0)

    mask_flag : bool
        Correct correlation with mask correlation function (True/False)
    
    maskname : str
        path and filename of mask image to use (if maskflag is True)
        Mask takes values 0 for pixels to ignore and 1 for pixels to include.

    rebin : int
        rebinning factor. Must be a power of 2 (e.g. 2, 4, 8, 16)
        if set to 1, then diffraction patterns are not rebinned

    diffcorr : bool
        Calculate a difference correlation (True/False)    

    outputdp : bool
        Write out diffraction patterns to file (True/False)

    dp_shift_flag : bool
        Shift the centre of the diffraction patterns (True/False)

    shiftx : float
        amount (in pixels) to shift centre of diffraction pattern (row coordinate)
        Only used if dpshiftflag is True.
        Non-integer shifts are interpolated.
    
    shifty : float
        amount (in pixels) to shift centre of diffraction pattern (column coordinate)
        Only used if dpshiftflag is True.
        Non-integer shifts are interpolated.

    nxcrop : int
        number of rows in cropped diffraction pattern.
        Diffraction pattern will be cropped if nxcrop and nycrop are positive integers.

    nycrop : int
        number of columns in cropped diffraction pattern.
    
    bg_estimate : bool
        Calculate the background correlation (True/False)
    """

        


    def __init__(self, path="/scratch/amartin1", tag="tag", flist=[], dps=[],
                 nx=128, ny=-1, wl=1e-10, pw=1.0, dz=1.0, nth=200,
                 nthreads=1, npatterns=100, bg_estimate=False,
                 mask_flag=0, crop_flag=0, nxcrop=0, nycrop=0,
                 dp_shift_flag=0, shiftx=0, shifty=0,
                 maskname="None", rebin=-1, nstart=0,
                 diffcorr=False, outputdp=False, fromlist=True, writecorrfreq=100000000,
                 qbmin=-1,qbmax=-1):

        """Constructs the correlation class
        """

        self.wl = wl
        self.pixel_width = pw
        self.detector_z = dz
        self.path = path
        self.tag = tag
        self.cx = nx // 2
        self.cy = ny // 2
        self.nth = nth
        self.nx = nx
        self.bg_estimate = bg_estimate
        self.diffcorrflag = diffcorr
        self.outputdp = outputdp
        self.flist = flist
        self.dps = []
        self.fromlist = fromlist
        self.writecorrfreq = writecorrfreq
        self.qbmin=qbmin
        self.qbmax=qbmax
        self.ny = ny
        if self.ny<0:
            self.ny=self.nx
        self.pwx = pw
        self.pwy = pw

        # other parameters
        self.nthreads = nthreads
        self.npatterns = npatterns
        self.nstart = nstart

        # flags
        self.mask_flag = mask_flag
        self.maskname = maskname
        self.crop_flag = crop_flag
        self.nxcrop = nxcrop
        self.nycrop = nycrop
        self.dp_shift_flag = dp_shift_flag
        self.shiftx = shiftx
        self.shifty = shifty
        self.rebin = rebin

        self.nxorig = self.nx
        self.nyorig = self.ny

        if self.crop_flag == 1:
            self.nx = int(nxcrop)
            self.ny = int(nycrop)
            self.cx = self.nx // 2
            self.cy = self.ny // 2
        #print("Debug rebin some more", self.rebin)
        self.set_rebin_flag()

        if self.rebin_flag == 1:
            self.nx = self.nx//rebin
            self.ny = self.ny//rebin
            self.pixel_width *= rebin
            self.cx = self.nx // 2
            self.cy = self.ny // 2
           
        if self.qbmax<0: self.qbmax = self.nx // 2
        if self.qbmin<0: self.qbmin = 0
        self.nqb = self.qbmax-self.qbmin
        print("debug correlation.py qbmin qbmax", self.qbmin, self.qbmax)

        self.inputType = 'dir'
        self.datafilename = None
        self.sym_filter = 0
        self.correlation_sum_name = None

        self.xshift_list = []
        self.yshift_list = []

        self.inputpath = "None"
        self.inputtag = "None"
       
        self.ac = crtls.angular_correlation() 
        self.qbins = self.ac.qbins( self.nx//2, self.nx//2, self.detector_z, 
                                         self.wl, self.pixel_width )
        #print(self.cx, self.cy,"check in init")

    def write_corr_config(self, corrfname="correlation_config.txt"):
        """
        Write all correlation parameters to a log file       
 
        Parameters
        ----------
        corrfname : str
            name of parameter log file (including path)        
        """ 
        fcorr = open(corrfname, 'w')
        fcorr.write("input = " + self.dpname + '\n')
        if self.bg_estimate:
            fcorr.write("inputb = " + self.dpname2 + '\n')
        if self.bg_estimate:
            fcorr.write("Xflag = 1\n")
        fcorr.write("outpath = " + self.path + '\n')
        fcorr.write("tag = " + self.tag + '\n')
        fcorr.write("wavelength =  " + str(self.wl) + '\n')
        fcorr.write("pixel_width =  " + str(self.pixel_width) + '\n')
        fcorr.write("detector_z =  " + str(self.detector_z) + '\n')
        fcorr.write("cx =  " + str(self.cx) + '\n')
        fcorr.write("cy =  " + str(self.cy) + '\n')
        fcorr.write("nth =  " + str(self.nth) + '\n')
        fcorr.write("nx =  " + str(self.nx) + '\n')
        fcorr.write("ny =  " + str(self.ny) + '\n')
        fcorr.write("pwx = " + str(self.pwx) + '\n')
        fcorr.write("pwy = " + str(self.pwy) + '\n')
        fcorr.close()

    def calculate_correlation(self):

        """
        Calculate the angular intensity correlation from the diffraction patterns
        The difference correlation or background correlation may also be calculated
        depending on flag settings.
        
        Returns
        -------
        corrsum : numpy array (floats)
            summed correaltion function from all the data        
        """ 
        #print("Debug 1 - correlation.py")
        if self.mask_flag == 1:
            maskname = self.maskname  # self.path+self.tag+"_mask_processed.dbin"
            mask = io.read_image(maskname, nx=self.nxorig, ny=self.nyorig).astype(np.float64)
            mask *= 1.0 / np.max(mask)
            # print "DEBUG <correlation.py calculate_correlation()> mask.shape", mask.shape
            mask_scb = self.shift_crop_bin(mask, True)

        # copy the following lines to the main script
        if self.fromlist==True:
            if self.npatterns > len(self.flist):
                self.npatterns = len(self.flist)
                print("npatterns larger than length of flist. Npatterns reset to length of flist.", self.npatterns)
        else:
            if self.npatterns > (self.dps.shape[0]-self.nstart):
                self.npatterns = self.dps.shape[0]-self.nstart
                print("npatterns larger than first dimension of diffraction pattern data array. npatterns reset to length to the number of diffraction patterns", self.npatterns)

        manager = mp.Manager()            
        return_dict = manager.dict()
        #pcorr = np.zeros( (self.nthreads, self.nx // 2, self.nx // 2, self.nth) )
        #corrsum = np.zeros( (self.nx // 2, self.nx // 2, self.nth, 2) )
        #corrblk = np.zeros( (self.nx // 2, self.nx // 2, self.nth, 2) )
        pcorr = np.zeros( (self.nthreads, self.nqb, self.nqb, self.nth) )
        corrsum = np.zeros( (self.nqb, self.nqb, self.nth, 2) )
        corrblk = np.zeros( (self.nqb, self.nqb, self.nth, 2) )
        icount, icountsum = 0,0
        for i in np.arange(self.npatterns // self.nthreads):
            processes = []
            d = []
            start = time.perf_counter() 
            for j in np.arange(self.nthreads):
                m = i * self.nthreads + j + 1 + self.nstart
                #print("correlation i, j, m", i, j, m, len(self.flist))
                #if not self.bg_estimate:
                #    print("Calculating correlation ", str(int(m-self.nstart)), "/", self.npatterns, " Pattern no:", int(m))
                #elif self.bg_estimate:
                #    print("Calculating background cross-correlation ", m)

                # Jack 31.10
                if self.fromlist:
                    if self.npatterns > len(self.flist):
                        print("WARNING: npatterns greater than number of files in dir...")
                        print("...quitting")
                        quit()
                
                oddeven = (i*self.nthreads+j)%2

                if (self.bg_estimate is True) or (self.diffcorrflag is True):
                    m = random_oddeven_index( self.npatterns, oddeven )
                    if self.fromlist:
                        image = io.read_image(self.flist[m - 1], nx=self.nxorig, ny=self.nyorig)
                    else:
                        image = self.dps[m-1,:,:]
                    m2 = m
                    while m2==m:
                        m2 = random_oddeven_index( self.npatterns, oddeven)
                    if self.fromlist:
                        image2 = io.read_image(self.flist[m2 - 1], nx=self.nxorig, ny=self.nyorig)
                    else:
                        image2 = self.dps[m2-1,:,:]
                else:
                    if self.fromlist:
                        image = io.read_image(self.flist[m - 1], nx=self.nxorig, ny=self.nyorig)
                    else:
                        image = self.dps[m-1,:,:]
                #print("debug max(image):", np.max(image) )


                # shift diffraction pattern
                if self.dp_shift_flag == 1:
                    if not len(self.xshift_list) == 0:
                        self.shiftx = self.xshift_list[m - 1]
                    if not len(self.yshift_list) == 0:
                        self.shifty = self.yshift_list[m - 1]

                    #print("DEBUG <correlation.py> shiftx shifty", self.shiftx, self.shifty)
                    image = self.array_shift(image, self.shiftx, self.shifty)

                    if (self.bg_estimate is True) or (self.diffcorrflag is True):
                        if not len(self.xshift_list) == 0:
                            self.shiftx = self.xshift_list[m2 - 1]
                        if not len(self.yshift_list) == 0:
                            self.shifty = self.yshift_list[m2 - 1]

                        image2 = self.array_shift(image2, self.shiftx, self.shifty)

                # crop diffraction pattern
                if self.crop_flag == 1:
                    image = self.crop_image(image, self.nxcrop)
                    if (self.bg_estimate is True) or (self.diffcorrflag is True):
                        image2 = self.crop_image(image2, self.nxcrop)

                # rebin image
                #print("Ok now we rebin if required, rebin_flag=",self.rebin_flag)
                if self.rebin_flag == 1:
                    image = self.rebin_pattern(image, self.rebin)
                    if (self.bg_estimate is True) or (self.diffcorrflag is True):
                        image2 = self.rebin_pattern(image2, self.rebin)
                    #print("DEBUG renbinning diffration pattern", image.shape)
               
                # mask diffraction pattern
                if self.mask_flag == 1:
                    #print("dp mask applied")
                    image *= mask_scb
                    if (self.bg_estimate is True) or (self.diffcorrflag is True):
                        image2 *= mask_scb

                self.nx = image.shape[0]
                #print("<correlation.py: calculate_correlation(): self.nx image.dtype", self.nx, image.shape, image.dtype)
                #print("debug <correlation.py> image max:", np.max(image))
                
                if self.outputdp:
                    #self.dpname = self.path + tag + "diffraction_" + str(j) + ".dbin"
                    #io.write_dbin(self.dpname, image)
                    self.dpname = io.makefname( self.path, self.tag, "diffraction_"+str(j), ".npy")               
                    np.save(self.dpname, image)
 
                if self.diffcorrflag is True:
                    image = image - image2
                
                if (self.bg_estimate is True):
                    d.append([image, image2])
                else:
                    d.append([image])

            for j in np.arange(self.nthreads):
                #print("Main threading loop", j)
                #print( "cx cy check", self.cx, self.cy)
                p = mp.Process(target=self.corr_calc, args=(d[j],j,return_dict))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()

            
            for j in np.arange(self.nthreads):
                #print( return_dict[j].type() )        `               `       
                oddeven = (i*self.nthreads+j)%2
                corrsum[:,:,:,oddeven] += return_dict[j] 
                corrblk[:,:,:,oddeven] += return_dict[j] 
                #print( "max corrsum:", np.max(corrsum), np.max(return_dict[j]) ) 
            
            stop = time.perf_counter()
            print(i+1, "/", self.npatterns//self.nthreads,f'  Chunked correlations {self.nthreads} took (i.e. all threads to finish)', stop-start," seconds") 
            icount+=self.nthreads
            if (icount>=self.writecorrfreq):
                icountsum +=icount
                outname = io.makefname( self.path, self.tag+"_a_", "npat"+str(icountsum)+"_correlation_sum", ".npy")
                np.save( outname, corrblk[:,:,:,0]/float(icount) )
                outname = io.makefname( self.path, self.tag+"_b_", "npat"+str(icountsum)+"_correlation_sum", ".npy")
                np.save( outname, corrblk[:,:,:,1]/float(icount) )
                corrblk*=0.0
                icount = 0

        corrsum *= 1.0 / float(self.npatterns)
        return corrsum

    def corr_calc(self, dps, j, return_dict):        
        """
        Calculate the angular correlation function of a single diffraction pattern
        or difference correlation of two patterns
        
        Parameters
        ----------
        dps : list (numpy arrays 2D)
            one or two diffraction patterns stored in a list
            if two patterns are provided, a difference correlation is calculated

        j : int
            index of thread
    
        return_dict : multiprocessing manager object
            stores the output

        """ 
        polar = self.ac.polar_plot_with_qbins( dps[0], self.qbins, self.nth, 0, 2*np.pi, self.cx, self.cy, False)
        #dpname = self.path + self.tag + "polar_" + str(j) + ".npy"
        #print( "debug corr_calc, cx, cy", self.cx, self.cy)
        #np.save( dpname, polar )
        if len(dps) == 2:
            polar2 = self.ac.polar_plot_with_qbins( dps[1], self.qbins, self.nth, 0, 2*np.pi, self.cx, self.cy, False)
        else:
            polar2 = polar
        #pcorr[j,:,:,:] = self.ac.polarplot_angular_intershell_correlation( polar, polar2)
        #print( "max pcorr:", np.max(pcorr), np.max(dps[0]) ) 
        return_dict[j] =  self.ac.polarplot_angular_intershell_correlation( polar, polar2,qbmin=self.qbmin,qbmax=self.qbmax)   


    def radial_profile_to_correlation(self, rad=np.ones(1)):
        """
        Maps a 1D radial profile to a correlation volume using an outer product.
        Useful for a type of background estimate

        Parameters
        ----------
        rad : numpy array
            1D array containing the radial intensity values

        Returns
        -------
        corr_out : numpy array
            3D array storing the correlation volume generated from 
            the radial profile
        """ 

        if rad.size == 1: rad = np.ones(self.nx // 2)

        corr_out = np.zeros((self.nx // 2, self.nx // 2, self.nth))
        for i in np.arange(self.nth):
            corr_out[:, :, i] = np.outer(rad, rad)

        return corr_out

    #
    # this should be sufficient for both hpfilter and the gaussian filter
    #
    def filter(self, filter=np.ones(1),
               ftailin="_padfcorr_correlation_sum.dbin",
               ftailout="_padfcorr_correlation_sum.dbin"):
        """
        
        Parameters
        ----------

        Returns
        -------
        
        """ 

        if filter.size == 1:
            filter = np.ones(self.nx // 2, self.nx // 2, self.nth)
        # routine to modify correlation with a hp filter
        cs = io.read_correlation(self.path + self.tag + ftailin)
        cs = cs.reshape(self.nx // 2, self.nx // 2, self.nth)
        cs *= filter
        io.write_dbin(self.path + self.tag + ftailout, cs)
        # add option not to overwrite??

    # routine to symmeterize the correlation function
    #
    # symmetry noise filter
    #
    def symmetry_filter(self, cs, width=10):
        """
        Remove the correlation data near theta=0
        using Friedel symmetry        

        Parameters
        ----------
        cs : vol object
            input correlation function

        width : int
            number of pixels to cut either side of zero

        Returns
        -------
        csmod : vol object
            correlation volume with symmetry filter applied        
        """ 

        cs = io.read_correlation(self.path + self.tag + ftailin)
        cs = cs.reshape(self.nx // 2, self.nx // 2, self.nth)

        filter = cs * 0.0
        filter[:, :, width:self.nth - width] = 1.0
        csmod = (cs * filter + np.roll(cs * filter, self.nth // 2, 2)) / (filter + np.roll(filter, self.nth // 2, 2))
        return csmod
    #
    # Divide by mask function correlation
    #
    def mask_correction(self, cs, mask):
        """
        Apply a mask correction to a correlation volume.
        Calculate the mask correlation

        Parameters
        ----------
        cs : vol object
            input correlation function

        mask : numpy array (floats)
            input mask array
    
        Returns
        -------
        corr_masked : vol object
            mask-corrected correlation volume        
        """ 

        maskcorr = io.read_correlation(self.path + self.tag + "_mask_correlation.dbin")
        #        print "DEBUG <correlation.py; mask_correlation()> maskcorr.shape", maskcorr.shape
        maskcorr = maskcorr.reshape(self.nx // 2, self.nx // 2, self.nth)
        imaskcorr = np.where(maskcorr > 0.05 * np.max(maskcorr))
        cs = io.read_correlation(self.path + self.tag + ftailin)
        cs = cs.reshape(self.nx // 2, self.nx // 2, self.nth)
        corr_masked = cs * 0.0
        #        print "DEBUG <correlation.py; mask_correlation()> cs.shape, maskcorr.shape", cs.shape, maskcorr.shape
        corr_masked[imaskcorr] = cs[imaskcorr] / maskcorr[imaskcorr]
        return corr_masked

    #
    # Subtract background correlation function 
    #
    def subtract_correlation(self, cs, csbg):
        """
        Subtract two correlation volumes        
        
        Parameters
        ----------
        cs : vol object
            input correlation volume

        csbg : vol object
            input background correlation volume

        Returns
        -------
        background subtracted volume
        
        """ 
        return cs-csbg

    # shift - a 2D version of numpy's roll
    #    def array_shift(self,array,xshift=0,yshift=0):
    #
    #        nx, ny = array.shape[0], array.shape[1]
    #        nx0 = nx - nx/2
    #        ny0 = ny - ny/2
    #        tmp = np.zeros( (nx*2, ny*2) )
    #        tmp[ nx-nx/2:nx+nx/2+1, ny-ny/2:ny+ny/2+1] = array
    #        tmp[ nx0:nx0+nx, ny0:ny0+ny] = array
    #
    #        tmp = np.roll(tmp,xshift,0)
    #        tmp = np.roll(tmp,yshift,1)
    #
    #        array = tmp[ nx0:nx0+nx, ny0:ny0+ny]
    #
    #	array = np.roll(array,xshift,0)
    #	array = np.roll(array,yshift,1)
    #	return array

    # shift - a 2D version of numpy's roll
    # with sub-pixel shifts
    # interpolation by nearest neighbour interpolation
    def array_shift(self, array, xshiftin=0.0, yshiftin=0.0):
        """
        2D version of numpy's roll with sub-pixel shifts
        interpolation by nearest neighbour interpolation.
        Shifts can be sub-pixel, i.e. with decimals
        
        Parameters
        ----------
        array : numpy array
            2D numpy array
        
        xshiftin : float
            shift in number of rows. Unit: pixels

        yshiftin : float
            shift in number of columns. Unit: pixels


        Returns
        -------
        array : numpy array
            shifted array
        """ 
        # print("JACK DEBUG: array[0,0]", array[0,0])
        # print("JACK DEBUG: xshiftin, yshiftin = ",xshiftin,yshiftin)
        xshift = int(xshiftin)
        yshift = int(yshiftin)
        # print("JACK DEBUG: xshift, yshift = ", xshift, yshift)
        xrem = xshiftin - xshift
        yrem = yshiftin - yshift
        # print("JACK DEBUG: xrem, yrem = ",xrem,yrem)
        if xrem >= 0.0:
            mx = 0
            alpha = xrem
        else:
            mx = -1
            alpha = 1 + xrem

        if yrem >= 0.0:
            my = 0
            beta = yrem
        else:
            my = -1
            beta = 1 + yrem
        # print("JACK DEBUG: xshift, yshift, xrem, yrem", xshift, yshift, xrem, yrem)
        # print("JACK DEBUG: mx, my, alpha, beta", mx, my, alpha, beta)
        nx, ny = array.shape[0], array.shape[1]
        # print("JACK DEBUG array shape", np.shape(array))
        nx0 = nx - nx // 2
        ny0 = ny - ny // 2
        # print("JACK DEBUG <correlation.py>: nx0, ny0 =", nx0, ny0)
        tmp = np.zeros((nx * 2, ny * 2))
        # print("JACK DEBUG, shape tmp", np.shape(tmp))
        #        tmp[ nx-nx/2:nx+nx/2+1, ny-ny/2:ny+ny/2+1] = array
        tmp[nx0:nx0 + nx, ny0:ny0 + ny] = array
        # integer shift
        tmp = np.roll(tmp, xshift, 0)
        tmp = np.roll(tmp, yshift, 1)

        # sub-pixel shift
        tmpsum = (1 - alpha) * (1 - beta) * np.roll(np.roll(tmp, mx, 0), my, 1)
        tmpsum += alpha * (1 - beta) * np.roll(np.roll(tmp, (mx + 1), 0), my, 1)
        tmpsum += (1 - alpha) * beta * np.roll(np.roll(tmp, mx, 0), (my + 1), 1)
        tmpsum += alpha * beta * np.roll(np.roll(tmp, (mx + 1), 0), (my + 1), 1)

        tmp = tmpsum

        array = tmp[nx0:nx0 + nx, ny0:ny0 + ny]
        return array


    # noinspection PyMethodMayBeStatic
    def crop_image(self, image, nxcrop, nycrop=-1):
        """
        crop an (2D) image array
        
        Parameters
        ----------
        image : numpy array
            input image to be cropped

        nxcrop : int
            no. of rows in cropped array

        nycrop : int
            no. of columns in cropped array
            (if not set, assumed equal to nxcrop)

        Returns
        -------
        dcrop : numpy array
            array of cropped values
        
        """ 

        #print("DEBUG <correlation.py; crop_image> nxcrop", nxcrop)
        if nycrop == -1:
            nycrop = nxcrop

        dcrop = np.zeros((nxcrop, nycrop))
        nx, ny = image.shape[0], image.shape[1]
        #print("DEBUG <correlation.py; crop_image> nx ny", nx, ny, nxcrop, nycrop)
        # print("JACK DEBUG:  <correlation.py; crop_image>  type nx and ny",type(nx),type(nxcrop))

        xoffset = 0
        xlow = nx // 2 - (nxcrop // 2)
        if xlow < 0:
            xlow = 0
            xoffset = (nxcrop - nx) // 2

        yoffset = 0
        ylow = ny // 2 - (nycrop // 2)
        if ylow < 0:
            ylow = 0
            yoffset = (nycrop - ny) // 2

        xhigh = nx // 2 + (nxcrop // 2)
        if xhigh > nx:
            xhigh = nx

        yhigh = ny // 2 + (nycrop // 2)
        if yhigh > ny:
            yhigh = ny

        #        print "DEBUG <correlation.py: crop_image> x/yoffset, x/ylow, x/yhigh", xoffset, yoffset,\
        #            xlow, ylow, xhigh, yhigh, dcrop.shape, image.shape
        dcrop[:, :] = image[xoffset + xlow:xoffset + xhigh, yoffset + ylow:yoffset + yhigh]
        #        dcrop[xoffset+xlow:xoffset+xhigh,yoffset+ylow:yoffset+yhigh] = image[xlow:xhigh,ylow:yhigh]
        #        dcrop[:,:] = image[nx/2-(nxcrop/2):nx/2+(nxcrop/2),ny/2-(nycrop/2):ny/2+(nycrop/2)]
        #        plt.imshow( image )
        #        plt.figure()
        #        plt.imshow( dcrop )
        #        plt.draw()
        #        plt.show()
        return dcrop

    #    def rebin_pattern(self, image, nbin ):
    #
    #        imagesum = image * 0.0
    #        for i in np.arange( nbin)-nbin/2:
    #            for j in np.arange( nbin)-nbin/2:
    #                imagesum += np.roll(np.roll( image, i, 0), j, 1)
    #        imagesum *= 1.0/float(nbin*nbin)
    #        out = imagesum[::nbin,::nbin]
    #        return out

    def rebin_pattern(self, imagein, nbin):
        """
        Rebin a diffraction pattern by a power of 2
        
        Parameters
        ----------
        imagein : numpy array (floats)
            2D array to be rebinned

        nbin : int
            rebinning factor (power of 2)
            

        Returns
        -------
        out : numpy array
            rebinned array
        
        """ 
        image = np.copy(imagein)
        # nearest neighbour interpolation for even rebin values
        #        if( (nbin%2)==0):
        #            imagesum = image * 0.0
        #            for i in np.arange( nbin)-nbin/2:
        #                for j in np.arange( nbin)-nbin/2:
        #                    imagesum += np.roll(np.roll( image, i, 0), j, 1)
        #                image *= imagesum/float(nbin*nbin)
        # rebinning

        imagesum = image * 0.0

        for i in np.arange(nbin) - nbin // 2:
            for j in np.arange(nbin) - nbin // 2:
                imagesum += np.roll(np.roll(image, i, 0), j, 1)
        imagesum *= 1.0 / float(nbin * nbin)
        out = imagesum[::nbin, ::nbin]
        return out

    def set_nxcrop_and_nycrop(self, nxcrop, nycrop=-1):
        """
        Sets the number of rows and columns in cropped array.
        Result is attributes nx, ny are equal to nxcrop, nycrop
        cx, cy are set to the middle of the cropped array.
        Assumes beam centred is located at image center.
        
        Parameters
        ----------
        nxcrop : int
            number of rows in cropped array

        nycrop : int
            number of columns in cropped array
        
        """ 

        self.nxcrop = nxcrop
        self.nx = nxcrop
        self.cx = self.nx // 2

        if nycrop == -1:
            self.nycrop = nxcrop
            self.ny = nxcrop
            self.cy = self.nx // 2
        else:
            self.nycrop = nycrop
            self.ny = nycrop
            self.cy = self.ny // 2

    def set_rebin_flag(self):
        """
        Sets a flag to determined if image is rebinned.
        if rebin attribute is not default value (-1), then flag is set to 1. 
        """ 

        #print("Debug rebin even more",self.rebin, self.nx, self.ny)
        if (self.rebin != -1) \
                and (self.rebin < self.nx) and (self.rebin < self.ny) \
                and (self.rebin > 0):

            self.rebin_flag = 1
        else:
            self.rebin_flag = 0
        #print("debug rebin flag", self.rebin_flag )

    def binary_mask(self, mask, tol=0.99):
        """
        Ensures mask is normalised to a maximum value of 1.
        Mask values below max(mask)*tol are set to zero.

        Parameters
        ----------
        mask : numpy array (float)
            input mask values

        tol : float
            tolerance between 0 and 1
            to be multiplied by the max(mask) value

        Returns
        -------
        mask : numpy array (float)
            approximate binary mask
        """ 

        mask *= 1.0 / np.max(mask)
        ilow = np.where(mask < tol * np.max(mask))
        mask[ilow] = 0.0
        return mask

    def shift_crop_bin(self, image, binarize=False):
        """
        Recentres, crops, rebins diffraction pattern
        according to flags set 
        (dp_shift_flag, crop_flag, rebin_flag)        

        Parameters
        ----------
        image : numpy array
            image to process

        binarize : bool
            make the final image binary (approximately)
            only useful for masks

        Returns
        -------
        tmp : numpy array
            processed image
        """ 

        tmp = np.copy(image)

        # shift diffraction pattern
        if self.dp_shift_flag == 1:
            tmp = self.array_shift(image, self.shiftx, self.shifty)

        # crop diffraction pattern
        if self.crop_flag == 1:
            tmp = self.crop_image(tmp, self.nxcrop)

        # rebin image
        if self.rebin_flag == 1:
            tmp = self.rebin_pattern(tmp, self.rebin)

        if binarize == True:
            tmp = self.binary_mask(tmp)

        return tmp

    def calculate_mask_correlation(self, dontreadfile=False):
        """
        Calculates the angular corrrelation of the mask file
        [DEBUG: may not currenlty work!]
 
        Parameters
        ----------
        dontreadfile : bool
            If True, then mask is set to a value of 1 everywhere
            If False, mask is read from file

        Returns
        -------
         N/A
         [TODO: verify the final location of the mask correlation]
        
        """ 

        if (dontreadfile == True):
            mask = np.ones((self.nxorig, self.nyorig))
        else:
            mask = io.read_image(self.maskname, nx=self.nxorig, ny=self.nyorig).astype(np.float64)
            mask *= 1.0 / np.max(mask)
            #print("DEBUG <correlation.py; calculate_mask_correlation> mask.shape", mask.shape, mask.dtype)

        mask = self.shift_crop_bin(mask, True)

        # shift diffraction pattern
        #        if self.dp_shift_flag == 1:
        #            mask = self.array_shift(mask, self.shiftx, self.shifty)

        #         # crop diffraction pattern
        #        if self.crop_flag == 1:
        #            mask = self.crop_image(mask, self.nxcrop)

        # rebin image
        #        if self.rebin_flag == 1:
        #            mask = self.rebin_pattern( mask, self.rebin )
        #            mask = self.binary_mask( mask )

        tag = self.tag
        self.tag = tag + "_mask"
        maskname = self.path + self.tag + "_processed.dbin"
        io.write_dbin(maskname, mask)
        #     print "DEBUG <correlation.py; calculate_mask_correlation> processsed mask.shape", mask.shape, mask.dtype
        self.dpname = maskname
        self.corrfname = self.path + self.tag + "_corr_config.txt"
        self.write_corr_config(self.corrfname)
        self.corr_calc(self.corrfname)
        self.tag = tag


    def set_inputpath(self):
        """
        Sets the inputpath (tag) to equal the output path and tag
        """ 
        if self.inputpath == "None":
            self.inputpath = self.path
        if self.inputtag == "None":
            self.inputtag = self.tag
