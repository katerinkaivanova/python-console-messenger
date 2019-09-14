"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
   Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

words = ["сетевое программирование", "сокет", "декоратор"]

with open("tmp_folder/output.txt", "w") as f:
    f.write(f"{words[0]}")
    if len(words) > 1:
        f.writelines(f"\n{elem}" for elem in words[1:])
    print(type(f))

with open("tmp_folder/output.txt", encoding="utf-8") as f:
    lines = [line.replace("\n", "") for line in f.readlines()]
    print(lines)
