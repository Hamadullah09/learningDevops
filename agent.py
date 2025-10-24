import socket
import time
import random
from utils import send_json, recv_json

def run_agent(agent_id, host="127.0.0.1", port=9000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.settimeout(1.0)
    buffer = b''

    send_json(sock, {"type": "register", "agent_id": agent_id})

    last_status = time.time()

    while True:
        msg, buffer = recv_json(sock, buffer)
        if msg and msg.get("type") == "ack":
            print(f"[{agent_id}] Registered successfully")

        if time.time() - last_status > 2:
            data = random.choice(["idle", "working", "waiting"])
            send_json(sock, {"type": "status", "agent_id": agent_id, "data": data})
            last_status = time.time()
        time.sleep(0.5)

if __name__ == "__main__":
    import sys
    agent_id = sys.argv[1] if len(sys.argv) > 1 else f"agent-{random.randint(100,999)}"
    run_agent(agent_id)
