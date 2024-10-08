import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #gets local ip address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#bind to address
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"NEW CONNECTION {addr} connected.")
    
    connected = True
    while connected:
        #wait for msg from client
        msg_length = conn.recv(HEADER).decode(FORMAT)
        #only do if msg is not null
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            print(f"[{addr}] {msg}")
            print("Msg received".encode(FORMAT))
            
    print(f"[{addr}] DISCONNECTED")
    conn.close()


def start():
    server.listen()
    print(f"LISTENING: Server is listening on {SERVER} ")
    while True:
        #wait for a new connection
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"ACTIVE CONNECTIONS: {threading.active_count() - 1}")

print("STARTING SERVER")
start()