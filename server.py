import socket
import cfg

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((cfg.HOST, cfg.PORT))

server_socket.listen()

print("Waiting for players...")
player1, address1 = server_socket.accept()
print(f"Player 1 ({address1}) conect.")
player2, address2 = server_socket.accept()
print(f"Player 2 ({address2}) conect.")

player1.sendall("welcome to the checkers game you are the white player".encode())
player2.sendall("welcome to the checkers game you are the red player".encode())
player1.sendall("white".encode())
player2.sendall("red".encode())

while True:
    data = player1.recv(1024).decode()
    if not data:
        break
    print(f"Plater 1 ({address1}) played: {data}")
    player2.sendall(data.encode())

    data = player2.recv(1024).decode()
    if not data:
        break
    print(f"Plater 2 ({address2}) played: {data}")
    player1.sendall(data.encode())

player1.close()
player2.close()
server_socket.close()