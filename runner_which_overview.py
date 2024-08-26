
import numpy as np

import glob
import os 
import sys
import subprocess


expnum =20027

run_start = int(sys.argv[1])

run_end = run_start+1
if len(sys.argv)>2:
    run_end = int(sys.argv[2])




# for each run
for run in range(run_start, run_end):

    # get the path to the run raw files
    raw_run_glob = glob.glob(f'/data/xfm/{expnum}/raw/eiger/*/*{run}')

    # if they don't exist
    if len(raw_run_glob) ==0:
        # print(f'echo NO RAW {run}')
        continue

    #group name
    grp = raw_run_glob[0].split('/')[-2]

    analysis_run_glob = glob.glob(f'/data/xfm/{expnum}/analysis/eiger/{grp}/*{run}')
    h5s_glob = glob.glob(f'/data/xfm/{expnum}/raw/eiger/*/*_{run}/*')


    if len(analysis_run_glob) == 0 and len(h5s_glob)>1:
        print(f'python runner_overview.py {grp} {run}')



















