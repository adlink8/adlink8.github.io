#!/usr/bin/env python3
"""
Hugo Blog Manager - Anime Style UI
Features:
- Create/Delete posts with category selection
- Start/Stop Hugo server
- Commit and push to GitHub
- Cute animated cat mascot
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

# Anime style colors - soft pastels with vibrant accents
COLORS = {
    'bg_main': '#1a1a2e',           # Dark purple background
    'bg_card': '#25253d',           # Card background
    'bg_input': '#2d2d4a',          # Input background
    'accent_pink': '#ff6b9d',       # Pink accent
    'accent_cyan': '#00d9ff',       # Cyan accent
    'accent_purple': '#b366ff',     # Purple accent
    'accent_orange': '#ff9f43',     # Orange accent
    'accent_green': '#5fe3b5',      # Green accent
    'accent_blue': '#54a0ff',       # Blue accent
    'text_white': '#ffffff',
    'text_pink': '#ffb8d0',
    'text_gray': '#a0a0b8',
    'border': '#3d3d5c',
    'glow_pink': '#ff6b9d',
    'glow_cyan': '#00d9ff',
}

# Category configuration
CATEGORIES = {
    "daily": {"name": "Timeline", "icon": "📅", "color": "#ff6b9d", "gradient": ["#ff6b9d", "#ff8fab"]},
    "pitfalls": {"name": "Lab Notes", "icon": "🛠️", "color": "#ff9f43", "gradient": ["#ff9f43", "#ffbe76"]},
    "insights": {"name": "Insights", "icon": "💡", "color": "#b366ff", "gradient": ["#b366ff", "#c990ff"]},
    "reflections": {"name": "Reflection", "icon": "🔄", "color": "#54a0ff", "gradient": ["#54a0ff", "#74b9ff"]},
    "project-logs": {"name": "Project Log", "icon": "📁", "color": "#5fe3b5", "gradient": ["#5fe3b5", "#7df0ca"]},
}


class AnimatedCat(tk.Canvas):
    """Cute animated cat mascot - side view with sleep/awake states"""
    
    def __init__(self, parent, size=70):
        super().__init__(parent, width=size, height=size, 
                        highlightthickness=0, bg=parent.cget('bg'))
        
        self.size = size
        self.is_awake = False
        self.frame = 0
        self.blink_counter = 0
        self.is_blinking = False
        self.tail_angle = 0
        self.tail_direction = 1
        self.breath_offset = 0
        self.z_offset = 0
        
        self.draw_cat()
        self.animate()
        
    def set_awake(self, awake):
        self.is_awake = awake
        self.draw_cat()
        
    def draw_cat(self):
        self.delete("all")
        
        s = self.size
        cx = s // 2
        
        if self.is_awake:
            self._draw_awake_cat(cx, s)
        else:
            self._draw_sleeping_cat(cx, s)
            
    def _draw_sleeping_cat(self, cx, s):
        """Draw cat sleeping curled up (side view) - cute version"""
        cy = s // 2 + 8
        
        # Tail wrapped around body
        self.create_arc(cx + 8, cy + 5, cx + 30, cy + 25, 
                       start=280, extent=180, style=tk.ARC,
                       outline='#ffccd5', width=4)
        
        # Body (curled up ball)
        body_y = cy + 3 + self.breath_offset * 0.3
        self.create_oval(cx - 8, body_y - 8, cx + 22, body_y + 15, 
                        fill='#fff5f8', outline='#ffccd5', width=1)
        
        # Head resting
        head_y = cy - 2 + self.breath_offset * 0.3
        self.create_oval(cx - 15, head_y - 10, cx + 8, head_y + 10, 
                        fill='#fff5f8', outline='#ffccd5', width=1)
        
        # Ear (side view, one visible)
        self.create_polygon(
            cx - 12, head_y - 6,
            cx - 16, head_y - 20,
            cx - 4, head_y - 8,
            fill='#ffccd5', outline='#ff99aa', width=1, smooth=True
        )
        # Inner ear
        self.create_polygon(
            cx - 11, head_y - 8,
            cx - 14, head_y - 16,
            cx - 6, head_y - 10,
            fill='#ff99aa', outline='', smooth=True
        )
        
        # Closed eyes (happy sleeping)
        self.create_arc(cx - 10, head_y - 3, cx - 2, head_y + 2, 
                       start=0, extent=180, style=tk.ARC,
                       outline='#666', width=1.5)
        
        # Nose
        self.create_oval(cx - 13, head_y + 3, cx - 9, head_y + 6, 
                        fill='#ff99aa', outline='')
        
        # Tiny smile
        self.create_arc(cx - 15, head_y + 5, cx - 9, head_y + 9, 
                       start=200, extent=140, style=tk.ARC,
                       outline='#ff99aa', width=1)
        
        # Blush
        self.create_oval(cx - 4, head_y + 4, cx, head_y + 7, 
                        fill='#ffccd5', outline='')
        
        # Floating Zs
        z_y = head_y - 22 - self.z_offset
        self.create_text(cx + 5, z_y, text="z", fill='#b366ff', 
                        font=("Arial", 7, "italic"))
        self.create_text(cx + 12, z_y - 6, text="Z", fill='#b366ff', 
                        font=("Arial", 9, "italic"))
        self.create_text(cx + 20, z_y - 14, text="Z", fill='#b366ff', 
                        font=("Arial", 11, "bold"))
        
    def _draw_awake_cat(self, cx, s):
        """Draw cat sitting up and alert (side view) - cute version"""
        cy = s // 2 - 2
        
        # Tail wagging
        tail_x = cx + 25 + self.tail_angle
        tail_y = cy + 22
        self.create_line(cx + 15, cy + 18, tail_x - 3, tail_y, 
                        fill='#ffccd5', width=4, smooth=True)
        self.create_oval(tail_x - 4, tail_y - 3, tail_x + 4, tail_y + 5, 
                        fill='#fff5f8', outline='#ffccd5', width=1)
        
        # Back leg
        self.create_oval(cx + 5, cy + 15, cx + 20, cy + 28, 
                        fill='#fff5f8', outline='#ffccd5', width=1)
        
        # Body
        self.create_oval(cx - 8, cy + 5, cx + 18, cy + 22, 
                        fill='#fff5f8', outline='#ffccd5', width=1)
        
        # Front paws
        self.create_oval(cx - 10, cy + 18, cx - 2, cy + 26, 
                        fill='#fff5f8', outline='#ffccd5', width=1)
        self.create_oval(cx + 2, cy + 18, cx + 10, cy + 26, 
                        fill='#fff5f8', outline='#ffccd5', width=1)
        
        # Head
        self.create_oval(cx - 16, cy - 12, cx + 8, cy + 6, 
                        fill='#fff5f8', outline='#ffccd5', width=1)
        
        # Ears
        self.create_polygon(
            cx - 12, cy - 6,
            cx - 16, cy - 22,
            cx - 3, cy - 10,
            fill='#ffccd5', outline='#ff99aa', width=1, smooth=True
        )
        self.create_polygon(
            cx - 2, cy - 8,
            cx + 2, cy - 20,
            cx + 10, cy - 6,
            fill='#ffccd5', outline='#ff99aa', width=1, smooth=True
        )
        # Inner ears
        self.create_polygon(
            cx - 10, cy - 8, cx - 13, cy - 18, cx - 5, cy - 11,
            fill='#ff99aa', outline='', smooth=True
        )
        self.create_polygon(
            cx, cy - 9, cx + 2, cy - 17, cx + 7, cy - 8,
            fill='#ff99aa', outline='', smooth=True
        )
        
        # Eyes
        if self.is_blinking:
            self.create_arc(cx - 11, cy - 4, cx - 3, cy + 1, 
                           start=0, extent=180, style=tk.ARC,
                           outline='#555', width=1.5)
        else:
            # Big cute eyes
            self.create_oval(cx - 12, cy - 5, cx - 3, cy + 3, 
                           fill='#4a4a6a', outline='')
            # Eye highlight
            self.create_oval(cx - 10, cy - 4, cx - 6, cy, 
                           fill='white', outline='')
            self.create_oval(cx - 8, cy - 2, cx - 6, cy, 
                           fill='#fff', outline='')
        
        # Nose
        self.create_oval(cx - 14, cy + 4, cx - 10, cy + 7, 
                        fill='#ff99aa', outline='')
        
        # Cute mouth
        self.create_arc(cx - 17, cy + 6, cx - 11, cy + 11, 
                       start=200, extent=140, style=tk.ARC,
                       outline='#ff99aa', width=1)
        self.create_arc(cx - 11, cy + 6, cx - 5, cy + 11, 
                       start=200, extent=140, style=tk.ARC,
                       outline='#ff99aa', width=1)
        
        # Blush
        self.create_oval(cx - 5, cy + 6, cx, cy + 9, 
                        fill='#ffccd5', outline='')
        
        # Whiskers
        self.create_line(cx - 20, cy + 2, cx - 12, cy + 4, 
                        fill='#ffccd5', width=1)
        self.create_line(cx - 20, cy + 5, cx - 12, cy + 6, 
                        fill='#ffccd5', width=1)
        
    def animate(self):
        self.frame += 1
        
        if self.is_awake:
            # Tail wagging
            self.tail_angle += 0.6 * self.tail_direction
            if self.tail_angle > 5 or self.tail_angle < -5:
                self.tail_direction *= -1
            
            # Blinking
            self.blink_counter += 1
            if self.blink_counter >= 60:
                self.is_blinking = True
                if self.blink_counter >= 66:
                    self.is_blinking = False
                    self.blink_counter = 0
        else:
            # Breathing
            self.breath_offset = 2 * (1 + (self.frame % 60) / 30 - 1)
            
            # Floating Zs
            self.z_offset = (self.frame % 50) * 0.25
        
        self.draw_cat()
        self.after(50, self.animate)


class CuteButton(tk.Canvas):
    """Kawaii style button with rounded corners and glow"""
    
    def __init__(self, parent, text, command=None, color="#ff6b9d", width=140, height=40, icon=""):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, bg=parent.cget('bg'))
        
        self.command = command
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.icon = icon
        self.hover = False
        
        self.draw_button()
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        
    def draw_button(self):
        self.delete("all")
        
        # Glow effect
        if self.hover:
            for i in range(3):
                self.create_rounded_rect(2+i, 2+i, self.width-2-i, self.height-2-i, 
                                        radius=12, fill="", outline=self.color, width=1)
        
        # Main button background
        fill_color = self._lighten_color(self.color, 0.2) if self.hover else self.color
        self.create_rounded_rect(2, 2, self.width-2, self.height-2, 
                                radius=12, fill=fill_color, outline="")
        
        # Highlight on top
        self.create_rounded_rect(4, 4, self.width-4, self.height//2, 
                                radius=10, fill=self._lighten_color(self.color, 0.3), outline="")
        
        # Button text
        display_text = f"{self.icon} {self.text}" if self.icon else self.text
        self.create_text(self.width//2, self.height//2 + 1, text=display_text, 
                        fill="white", font=("Segoe UI", 10, "bold"))
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        points = [
            x1+radius, y1, x2-radius, y1, 
            x2, y1, x2, y1+radius,
            x2, y2-radius, x2, y2, x2-radius, y2,
            x1+radius, y2, x1, y2, x1, y2-radius,
            x1, y1+radius, x1, y1, x1+radius, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _lighten_color(self, color, factor):
        color = color.lstrip('#')
        r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _on_enter(self, event):
        self.hover = True
        self.draw_button()
        self.config(cursor="hand2")
        
    def _on_leave(self, event):
        self.hover = False
        self.draw_button()
        
    def _on_click(self, event):
        if self.command:
            self.command()


class AnimePanel(tk.Frame):
    """Anime style panel with decorative elements"""
    
    def __init__(self, parent, title, accent_color="#ff6b9d"):
        super().__init__(parent, bg=COLORS['bg_card'])
        
        self.accent_color = accent_color
        
        # Top decoration bar
        top_bar = tk.Frame(self, bg=accent_color, height=3)
        top_bar.pack(fill=tk.X)
        
        # Header
        header = tk.Frame(self, bg=COLORS['bg_card'])
        header.pack(fill=tk.X, padx=15, pady=(12, 8))
        
        # Decorative icon
        icon_canvas = tk.Canvas(header, width=24, height=24, bg=COLORS['bg_card'], highlightthickness=0)
        icon_canvas.pack(side=tk.LEFT)
        icon_canvas.create_oval(2, 2, 22, 22, fill=accent_color, outline="")
        icon_canvas.create_text(12, 12, text="◆", fill="white", font=("Segoe UI", 8))
        
        # Title with accent
        tk.Label(header, text=title, bg=COLORS['bg_card'],
                fg=COLORS['text_white'], font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=(8, 0))
        
        # Content area
        self.content = tk.Frame(self, bg=COLORS['bg_card'])
        self.content.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))


class HugoBlogManager:
    def __init__(self, root):
        self.root = root
        self.root.title("✧ Hugo Blog Manager ✧")
        self.root.geometry("1150x600")
        self.root.configure(bg=COLORS['bg_main'])
        self.root.resizable(True, True)
        
        self.server_process = None
        self.server_running = False
        self.posts_list = []
        
        self.setup_ui()
        self.refresh_posts()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['bg_main'], padx=16, pady=16)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid
        for i in range(4):
            main_frame.columnconfigure(i, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header with kawaii style
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
        
        # Kawaii sparkles
        tk.Label(left_frame, text="✧･ﾟ: *✧･ﾟ:*  ", bg=COLORS['bg_main'],
                fg=COLORS['accent_pink'], font=("Segoe UI", 10)).pack(side=tk.LEFT)
        
        # Main title
        title_frame = tk.Frame(left_frame, bg=COLORS['bg_main'])
        title_frame.pack(side=tk.LEFT)
        
        tk.Label(title_frame, text="Hugo", bg=COLORS['bg_main'],
                fg=COLORS['accent_cyan'], font=("Segoe UI", 18, "bold")).pack(side=tk.LEFT)
        
        tk.Label(title_frame, text=" Blog Manager", bg=COLORS['bg_main'],
                fg=COLORS['accent_pink'], font=("Segoe UI", 18, "bold")).pack(side=tk.LEFT)
        
        # Subtitle
        tk.Label(left_frame, text="  ✿", bg=COLORS['bg_main'],
                fg=COLORS['accent_purple'], font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Right side - Cat and Status
        right_frame = tk.Frame(header, bg=COLORS['bg_main'])
        right_frame.pack(side=tk.RIGHT)
        
        # Animated cat mascot
        self.cat = AnimatedCat(right_frame, size=55)
        self.cat.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Status
        status_frame = tk.Frame(right_frame, bg=COLORS['bg_card'], padx=15, pady=6)
        status_frame.pack(side=tk.RIGHT)
        
        self.status_indicator = tk.Canvas(status_frame, width=12, height=12, 
                                          bg=COLORS['bg_card'], highlightthickness=0)
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 8))
        self.status_indicator.create_oval(0, 0, 12, 12, fill=COLORS['text_gray'], outline="")
        
        self.status_label = tk.Label(status_frame, text="● Offline", bg=COLORS['bg_card'],
                                    fg=COLORS['text_gray'], font=("Segoe UI", 10, "bold"))
        self.status_label.pack(side=tk.LEFT)
        
    def create_server_panel(self, parent, col):
        panel = AnimePanel(parent, "Server Control", COLORS['accent_cyan'])
        panel.grid(row=1, column=col, sticky="nsew", padx=(0, 8))
        
        # Status display box
        status_box = tk.Frame(panel.content, bg=COLORS['bg_input'], padx=10, pady=10)
        status_box.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(status_box, text="Status", bg=COLORS['bg_input'],
                fg=COLORS['text_gray'], font=("Segoe UI", 8)).pack(anchor=tk.W)
        
        self.server_status_text = tk.Label(status_box, text="~ Sleeping ~", bg=COLORS['bg_input'],
                                           fg=COLORS['text_pink'], font=("Segoe UI", 10))
        self.server_status_text.pack(anchor=tk.W)
        
        # Control buttons
        CuteButton(panel.content, "Start", command=self.start_server,
                  color=COLORS['accent_green'], icon="▶").pack(fill=tk.X, pady=(0, 6))
        
        CuteButton(panel.content, "Stop", command=self.stop_server,
                  color=COLORS['accent_pink'], icon="■").pack(fill=tk.X, pady=(0, 6))
        
        CuteButton(panel.content, "Browser", command=self.open_browser,
                  color=COLORS['accent_cyan'], icon="◎").pack(fill=tk.X, pady=(0, 12))
        
        # Separator
        sep_frame = tk.Frame(panel.content, height=2, bg=COLORS['border'])
        sep_frame.pack(fill=tk.X, pady=8)
        
        # Quick actions
        tk.Label(panel.content, text="Quick Actions ✿", bg=COLORS['bg_card'],
                fg=COLORS['text_gray'], font=("Segoe UI", 9)).pack(anchor=tk.W, pady=(0, 6))
        
        CuteButton(panel.content, "Open Folder", command=lambda: os.startfile(PROJECT_DIR),
                  color=COLORS['accent_purple'], icon="📁").pack(fill=tk.X, pady=(0, 6))
        
        CuteButton(panel.content, "Build Site", command=self.build_site,
                  color=COLORS['accent_orange'], icon="⚙").pack(fill=tk.X)
        
    def create_post_panel(self, parent, col):
        panel = AnimePanel(parent, "Create Post", COLORS['accent_pink'])
        panel.grid(row=1, column=col, sticky="nsew", padx=4)
        
        # Filename input
        tk.Label(panel.content, text="Filename ✎", bg=COLORS['bg_card'],
                fg=COLORS['text_gray'], font=("Segoe UI", 9)).pack(anchor=tk.W)
        
        input_frame = tk.Frame(panel.content, bg=COLORS['bg_input'], padx=10, pady=8)
        input_frame.pack(fill=tk.X, pady=(4, 12))
        
        self.filename_entry = tk.Entry(input_frame, bg=COLORS['bg_input'], fg=COLORS['text_white'],
                                       insertbackground=COLORS['accent_pink'], font=("Segoe UI", 10),
                                       relief=tk.FLAT, borderwidth=0)
        self.filename_entry.pack(fill=tk.X)
        
        # Category selection
        tk.Label(panel.content, text="Category ✿", bg=COLORS['bg_card'],
                fg=COLORS['text_gray'], font=("Segoe UI", 9)).pack(anchor=tk.W, pady=(0, 6))
        
        for cat_key, cat_info in CATEGORIES.items():
            CuteButton(panel.content, f"{cat_info['icon']} {cat_info['name']}", 
                      command=lambda k=cat_key: self.create_post(k),
                      color=cat_info['color'], width=150).pack(fill=tk.X, pady=2)
        
    def create_manage_panel(self, parent, col):
        panel = AnimePanel(parent, "Manage Posts", COLORS['accent_purple'])
        panel.grid(row=1, column=col, sticky="nsew", padx=4)
        
        # Filter row
        filter_frame = tk.Frame(panel.content, bg=COLORS['bg_card'])
        filter_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(filter_frame, text="Filter", bg=COLORS['bg_card'],
                fg=COLORS['text_gray'], font=("Segoe UI", 9)).pack(side=tk.LEFT)
        
        self.filter_category = ttk.Combobox(filter_frame, values=["All"] + [c['name'] for c in CATEGORIES.values()],
                                            width=12, state="readonly", font=("Segoe UI", 8))
        self.filter_category.set("All")
        self.filter_category.pack(side=tk.LEFT, padx=(8, 4))
        self.filter_category.bind("<<ComboboxSelected>>", lambda e: self.refresh_posts())
        
        # Refresh button
        refresh_canvas = tk.Canvas(filter_frame, width=28, height=28, bg=COLORS['bg_card'], highlightthickness=0)
        refresh_canvas.pack(side=tk.LEFT)
        refresh_canvas.create_text(14, 14, text="🔄", font=("Segoe UI", 10))
        refresh_canvas.bind("<Button-1>", lambda e: self.refresh_posts())
        
        # Posts list
        list_frame = tk.Frame(panel.content, bg=COLORS['bg_input'], padx=4, pady=4)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        
        self.posts_listbox = tk.Listbox(list_frame, bg=COLORS['bg_input'], fg=COLORS['text_white'],
                                        selectbackground=COLORS['accent_pink'], selectforeground='white',
                                        font=("Segoe UI", 9), relief=tk.FLAT, borderwidth=0,
                                        highlightthickness=0)
        self.posts_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Delete button
        CuteButton(panel.content, "Delete Selected", command=self.delete_post,
                  color=COLORS['accent_pink'], icon="✕").pack(fill=tk.X)
        
    def create_git_panel(self, parent, col):
        panel = AnimePanel(parent, "Git Control", COLORS['accent_green'])
        panel.grid(row=1, column=col, sticky="nsew", padx=(8, 0))
        
        # Git buttons row 1
        btn_row = tk.Frame(panel.content, bg=COLORS['bg_card'])
        btn_row.pack(fill=tk.X, pady=(0, 6))
        
        CuteButton(btn_row, "Stat", command=self.git_status, 
                  color=COLORS['accent_cyan'], width=45).pack(side=tk.LEFT, padx=(0, 4))
        CuteButton(btn_row, "Add", command=self.git_add, 
                  color=COLORS['accent_green'], width=45).pack(side=tk.LEFT, padx=(0, 4))
        CuteButton(btn_row, "Commit", command=self.git_commit, 
                  color=COLORS['accent_orange'], width=55).pack(side=tk.LEFT)
        
        CuteButton(panel.content, "Push to GitHub", command=self.git_push,
                  color=COLORS['accent_blue'], icon="🚀").pack(fill=tk.X, pady=(0, 10))
        
        # Commit message
        tk.Label(panel.content, text="Commit Message ♪", bg=COLORS['bg_card'],
                fg=COLORS['text_gray'], font=("Segoe UI", 9)).pack(anchor=tk.W)
        
        input_frame = tk.Frame(panel.content, bg=COLORS['bg_input'], padx=10, pady=6)
        input_frame.pack(fill=tk.X, pady=(4, 6))
        
        self.commit_msg_entry = tk.Entry(input_frame, bg=COLORS['bg_input'], fg=COLORS['text_white'],
                                         insertbackground=COLORS['accent_green'], font=("Segoe UI", 9),
                                         relief=tk.FLAT, borderwidth=0)
        self.commit_msg_entry.pack(fill=tk.X)
        
        CuteButton(panel.content, "Quick Deploy", command=self.quick_commit,
                  color=COLORS['accent_purple'], icon="✧").pack(fill=tk.X, pady=(0, 10))
        
        # Log output
        tk.Label(panel.content, text="Log ✿", bg=COLORS['bg_card'],
                fg=COLORS['text_gray'], font=("Segoe UI", 9)).pack(anchor=tk.W)
        
        log_frame = tk.Frame(panel.content, bg=COLORS['bg_input'], padx=8, pady=8)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_output = tk.Text(log_frame, bg=COLORS['bg_input'], fg=COLORS['accent_green'],
                                  font=("Consolas", 8), relief=tk.FLAT, borderwidth=0,
                                  highlightthickness=0, wrap=tk.WORD)
        self.log_output.pack(fill=tk.BOTH, expand=True)
        
    def log(self, message, level="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_output.see(tk.END)
        
    def update_server_status(self, running):
        if running:
            self.status_indicator.delete("all")
            self.status_indicator.create_oval(0, 0, 12, 12, fill=COLORS['accent_green'], outline="")
            self.status_label.config(text="● Online!", fg=COLORS['accent_green'])
            self.server_status_text.config(text="~ Running ~", fg=COLORS['accent_green'])
            self.cat.set_awake(True)  # Wake up the cat
        else:
            self.status_indicator.delete("all")
            self.status_indicator.create_oval(0, 0, 12, 12, fill=COLORS['text_gray'], outline="")
            self.status_label.config(text="● Offline", fg=COLORS['text_gray'])
            self.server_status_text.config(text="~ Sleeping ~", fg=COLORS['text_pink'])
            self.cat.set_awake(False)  # Put cat to sleep
        
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
        
        self.log(f"Loaded {len(self.posts_list)} posts ✿")
        
    def start_server(self):
        if self.server_running:
            self.log("Already running~")
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
                self.root.after(0, lambda: self.log(f"Online at :{HUGO_PORT} ✧"))
            except Exception as e:
                self.root.after(0, lambda: self.log(f"Error: {e}"))
        
        threading.Thread(target=run_server, daemon=True).start()
        
    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
            self.server_running = False
            self.update_server_status(False)
            self.log("Server stopped ~")
        else:
            self.log("No server running")
            
    def open_browser(self):
        webbrowser.open(f"http://localhost:{HUGO_PORT}")
        self.log("Opening browser ✿")
        
    def build_site(self):
        self.log("Building site...")
        returncode, stdout, stderr = self.run_command("hugo --minify")
        if returncode == 0:
            self.log("Build complete ✧")
        else:
            self.log(f"Build failed: {stderr}")
        
    def create_post(self, category):
        filename = self.filename_entry.get().strip()
        
        if not filename:
            messagebox.showwarning("♪ Notice", "Please enter a filename!")
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
            self.log(f"Created successfully ✿")
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
            messagebox.showwarning("♪ Notice", "Please select a post!")
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
        
        if messagebox.askyesno("♪ Confirm", f"Delete {post['filename']}?"):
            try:
                os.remove(post["filepath"])
                self.log(f"Deleted {post['filename']} ✕")
                self.refresh_posts()
            except Exception as e:
                self.log(f"Error: {e}")
            
    def git_status(self):
        returncode, stdout, stderr = self.run_command("git status -s")
        if returncode == 0:
            self.log(stdout.strip() if stdout.strip() else "Working tree clean ✿")
        else:
            self.log(f"Error: {stderr}")
            
    def git_add(self):
        returncode, stdout, stderr = self.run_command("git add .")
        self.log("Files added ✧" if returncode == 0 else f"Error: {stderr}")
            
    def git_commit(self):
        message = self.commit_msg_entry.get().strip() or f"Update {datetime.now().strftime('%m/%d')}"
        returncode, stdout, stderr = self.run_command(f'git commit -m "{message}"')
        if returncode == 0:
            self.log(f"Committed: {message} ✿")
            self.commit_msg_entry.delete(0, tk.END)
        else:
            self.log(f"Error: {stderr}")
            
    def git_push(self):
        self.log("Pushing to GitHub...")
        returncode, stdout, stderr = self.run_command("git push")
        if returncode == 0:
            self.log("Push complete ✧")
            messagebox.showinfo("♪ Success", "Changes pushed to GitHub!")
        else:
            self.log(f"Error: {stderr}")
            
    def quick_commit(self):
        message = self.commit_msg_entry.get().strip()
        if not message:
            messagebox.showwarning("♪ Notice", "Please enter a commit message!")
            return
            
        self.git_add()
        returncode, stdout, stderr = self.run_command(f'git commit -m "{message}"')
        if returncode == 0 or "nothing to commit" in stdout:
            self.log(f"Committed: {message} ✧")
            self.commit_msg_entry.delete(0, tk.END)
            self.git_push()
        else:
            self.log(f"Error: {stderr}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HugoBlogManager(root)
    root.mainloop()
