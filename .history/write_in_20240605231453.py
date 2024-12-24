import os
 for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.ops'):
                file_path = os.path.join(root, file)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'File {file_path} has been rewritten.')