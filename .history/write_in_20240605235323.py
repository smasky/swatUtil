import os
folder_path="D:\SWAT\TxtInOut"

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.ops'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                lines=f.readlines()
                
            while(len(lines)<3):
                lines.append(" ")
                
            with open(file_path, 'w') as f:  
                lines[2]="  1  1     2021  7    1       0.35      0.00500   2.00    30.00000  1000.00     0.10"
                lines[1]="  1  1     2021  4    1       40        0.5        0.0\n"
                f.writelines(lines)