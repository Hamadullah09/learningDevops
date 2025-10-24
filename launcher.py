import subprocess
import sys

PY = sys.executable

for i in range(3):
    subprocess.Popen([PY, "agent.py", f"agent-{i+1}"])
