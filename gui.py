import tkinter as tk
from tkinter import ttk
import threading
from queue import Queue, Empty
import runner

# Initialize the log queue
log_queue = Queue()
runner.log_queue = log_queue  # Pass the queue to runner.py

def update_logs_from_queue():
    while True:
        try:
            log_message = log_queue.get_nowait()
            logs_text.insert(tk.END, log_message + "\n")
            logs_text.yview(tk.END)
        except Empty:
            break
    root.after(100, update_logs_from_queue)

def scan_completed():
    run_stop_button.config(text="Run", bg="green")

runner.scan_completed_callback = scan_completed

# Function to handle the "Run" button click
def toggle_button():
    if run_stop_button["text"] == "Run":
        run_stop_button.config(text="Stop", bg="red")
        start_scan()
    else:
        run_stop_button.config(text="Run", bg="green")
        stop_scan()

def start_scan():
    # Collect the target
    targets = target_entry.get().split(",")

    # Collect arguments for each tool
    subfinder_args = build_subfinder_args()
    httpx_args = build_httpx_args()
    dirsearch_args = build_dirsearch_args()

    # Call the run_scan function from runner.py
    scan_thread = threading.Thread(target=runner.run_scan, args=(targets, subfinder_args, httpx_args, dirsearch_args))
    scan_thread.start()
    # Start updating logs from queue
    root.after(100, update_logs_from_queue)

def stop_scan():
    runner.stop_scan()

def build_subfinder_args():
    subfinder_args = []
    if subfinder_all.var.get(): subfinder_args.append("-all")
    if subfinder_recursive.var.get(): subfinder_args.append("-recursive")
    if subfinder_nw.var.get(): subfinder_args.append("-nW")
    subfinder_args.extend(subfinder_additional_args.get().split())
    return subfinder_args

def build_httpx_args():
    httpx_args = []
    httpx_args.extend(httpx_mc.get().split())
    httpx_args.extend(httpx_fc.get().split())
    httpx_args.extend(httpx_t.get().split())
    if httpx_status_code.var.get(): httpx_args.append("-sc")
    httpx_args.extend(httpx_additional_args.get().split())
    return httpx_args

def build_dirsearch_args():
    dirsearch_args = []
    if dirsearch_random_agent.var.get(): dirsearch_args.append("--random-agent")
    if dirsearch_crawl.var.get(): dirsearch_args.append("--crawl")
    dirsearch_args.extend(dirsearch_r.get().split())
    dirsearch_args.extend(dirsearch_t.get().split())
    dirsearch_args.extend(dirsearch_i.get().split())
    dirsearch_args.extend(dirsearch_x.get().split())
    dirsearch_args.extend(dirsearch_additional_args.get().split())
    return dirsearch_args

# Create the main window
root = tk.Tk()
root.title("N3tScout")
root.minsize(800, 500)

# Target input field
target_frame = ttk.Frame(root, padding=(10, 5))
target_frame.pack(fill="x", padx=10, pady=5)
target_label = tk.Label(target_frame, text="Targets:")
target_label.pack(side="left")
target_entry = tk.Entry(target_frame, width=70)
target_entry.pack(side="left", padx=10)

# Define frame for each tool
def create_tool_frame(parent, tool_name):
    frame = ttk.LabelFrame(parent, text=tool_name, padding=(10, 5))
    frame.pack(fill="x", padx=10, pady=5, expand=True)
    return frame

# Create entry fields for options
def create_option_entry(parent, label_text, entry_width=10):
    label = tk.Label(parent, text=label_text)
    label.pack(side="left", padx=(0, 5))
    entry = tk.Entry(parent, width=entry_width)
    entry.pack(side="left", padx=(0, 10))
    return entry

# Create checkbox fields for options
def create_option_checkbox(parent, label_text):
    var = tk.BooleanVar()
    label = tk.Checkbutton(parent, text=label_text, variable=var)
    label.pack(side="left", padx=(0, 10))
    label.var = var
    return label

# Create frame for subfinder
subfinder_frame = create_tool_frame(root, "subfinder")
subfinder_all = create_option_checkbox(subfinder_frame, "-all")
subfinder_recursive = create_option_checkbox(subfinder_frame, "-recursive")
subfinder_nw = create_option_checkbox(subfinder_frame, "-nW")
subfinder_additional_args = create_option_entry(subfinder_frame, "additional args:", 30)

# Create frame for httpx
httpx_frame = create_tool_frame(root, "httpx")
httpx_mc = create_option_entry(httpx_frame, "-mc", 5)
httpx_fc = create_option_entry(httpx_frame, "-fc", 5)
httpx_t = create_option_entry(httpx_frame, "-t", 5)
httpx_status_code = create_option_checkbox(httpx_frame, "-sc")
httpx_additional_args = create_option_entry(httpx_frame, "additional args:", 30)

# Create frame for dirsearch
dirsearch_frame = create_tool_frame(root, "dirsearch")
dirsearch_random_agent = create_option_checkbox(dirsearch_frame, "--random-agent")
dirsearch_crawl = create_option_checkbox(dirsearch_frame, "--crawl")
dirsearch_r = create_option_entry(dirsearch_frame, "-r", 5)
dirsearch_t = create_option_entry(dirsearch_frame, "-t", 5)
dirsearch_i = create_option_entry(dirsearch_frame, "-i", 5)
dirsearch_x = create_option_entry(dirsearch_frame, "-x", 5)
dirsearch_additional_args = create_option_entry(dirsearch_frame, "additional args:", 30)

# Run/Stop button
action_frame = ttk.Frame(root, padding=(10, 5))
action_frame.pack(fill="x", padx=10, pady=5)
run_stop_button = tk.Button(action_frame, text="Run", width=10, bg="green", fg="white", command=toggle_button)
run_stop_button.pack(side="left", padx=5)

# Logs section
logs_frame = ttk.Frame(root, padding=(10, 5))
logs_frame.pack(fill="both", padx=10, pady=5, expand=True)
logs_text = tk.Text(logs_frame, wrap="word", height=15)
logs_text.pack(fill="both", expand=True)
logs_scroll = tk.Scrollbar(logs_frame, command=logs_text.yview)
logs_scroll.pack(side="right", fill="y")
logs_text.config(yscrollcommand=logs_scroll.set)

# Run the application
root.mainloop()
