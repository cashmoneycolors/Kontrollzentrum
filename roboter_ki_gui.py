#!/usr/bin/env python3
"""ROBOTER_KI_APP - GUI Wrapper"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

class RoboterKIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ROBOTER KI APP v5.0")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Header
        header = ttk.Label(root, text="🤖 ROBOTER KI APP v5.0", font=("Arial", 16, "bold"))
        header.pack(pady=20)
        
        # Buttons
        self.create_button("🚀 Start Team Mode", self.start_team_mode)
        self.create_button("🔌 Start API Gateway", self.start_api)
        self.create_button("📊 Start Dashboard", self.start_dashboard)
        self.create_button("🏥 Health Check", self.health_check)
        self.create_button("📋 Run Week 1", self.run_week_1)
        self.create_button("📋 Run Week 2", self.run_week_2)
        self.create_button("📋 Run Week 3", self.run_week_3)
        self.create_button("📋 Run Week 4", self.run_week_4)
        self.create_button("🚀 Run All Weeks", self.run_all)
        self.create_button("❌ Exit", self.exit_app)
        
        # Status
        self.status = ttk.Label(root, text="Status: Ready", foreground="green")
        self.status.pack(pady=10)
    
    def create_button(self, text, command):
        btn = ttk.Button(self.root, text=text, command=command, width=40)
        btn.pack(pady=5)
    
    def start_team_mode(self):
        self.status.config(text="Status: Running Team Mode...", foreground="blue")
        subprocess.Popen([sys.executable, "main.py", "team"])
    
    def start_api(self):
        self.status.config(text="Status: Starting API Gateway...", foreground="blue")
        subprocess.Popen([sys.executable, "main.py", "api"])
    
    def start_dashboard(self):
        self.status.config(text="Status: Starting Dashboard...", foreground="blue")
        subprocess.Popen([sys.executable, "-m", "streamlit", "run", "main.py"])
    
    def health_check(self):
        self.status.config(text="Status: Running Health Check...", foreground="blue")
        subprocess.Popen([sys.executable, "main.py", "health"])
    
    def run_week_1(self):
        self.status.config(text="Status: Running Week 1...", foreground="blue")
        subprocess.Popen([sys.executable, "WEEK_1_EXECUTION.py"])
    
    def run_week_2(self):
        self.status.config(text="Status: Running Week 2...", foreground="blue")
        subprocess.Popen([sys.executable, "WEEK_2_EXECUTION.py"])
    
    def run_week_3(self):
        self.status.config(text="Status: Running Week 3...", foreground="blue")
        subprocess.Popen([sys.executable, "WEEK_3_EXECUTION.py"])
    
    def run_week_4(self):
        self.status.config(text="Status: Running Week 4...", foreground="blue")
        subprocess.Popen([sys.executable, "WEEK_4_EXECUTION.py"])
    
    def run_all(self):
        self.status.config(text="Status: Running All Weeks...", foreground="blue")
        subprocess.Popen([sys.executable, "RUN_NOW.py"])
    
    def exit_app(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = RoboterKIApp(root)
    root.mainloop()
