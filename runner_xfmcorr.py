
import os
import sys
import time
import glob
#
# This script batch runs correlations
#
#
expnum = 20027
group = sys.argv[1]
runstart = int(sys.argv[2])
if len(sys.argv)>3:
	runstop = int(sys.argv[3])
else:
	runstop = runstart

configpath=f'/data/xfm/20027/python/20027_config.txt'

f
ftypes ['maxpeaks']*2
flabels = ['0_20', '20_250']

for run in range(runstart,runstop+1,1):
    start = time.perf_counter()
    
    # checking if the current run is in this group
    globcheck = glob.glob(f'/data/xfm/{expnum}/raw/eiger/{group}/*_{run}')
    # if they don't exist
    if len(globcheck) ==0: continue
    
    
    flags = "--xfmgroup "+group+" --run "+str(run)+" --xfmconfig "+configpath
    os.system("python ./pypadf/xfmcorr.py --config ./configs/config_xfmcorr_20027.txt "+flags)
    stop = time.perf_counter()
    print("time (s) to correlate run:", stop-start) 	
