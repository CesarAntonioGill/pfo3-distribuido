import socket
import threading
import json
from concurrent.futures import ThreadPoolExecutor
import time

HOST = '0.0.0.0'
PORT = 5000
MAX_WORKERS = 4

def process_task(task):
    """Simula el procesamiento de una tarea."""
    print(f"[WORKER] Procesando tarea id={task.get('id')}")
    time.sleep(2)
    result = {
        "id": task.get("id"),
        "status": "ok",
        "input": task,
        "output": f"Resultado de {task.get('action')}"
    }
    return result

def handle_client(conn, addr, executor):
    print(f"[SERVER] Cliente conectado: {addr}")
    try:
        data = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
            if b"\n" in chunk:
                break
        if not data:
            return
        task = json.loads(data.decode().strip())
        future = executor.submit(process_task, task)
        result = future.result()
        conn.sendall((json.dumps(result) + "\n").encode())
        print(f"[SERVER] Resultado enviado a {addr}")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

def main():
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER] Escuchando en {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr, executor))
            thread.start()

if __name__ == "__main__":
    main()
