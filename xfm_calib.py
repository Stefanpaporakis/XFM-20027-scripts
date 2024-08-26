import numpy as np
#from PIL import Image
from skimage.feature import peak_local_max
import matplotlib.pyplot as plt
#import numba
import math as m


#@numba.njit()
def fast_vec_difmag(x1, x2, y1, y2):
    return m.sqrt((y1 - x1) ** 2 + (y2 - x2) ** 2)


class DiffImage:

    def __init__(self, path):
        self.path = path
        self.image = np.array([])
        self.exclusion_boxes = [(0, 0, 0, 0)]
        self.fileread()
        self.initial_center = (0.0, 0.0)
        self.peaks = []
        self.intensity_threshold = 0.0  # absolute minimum
        self.num_peaks = 1000
        self.exclusion_radii = (100,400)
        self.sample_box = 20.0
        self.fom_int = 1
        self.mc_cycle_num = 1000
        self.cycle_zero = (0.0, 0.0)

    def fileread(self):
        if self.path[-3:] == 'npy':
            print("Reading .npy")
            self.npyread()
        elif self.path[-3:] == 'tif':
            print("Reading .tif")
            self.tifread()

    def npyread(self):
        #print(f"Loaded image...{self.path}")
        data = np.load(self.path)
        #print(f"Shape: {data.shape}")
        data = np.array(data)
        data = data.transpose()
        self.image = data

    def tifread(self):
        data = np.asarray(Image.open(self.path))
        # Checks if the array is 3D then flattens it
        if len(np.shape(data)) > 2:
            dig_data = np.ones((data.shape[0], data.shape[1]))
            xlen = len(data[:, 0, 0])
            ylen = len(data[0, :, 0])
            for x in range(0, xlen):
                for y in range(0, ylen):
                    dig_data[x][y] = data[x][y][0]
            self.image = dig_data
            return dig_data
        else:
            print(f"Loaded image...{self.path}")
            data = data.transpose()
            print(f"Shape: {data.shape}")
            self.image = data
            return data

    def clean_beamstop(self):
        clean_peaks = []
        print("Cleaning around beamstop ")
        print(f"{len(self.peaks)} peaks before cleaning")
        for peak in self.peaks:
            diff = fast_vec_difmag(peak[0], peak[1], self.initial_center[0], self.initial_center[1])
            if self.exclusion_radii[0] < diff < self.exclusion_radii[1]:
                clean_peaks.append(peak)
        self.peaks = np.array(clean_peaks)
        print(f"{len(self.peaks)} peaks after cleaning")
        return self.peaks

    def clean_exclusion_boxes(self):
        clean_peaks = []
        print("Cleaning exclusion boxes")
        print(f"{len(self.peaks)} peaks before cleaning")
        for peak in self.peaks:
            excluded_flag = False
            for exbox in self.exclusion_boxes:
                if peak[0] in np.arange(start=exbox[0], stop=exbox[1]) and peak[1] in np.arange(start=exbox[2],
                                                                                                stop=exbox[3]):
                    #print(f"Excluding peak {peak} from box {exbox}")
                    excluded_flag = True
                    continue
            if not excluded_flag:
                clean_peaks.append(peak)
        self.peaks = np.array(clean_peaks)
        print(f"{len(self.peaks)} peaks after cleaning")
        return self.peaks

    def find_cycle_diffs(self):
        diffs = []
        for peak in self.peaks:
            diff = fast_vec_difmag(peak[0], peak[1], self.cycle_zero[0], self.cycle_zero[1])
            if diff > self.exclusion_radius:
                diffs.append(diff)
        ap_diffs = [round(x, self.fom_int) for x in diffs]
        diff_stdev = np.std(np.array(diffs))
        values = np.unique(np.array(ap_diffs))
        # print(len(values))
        return len(values)

    def stddev_fom(self):
        diffs = []
        for peak in self.peaks:
            diff = fast_vec_difmag(peak[0], peak[1], self.cycle_zero[0], self.cycle_zero[1])
            if diff > self.exclusion_radii[0]:
                diffs.append(abs(diff))
        #ap_diffs = [round(x, self.fom_int) for x in diffs]
        diff_stdev = np.std(np.array(diffs))
        # values = np.unique(np.array(ap_diffs))
        # print(len(values))
        # print('diff_stdev = ', diff_stdev)
        return diff_stdev

    def find_centre(self, clims=[]):
        # Let's find peaks
        print(type(self.image))
        plt.imshow(np.transpose(self.image), clim=clims)
        self.peaks = peak_local_max(self.image, min_distance=2, threshold_abs=self.intensity_threshold, num_peaks=self.num_peaks)
        # Exclude peaks close to the beamstop on the basis of the initial guess
        self.peaks = self.clean_beamstop()
        self.peaks = self.clean_exclusion_boxes()
        plt.plot(self.peaks[:, 0], self.peaks[:, 1], 'r.')
        plt.title("Image with peaks, before refinement (i think - Andrew)")
        plt.show()
        cycle_tot = 0
        cycle_account = []
        best_fom = 1000
        while cycle_tot < self.mc_cycle_num:
            x_jit = np.random.uniform(-self.sample_box, self.sample_box)
            y_jit = np.random.uniform(-self.sample_box, self.sample_box)
            self.cycle_zero = (self.initial_center[0] + x_jit, self.initial_center[1] + y_jit)
            # cycle_fom = self.find_cycle_diffs()
            cycle_fom = self.stddev_fom()
            if cycle_fom < best_fom:
                best_cen = self.cycle_zero
                best_fom = cycle_fom
            cycle_account.append([self.cycle_zero[0], self.cycle_zero[1], cycle_fom])
            cycle_tot += 1

        print(f"I find the minimum at {np.array(best_cen)}")
        cycle_account = np.array(cycle_account)
        plt.scatter(cycle_account[:, 0], cycle_account[:, 1], c=cycle_account[:, 2], cmap='viridis')
        best_cen = np.array(best_cen)
        plt.plot(best_cen[0], best_cen[1], 'r1')
        plt.show()


