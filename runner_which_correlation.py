
import numpy as np

import glob
import os 
import sys
import subprocess


expnum =20027

run_start = int(sys.argv[1])
run_end = int(sys.argv[2])




# for each run
for run in range(run_start, run_end):

    # get the path to the run raw files
    raw_run_glob = glob.glob(f'/data/xfm/{expnum}/raw/eiger/*/*_{run}')

    # if they don't exist
    if len(raw_run_glob) ==0:
        print(f'echo NO RAW GROUP {run}')
        continue

    grp = raw_run_glob[0].split('/')[-2]

    corr_glob = glob.glob(f'/data/xfm/{expnum}/analysis/eiger/{grp}/*_{run}/corr/')

    if len(corr_glob)==0:
        print(f'python runner_xfmcorr.py {grp} {run}')
    else:
        print(f'echo corr {grp} {run} complete')




    # if len(analysis_run_glob) == 0:
        # print(f'echo NO corr')
    # else:
        # red_file_glob = glob.glob(analysis_run_glob[0]+'/*_sum.png')
        # if len(red_file_glob) >0:
            # over_flag = True
        # else:
            # over_flag = False


    # # print(f'{grp} {run}')
    # if not over_flag:

















