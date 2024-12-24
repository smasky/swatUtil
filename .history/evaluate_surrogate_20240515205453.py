from UQPyL.surrogates import RBF
from UQPyL.surrogates.rbf_kernels import Cubic
from UQPyL.utility.scalers import MinMaxScaler
from UQPyL.utility.metrics import r2_score
import numpy as np

X=np.loadtxt('./res_X_1000.txt', dtype=np.float64)
Y=np.loadtxt('./res_Y_1000.txt', dtype=np.float64)

test_X=np.loadtxt('./res_X_50.txt', dtype=np.float64)
test_Y=np.loadtxt('./res_Y_50.txt', dtype=np.float64)

kernel=Cubic()
rbf=RBF(kernel=kernel, scalers=(MinMaxScaler(0,1), MinMaxScaler(0,1)))
rbf.fit(X, Y)
pre_Y=rbf.predict(test_X)