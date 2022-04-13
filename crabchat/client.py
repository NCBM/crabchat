import socket
import hashlib


def login(host, port, username, token):
    host = socket.gethostbyname(host)
    ha = hashlib.sha256(token.encode("utf-8")).hexdigest()
    with socket.create_connection((host, port)) as so:
        so.sendall(f"CRAB_CHAT_TOKEN_{ha}_B_A_R_C".encode("utf-8"))
        rc = so.recv(16)
        if rc == b"CRABPASSUSERNAME":
            so.sendall(username.encode("utf-8"))
            rc = so.recv(12)
            if rc == b"CRAB_SUCCESS":
                print("Login success!")
        else:
            print("Login failure!")


def main():
    host = input("Host: ")
    port = input("Port(26713): ")
    if port.isalnum():
        port = int(port)
    else:
        port = 26713
    username = input("Username: ")
    token = input("Token: ")
    login(host, port, username, token)


if __name__ == "__main__":
    main()
