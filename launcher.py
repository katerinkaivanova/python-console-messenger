import os
import subprocess
import psutil
import time

all_processes = []

while True:
    action = input('q - выход \n'
                   's - запустить сервер и клиенты \n'
                   'x - закрыть все окна \n'
                   'Введите действие: ')

    if action == 'q':
        break
    elif action == 's':

        server_path = os.getcwd() + '/' + 'server.py'
        client_path = os.getcwd() + '/' + 'client.py'
        bash_path = os.getcwd() + '/' + 'run.sh'

        server_start = f'python {server_path}'
        client_send_start = f'python {client_path} -m send'
        client_listen_start = f'python {client_path} -m listen'

        # shell=True неявно запускает процесс /bin/sh
        all_processes.append(subprocess.Popen(f'{bash_path} {server_start}', stdout=subprocess.PIPE, shell=True))
        time.sleep(1)

        for i in range(1):
            all_processes.append(subprocess.Popen(f'{bash_path} {client_send_start}', stdout=subprocess.PIPE, shell=True))
            time.sleep(1)
            all_processes.append(subprocess.Popen(f'{bash_path} {client_listen_start}', stdout=subprocess.PIPE, shell=True))

        print(all_processes)

    elif action == 'x':
        for p in all_processes:
            main_process = psutil.Process(p.pid)
            print(print(p.pid), main_process)
            for child_process in main_process.children(recursive=True):
                child_process.terminate()

        all_processes.clear()
        print(all_processes)
