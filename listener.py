import socket
import time

HOST = "localhost"
PORT = 3000

s = socket.socket()
s.bind((HOST, PORT))
print(f"Waiting for connection on port: {PORT}")

s.listen(5)
conn, address = s.accept()

print(f"Receiving request from IP: {address}")

messages = [
    "msg A", "msg B", "msg C", "msg D"
]

for m in messages:
    m = bytes(m, "utf-8")
    conn.send(m)
    time.sleep(2)

conn.close()
