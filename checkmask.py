import numpy as np
import matplotlib.pyplot as plt



maskname =  "/data/xfm/20027/analysis/eiger/75MO_W_P2_1H/138104_95/138104_95_mask.npy"
mask = np.load(maskname)
plt.imshow(mask)
plt.show()
