import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 9999

clients = []
lock = threading.Lock()


def broadcast(message: bytes, sender_conn: socket.socket):
    with lock:
        for conn in clients:
            if conn is not sender_conn:
                try:
                    conn.sendall(message)
                except OSError:
                    pass


def handle_client(conn: socket.socket, addr: tuple, name: str):
    join_msg = f"[Server] {name} joined the chat.\n"
    print(join_msg, end="")
    broadcast(join_msg.encode(), conn)

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            text = data.decode().strip()
            relay = f"[{name}] {text}\n"
            print(relay, end="")
            broadcast(relay.encode(), conn)
    except (ConnectionResetError, OSError):
        pass
    finally:
        leave_msg = f"[Server] {name} left the chat.\n"
        print(leave_msg, end="")
        with lock:
            if conn in clients:
                clients.remove(conn)
        broadcast(leave_msg.encode(), conn)
        conn.close()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, port))
    server.listen(5)
    print(f"Chat server listening on {HOST}:{port}")

    try:
        while True:
            conn, addr = server.accept()
            conn.sendall(b"Enter your name: ")
            name = conn.recv(1024).decode().strip()
            if not name:
                name = f"User-{addr[1]}"
            with lock:
                clients.append(conn)
            t = threading.Thread(target=handle_client, args=(conn, addr, name), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
