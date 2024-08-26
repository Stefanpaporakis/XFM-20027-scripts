
import os
import sys

#don't change these
refnum, refrun = 99118, 43

#
# This script batch runs padf calculations
#
#
group = sys.argv[1]
runstart =sys.argv[2]
if len(sys.argv)>3:
	runstop =sys.argv[3]
    tag = sys.argv[4]
else:
	runstop = runstart
    tag = sys.argv[3]


for run in range(runstart,runstop+1,1):
    xfmno = refnum + run - refrun
    dataid = str(xfmno)+"_"+str(run)
    #set up correlation filename   
    datapath =  "/data/xfm/18580/analysis/eiger/SAXS/"+group+"/"+dataid+"/corr/"
    fname = datapath+dataid+suffix+".npy"
    flags = "--fname "+fname+" --outpath "+datapath+" --tag "+tag
    os.system("python ./pypadf/corrtopadf.py --config ./configs/config_xfm_padf.txt "+flags)
