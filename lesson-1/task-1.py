"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
   соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
   и также проверить тип и содержимое переменных.
"""

words_lst = ["разработка", "сокет", "декоратор"]

for elem in words_lst:
    print(len(elem))
    print(type(elem))
    print(elem.__dir__())

unicode_lst = [
    "\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430",
    "\u0441\u043e\u043a\u0435\u0442",
    "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440"
]

for elem in unicode_lst:
    print(len(elem))
    print(type(elem))
    print(elem.__dir__())

for i in range(len(words_lst)):
    print(words_lst[i] == unicode_lst[i])