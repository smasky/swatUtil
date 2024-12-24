import re
import os
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

data=np.loadtxt('./jz.txt', dtype=np.float32)
dates = pd.date_range(start='2011-1-1', end='2013-12-31')
# 创建图形
plt.figure(figsize=(10,6))

# 修改线条颜色为蓝色，线条样式为虚线，线条宽度为2
plt.plot(dates, data[:,0], color='#151515', linewidth=2)
plt.plot(dates, data[:,1], color='#FF7F3E',linewidth=2)
plt.plot(dates, data[:,2],  color='#006769',linewidth=2)
plt.plot(dates, data[:,3],  color='#FF5F00',linewidth=2)
plt.plot(dates, data[:,4], color='#577B8D',linewidth=2)
plt.plot(dates, data[:,5], color='#C7B7A3', linewidth=2)
plt.plot(dates, data[:,6], color='',linewidth=2)
interval = 2
# plt.scatter(dates[::interval], data[::interval], color='#FC4100', zorder=5, s=15)
# 添加网格
# plt.grid(True)

# 设置标题和标签，修改字体大小和颜色
plt.xlabel('years', fontsize=20)
plt.ylabel('discharge(m^3/s)', fontsize=20)
# 加粗边框
ax = plt.gca()
ax.spines['top'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.tick_params(axis='both', which='major', direction='in', width=2, labelsize=15)
# 显示图形
start = datetime.strptime('2011-1-1', '%Y-%m-%d')
end = datetime.strptime('2013-12-31', '%Y-%m-%d')
plt.xlim(start, end)

plt.show()

