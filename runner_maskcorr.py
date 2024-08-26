
import os
import sys

#don't change these
refnum, refrun = 99118, 43

#
# This script batch masks the correlation functions
#
#
group = sys.argv[1]
runstart =sys.argv[2]
if len(sys.argv)>4:
	runstop =sys.argv[3]
    suffix = sys.argv[4]
else:
	runstop = runstart
    suffix = sys.argv[3]

for run in range(runstart,runstop+1,1):
    xfmno = refnum + run - refrun
    dataid = str(xfmno)+"_"+str(run)
    #set up correlation filename   
    datapath =  "/data/xfm/18580/analysis/eiger/SAXS/"+group+"/"+dataid+"/corr/"
    fname = datapath+dataid+suffix+".npy"
    flags = "--fname "+fname+" --outpath "+datapath+" --suffix "+suffix
    os.system("python ./pypadf/maskcorr.py --config ./configs/config_xfm_mask.txt "+flags)
