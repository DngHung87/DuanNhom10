import tkinter as tk
from common.theme import BG_DARK
from page.login import LoginPage
from page.taotk import TaoTKPage
from page.quanlytk import QuanLyTKPage
from page.suatk import SuaTKPage


class AppManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        # Center window on screen
        self._center(420, 540)

        self.current_page = None
        self.show_login_page()

    def _center(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_page(self):
        self._clear()
        self._center(420, 540)
        self.current_page = LoginPage(self.root, self)

    def show_taotk_page(self):
        self._clear()
        self._center(460, 600)
        self.current_page = TaoTKPage(self.root, self)

    def show_quanlytk_page(self):
        self._clear()
        self._center(900, 560)
        self.current_page = QuanLyTKPage(self.root, self)

    def show_suatk_page(self, username=None, password=None, hoten=None, sdt=None, chucvu=None):
        self._clear()
        self._center(480, 600)
        self.current_page = SuaTKPage(self.root, self, username, password, hoten, sdt, chucvu)

    def run(self):
        self.root.mainloop()
