import socket
import datetime
import threading

SERVERIP = 'localhost'  # your ip
PORT = 7500
BUFSIZE = 4096

clist = []
cdict = {}

def client_handler(client, addr):
    while True:
        try:
            data = client.recv(BUFSIZE)
            check = data.decode('utf-8').split('|')
            if check[0] == 'NAME':
                cdict[str(addr)] = check[1]
        except:
            clist.remove(client)
            break

        if(not data) or (data.decode('utf-8') == 'q'):
            clist.remove(client)
            print('quit: ', client)
            break

        try:
            username = cdict[str(addr)]
            msg = username + '>>>  ' + data.decode('utf-8')  # message for send for another user
        except:
            msg = str(addr) + '>>>  ' + data.decode('utf-8')  # message for send for another user
        print('user: ', msg)
        print('--------------')
        for c in clist:
            c.sendall(msg.encode('utf-8'))

    client.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create server type ipv4
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVERIP, PORT))  # set ip and port
server.listen(5)

while True:
    client, addr = server.accept()
    clist.append(client)
    print('ALL client: ', client)

    task = threading.Thread(target=client_handler, args=(client, addr))
    task.start()





