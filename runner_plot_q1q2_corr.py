import fluxfm
import sys
import random
import numpy as np


from skimage.transform import warp_polar
import matplotlib.pyplot as plt

def gblur( image, wid ):
    s = image.shape
    xy = np.mgrid[0:s[0],0:s[1]]
    x = np.roll(xy[0] - s[0]/2, 0, 0)
    y = np.roll(xy[1] - s[1]/2, 0, 1)
    r2 = x*x + y*y
    g = np.exp( -r2/(2*wid**2))
    g = np.roll(np.roll(g, s[0]//2, 0), s[1]//2, 1)
    #plt.figure()
    #plt.imshow(g)
    fg = np.fft.fft2( g )
    fim = np.fft.fft2(image)
    output = np.real(np.fft.ifft2( np.conjugate(fg)*fim))
    return output

if __name__ == '__main__':

    # Here you select the group and run for the data set
    dset.group = sys.argv[1]
    run_num = int(sys.argv[2])


    # run_nums = list(range(602, 611))
    # for run_num in run_nums:


    print('fluxfm  ----   XFM h5 Processing...')
    configname = './20027_config.txt'
    dset = fluxfm.XfmHfiveDataset(configpath=configname)


    bgflag = False
    if len(sys.argv)>=4:
        bset = fluxfm.XfmHfiveDataset(configpath=configname)
        bset.group = sys.argv[3]
        run_num_bg = int(sys.argv[4])
        bgflag = True
        # Set the paths and pass mask values to the XfmHfiveDataset
        bset.tag = f'{bset.maia_num + run_num_bg}_{run_num_bg}'
        bset.dpath = f'{bset.dpath}{bset.group}/{bset.tag}/'
        bset.apath = f'{bset.apath}{bset.group}/{bset.tag}/'
        bset.grab_dset_members()


    """
    Mask details:
    """

    # Set the paths and pass mask values to the XfmHfiveDataset
    dset.tag = f'{dset.maia_num + run_num}_{run_num}'
    dset.dpath = f'{dset.dpath}{dset.group}/{dset.tag}/'
    dset.apath = f'{dset.apath}{dset.group}/{dset.tag}/'
    dset.grab_dset_members()
    dset.mk_scratch('')





    # load correlations
    try:
       corra = np.load(f'{dset.apath}/corr/{dset.tag}_corrq1q2_a_nstart0_nframes2872.npy')
       corrb = np.load(f'{dset.apath}/corr/{dset.tag}_corrq1q2_b_nstart0_nframes2872.npy')
    except:
       corra = np.load(f'{dset.apath}/corr/{dset.tag}_corrq1q2_a.npy')
       corrb = np.load(f'{dset.apath}/corr/{dset.tag}_corrq1q2_b.npy')
    if bgflag:
        corrbg = np.load(f'{bset.apath}/corr/{bset.tag}_corrq1q2_a.npy')
        corrbg2 = np.load(f'{bset.apath}/corr/{bset.tag}_corrq1q2_b.npy')
        plt.figure()
        thline = 180
        r0 = 50
        plt.plot(corra[r0:,thline])
        plt.plot(corrb[r0:,thline])
        plt.plot(corrbg[r0:,thline])

        plt.figure()
        plt.plot(corra[r0:,thline]/corrbg[r0:,thline])
        plt.plot(corrb[r0:,thline]/corrbg[r0:,thline])

        nmin, nmax = 50, 60 #150, 180
        thmin, thmax = 178, 182
        normbg = np.sqrt(np.sum(corrbg[nmin:nmax,thmin:thmax]**2))
        normbg2 = np.sqrt(np.sum(corrbg2[nmin:nmax,thmin:thmax]**2))
        norma = np.sqrt(np.sum(corra[nmin:nmax,thmin:thmax]**2))
        normb = np.sqrt(np.sum(corrb[nmin:nmax,thmin:thmax]**2))
        #normbg = 1 #(1710/2872)**2 #np.sum(corrbg[nmin:nmax,thmin:thmax])
        #norma = 1 #np.sum(corra[nmin:nmax,thmin:thmax])
        #normb = 1 #np.sum(corrb[nmin:nmax,thmin:thmax])
        corra += -corrbg *norma/normbg
        corrb += -corrbg2 *normb/normbg2
       

        plt.figure()
        plt.plot(corra[r0:,thline])
        plt.plot(corrb[r0:,thline])
        plt.plot(corrbg[r0:,thline])

        

    # q^2 scaling
    q_scale = np.linspace(1, corra.shape[0], corra.shape[0])**2
    corra *= np.outer(q_scale,np.ones(corra.shape[1]))
    corrb *= np.outer(q_scale,np.ones(corrb.shape[1]))


    # crop theta=0 and theta=180
    tcrop = 5
    corra[:,:tcrop] = 0
    corra[:,-tcrop:] = 0
    corrb[:,:tcrop] = 0
    corrb[:,-tcrop:] = 0



    # qs = [[i for i in range(109, 140)]] #407

    #qs = [ list(range(74,81)), list(range(89,95)), list(range(107,113)), list(range(133,137))] #run 455
    #qs = [ list(range(99,105)) , list(range(120, 125)),] #run 456
    #qs = [ list(range(74,81)), list(range(92,98)), list(range(107,113)), list(range(133,137))] #run 462
    #qs = [ list(range(99,105)) , list(range(120, 125)), 123,  102] #run 463

    #qs = [ list(range(74,81)), list(range(92,98)), list(range(107,113)), list(range(133,137))] #run 468
    #qs = [ list(range(93,96)), list(range(110,114)), list(range(151,155))] #run 468 based on powder peaks
    #qs = [ list(range(99,105)) , list(range(120, 125)), 123,  102] #run 469

    #qs = [ list(range(110,118)) , list(range(130,136)), list(range(200, 204)), list(range(234, 236))] #run 376
    #qs = [ list(range(118,132)) , list(range(135,146))] #run 376 based on powder data
    #qs = [ list(range(115,125)) , list(range(132,140))] #run 344 based on powder data


    qs = [ list(range(85,90)) ] #changable

    # 29, 47, 63, 88

    # qs = [157] #run 441
    # qs = [135] #run 423



    #run 602
    #qs = [list(range(114, 126))]


    #run 607
    # qs = [list(range(111, 120))]

    #run 613
    #qs = [list(range(115,125)), list(range(95,105))]

#run 620
#    qs = [144, list(range(124, 136))]

#run 621
#    qs = [list(range(124, 136))]

#run 622
#    qs = [list(range(124, 136))]

#run 142
#    qs = [list(range(142,148)), list(range(162,167))]

    #run 411
    #qs = [list(range(130,190))]
    #run 412
    #qs = [list(range(140,150))] 
    rmin = 25
    corra[:rmin,:]=0
    corrb[:rmin,:]=0

    #gaussian blur
    #corra = gblur( corra, 0.5)
    #corrb = gblur( corrb, 0.5)

    fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
    scl, scl2 = 0.005, 0.005
    c0, c1 = -np.max(corra)*scl, np.max(corra)*scl2
    #c0, c1 = np.min(corra), np.min(corra)*0.0

    plt.suptitle(f'grp:{dset.group} run:{run_num}')
    axes[0].imshow(corra, vmin=c0, vmax=c1)
    axes[0].set_title(f'corra')
    #plt.clim([-np.max(corra)*scl,np.max(corra)*scl])
    axes[1].imshow(corrb,vmin=c0, vmax=c1)
    axes[1].set_title(f'corrb')
    #plt.clim([-np.max(corrb)*scl,np.max(corrb)*scl])




    # qs = [71] #187
    # qs = [71] #193
    # qs = [75] #199
    # qs = [78] #211
    # qs = [78] #217


    #qs = [81, 100, 114, 140] #run 221
#    qs = [127,159,280] #run 259
    #qs = [73,144,288] #run 261
    # qs = [86, 95, 104,200] #run 367


    for qq in qs:
        plt.figure()
        plt.title(f'corr grp:{dset.group} run:{run_num} q={qq}')
        if type(qq) is list:
            plt.plot(np.sum(corra[ qq,:], axis=0))
            plt.plot(np.sum(corrb[ qq,:], axis=0))
        else:
            plt.plot(corra[qq,:])
            plt.plot(corrb[qq,:])

    """
    plt.figure()
    plt.plot( np.sum(corra[:,75:105],1))
    plt.plot( np.sum(corrb[:,75:105],1))
    plt.title("90 degree line")

    plt.figure()
    plt.plot( np.sum(corra[:,165:195],1))
    plt.plot( np.sum(corrb[:,165:195],1))
    plt.title("180 degree line")
    """







    plt.show()
