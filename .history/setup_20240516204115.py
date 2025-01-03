from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import sys

# 定义扩展模块
ext_modules = [
    Pybind11Extension(
        "my_module",  # 模块名
        [".cpp"],  # 源代码文件
        # 可以在这里定义额外的编译器和链接器选项
        extra_compile_args=['-std=c++20'] if sys.platform != 'win32' else ['/std:c++20'],
        define_macros=[('VERSION_INFO', '"1.0"')],
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