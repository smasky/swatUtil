from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
import numpy
import sys
import os

# 设置环境变量以强制使用无标准库的模式
if sys.platform != "win32":  # 非 Windows 平台
    os.environ["CC"] = "gcc"
    os.environ["CXX"] = "g++"

# 定义扩展模块
ext_modules = [
    Pybind11Extension(
        "swat_utility",  # 模块名
        ["swat_utility.cpp"],  # 源代码文件
        extra_compile_args=[
            "-std=c++20",  # 使用 C++20 标准
            "-O3",  # 优化级别
            "-fno-exceptions",  # 禁用 C++ 异常
            "-fno-rtti",  # 禁用运行时类型信息（RTTI）
            "-fno-threadsafe-statics",  # 禁用线程安全的静态变量初始化
            "-nostdlib++",  # 不链接 C++ 标准库
            "-ffreestanding",  # 生成无依赖环境的代码
            "-fno-use-cxa-atexit",  # 禁用全局对象析构注册
            "-fPIC",  # 生成与位置无关的代码（便于移植）
        ],
        include_dirs=[
            numpy.get_include(),  # 添加 numpy 头文件的路径
        ],
    ),
]

setup(
    name="my_module",
    version="1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python module that extends Python with C++ code using Pybind11.",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
