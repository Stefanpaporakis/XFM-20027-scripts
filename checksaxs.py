import numpy as np
import matplotlib.pyplot as plt



saxsname =  "/data/xfm/20027/analysis/eiger/50MO_EtAN_P6_4H/138509_500/138509_500_avg_red.npy"
saxs = np.load(saxsname)
print(saxs.shape)
plt.plot(saxs[:,1])
plt.show()
