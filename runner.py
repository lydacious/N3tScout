import os
import subprocess
import threading
from queue import Queue

# Global queue for logging
log_queue = None
processes = []
scan_completed_callback = None  # A callback to notify when scan is complete

def log_message(message):
    if log_queue:
        log_queue.put(message)
    print(message)  # Also print to the terminal

def timestamp():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def log_and_run(command):
    log_message(f"Running command: {' '.join(command)}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    processes.append(process)
    
    for line in iter(process.stdout.readline, ''):
        log_message(line.strip())
    for line in iter(process.stderr.readline, ''):
        log_message(line.strip())

    process.wait()
    processes.remove(process)

def run_scan(targets, subfinder_args, httpx_args, dirsearch_args):
    original_dir = os.getcwd()

    for target in targets:
        target_dir = os.path.join(original_dir, target)
        os.makedirs(target_dir, exist_ok=True)
        os.chdir(target_dir)

        try:
            log_message(f"Starting scan for {target} at {timestamp()}")

            # Run subfinder
            subfinder_cmd = ["subfinder", "-d", target, *subfinder_args, "-o", "subs.txt"]
            log_and_run(subfinder_cmd)

            # Run httpx
            httpx_cmd = ["httpx", "-l", "subs.txt", *httpx_args, "-o", "active_subs.txt"]
            log_and_run(httpx_cmd)

            # Run subzy
            subzy_cmd = ["subzy", "run", "--targets", "active_subs.txt"]
            log_and_run(subzy_cmd)

            # Run dirsearch
            dirsearch_cmd = ["dirsearch", "-l", "active_subs.txt", *dirsearch_args, "-o", "dirs.txt"]
            log_and_run(dirsearch_cmd)

            log_message(f"Completed scan for {target} at {timestamp()}")

        except Exception as e:
            log_message(f"Error occurred during scan for {target}: {str(e)}")

        finally:
            os.chdir(original_dir)  # Ensure returning to the original directory

    # Notify that all scans are complete
    if scan_completed_callback:
        scan_completed_callback()

def stop_all_processes():
    global processes
    for process in processes:
        if process.poll() is None:  # Check if the process is still running
            process.terminate()
            log_message(f"Terminated process: {process.pid}")
    processes.clear()

# To be used in the GUI's stop button callback
def stop_scan():
    stop_thread = threading.Thread(target=stop_all_processes)
    stop_thread.start()
