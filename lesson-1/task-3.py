"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""

words_lst = ["attribute", "класс", "функция", "type"]

for i in range(len(words_lst)):
    try:
        print(f"{i}. {bytes(words_lst[i], encoding = 'utf-8')}")
    except SyntaxError:
        print(f"{i}. Element contains not ASCII characters")

"""
Методом b'bytes' невозможно преобразовать слова "класс", "функция"
"""