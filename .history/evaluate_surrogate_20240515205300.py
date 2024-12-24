from UQPyL.surrogates import RBF
from UQPyL.surrogates.rbf_kernels import Cubic
from UQPyL.utility.scalers import MinMaxScaler
import numpy as np

X=np.loadtxt('./res_X_1000.txt', dtype=np.float64)
Y=np.loadtxt('./res_Y_1000.txt', dtype=np.float64)

kernel=Cubic()
rbf=RBF(kernel=kernel)
rbf.fit(X, Y)