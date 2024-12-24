import swat_utility

# 方法 1: 使用 __version__ 属性（如果存在）
try:
    print(f"swat_utility version: {swat_utility.__version__}")
except AttributeError:
    print("swat_utility does not have a __version__ attribute.")

# 方法 2: 检查是否有其他的版本属性
try:
    print(f"swat_utility version: {swat_utility.VERSION}")
except AttributeError:
    print("swat_utility does not have a VERSION attribute.")

# 方法 3: 检查模块提供的其他获取版本信息的方法
try:
    version_info = swat_utility.get_version()  # 替换为实际函数名（如果存在）
    print(f"swat_utility version: {version_info}")
except AttributeError:
    print("Unable to retrieve swat_utility version.")
