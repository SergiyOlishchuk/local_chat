import socket
from threading import Thread
from time import sleep

running = True
clients = []

def receiving_server(server: socket.socket):
    global clients  
    global running
    
    while running:
        data, addr = server.recvfrom(1024)

        data = data.decode('utf-8')

        if addr not in clients:
            clients.append(addr)

        print(data)

        for client in clients:
            if client != addr:
                server.sendto(data.encode('utf-8'), client)
        
        sleep(0.3)

def receiving_client(client: socket.socket):
    
    global running
    while running:
        data, addr = client.recvfrom(1024)

        data = data.decode('utf-8')

        if data == '!q':
            running = False
            break
        else:
            print(data)

def server_socket():
    global running

    HOST = socket.gethostbyname(socket.gethostname())
    
    while True:
        try:
            PORT = int(input('Введите порт, на котором будет чат (> 1024): '))
        except ValueError:
            print('Invalid input\nTry again')
            continue
        
        if PORT > 1024:
            break
        else:
            print('Try again')

    print(f'Ваш ip: {HOST}')

    name = input('Введите свое имя: ')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))

        print('[ SERVER STARTED ]')

        receiving = Thread(target=receiving_server, args=(server, ))
        receiving.start()

        while running:
            message = input()

            if message == '!q':
                for client in clients:
                    server.sendto('!q'.encode('utf-8'), client)
                running = False
            else:
                for client in clients:
                    server.sendto(f'[{name}] :: {message}'.encode('utf-8'), client)
    
    print('[ SERVER STOPPED ]')

def client_socket():
    global running
    join = False

    HOST = input('Введите ip хоста: ')
    
    while True:
        try:
            PORT = int(input('Введите порт, на котором будет чат (> 1024): '))
        except ValueError:
            print('Invalid input\nTry again')
            continue
        
        if PORT > 1024:
            break
        else:
            print('Try again')

    name = input('Введите свое имя: ')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.connect((HOST, PORT))

        print('[SUCCESSFULY CONNECTED]')

        receiving = Thread(target=receiving_client, args=(client, ))
        receiving.start()

        while running:
            if not join:
                client.send(f'{name} join chat'.encode('utf-8'))
                join = True
            
            message = input()

            client.send(f'[{name}] :: {message}'.encode('utf-8'))
    
    print('[CONNECTING STOPPED]')

def main():
    todo = input('Вы хотите подключиться или создать сервер? (1, 2): ')
    if todo == '1':
        client_socket()
    elif todo == '2':
        server_socket()

if __name__ == '__main__':
    main()