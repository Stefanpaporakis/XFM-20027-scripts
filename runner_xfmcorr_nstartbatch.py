
import os
import sys
import time
#
# This script batch runs correlations
#
#
group = sys.argv[1]
run = int(sys.argv[2])
npatterns = int(sys.argv[3])
nstart = int(sys.argv[4])
if len(sys.argv)>5:
	nstop = int(sys.argv[5])
else:
	nstop = nstart

configpath=f'/data/xfm/20027/python/20027_config.txt'
print("Dont use runner batch for xfm corr!!!!!")
exit()
for ns in range(nstart,nstop+npatterns,npatterns):
    start = time.perf_counter()
    flags = "--xfmgroup "+group+" --run "+str(run)+" --xfmconfig "+configpath+" --nstart "+str(ns)+" --npatterns "+str(npatterns)
    os.system("python ./pypadf/xfmcorr.py --config ./configs/config_xfmcorr_20027.txt "+flags)
    stop = time.perf_counter()
    print("time (s) to correlate run:", stop-start) 	
