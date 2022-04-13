import socket
import hashlib
from multiprocessing import Process
from datetime import datetime


registered = []


def user_session(conn, addr, token, ha):
    ve = conn.recv(88).decode("utf-8")
    if ve.find("CRAB_CHAT_TOKEN_") == 0 and \
            ve.rfind("_B_A_R_C") == 80:
        hashed = ve[16:-8]
        if ha == hashed or not token:
            print(
                f"[{datetime.now().isoformat()}]",
                f"'{addr[0]}:{addr[1]}':",
                "Verify success!"
            )
            conn.sendall(b"CRABPASSUSERNAME")
            name = conn.recv(256).decode("utf-8")
            if name not in registered:
                registered.append(name)
            conn.sendall(b"CRAB_SUCCESS")
            print(
                f"[{datetime.now().isoformat()}]",
                f"'{addr[0]}:{addr[1]}': Login as '{name}'"
            )
        else:
            conn.sendall(b"CRABLOGINFAILURE")
            print(
                f"[{datetime.now().isoformat()}]",
                f"'{addr[0]}:{addr[1]}': Verify failure!"
            )


def start_server(port: int = 26713, token: str = ""):
    if token:
        ha = hashlib.sha256(token.encode("utf-8")).hexdigest()
    with socket.create_server(('', port)) as server:
        print(
            f"[{datetime.now().isoformat()}]",
            f"Server started on '127.0.0.1:{port}'."
        )
        while True:
            conn, addr = server.accept()
            print(
                f"[{datetime.now().isoformat()}]",
                f"Accepted connection from '{addr[0]}:{addr[1]}'."
            )
            proc = Process(target=user_session, args=(conn, addr, token, ha))
            proc.start()


def main():
    start_server(token=input("Token: "))


if __name__ == "__main__":
    main()
