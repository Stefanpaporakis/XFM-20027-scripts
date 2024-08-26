import fluxfm
import numpy as np
import sys

if __name__ == '__main__':
    print('fluxfm  ----   XFM h5 Processing...')

    group = sys.argv[1]

    run_num = int(sys.argv[2])

    dset = fluxfm.XfmHfiveDataset(configpath=f'/data/xfm/20027/python/20027_config.txt')

    # Here you select the group and run for the data set
    dset.group = group

    # image_center = (514, 531)
    # image_center = (517.561,553.128)
    # image_center = (517, 553)

    #three point cirlce method
    # image_center = (503.304,540.555)


    #average of 6 midpoint measurements
    image_center = (517.0902, 543.7068)



    """
    Mask details:
    """
    # xmin, xmax, ymin, ymax
    bboxes = [(0.0, 1028.0, 511.0, 549.0)]
    # Final value in the list is the radius
    circs = [(image_center[0], image_center[1], 0.00)]

    dset.bboxes = bboxes
    dset.circs = circs

    # Set the paths and pass mask values to the XfmHfiveDataset
    dset.tag = f'{dset.maia_num + run_num}_{run_num}'
    dset.image_center = image_center
    dset.dpath = f'{dset.dpath}{dset.group}/{dset.tag}/'
    dset.apath = f'{dset.apath}{dset.group}/{dset.tag}/'
    # print(dset.dpath)
    # print(dset.apath)
    dset.grab_dset_members()
    dset.mk_scratch('')
    
    
    dset.quick_overview(run_limit=10, show=False)  # set to 1 to examine just the first run, quickest method
    dset.show_overview_figures(dump=True,show=False)




    """
    Define average and filter manifest    
    """

    #dset.define_average_profile()
    #dset.filter_against_average(itera=1, rfac_threshold=1.0, inspect=False, qlims=[0,10])

    # random pairs of patterns of difference - take abs val - compare 

    """
    Inspect random frames	
    """
    #dset.scatter_shot_inspect(dbin_folder='h5_frames', sample_size=3, dump=False)

    #
    # """
    # Processing:
    # """
    #
    # # Grab an overview of the data structure. frame numbers etc.
    # # this will also out put a series of profiles for each h5 (*_sum_h5_k_red.dat/npy)
    # #    Plot these up to compare how the profiles change through the whole data set if
    # #    you have multple h5s
    # # Turn me off once you've done once
    # # dset.overview(run_limit=5)
    # #
    # # dset.run_movie(run_id=3, step=20,cmin=0,cmax=20)
    # #
    #
    # # Here you can check the mask and the centering
    # dset.dsum = np.load(f'{dset.apath}{dset.tag}_sum.npy')
    # dset.gen_mask(dset.dsum, bboxes=True, circs=True, max_lim=constants_config.MASK_MAX, dump=True)
    # dset.mask = np.load(f'{dset.apath}{dset.tag}_mask.npy')
    # # dset.scatter_shot_inspect(sample_size=50)
    # # uw = dset.frm_integration(dset.dsum)
    # # uwai = dset.pyFAI_frm_integration(dset.dsum*dset.mask,unit="q_nm^-1")
    # # np.savetxt(f'{dset.apath}{dset.tag}_sum_qnm.dat', uwai)
    # # uwai = dset.pyFAI_frm_integration(dset.dsum*dset.mask,unit="q_nm^-1")
    # # np.savetxt(f'{dset.apath}{dset.tag}_sum_2th.dat', uwai)
    #
    # # dset.inspect_mask(dset.dsum*dset.mask, cmin=0, cmax=1e8)
    # # dset.inspect_unwarp(dset.dsum * dset.mask,cmin=0,cmax=1e6)
    # plt.figure()
    # uwai = dset.frm_integration(dset.dsum * dset.mask)
    # print(uwai.shape)
    # plt.plot(uwai[:, 0], uwai[:, 1])
    # plt.title('pyFAI integration')
    # plt.show()
    # np.savetxt(f'{dset.apath}{dset.tag}_pyfai_sum_2th.txt', uwai)
    # np.save(f'{dset.apath}{dset.tag}_pyfai_sum_2th.npy', uwai)
    #
    # # Now to prepare for PADF calculations, atomize (using start and limit if you want)
    #
    # # LIMITS ARE GIVEN IN PYTHON COUNTING
    # dset.atomize_h5(folder='h5_frames', start=0, limit=3,
    #                 masked=False)  # dbins are gnerated in the folder with a manifest.txt file for py3padf
    # dset.reduce_h5(scatter_mode='s', start=0, limit=3)
    #
    # #
    # # dset.define_average_profile()
    #
    # # plt.figure()
    # # plt.title("average profile")
    # # plt.plot(dset.average_profile[:,0], dset.average_profile[:,1])
    # # plt.show()
    # # dset.filter_against_average(itera=1, rfac_threshold=1.0, inspect=False, qlims=[0,10])
