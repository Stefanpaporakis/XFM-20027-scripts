import numpy as np
import matplotlib.pyplot as plt



maskname =  "/data/xfm/20027/analysis/eiger/75MO_W_P2_4H/138113_104/138113_104_sum.npy"
mask = np.load(maskname)
mask[mask>1.5e13]=0
plt.imshow(mask)
plt.clim([0,1200])
plt.show()
