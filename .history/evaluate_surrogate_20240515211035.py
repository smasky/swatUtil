from UQPyL.surrogates import RBF
from UQPyL.surrogates import KRG

from UQPyL.surrogates.rbf_kernels import Cubic
from UQPyL.surrogates.krg_kernels import Guass_Kernel

from UQPyL.utility.scalers import MinMaxScaler
from UQPyL.utility.metrics import r2_score
import numpy as np

X=np.loadtxt('./res_X_1000.txt', dtype=np.float64)
Y=np.loadtxt('./res_Y_1000.txt', dtype=np.float64)

test_X=np.loadtxt('./res_X_50.txt', dtype=np.float64)
test_Y=np.loadtxt('./res_Y_50.txt', dtype=np.float64).reshape(-1,1)

# kernel=Cubic()
# rbf=RBF(kernel=kernel, scalers=(MinMaxScaler(0,1), MinMaxScaler(0,1)))
# rbf.fit(X, Y)
# pre_Y=rbf.predict(test_X)
# r2=r2_score(test_Y, pre_Y)
# print(r2)
gua=Guass_Kernel(theta=np.ones(10), theta_lb=np.ones(10)*1e-5, theta_ub=np.ones(10))
krg=KRG(kernel=gua, scalers=(MinMaxScaler(0,1), MinMaxScaler(0,1)), fitMode="predictError", optimizer='Boxmin')
krg.fit(X, Y)
pre_Y=krg.predict(test_X)
r2=r2_score(test_Y, pre_Y)
print(r2)        
