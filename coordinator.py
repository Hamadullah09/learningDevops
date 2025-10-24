import socket
import threading
import json
from utils import send_json, recv_json

AGENTS = {}
LOCK = threading.Lock()

def handle_agent(conn, addr):
    conn.settimeout(1.0)
    buffer = b''
    agent_id = None
    print(f"[+] Agent connected from {addr}")

    while True:
        msg, buffer = recv_json(conn, buffer)
        if msg is None:
            continue  # ignore timeout or no complete message
        if msg.get("type") == "register":
            agent_id = msg["agent_id"]
            with LOCK:
                AGENTS[agent_id] = conn
            print(f"[✓] Agent registered: {agent_id}")
            send_json(conn, {"type": "ack", "msg": "registered"})
        elif msg.get("type") == "status":
            print(f"[{agent_id}] status: {msg['data']}")
        elif msg.get("type") == "disconnect":
            print(f"[-] {agent_id} disconnected")
            break

    with LOCK:
        if agent_id in AGENTS:
            del AGENTS[agent_id]
    conn.close()

def start_socket_server(host="127.0.0.1", port=9000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(10)
    print(f"[Coordinator] Listening on {host}:{port}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_agent, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_socket_server()
