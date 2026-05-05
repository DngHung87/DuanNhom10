import tkinter as tk
from tkinter import messagebox
from common.theme import *
from common.widgets import GlowButton, StyledEntry
from query.quanLyTK import QuanLyTK


class TaoTKPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.quan_ly_tk = QuanLyTK("database/tk.csv", ["username", "password", "hoten", "sdt", "chucvu"])
        self.config()
        self.view()

    def config(self):
        self.master.title("➕ Tạo tài khoản mới")
        self.master.geometry("460x600")
        self.master.configure(bg=BG_DARK)
        self.master.resizable(False, False)

    def view(self):
        # Top accent bar
        tk.Frame(self.master, bg=SUCCESS, height=4).pack(fill="x")

        outer = tk.Frame(self.master, bg=BG_DARK)
        outer.pack(expand=True, fill="both", padx=40, pady=20)

        # Header
        tk.Label(outer, text="➕", font=("Segoe UI", 36),
                 bg=BG_DARK, fg=SUCCESS).pack(pady=(10, 0))
        tk.Label(outer, text="TẠO TÀI KHOẢN MỚI", font=("Segoe UI", 16, "bold"),
                 bg=BG_DARK, fg=TEXT_PRIMARY).pack(pady=(4, 2))
        tk.Label(outer, text="Điền đầy đủ thông tin bên dưới",
                 font=FONT_SMALL, bg=BG_DARK, fg=TEXT_SECONDARY).pack(pady=(0, 18))

        # Card
        card = tk.Frame(outer, bg=BG_SURFACE, padx=28, pady=24)
        card.pack(fill="x")

        fields = [
            ("TÊN ĐĂNG NHẬP *", "entry_username", None),
            ("MẬT KHẨU *", "entry_password", "●"),
            ("HỌ VÀ TÊN", "entry_hoten", None),
            ("SỐ ĐIỆN THOẠI", "entry_sdt", None),
            ("CHỨC VỤ", "entry_chucvu", None),
        ]

        for label_text, attr, show in fields:
            tk.Label(card, text=label_text, font=("Segoe UI", 9, "bold"),
                     bg=BG_SURFACE, fg=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(0, 4))
            entry = StyledEntry(card, show=show, width=34)
            entry.pack(fill="x", pady=(0, 12))
            setattr(self, attr, entry)

        # Buttons
        btn_frame = tk.Frame(card, bg=BG_SURFACE)
        btn_frame.pack(fill="x", pady=(8, 0))

        GlowButton(btn_frame, text="TẠO TÀI KHOẢN", command=self.tao_tk,
                   style_type="success", width=20).pack(side="left", padx=(0, 8))
        GlowButton(btn_frame, text="QUAY LẠI", command=self.back_login,
                   style_type="secondary", width=14).pack(side="left")

    def back_login(self):
        self.app_manager.show_login_page()

    def tao_tk(self):
        username  = self.entry_username.get().strip()
        password  = self.entry_password.get().strip()
        hoten     = self.entry_hoten.get().strip()
        sdt       = self.entry_sdt.get().strip()
        chuc_vu   = self.entry_chucvu.get().strip()

        if not username or not password:
            messagebox.showwarning("⚠️ Thiếu thông tin", "Tên đăng nhập và mật khẩu là bắt buộc!")
            return

        self.quan_ly_tk.create([username, password, hoten, sdt, chuc_vu])
        messagebox.showinfo("✅ Thành công", f"Đã tạo tài khoản '{username}' thành công!")
        self.app_manager.show_login_page()
