import os

def write_files_content_to_txt(folder_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                outfile.write(f'Путь до файла: {file_path}\n')
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(f'Содержимое:\n{content}\n')
                except Exception as e:
                    outfile.write(f'Не удалось прочитать файл {file_path}: {e}\n')
                outfile.write('\n' + ('-' * 40) + '\n\n')

# Задайте путь к папке и имя выходного файла
folder_path = "D:\PetProjects\GIT_Library\SPB-SO\est-1"  # Замените на ваш путь
output_file = 'выходной_файл.txt'    # Замените на имя выходного файла

write_files_content_to_txt(folder_path, output_file)

