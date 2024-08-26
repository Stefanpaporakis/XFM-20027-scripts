
import sys
import numpy as np
import os

#don't change these
refnum, refrun = 138110, 101

# set up run and id numbers for the dataset
group = sys.argv[1]
run = int(sys.argv[2])
suffix = sys.argv[3]    #a or b
xfmno = refnum + run - refrun
dataid = str(xfmno)+"_"+str(run)


#load the correlation data
datapath =  "/data/xfm/19545/analysis/eiger/"+group+"/"+dataid+"/corr/"
fname = datapath+dataid+"_"+suffix+"_correlation_sum.npy"

flags = " -f "+fname+" -o "+datapath+" --suffix "+suffix
print(flags)
os.system("python ./pypadf/plotfxs3d.py --config ./configs/config_xfmcorr_plot.txt "+flags)
