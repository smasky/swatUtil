import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 假设 matrix 是你的数据矩阵，它有三列分别代表 X, Y, Z 坐标
# 下面是一个生成随机数据的例子
np.random.seed(0)
matrix = np.random.random((100, 3))

# 分别获取X, Y, Z数据
x = matrix[:, 0]
y = matrix[:, 1]
z = matrix[:, 2]

# 创建一个图形和一个3D坐标轴
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 添加散点图
ax.scatter(x, y, z)

# 设置坐标轴标签
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')

# 显示图形
plt.show()