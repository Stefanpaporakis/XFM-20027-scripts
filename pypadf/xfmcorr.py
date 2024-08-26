
import numpy as np
import array
import os
import glob
import params.paramsCORRXFM as params
import fxstools.padfio as padfio
import fxstools.correlation as correlation
import pathlib
#from ... import fluxfm
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import fluxfm
import h5py

if __name__ == '__main__': 
    

    print("\n-------------------------------------------------------------------------")
    print(" difftocorr.py : calculate correlation function from diffraction patterns" )
    print("-------------------------------------------------------------------------")

    #
    # set up parameter class
    #
    p = params.paramsCORRXFM()

    print("pypadf version ",p.version,"\n")

    #
    # Read input parameters from a file
    #
    p.read_config_file()
    print('pa: x')
    p.qmax_calc()

	# read the data frame list, if required
    if p.dlistflag==True:
        dlist = np.loadtxt( p.dlistfile, skiprows=1, delimiter = '	')[:,3:]
		
    #
    # Set up XFM class
    #
    refnum, refrun = 138016, 7
    print("xfmconfig", p.xfmconfig)
    dset = fluxfm.XfmHfiveDataset(configpath=p.xfmconfig)
    dset.group = p.xfmgroup
    run_num = p.run
    dset.tag = f'{dset.maia_num + run_num}_{run_num}'
    dset.dpath = f'{dset.dpath}{dset.group}/{dset.tag}/'
    dset.apath = f'{dset.apath}{dset.group}/{dset.tag}/'
    print(dset.dpath)
    print(dset.apath)
    dset.grab_dset_members()
    run = p.run
    xfmno = refnum + run - refrun
    runtag = str(xfmno)+"_"+str(run)
    print("tag check", dset.tag, runtag) 
    if p.dlistflag:
        p.outpath = pathlib.Path(dset.apath+f"corr_nps{p.npatsum}/{p.filtertype}/{p.filterlabel}/") #STEFAN HAS CHANGED THIS FOR MAPPING
    else:
        p.outpath = pathlib.Path(dset.apath+f"corr_nps{p.npatsum}/")
    p.tag = runtag+"_nstart"+str(p.nstart)
    if os.path.exists(p.outpath.resolve())==False:
          os.makedirs(p.outpath.resolve())
    dset.scratch = p.outpath.resolve()

    outname = p.makefname( p.outpath, p.tag, "_xfmcorr_parameter_log", ".txt")
    p.write_params_to_file( outname )
    #print("debug xfmcorr", p.nstart, p.npatterns)
    #exit()
    #
    # Loop over the h5 data files
    #
    for k, h5 in enumerate(dset.h5ls[:p.run_limit]):
         print('<fluxfm.overview> h5:', h5)
         print('<fluxfm.overview> Reading:', dset.dpath + h5)        
         with h5py.File(dset.dpath + h5) as f:
             d = np.array(f['entry/data/data'])
             #print('dlist is',dlist)
             if p.dlistflag==True:
                 framemask = dlist[dlist[:,0]==k+1,1].astype(np.int)
                 print("framemask shape is", framemask.shape)
                 d = d[framemask,:,:]
                 print("reduced data frames", d.shape, framemask.shape, dlist.shape)
             print("h5 data shape", d.shape)
             h5tag = p.tag+"_h5file"+str(k+1)
             if k == 0:
                 dset.run_data_array = d
                 dset.mask = np.load(dset.apath+runtag+"_mask.npy") #dset.gen_mask(d[0], max_lim=dset.max_px_count)
                 p.maskflag = True
                 print(f'mask shape: {dset.mask.shape}')
                 p.nx = d.shape[1]
                 p.ny = d.shape[2]
                 
                 if p.npatsum>1:
                      s = d[::p.npatsum,:,:].shape
                      npatnew = s[0]
                      dsum = np.zeros( s ) 
                      for i in range(p.npatsum):
                           ns = d[i::p.npatsum,:,:]
                           dsum[:ns.shape[0],:,:] += ns   
                
                      nstart = p.nstart//p.npatsum
                      npatterns = p.npatterns//p.npatsum
                      writecorrfreq = p.writecorrfreq//p.npatsum
                      if nstart+npatterns>=npatnew:
                          npatterns = npatnew-nstart-1
                 else:
                        nstart = p.nstart
                        npatterns = p.npatterns
                        writecorrfreq = p.writecorrfreq
                        dsum = d
                 #
                 # Set up an instance of the correlation class
                 #
                 corr = correlation.correlation(path=p.outpath, tag=h5tag, fromlist=False, dps=dsum,
                     nx=p.nx, ny=p.ny, wl=p.wl, pw=p.pw, dz=p.dz, nth=p.nth,
                     nthreads=p.nthreads, npatterns=npatterns, 
                     bg_estimate=p.bg_estimate,
                     mask_flag=p.maskflag, crop_flag=p.cropflag, 
                     nxcrop=p.nxcrop, nycrop=p.nycrop,
                     dp_shift_flag=p.dp_shift_flag, 
                     shiftx=p.shiftx, shifty=p.shifty,
                     maskname=dset.apath+runtag+'_mask.npy', rebin=p.rebin, nstart=nstart,
                     diffcorr=p.diffcorrflag, outputdp=p.outputdp, writecorrfreq=writecorrfreq,
                     qbmin=p.qbmin, qbmax=p.qbmax)

                 if p.cropflag == True:  
                     corrsum = np.zeros( (corr.nqb, corr.nqb, p.nth, 2) )
                 else:
                     corrsum = np.zeros( (corr.nqb, corr.nqb, p.nth, 2) )

             corr.tag = h5tag
             d[d>4.29e9] = 0
             corr.dps = d

             #
             # calculate the correlation function
             #
             print("\nPerforming Correlations\n")
             corrh5 = corr.calculate_correlation()
             corrsum += corrh5
             #outname = p.outpath / (h5tag+"_a_correlation_sum.npy")
             outname = p.outpath / (h5tag+"_a_correlation_sum.npy")  #append diff or bg as appropriate
             np.save( outname, corrh5[:,:,:,0] ) 
             print("Written correlation sum:", outname)
             #outname = p.outpath / (h5tag+"_b_correlation_sum.npy") 
             outname = p.outpath / (h5tag+"_b_correlation_sum.npy")  #append diff or bg as appropriate
             np.save( outname, corrh5[:,:,:,1] ) 
             print("Written correlation sum:", outname)
             print("\n")

    #
    # write the correlation function to file
    #
    #outname = p.outpath+p.tag+"_correlation_sum.dbin"  #append diff or bg as appropriate
    #padfio.write_dbin( outname, corrsum ) 
    outname = p.outpath / ('reduced'+p.tag+"_a_correlation_sum.npy")  #append diff or bg as appropriate
    np.save( outname, corrsum[:,:,:,0] ) 
    print("Written correlation sum:", outname)
    outname = p.outpath / ('reduced'+p.tag+"_b_correlation_sum.npy")  #append diff or bg as appropriate
    np.save( outname, corrsum[:,:,:,1] ) 
    print("Written correlation sum:", outname)
    print("Correlations Done.")
