import numpy as np
import matplotlib.pyplot as plt


analysis_dir = '/data/xfm/20027/analysis/eiger'

group = '75MO_W_8H'
run_tag = '138054_45' 
corr_tag = '120640_45' 

corra = np.load(f'{analysis_dir}/{group}/{run_tag}/corr/{corr_tag}_a_correlation_sum.npy')
corrb = np.load(f'{analysis_dir}/{group}/{run_tag}/corr/{corr_tag}_b_correlation_sum.npy')


# corra = corra[:250,:250, :]


corra_q1q2 = np.zeros((corra.shape[0], corra.shape[-1]))
corrb_q1q2 = np.zeros((corrb.shape[0], corrb.shape[-1]))

for q in range(corra.shape[0]):
    corra_q1q2[q, :] = corra[q,q,:]
    corrb_q1q2[q, :] = corrb[q,q,:]



fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
axes[0].imshow(corra_q1q2, clim=(-1e3, 1e19))
axes[1].imshow(corrb_q1q2, clim=(-1e3, 1e19))


plt.figure()
plt.plot(corra_q1q2[211,:])
plt.plot(corrb_q1q2[211,:])


plt.show()


