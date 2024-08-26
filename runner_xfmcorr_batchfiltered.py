
import os
import sys
import time
import glob

class runinfo():
    def __init__(self,group,run,ftype,flabel):
        self.group = group
        self.run = run
        self.ftype = ftype
        self.flabel = flabel



#
# This script batch runs correlations
#
#
expnum = 20027


configpath=f'/data/xfm/20027/python/20027_config.txt'

batch = []
batch.append( runinfo('75MO_W_P4_2H',381,'radpeakpos','1.43_1.9') )
batch.append( runinfo('75MO_W_P4_2H',383,'radpeakpos','1.45_1.9') )
batch.append( runinfo('75MO_W_P4_2H',384,'radpeakpos','1.48_1.9') )
batch.append( runinfo('75MO_W_P4_2H',385,'radpeakpos','1.5_1.9') )
batch.append( runinfo('75MO_W_P4_2H',386,'radpeakpos','1.52_1.9') )
batch.append( runinfo('75MO_W_P4_2H',388,'radpeakpos','1.52_1.9') )
batch.append( runinfo('75MO_W_P4_2H',389,'radpeakpos','1.51_1.9') )
batch.append( runinfo('75MO_W_P4_2H',390,'radpeakpos','1.56_1.9') )
batch.append( runinfo('75MO_W_P4_2H',391,'radpeakpos','1.58_1.9') )
batch.append( runinfo('75MO_W_P4_2H',392,'radpeakpos','1.66_1.9') )
batch.append( runinfo('75MO_W_P4_2H',393,'radpeakpos','1.64_1.9') )














for ri in batch:
    start = time.perf_counter()
    
    # checking if the current run is in this group
    globcheck = glob.glob(f'/data/xfm/{expnum}/raw/eiger/{ri.group}/*_{ri.run}')
    # if they don't exist
    if len(globcheck) ==0: continue
    
    
    flags = "--xfmgroup "+ri.group+" --run "+str(ri.run)+" --xfmconfig "+configpath
    flags += f' --filtertype {ri.ftype} --filterlabel {ri.flabel}'
    os.system("python ./pypadf/xfmcorr.py --config ./configs/config_xfmcorr_20027.txt "+flags)
    stop = time.perf_counter()
    print("time (s) to correlate run:", stop-start) 	
