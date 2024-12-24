import os
folder_path="D:\SWAT\TxtInOut"
def format_fortran(values):
    # 按照Fortran的FORMAT定义
    # values 需要包含以下格式的数据：
    # 2个i2, 1个i4, 1个i2, 1个i4, 1个i3, 1个f6.2, 1个f12.5, 1个f6.2,
    # 1个f11.5, 1个f8.2, 1个f6.2, 16个f5.2
    format_str = (
        " {0:2d} {1:2d}     {2:4d} {3:2d} {4:4d} {5:3d} {6:6.2f} {7:12.5f} "
        "{8:6.2f} {9:11.5f} {10:8.2f} {11:6.2f}" + " ".join(["{12[%d]:5.2f}" % i for i in range(16)])
    )
    return format_str.format(*values)
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.ops'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                lines=f.readlines()
                
            while(len(lines)<3):
                lines.append(" ")
                
            with open(file_path, 'w') as f:  
                lines[1]=fo
                lines[2]=" 1 1     2021 4    0       40        0.5        0.0"
                f.writelines(lines)
                
