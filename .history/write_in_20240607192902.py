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
template=[0,0,0,0,0,0]+[0.0]*10
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.ops'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                lines=f.readlines()
                
            while(len(lines)<3):
                lines.append(" ")
                
            with open(file_path, 'w') as f:
                template1=template.copy()
                template1[0]=1
                template1[1]=1
                template1[2]=2021
                template1[3]=7
                template1[4]=1
                template1[6]=0.35
                template1[7]=0.005
                template1[8]=2.0
                template1[9]=30.0
                template1[10]=1000.0
                template1[11]=0.1
                lines[1]=format_fortran(template1)
                lines[1]=" 1 1     2021 7    0   0  0.35  0.00500  2.00  30.00000 1000.00  0.10\n"
                lines[2]=" 1 1     2021 4    0       40        0.5        0.0"
                f.writelines(lines)
                
