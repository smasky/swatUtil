from UQPyL.surrogates import RBF
from UQPyL.surrogates.rbf_kernels import Cubic

import numpy as np

X=np.loadtxt('./res_X_1000.txt', dtype=np.float64)
Y=np.loadtxt('./res_Y_1000.txt', dtype=np.float64)

kernel=Cubic()