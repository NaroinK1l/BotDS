import os
import sys
import signal
import psutil

def stop_bot(pid):
    print(f"Stopping bot with PID {pid}...")
    try:
        p = psutil.Process(pid)
        p.terminate()
        p.wait(timeout=3)  # Wait for process to terminate
        print("Bot stopped.")
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} does not exist.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python stop_bot.py <pid>")
        sys.exit(1)

    bot_pid = int(sys.argv[1])
    stop_bot(bot_pid)
