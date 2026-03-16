#!/usr/bin/env python3
"""
Hugo Blog Manager - Clean Professional UI
Features:
- Create/Delete posts with category selection
- Start/Stop Hugo server
- Commit and push to GitHub
- Clean, minimal interface matching blog style
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import webbrowser
from datetime import datetime
import threading

# Project configuration
PROJECT_DIR = r"c:\Users\li\adlink8.github.io"
HUGO_PORT = 1313

# Professional dark color scheme - clean and readable
COLORS = {
    'bg_main': '#1e1e1e',           # Dark background
    'bg_card': '#2d2d2d',           # Card background
    'bg_input': '#3c3c3c',          # Input background
    'accent_primary': '#3b82f6',    # Primary blue
    'accent_secondary': '#64748b',  # Secondary gray
    'accent_success': '#22c55e',    # Green for success
    'accent_danger': '#ef4444',     # Red for danger
    'accent_warning': '#f97316',    # Orange for warning
    'accent_info': '#06b6d4',       # Cyan for info
    'accent_purple': '#a855f7',     # Purple accent
    'text_primary': '#f1f5f9',      # Primary text
    'text_secondary': '#94a3b8',    # Secondary text
    'text_muted': '#64748b',        # Muted text
    'border': '#404040',            # Border color
    'border_focus': '#3b82f6',      # Focus border
}

# Category configuration
CATEGORIES = {
    "daily": {"name": "Timeline", "icon": "📅", "color": "#2563eb"},
    "pitfalls": {"name": "Lab Notes", "icon": "🛠️", "color": "#ea580c"},
    "insights": {"name": "Insights", "icon": "💡", "color": "#7c3aed"},
    "reflections": {"name": "Reflection", "icon": "🔄", "color": "#0891b2"},
    "project-logs": {"name": "Project Log", "icon": "📁", "color": "#16a34a"},
}


class ModernButton(tk.Frame):
    """Modern flat button with hover effect"""
    
    def __init__(self, parent, text, command=None, color="#2563eb", width=140, height=36):
        super().__init__(parent, bg=parent.cget('bg'))
        
        self.command = command
        self.color = color
        self.hover_color = self._lighten_color(color, 0.15)
        
        self.btn = tk.Button(
            self, text=text, command=command,
            bg=color, fg='white',
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT, cursor="hand2",
            width=width//8, height=1,
            activebackground=self.hover_color,
            activeforeground='white',
            borderwidth=0
        )
        self.btn.pack(fill=tk.BOTH, expand=True)
        
        self.btn.bind("<Enter>", self._on_enter)
        self.btn.bind("<Leave>", self._on_leave)
        
    def _lighten_color(self, color, factor):
        color = color.lstrip('#')
        r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _on_enter(self, event):
        self.btn.config(bg=self.hover_color)
        
    def _on_leave(self, event):
        self.btn.config(bg=self.color)


class CardPanel(tk.Frame):
    """Material design style card panel"""
    
    def __init__(self, parent, title, accent_color="#2563eb"):
        super().__init__(parent, bg=COLORS['bg_card'], padx=0, pady=0)
        
        # Subtle border
        self.config(highlightbackground=COLORS['border'], highlightthickness=1)
        
        # Header with accent line
        header_frame = tk.Frame(self, bg=COLORS['bg_card'])
        header_frame.pack(fill=tk.X)
        
        # Left accent bar
        accent_bar = tk.Frame(header_frame, bg=accent_color, width=4)
        accent_bar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Title
        tk.Label(
            header_frame, text=title, 
            bg=COLORS['bg_card'], fg=COLORS['text_primary'],
            font=("Segoe UI", 11, "bold"), padx=12, pady=10
        ).pack(side=tk.LEFT)
        
        # Content area
        self.content = tk.Frame(self, bg=COLORS['bg_card'], padx=12, pady=12)
        self.content.pack(fill=tk.BOTH, expand=True)


class HugoBlogManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Hugo Blog Manager")
        self.root.geometry("1100x580")
        self.root.configure(bg=COLORS['bg_main'])
        self.root.resizable(True, True)
        
        self.server_process = None
        self.server_running = False
        self.posts_list = []
        
        self.setup_ui()
        self.refresh_posts()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['bg_main'], padx=12, pady=12)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid
        for i in range(4):
            main_frame.columnconfigure(i, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Panels
        self.create_server_panel(main_frame, 0)
        self.create_post_panel(main_frame, 1)
        self.create_manage_panel(main_frame, 2)
        self.create_git_panel(main_frame, 3)
        
    def create_header(self, parent):
        header = tk.Frame(parent, bg=COLORS['bg_main'])
        header.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 12))
        
        # Left side - Logo
        left_frame = tk.Frame(header, bg=COLORS['bg_main'])
        left_frame.pack(side=tk.LEFT)
        
        # Main title
        tk.Label(
            left_frame, text="Hugo", 
            bg=COLORS['bg_main'], fg=COLORS['accent_primary'],
            font=("Segoe UI", 20, "bold")
        ).pack(side=tk.LEFT)
        
        tk.Label(
            left_frame, text=" Blog Manager", 
            bg=COLORS['bg_main'], fg=COLORS['text_primary'],
            font=("Segoe UI", 20)
        ).pack(side=tk.LEFT)
        
        # Right side - Status
        right_frame = tk.Frame(header, bg=COLORS['bg_main'])
        right_frame.pack(side=tk.RIGHT)
        
        # Status indicator
        status_frame = tk.Frame(right_frame, bg=COLORS['bg_card'], padx=12, pady=6)
        status_frame.pack(side=tk.RIGHT)
        
        self.status_indicator = tk.Canvas(
            status_frame, width=10, height=10, 
            bg=COLORS['bg_card'], highlightthickness=0
        )
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 6))
        self.status_indicator.create_oval(0, 0, 10, 10, fill=COLORS['text_muted'], outline="")
        
        self.status_label = tk.Label(
            status_frame, text="Offline", 
            bg=COLORS['bg_card'], fg=COLORS['text_muted'],
            font=("Segoe UI", 9)
        )
        self.status_label.pack(side=tk.LEFT)
        
    def create_server_panel(self, parent, col):
        panel = CardPanel(parent, "Server", COLORS['accent_primary'])
        panel.grid(row=1, column=col, sticky="nsew", padx=(0, 8))
        
        # Status display
        status_box = tk.Frame(panel.content, bg=COLORS['bg_input'], padx=10, pady=8)
        status_box.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(
            status_box, text="Status", 
            bg=COLORS['bg_input'], fg=COLORS['text_muted'],
            font=("Segoe UI", 8)
        ).pack(anchor=tk.W)
        
        self.server_status_text = tk.Label(
            status_box, text="Stopped", 
            bg=COLORS['bg_input'], fg=COLORS['text_secondary'],
            font=("Segoe UI", 10)
        )
        self.server_status_text.pack(anchor=tk.W)
        
        # Control buttons
        ModernButton(
            panel.content, "Start Server", 
            command=self.start_server,
            color=COLORS['accent_success']
        ).pack(fill=tk.X, pady=(0, 6))
        
        ModernButton(
            panel.content, "Stop Server", 
            command=self.stop_server,
            color=COLORS['accent_danger']
        ).pack(fill=tk.X, pady=(0, 6))
        
        ModernButton(
            panel.content, "Open Browser", 
            command=self.open_browser,
            color=COLORS['accent_info']
        ).pack(fill=tk.X, pady=(0, 12))
        
        # Separator
        tk.Frame(panel.content, height=1, bg=COLORS['border']).pack(fill=tk.X, pady=8)
        
        # Quick actions
        tk.Label(
            panel.content, text="Quick Actions", 
            bg=COLORS['bg_card'], fg=COLORS['text_muted'],
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W, pady=(0, 6))
        
        ModernButton(
            panel.content, "Open Project Folder", 
            command=lambda: os.startfile(PROJECT_DIR),
            color=COLORS['accent_purple']
        ).pack(fill=tk.X, pady=(0, 6))
        
        ModernButton(
            panel.content, "Build Site", 
            command=self.build_site,
            color=COLORS['accent_warning']
        ).pack(fill=tk.X)
        
    def create_post_panel(self, parent, col):
        panel = CardPanel(parent, "Create Post", COLORS['accent_purple'])
        panel.grid(row=1, column=col, sticky="nsew", padx=4)
        
        # Filename input
        tk.Label(
            panel.content, text="Filename", 
            bg=COLORS['bg_card'], fg=COLORS['text_muted'],
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W)
        
        input_frame = tk.Frame(panel.content, bg=COLORS['bg_input'], padx=8, pady=6)
        input_frame.pack(fill=tk.X, pady=(4, 12))
        
        self.filename_entry = tk.Entry(
            input_frame, bg=COLORS['bg_input'], fg=COLORS['text_primary'],
            insertbackground=COLORS['accent_primary'], 
            font=("Segoe UI", 10),
            relief=tk.FLAT, borderwidth=0
        )
        self.filename_entry.pack(fill=tk.X)
        
        # Category selection
        tk.Label(
            panel.content, text="Category", 
            bg=COLORS['bg_card'], fg=COLORS['text_muted'],
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W, pady=(0, 6))
        
        for cat_key, cat_info in CATEGORIES.items():
            ModernButton(
                panel.content, 
                f"{cat_info['icon']} {cat_info['name']}", 
                command=lambda k=cat_key: self.create_post(k),
                color=cat_info['color']
            ).pack(fill=tk.X, pady=2)
        
    def create_manage_panel(self, parent, col):
        panel = CardPanel(parent, "Manage Posts", COLORS['accent_info'])
        panel.grid(row=1, column=col, sticky="nsew", padx=4)
        
        # Filter row
        filter_frame = tk.Frame(panel.content, bg=COLORS['bg_card'])
        filter_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(
            filter_frame, text="Filter", 
            bg=COLORS['bg_card'], fg=COLORS['text_muted'],
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT)
        
        self.filter_category = ttk.Combobox(
            filter_frame, 
            values=["All"] + [c['name'] for c in CATEGORIES.values()],
            width=12, state="readonly", font=("Segoe UI", 8)
        )
        self.filter_category.set("All")
        self.filter_category.pack(side=tk.LEFT, padx=(8, 4))
        self.filter_category.bind("<<ComboboxSelected>>", lambda e: self.refresh_posts())
        
        # Refresh button
        refresh_btn = tk.Button(
            filter_frame, text="↻", 
            command=self.refresh_posts,
            bg=COLORS['bg_input'], fg=COLORS['text_secondary'],
            font=("Segoe UI", 10), relief=tk.FLAT, cursor="hand2",
            width=3, borderwidth=0
        )
        refresh_btn.pack(side=tk.LEFT)
        
        # Posts list
        list_frame = tk.Frame(panel.content, bg=COLORS['bg_input'], padx=4, pady=4)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        
        self.posts_listbox = tk.Listbox(
            list_frame, bg=COLORS['bg_input'], fg=COLORS['text_primary'],
            selectbackground=COLORS['accent_primary'], selectforeground='white',
            font=("Segoe UI", 9), relief=tk.FLAT, borderwidth=0,
            highlightthickness=0
        )
        self.posts_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Delete button
        ModernButton(
            panel.content, "Delete Selected", 
            command=self.delete_post,
            color=COLORS['accent_danger']
        ).pack(fill=tk.X)
        
    def create_git_panel(self, parent, col):
        panel = CardPanel(parent, "Git Control", COLORS['accent_success'])
        panel.grid(row=1, column=col, sticky="nsew", padx=(8, 0))
        
        # Git buttons row
        btn_row = tk.Frame(panel.content, bg=COLORS['bg_card'])
        btn_row.pack(fill=tk.X, pady=(0, 6))
        
        ModernButton(
            btn_row, "Status", 
            command=self.git_status, 
            color=COLORS['accent_info']
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))
        
        ModernButton(
            btn_row, "Add", 
            command=self.git_add, 
            color=COLORS['accent_success']
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))
        
        ModernButton(
            btn_row, "Commit", 
            command=self.git_commit, 
            color=COLORS['accent_warning']
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        ModernButton(
            panel.content, "Push to GitHub", 
            command=self.git_push,
            color=COLORS['accent_primary']
        ).pack(fill=tk.X, pady=(0, 10))
        
        # Commit message
        tk.Label(
            panel.content, text="Commit Message", 
            bg=COLORS['bg_card'], fg=COLORS['text_muted'],
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W)
        
        input_frame = tk.Frame(panel.content, bg=COLORS['bg_input'], padx=8, pady=6)
        input_frame.pack(fill=tk.X, pady=(4, 6))
        
        self.commit_msg_entry = tk.Entry(
            input_frame, bg=COLORS['bg_input'], fg=COLORS['text_primary'],
            insertbackground=COLORS['accent_primary'], 
            font=("Segoe UI", 9),
            relief=tk.FLAT, borderwidth=0
        )
        self.commit_msg_entry.pack(fill=tk.X)
        
        ModernButton(
            panel.content, "Quick Deploy", 
            command=self.quick_commit,
            color=COLORS['accent_purple']
        ).pack(fill=tk.X, pady=(0, 10))
        
        # Log output
        tk.Label(
            panel.content, text="Log", 
            bg=COLORS['bg_card'], fg=COLORS['text_muted'],
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W)
        
        log_frame = tk.Frame(panel.content, bg=COLORS['bg_input'], padx=6, pady=6)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_output = tk.Text(
            log_frame, bg=COLORS['bg_input'], fg=COLORS['text_secondary'],
            font=("Consolas", 8), relief=tk.FLAT, borderwidth=0,
            highlightthickness=0, wrap=tk.WORD
        )
        self.log_output.pack(fill=tk.BOTH, expand=True)
        
    def log(self, message, level="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_output.see(tk.END)
        
    def update_server_status(self, running):
        if running:
            self.status_indicator.delete("all")
            self.status_indicator.create_oval(0, 0, 10, 10, fill=COLORS['accent_success'], outline="")
            self.status_label.config(text="Online", fg=COLORS['accent_success'])
            self.server_status_text.config(text="Running", fg=COLORS['accent_success'])
        else:
            self.status_indicator.delete("all")
            self.status_indicator.create_oval(0, 0, 10, 10, fill=COLORS['text_muted'], outline="")
            self.status_label.config(text="Offline", fg=COLORS['text_muted'])
            self.server_status_text.config(text="Stopped", fg=COLORS['text_secondary'])
        
    def run_command(self, command, cwd=PROJECT_DIR):
        try:
            result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, shell=True)
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)
    
    def get_all_posts(self):
        posts = []
        content_dir = os.path.join(PROJECT_DIR, "content")
        
        for cat_key, cat_info in CATEGORIES.items():
            cat_dir = os.path.join(content_dir, cat_key)
            if os.path.exists(cat_dir):
                for filename in os.listdir(cat_dir):
                    if filename.endswith(".md") and filename != "_index.md":
                        filepath = os.path.join(cat_dir, filename)
                        mtime = os.path.getmtime(filepath)
                        posts.append({"category": cat_key, "filename": filename, "filepath": filepath, "mtime": mtime})
        
        posts.sort(key=lambda x: x["mtime"], reverse=True)
        return posts
        
    def refresh_posts(self):
        self.posts_list = self.get_all_posts()
        self.posts_listbox.delete(0, tk.END)
        
        filter_val = self.filter_category.get()
        
        for post in self.posts_list:
            cat_info = CATEGORIES[post["category"]]
            if filter_val == "All" or filter_val == cat_info['name']:
                display = f"{cat_info['icon']} {post['filename']}"
                self.posts_listbox.insert(tk.END, display)
        
        self.log(f"Loaded {len(self.posts_list)} posts")
        
    def start_server(self):
        if self.server_running:
            self.log("Server already running")
            return
            
        self.log("Starting server...")
        
        def run_server():
            try:
                self.server_process = subprocess.Popen(
                    f"hugo server -D --port {HUGO_PORT}",
                    cwd=PROJECT_DIR, shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
                )
                self.server_running = True
                self.root.after(0, lambda: self.update_server_status(True))
                self.root.after(0, lambda: self.log(f"Server running at http://localhost:{HUGO_PORT}"))
            except Exception as e:
                self.root.after(0, lambda: self.log(f"Error: {e}"))
        
        threading.Thread(target=run_server, daemon=True).start()
        
    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
            self.server_running = False
            self.update_server_status(False)
            self.log("Server stopped")
        else:
            self.log("No server running")
            
    def open_browser(self):
        webbrowser.open(f"http://localhost:{HUGO_PORT}")
        self.log("Opening browser")
        
    def build_site(self):
        self.log("Building site...")
        returncode, stdout, stderr = self.run_command("hugo --minify")
        if returncode == 0:
            self.log("Build complete")
        else:
            self.log(f"Build failed: {stderr}")
        
    def create_post(self, category):
        filename = self.filename_entry.get().strip()
        
        if not filename:
            messagebox.showwarning("Notice", "Please enter a filename!")
            return
            
        filename = filename.lower().replace(" ", "-")
        if filename.endswith(".md"):
            filename = filename[:-3]
            
        cat_info = CATEGORIES[category]
        self.log(f"Creating {cat_info['icon']} {filename}.md")
        
        command = f"hugo new {category}/{filename}.md"
        returncode, stdout, stderr = self.run_command(command)
        
        if returncode == 0:
            filepath = os.path.join(PROJECT_DIR, "content", category, f"{filename}.md")
            self.log(f"Created successfully")
            self.refresh_posts()
            
            try:
                subprocess.run(f'code "{filepath}"', shell=True)
            except:
                try:
                    os.startfile(filepath)
                except:
                    pass
            
            self.filename_entry.delete(0, tk.END)
        else:
            self.log(f"Error: {stderr}")
            
    def delete_post(self):
        selection = self.posts_listbox.curselection()
        
        if not selection:
            messagebox.showwarning("Notice", "Please select a post!")
            return
        
        filter_val = self.filter_category.get()
        visible_posts = []
        for post in self.posts_list:
            cat_info = CATEGORIES[post["category"]]
            if filter_val == "All" or filter_val == cat_info['name']:
                visible_posts.append(post)
        
        if selection[0] >= len(visible_posts):
            return
            
        post = visible_posts[selection[0]]
        
        if messagebox.askyesno("Confirm", f"Delete {post['filename']}?"):
            try:
                os.remove(post["filepath"])
                self.log(f"Deleted {post['filename']}")
                self.refresh_posts()
            except Exception as e:
                self.log(f"Error: {e}")
            
    def git_status(self):
        returncode, stdout, stderr = self.run_command("git status -s")
        if returncode == 0:
            self.log(stdout.strip() if stdout.strip() else "Working tree clean")
        else:
            self.log(f"Error: {stderr}")
            
    def git_add(self):
        returncode, stdout, stderr = self.run_command("git add .")
        self.log("Files staged" if returncode == 0 else f"Error: {stderr}")
            
    def git_commit(self):
        message = self.commit_msg_entry.get().strip() or f"Update {datetime.now().strftime('%m/%d')}"
        returncode, stdout, stderr = self.run_command(f'git commit -m "{message}"')
        if returncode == 0:
            self.log(f"Committed: {message}")
            self.commit_msg_entry.delete(0, tk.END)
        else:
            self.log(f"Error: {stderr}")
            
    def git_push(self):
        self.log("Pushing to GitHub...")
        returncode, stdout, stderr = self.run_command("git push")
        if returncode == 0:
            self.log("Push complete")
            messagebox.showinfo("Success", "Changes pushed to GitHub!")
        else:
            self.log(f"Error: {stderr}")
            
    def quick_commit(self):
        message = self.commit_msg_entry.get().strip()
        if not message:
            messagebox.showwarning("Notice", "Please enter a commit message!")
            return
            
        self.git_add()
        returncode, stdout, stderr = self.run_command(f'git commit -m "{message}"')
        if returncode == 0 or "nothing to commit" in stdout:
            self.log(f"Committed: {message}")
            self.commit_msg_entry.delete(0, tk.END)
            self.git_push()
        else:
            self.log(f"Error: {stderr}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HugoBlogManager(root)
    root.mainloop()
