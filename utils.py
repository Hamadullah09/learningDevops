import json
import socket

def send_json(sock, data):
    try:
        msg = json.dumps(data).encode('utf-8') + b'\n'
        sock.sendall(msg)
    except (socket.error, BrokenPipeError) as e:
        print(f"[send_json] error: {e}")

def recv_json(sock, buffer):
    """Non-blocking JSON receive that keeps partial buffer."""
    try:
        chunk = sock.recv(4096)
        if not chunk:
            return None, buffer
        buffer += chunk
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)
            try:
                return json.loads(line.decode('utf-8')), buffer
            except json.JSONDecodeError:
                continue
    except socket.timeout:
        return None, buffer  # non-fatal
    except BlockingIOError:
        return None, buffer
    except ConnectionResetError:
        return None, buffer
    return None, buffer
