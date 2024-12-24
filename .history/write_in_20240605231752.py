import os
folder_path="D:\SWAT\TxtInOut"

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.ops'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines=f.readlines()
                lines[1]="  1  1     2021  7    0       0.35      0.00500   2.00    30.00000  10.00     0.10"
                lines[2]="  1  1     2021  7    0       40        0.5        0.0"
                f.writelines(lines)