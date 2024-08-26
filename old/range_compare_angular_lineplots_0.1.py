


#This script is an updated version that will show accruate correlations 
#if peak shifts greatly between runs because you set it in rcen.







import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn as sns

#don't chage these
refnum, refrun = 138490, 481

# set data to plot here
analysis_path = "/data/xfm/20027/analysis/eiger/"

########### Plate 6 temps and runs################################
##heating
'''
title = "50MO_EtAN_P6 heating run"
runs = [456,465,474,483,492,501,510,519,528,537,546,555]
groups = ["60DPPC_W_P6_5H"]*len(runs)
labels = [30,35,40,45,50,52,54,56,58,60,65,70]

width = 0
rcen = np.array([25,26,26,26,26,26,26,26,26,26,26,30])
r0s = rcen-width
r1s = rcen+width+1
rmin = 10
'''

##cooling
title = "50MO_EtAN_P6 heating run"
runs = [573,582,591,600,609,618,627,636,643]
groups = ["60DPPC_W_P6_5C"]*len(runs)
labels = [65,60,58,56,54,50,45,40,35]

width = 0
rcen = np.array([26,26,26,26,26,26,26,26,26])
r0s = rcen-width
r1s = rcen+width+1
rmin = 10

'''
########## No plate heating and cooling################################
##heating
title = "50MO_EtAN_P6 heating run"
runs = [149,157,164,171,178,185,192]
groups = ["50MO_EAF_8H"]*len(runs)
labels = [30,35,40,45,50,55,60]

width = 0
rcen = np.array([26,26,26,26,27,30,33])
r0s = rcen-width
r1s = rcen+width+1
rmin = 10

##cooling
title = "50MO_EtAN_P6 heating run"
runs = [199,205,210,215,220,225]
groups = ["50MO_EAF_8C"]*len(runs)
labels = [60,55,50,45,40,35]

width = 0
rcen = np.array([34,35,35,35,35,35])
r0s = rcen-width
r1s = rcen+width+1
rmin = 10

'''
'''
############Plate 3 heating/cooling##############################
##heating
title = "50MO_EtAN_P6 heating run"
#runs = [233,243,248,253,258,263,269]
#groups = ["75MO_W_P3_5C"]*len(runs)
#labels = [30,40,50,60,65,70,75]

##cooling
runs = [274,294,294,304,314,324,332,340,348,356,361,362,367]
groups = ["75MO_W_P3_5C"]*len(runs)
labels = [70,65,62.5,60,57.5,55,52.5,50,47.5,45,40,35,30]

width = 0
rcen = np.array([39,43,44,47,47,48,48,48,48,48,48,47,47])
r0s = rcen-width
r1s = rcen+width+1
rmin = 10

'''

dlistA = []
dlistB = []
dlistC = []
for i, run in enumerate (runs):
    group = groups[i]
    xfmno = refnum + run - refrun
    tag = str(xfmno)+"_"+str(run) 
    path = analysis_path+group+"/"+tag+"/corr/"
    dataA = np.load( path+tag+"_nstart400_a_correlation_sum.npy")
    dataB =  np.load( path+tag+"_nstart400_b_correlation_sum.npy")
    dataC = dataA+dataB
    dlistC.append(dataC)
    #print(data.shape)
    dlistA.append(dataA)
    dlistB.append(dataB)

nth = dlistC[0].shape[2]
thmax = 360
thvals = np.arange(nth)*thmax/nth

plist = []
for i, data in enumerate(dlistC):
    tmp = np.average(data[r0s[i]:r1s[i],:,:],0)
    disp = np.average(tmp[r0s[i]:r1s[i],:],0) -i*0.001e1
    p, = plt.plot(thvals, disp)
    plist.append(p)
#plt.title(title+" A+B")
#plt.yscale("log")
plt.ylabel("log Correlation (arb units)")
plt.xlabel(r'theta (degrees)')
plt.legend(plist, labels, loc = 'lower left')
#plt.figure()
'''
plist = []
for i, data in enumerate(dlistA):
    tmp = np.average(data[r0s[i]:r1s[i],:,:],0)
    disp = np.average(tmp[r0s[i]:r1s[i],:],0) +i*0.5e1
    p, = plt.plot(thvals, disp)
    plist.append(p)
plt.title(title+" A")
plt.yscale("log")
plt.ylabel("log Correlation (arb units)")
plt.xlabel(r'theta (degrees)')
plt.legend(plist, labels)

plt.figure()
plist = []
for i, data in enumerate(dlistB):
    tmp = np.average(data[r0s[i]:r1s[i],:,:],0)
    disp = np.average(tmp[r0s[i]:r1s[i],:],0) +i*0.5e1
    p, = plt.plot(thvals, disp)
    plist.append(p)
plt.title(title+" B")
plt.yscale("log")
plt.ylabel("log Correlation (arb units)")
plt.xlabel(r'theta (degrees)')
plt.legend(plist, labels)
'''
plt.draw()
plt.show()    