if __name__ == '__main__':
    """
    Constants:
    """
    EIGER_nx = 1062
    EIGER_ny = 1028
    MAX_PX_COUNT = 2 ** 32 - 1
    MASK_MAX = 1e11

    cam_length = 0.64
    wavelength = 0.67018E-10
    pix_size = 75E-6
    #image_center = (514.375,532.340)
    #image_center = (544.294,534.043)

    image_center = (517.0902, 543.7068)
    """
    Monte Carlo determination of the beam center 
    """
    print("XFM .h5 geomopt")
    im = '138015_6' #runid and run number
    grp = 'calibration'
    unmasked_im = np.load(f'/data/xfm/20027/analysis/eiger/{grp}/{im}/{im}_sum.npy')
    mask_im = np.load(f'/data/xfm/20027/analysis/eiger/{grp}/{im}/{im}_mask.npy')
    masked_im = unmasked_im * mask_im
    np.save(f'/data/xfm/20027/analysis/eiger/{grp}/{im}/{im}_masksum.npy', masked_im)

    calib_im = DiffImage(f'/data/xfm/20027/analysis/eiger/{grp}/{im}/{im}_masksum.npy')
    calib_im.path = f'/data/xfm/20027/analysis/eiger/{grp}/{im}/{im}_masksum.npy'
    plt.imshow(calib_im.image, clim=(0,1e5))
    plt.colorbar()
    plt.title("Init")
    plt.show()
    calib_im.initial_center =(517.0902, 543.7068)
    calib_im.fom_int = 1
    calib_im.mc_cycle_num = 10000
    calib_im.exclusion_radii = (260,272)
    calib_im.exclusion_boxes = [(510.0, 525.0, 601.0, 619.0),
                                (501.0, 525.0, 421.0, 478.0)]  # define xmin, xmax, ymin,ymax
    
    # calib_im.exclusion_boxes = [(450.0, 450.0, 600.0, 600.0),
                                # (501.0, 525.0, 421.0, 478.0)]  # define xmin, xmax, ymin,ymax
    calib_im.sample_box = 0.7
    calib_im.intensity_threshold = 1e2
    calib_im.num_peaks = 30000
    calib_im.find_centre(clims=(0,1e5))
    plt.figure()
    plt.imshow(np.transpose(calib_im.image), clim=(0,1e5))
    plt.plot(calib_im.peaks[:, 0], calib_im.peaks[:, 1], 'r.')
    plt.title("Image + peaks after centre refinement")
    plt.show()
