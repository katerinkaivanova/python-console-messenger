"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
   преобразовать результаты из байтовового в строковый тип на кириллице.
"""

import subprocess
import chardet
import time

resources = ['yandex.ru', 'youtube.com']
for address in resources:
    print(address)
    ping_address = subprocess.Popen(['ping', address], stdout=subprocess.PIPE)

    timeout = time.time() + 3
    while True:

        for line in ping_address.stdout:
            if time.time() > timeout:
                break

            result = chardet.detect(line)
            print(result)
            line = line.decode(result['encoding']).encode('utf-8')
            print(line.decode('utf-8'))

        if time.time() > timeout:
            break
