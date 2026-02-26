import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 9999


def receive_messages(conn: socket.socket):
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                print("\n[Disconnected from server]")
                break
            sys.stdout.write(data.decode())
            sys.stdout.flush()
    except (ConnectionResetError, OSError):
        print("\n[Connection lost]")


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else PORT

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((host, port))

    # Server asks for name
    prompt = conn.recv(1024).decode()
    sys.stdout.write(prompt)
    sys.stdout.flush()
    name = input()
    conn.sendall(name.encode())

    print(f"Connected as '{name}'. Type messages and press Enter to send. Ctrl+C to quit.\n")

    reader = threading.Thread(target=receive_messages, args=(conn,), daemon=True)
    reader.start()

    try:
        while True:
            msg = input()
            if msg:
                conn.sendall(msg.encode())
    except (KeyboardInterrupt, EOFError):
        print("\nDisconnecting...")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
