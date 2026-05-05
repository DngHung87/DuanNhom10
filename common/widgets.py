import tkinter as tk
from common.theme import *


class GlowButton(tk.Button):
    """Nút bấm hiện đại với hiệu ứng hover glow"""

    STYLES = {
        "primary":   {"bg": ACCENT,    "fg": BG_DARK,  "hover": "#33ddff"},
        "success":   {"bg": SUCCESS,   "fg": "#fff",   "hover": "#34d399"},
        "danger":    {"bg": DANGER,    "fg": "#fff",   "hover": "#f87171"},
        "warning":   {"bg": WARNING,   "fg": BG_DARK,  "hover": "#fbbf24"},
        "info":      {"bg": INFO,      "fg": "#fff",   "hover": "#60a5fa"},
        "secondary": {"bg": BG_SURFACE,"fg": TEXT_SECONDARY, "hover": "#2d3748"},
        "ghost":     {"bg": BG_DARK,   "fg": ACCENT,   "hover": "#0d1526"},
    }

    def __init__(self, parent, text="", command=None, style_type="primary", width=None, **kwargs):
        s = self.STYLES.get(style_type, self.STYLES["primary"])
        w = width if width else max(len(text) + 4, 12)
        super().__init__(
            parent, text=text, command=command,
            bg=s["bg"], fg=s["fg"],
            font=FONT_BTN,
            relief="flat", bd=0,
            cursor="hand2",
            width=w,
            padx=12, pady=6,
            **kwargs
        )
        self._bg = s["bg"]
        self._hover = s["hover"]
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, e):
        self.config(bg=self._hover)

    def _on_leave(self, e):
        self.config(bg=self._bg)


class StyledEntry(tk.Frame):
    """Input field với viền glow"""

    def __init__(self, parent, placeholder="", show=None, **kwargs):
        super().__init__(parent, bg=BG_SURFACE, padx=2, pady=2)
        self.placeholder = placeholder
        self._has_placeholder = True

        self.entry = tk.Entry(
            self, bg=BG_INPUT, fg=TEXT_SECONDARY if placeholder else TEXT_PRIMARY,
            insertbackground=ACCENT,
            relief="flat", bd=0,
            font=FONT_BODY,
            **kwargs
        )
        if show:
            self.entry.config(show=show)
        self.entry.pack(padx=8, pady=6, fill="x")

        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.bind("<FocusIn>", self._clear_placeholder)
            self.entry.bind("<FocusOut>", self._restore_placeholder)

        self.entry.bind("<FocusIn>", self._glow_on, add="+")
        self.entry.bind("<FocusOut>", self._glow_off, add="+")

    def _clear_placeholder(self, e):
        if self._has_placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=TEXT_PRIMARY)
            self._has_placeholder = False

    def _restore_placeholder(self, e):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=TEXT_SECONDARY)
            self._has_placeholder = True

    def _glow_on(self, e):
        self.config(bg=ACCENT)

    def _glow_off(self, e):
        self.config(bg=BG_SURFACE)

    def get(self):
        if self._has_placeholder:
            return ""
        return self.entry.get()

    def set(self, value):
        self._has_placeholder = False
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
        self.entry.config(fg=TEXT_PRIMARY)

    def clear(self):
        self._has_placeholder = False
        self.entry.delete(0, tk.END)

    def config_show(self, show):
        self.entry.config(show=show)


class SectionCard(tk.Frame):
    """Card với border đẹp"""

    def __init__(self, parent, title="", **kwargs):
        super().__init__(parent, bg=BG_CARD, relief="flat", bd=0, **kwargs)

        if title:
            header = tk.Frame(self, bg=ACCENT2, height=2)
            header.pack(fill="x")

            title_lbl = tk.Label(self, text=title, bg=BG_CARD, fg=ACCENT,
                                 font=FONT_HEADER, anchor="w")
            title_lbl.pack(padx=16, pady=(10, 5), anchor="w")

            sep = tk.Frame(self, bg=BORDER, height=1)
            sep.pack(fill="x", padx=16)
