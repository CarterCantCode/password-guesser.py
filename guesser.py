import tkinter as tk
from tkinter import messagebox
import os
import json
import threading
import time
import pyautogui
import numpy as np
import cv2
from tkinter import ttk
from typing import List

# VALIDATE 'MAX_LEN' WITH FUNCTION
def validate_charset(charset: str) -> bool:
    if not charset:
        messagebox.showerror("Input Error", "Charset cannot be empty.")
        return False
    if len(charset) < 2:
        messagebox.showerror("Input Error", "Charset must contain at least two characters.")
        return False
    return True

# VALIDATE 'DELAY' WITH FUNCTION
def validate_max_len(max_len: int) -> bool:
    if max_len <= 0 or max_len > 12:  # Limiting max length to prevent large search space
        messagebox.showerror("Input Error", "Max length should be a positive integer between 1 and 12.")
        return False
    return True

# CHECK IF TEMPLATES FOLDER EXISTS & CONTAINS VALID IMAGES WITH FUNCTION
def validate_delay(delay: float) -> bool:
    if delay < 0:
        messagebox.showerror("Input Error", "Delay cannot be negative.")
        return False
    return True


def validate_templates_folder() -> bool:
    templates_folder = "templates"
    if not os.path.exists(templates_folder):
        messagebox.showerror("Folder Error", f"'{templates_folder}' folder does not exist.")
        return False

    template_files = [f for f in os.listdir(templates_folder) if f.endswith('.png')]
    if not template_files:
        messagebox.showerror("Template Error", "No PNG template files found in the 'templates' folder.")
        return False

    return True

# BRUTE FORCE PROGRAM
class BruteForceApp:
    def __init__(self, root: tk.Tk, charset: str, max_len: int, delay: float, threshold: float):
        self.root = root
        self.charset = charset
        self.max_len = max_len
        self.delay = delay
        self.threshold = threshold
        self.is_running = False
        self.is_paused = False
        self.stop_event = threading.Event()

        self.create_gui()
        self.load_checkpoint()

    def create_gui(self):
        self.root.title("Password Brute Force")

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.root, length=300, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, columnspan=2, pady=20)

        # Text log area
        self.log_area = tk.Text(self.root, height=10, width=50)
        self.log_area.grid(row=2, column=0, columnspan=2, padx=20)

        # Buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.grid(row=3, column=0, padx=20)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause, state=tk.DISABLED)
        self.pause_button.grid(row=3, column=1, padx=20)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_button.grid(row=3, column=2, padx=20)

    def log(self, msg, overwrite=False):
        if overwrite:
            self.log_area.delete(1.0, tk.END)
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.yview(tk.END)

    def load_checkpoint(self):
        checkpoint_file = "checkpoint.json"
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file, 'r') as f:
                data = json.load(f)
                self.charset = data.get('charset', self.charset)
                self.max_len = data.get('max_len', self.max_len)
                self.delay = data.get('delay', self.delay)
                self.threshold = data.get('threshold', self.threshold)
        else:
            self.log("No checkpoint found. Starting fresh.")

    def save_checkpoint(self):
        checkpoint_data = {
            'charset': self.charset,
            'max_len': self.max_len,
            'delay': self.delay,
            'threshold': self.threshold
        }
        with open("checkpoint.json", 'w') as f:
            json.dump(checkpoint_data, f)

    def start(self):
        if not validate_charset(self.charset) or not validate_max_len(self.max_len) or not validate_delay(self.delay):
            return

        if not validate_templates_folder():
            return

        self.is_running = True
        self.is_paused = False
        self.stop_event.clear()

        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)

        self.run_bruteforce()

    def pause(self):
        if self.is_running:
            self.is_paused = True
            self.pause_button.config(text="Resume", command=self.resume)
            self.log("Brute force paused.")
        else:
            self.log("Brute force is already paused.")

    def resume(self):
        if self.is_paused:
            self.is_paused = False
            self.pause_button.config(text="Pause", command=self.pause)
            self.log("Resuming brute force...")
            self.run_bruteforce()

    def stop(self):
        self.is_running = False
        self.stop_event.set()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.log("Brute force stopped.")

    def run_bruteforce(self):
        def brute_force():
            total_combinations = len(self.charset) ** self.max_len
            completed = 0
            for i in range(total_combinations):
                if self.stop_event.is_set():
                    break

                if self.is_paused:
                    time.sleep(0.5)
                    continue

                password_attempt = self.generate_password(i)
                self.log(f"Attempting: {password_attempt}")
                self.save_checkpoint()

                if self.match_templates(password_attempt):
                    self.log(f"Success! Password found: {password_attempt}", overwrite=True)
                    self.stop()
                    return

                completed += 1
                progress = (completed / total_combinations) * 100
                self.progress_bar['value'] = progress
                time.sleep(self.delay)

            if not self.stop_event.is_set():
                self.log("Password brute force complete.")
                self.stop()

        threading.Thread(target=brute_force, daemon=True).start()

    def generate_password(self, index: int) -> str:
        password = ""
        charset_len = len(self.charset)
        for _ in range(self.max_len):
            password = self.charset[index % charset_len] + password
            index //= charset_len
        return password

    def match_templates(self, password: str) -> bool:
        # Template matching logic (dummy implementation)
        return np.random.random() < self.threshold

# PROGRAM EXECUTION
if __name__ == "__main__":
    # CUSTOMIZE PARAMETERS
    charset = "abc123"
    max_len = 3
    delay = 0.5
    threshold = 0.9

    root = tk.Tk()
    app = BruteForceApp(root, charset, max_len, delay, threshold)
    root.mainloop()
