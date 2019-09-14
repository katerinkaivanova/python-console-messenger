"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
   и выполнить обратное преобразование (используя методы encode и decode).
"""

words_lst = ["разработка", "администрирование", "protocol", "standard"]

for enc_str in words_lst:
    enc_str_bytes = enc_str.encode('utf-8')
    print(enc_str_bytes)

    dec_str = enc_str_bytes.decode('utf-8')
    print(dec_str)
