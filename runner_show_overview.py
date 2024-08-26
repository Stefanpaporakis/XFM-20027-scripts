import fluxfm
import numpy as np
import sys
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print('fluxfm  ----   XFM h5 Processing...')

    group = sys.argv[1]

    run_start = int(sys.argv[2])

    if len(sys.argv)>3:
        run_end = int(sys.argv[3])
    else:
        run_end = run_start

    plt.figure()
    for i_run, run_num in enumerate(range(run_start, run_end)):


        dset = fluxfm.XfmHfiveDataset(configpath=f'/data/xfm/20027/python/20027_config.txt')

        dset.group = group


        """
        Mask details:
        """

        # Set the paths and pass mask values to the XfmHfiveDataset
        dset.tag = f'{dset.maia_num + run_num}_{run_num}'

        dset.dpath = f'{dset.dpath}{dset.group}/{dset.tag}/'
        dset.apath = f'{dset.apath}{dset.group}/{dset.tag}/'

        """
        plot sums
        """
        # mask_img = np.load(f'{dset.apath}/{dset.tag}_mask.npy')
        # plt.figure()
        # plt.imshow(mask_img)

        # sum_img = np.load(f'{dset.apath}/{dset.tag}_sum.npy')
        # plt.figure()
        # plt.imshow(sum_img*mask_img, clim=(0, np.median(sum_img*mask_img)*10))


        saxs = np.load(f'{dset.apath}/{dset.tag}_avg_red.npy')

        plt.plot(saxs[:,0], saxs[:,1]+0.015*i_run)


        # plt.figure()
        # plt.plot(saxs[:,1])





    plt.show()
