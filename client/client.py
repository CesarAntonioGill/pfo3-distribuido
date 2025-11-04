import socket
import json

HOST = '127.0.0.1'
PORT = 5000

def send_task(task):
    with socket.create_connection((HOST, PORT)) as sock:
        payload = json.dumps(task) + "\n"
        sock.sendall(payload.encode())
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
            if b"\n" in chunk:
                break
        if not data:
            print("No se recibió respuesta del servidor.")
            return
        result = json.loads(data.decode().strip())
        print("Resultado recibido:", result)

if __name__ == "__main__":
    tarea = {"id": 1, "action": "saludo", "data": "Antonio"}
    send_task(tarea)
