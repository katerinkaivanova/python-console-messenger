"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
  (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""

bytes_lst = [
    b"\u0063\u006c\u0061\u0073\u0073",
    b"\u0066\u0075\u006e\u0063\u0074\u0069\u006f\u006e",
    b"\u006d\u0065\u0074\u0068\u006f\u0064"
]

for elem in bytes_lst:
    print(elem)
    print(len(elem))
    print(type(elem))
    print(elem.__dir__())
