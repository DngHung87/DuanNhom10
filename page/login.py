import tkinter as tk
from tkinter import messagebox
from common.theme import *
from common.widgets import GlowButton, StyledEntry
from query.quanLyTK import QuanLyTK


class LoginPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.quan_ly_tk = QuanLyTK("database/tk.csv", ["username", "password", "hoten", "sdt", "chucvu"])
        self.config()
        self.view()

    def config(self):
        self.master.title("🔐 Hệ thống Đăng nhập")
        self.master.geometry("420x540")
        self.master.configure(bg=BG_DARK)
        self.master.resizable(False, False)

    def view(self):
        # ── Top decorative bar ──────────────────────────────────────────
        bar = tk.Frame(self.master, bg=ACCENT2, height=4)
        bar.pack(fill="x")

        # ── Main container ──────────────────────────────────────────────
        outer = tk.Frame(self.master, bg=BG_DARK)
        outer.pack(expand=True, fill="both", padx=40, pady=20)

        # Logo / icon area
        logo_frame = tk.Frame(outer, bg=BG_DARK)
        logo_frame.pack(pady=(10, 0))

        logo_circle = tk.Label(logo_frame, text="⬡", font=("Segoe UI", 48),
                                bg=BG_DARK, fg=ACCENT)
        logo_circle.pack()

        # Title
        tk.Label(outer, text="ĐĂNG NHẬP HỆ THỐNG", font=("Segoe UI", 16, "bold"),
                 bg=BG_DARK, fg=TEXT_PRIMARY).pack(pady=(0, 4))

        tk.Label(outer, text="Nhập thông tin tài khoản để tiếp tục",
                 font=FONT_SMALL, bg=BG_DARK, fg=TEXT_SECONDARY).pack(pady=(0, 24))

        # ── Card ────────────────────────────────────────────────────────
        card = tk.Frame(outer, bg=BG_SURFACE, padx=28, pady=28)
        card.pack(fill="x")

        # Username
        tk.Label(card, text="TÊN ĐĂNG NHẬP", font=("Segoe UI", 9, "bold"),
                 bg=BG_SURFACE, fg=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(0, 4))

        self.entry_username = StyledEntry(card, width=30)
        self.entry_username.set("admin")
        self.entry_username.pack(fill="x", pady=(0, 14))

        # Password
        tk.Label(card, text="MẬT KHẨU", font=("Segoe UI", 9, "bold"),
                 bg=BG_SURFACE, fg=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(0, 4))

        self.entry_password = StyledEntry(card, show="●", width=30)
        self.entry_password.set("admin")
        self.entry_password.pack(fill="x", pady=(0, 6))

        # Show password toggle
        self._show_pass = tk.BooleanVar()
        chk = tk.Checkbutton(card, text="Hiển thị mật khẩu",
                              variable=self._show_pass, command=self._toggle_pass,
                              bg=BG_SURFACE, fg=TEXT_SECONDARY,
                              selectcolor=BG_INPUT, activebackground=BG_SURFACE,
                              font=FONT_SMALL, cursor="hand2")
        chk.pack(anchor="e", pady=(0, 20))

        # Buttons
        btn_login = GlowButton(card, text="  ĐĂNG NHẬP  ", command=self.login,
                               style_type="primary", width=32)
        btn_login.pack(fill="x", pady=(0, 8))

        btn_reg = GlowButton(card, text="  TẠO TÀI KHOẢN MỚI  ", command=self.tao_tk,
                             style_type="ghost", width=32)
        btn_reg.pack(fill="x")

        # ── Footer ──────────────────────────────────────────────────────
        tk.Label(outer, text="© 2025 Hệ thống Quản lý Tài khoản",
                 font=FONT_SMALL, bg=BG_DARK, fg=BORDER).pack(pady=(16, 0))

    def _toggle_pass(self):
        show = "" if self._show_pass.get() else "●"
        self.entry_password.config_show(show)

    def tao_tk(self):
        self.app_manager.show_taotk_page()

    def login(self):
        u = self.entry_username.get().strip()
        p = self.entry_password.get().strip()
        if not u or not p:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        if self.quan_ly_tk.checkLogin(u, p):
            messagebox.showinfo("✅ Thành công", f"Chào mừng {u}!")
            self.app_manager.show_quanlytk_page()
        else:
            messagebox.showerror("❌ Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
