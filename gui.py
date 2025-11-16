import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import pygame
from main import text_to_morse, morse_to_text, morse_to_wave_bytes

pygame.mixer.init()

# -------------------- FUTURISTIC DARK THEME --------------------
BG = "#0b0f14"           # main background
PANEL = "#111821"        # card background
ACCENT = "#38bdf8"       # neon cyan
TEXT = "#e2e8f0"         # light text
SUBTEXT = "#7b8794"      # muted grey
HIGHLIGHT = "#1a2330"    # hover panels

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_NORMAL = ("Segoe UI", 11)
FONT_BUTTON = ("Segoe UI", 10, "bold")
FONT_BOX = ("Consolas", 12)

# Custom styled frame with rounded corners
class RoundFrame(tk.Canvas):
    def __init__(self, parent, bg_color=PANEL, radius=20, **kwargs):
        super().__init__(parent, highlightthickness=0, bg=BG)
        self.radius = radius
        self.bg_color = bg_color
        self.config(**kwargs)

    def place_rounded(self, x, y, w, h):
        r = self.radius
        self.place(x=x, y=y, width=w, height=h)
        self.create_round_rect(0, 0, w, h, r, fill=self.bg_color, outline=self.bg_color)

    def create_round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1+r,
            x2, y2-r,
            x2-r, y2,
            x1+r, y2,
            x1, y2-r,
            x1, y1+r
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

# -------------------- APP --------------------
class MorseApp:
    def __init__(self, root):
        self.root = root
        root.title("Morse Code Converter")
        root.geometry("900x600")
        root.configure(bg=BG)
        root.resizable(False, False)

        # ---------------- HEADER ----------------
        header = RoundFrame(root, radius=25, bg_color=PANEL)
        header.place_rounded(20, 20, 860, 80)

        tk.Label(root, text="MORSE CODE LAB",
                 fg=ACCENT, bg=PANEL, font=FONT_TITLE).place(x=50, y=45)

        # ---------------- MAIN PANEL ----------------
        main = RoundFrame(root, radius=20, bg_color=PANEL)
        main.place_rounded(20, 120, 860, 400)

        # Input box
        tk.Label(root, text="Input", fg=TEXT, bg=PANEL, font=FONT_NORMAL).place(x=50, y=140)

        self.input_box = tk.Text(root, height=10, bg=HIGHLIGHT,
                                 fg=TEXT, insertbackground=TEXT,
                                 bd=0, relief="flat", font=FONT_BOX)
        self.input_box.place(x=50, y=170, width=380, height=200)

        # Output box
        tk.Label(root, text="Output", fg=TEXT, bg=PANEL, font=FONT_NORMAL).place(x=470, y=140)

        self.output_box = tk.Text(root, height=10, bg=HIGHLIGHT,
                                  fg=TEXT, bd=0, relief="flat",
                                  insertbackground=TEXT, font=FONT_BOX)
        self.output_box.place(x=470, y=170, width=380, height=200)

        # ---------------- BUTTON PANEL ----------------
        btn_panel = RoundFrame(root, radius=20, bg_color=PANEL)
        btn_panel.place_rounded(50, 380, 800, 120)

        self._make_btn("→ Encode →", self.encode, 60, 400)
        self._make_btn("← Decode ←", self.decode, 240, 400)
        self._make_btn("Play Audio", self.play_audio, 420, 400)
        self._make_btn("Clear", self._clear_boxes, 600, 400)

        # ---------------- SETTINGS ----------------
        tk.Label(root, text="WPM:", fg=TEXT, bg=PANEL, font=FONT_NORMAL).place(x=60, y=450)
        self.wpm_var = tk.IntVar(value=18)
        self._make_spin(self.wpm_var, 110, 445, 60)

        tk.Label(root, text="Freq (Hz):", fg=TEXT, bg=PANEL, font=FONT_NORMAL).place(x=200, y=450)
        self.freq_var = tk.IntVar(value=700)
        self._make_spin(self.freq_var, 280, 445, 80)

        # Status bar
        self.status = tk.Label(root, text="Ready", fg=SUBTEXT, bg=BG,
                               anchor="w", font=("Segoe UI", 10))
        self.status.place(x=20, y=560, width=860)

    # ---------------- BUTTON MAKER ----------------
    def _make_btn(self, text, cmd, x, y):
        btn = tk.Button(self.root, text=text, command=cmd,
                        fg=ACCENT, bg=HIGHLIGHT,
                        activebackground=ACCENT, activeforeground="black",
                        relief="flat", bd=0, font=FONT_BUTTON)
        btn.place(x=x, y=y, width=150, height=40)

        # Hover glow effect
        btn.bind("<Enter>", lambda e: btn.config(bg="#16202c"))
        btn.bind("<Leave>", lambda e: btn.config(bg=HIGHLIGHT))

    def _make_spin(self, var, x, y, w):
        spin = tk.Spinbox(self.root, from_=1, to=50, textvariable=var,
                          fg=TEXT, bg=HIGHLIGHT, insertbackground=TEXT,
                          bd=0, relief="flat", font=FONT_NORMAL, width=5)
        spin.place(x=x, y=y, width=w, height=35)

    # ---------------- LOGIC ----------------
    def encode(self):
        text = self.input_box.get('1.0', 'end').strip()
        if not text:
            self._alert("Input is empty.")
            return
        morse = text_to_morse(text)
        self._set_output(morse)
        self.status.config(text="Encoded to Morse")

    def decode(self):
        morse = self.input_box.get('1.0', 'end').strip()
        if not morse:
            self._alert("Input is empty.")
            return
        text = morse_to_text(morse)
        self._set_output(text)
        self.status.config(text="Decoded to Text")

    def play_audio(self):
        morse = self.output_box.get('1.0', 'end').strip()
        if not morse:
            self._alert("Nothing to play. Encode first!")
            return

        wpm = self.wpm_var.get()
        freq = self.freq_var.get()

        self.status.config(text="Generating audio...")

        wav_bytes = morse_to_wave_bytes(morse, wpm=wpm, freq=freq)

        with open("temp_morse.wav", "wb") as f:
            f.write(wav_bytes)

        self.status.config(text="Playing audio...")

        def play_thread():
            pygame.mixer.music.load("temp_morse.wav")
            pygame.mixer.music.play()

        threading.Thread(target=play_thread, daemon=True).start()

        self.status.config(text="Done")

    # ---------------- UTIL ----------------
    def _set_output(self, text):
        self.output_box.delete('1.0', 'end')
        self.output_box.insert('1.0', text)

    def _clear_boxes(self):
        self.input_box.delete('1.0', 'end')
        self.output_box.delete('1.0', 'end')
        self.status.config(text="Cleared")

    def _alert(self, msg):
        messagebox.showinfo("Info", msg)

# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    MorseApp(root)
    root.mainloop()
