import socket
import threading

host = '192.168.1.8'
port = 80
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(host)
server.bind((host, port))
server.listen()
clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle_connection(client):
    stop = False
    while not stop:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat!".encode('utf-8'))
            stop = True


def main():
    print("server is running...")
    while True:
        client, addr = server.accept()
        print(f"connected to {addr}")
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        broadcast(f"{nickname} joined the chat!\n".encode('utf-8'))
        client.send("you are now connected!".encode('utf-8'))
        thread = threading.Thread(target=handle_connection, args=(client,))
        thread.start()
        


if __name__ == '__main__':
    main()
