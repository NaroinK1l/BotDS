import os
import sys
import time
import signal
import subprocess
import psutil

def restart_bot(pid):
    print(f"Restarting bot with PID {pid}...")
    try:
        p = psutil.Process(pid)
        p.terminate()
        p.wait(timeout=3)  # Wait for process to terminate
        print(f"Process with PID {pid} terminated.")
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} does not exist.")

    subprocess.Popen([sys.executable, "bot.py"])
    print("Bot restarted.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python restart_bot.py <pid>")
        sys.exit(1)

    bot_pid = int(sys.argv[1])
    restart_bot(bot_pid)
