import tkinter as tk
from tkinter import messagebox
from common.theme import *
from common.widgets import GlowButton, StyledEntry
from query.quanLyTK import QuanLyTK


class SuaTKPage:
    def __init__(self, master, app_manager, username=None, password=None, hoten=None, sdt=None, chucvu=None):
        self.master = master
        self.app_manager = app_manager
        self.old = {
            "username": username or "",
            "password": password or "",
            "hoten":    hoten or "",
            "sdt":      sdt or "",
            "chucvu":   chucvu or "",
        }
        self.qualy_tk = QuanLyTK("database/tk.csv", ["username", "password", "hoten", "sdt", "chucvu"])
        self.config()
        self.view()

    def config(self):
        self.master.title("✏️ Sửa thông tin tài khoản")
        self.master.geometry("480x600")
        self.master.configure(bg=BG_DARK)
        self.master.resizable(False, False)

    def view(self):
        # Top accent bar
        tk.Frame(self.master, bg=WARNING, height=4).pack(fill="x")

        outer = tk.Frame(self.master, bg=BG_DARK)
        outer.pack(expand=True, fill="both", padx=36, pady=20)

        # Header
        tk.Label(outer, text="✏️", font=("Segoe UI", 36),
                 bg=BG_DARK, fg=WARNING).pack(pady=(10, 0))
        tk.Label(outer, text="SỬA THÔNG TIN TÀI KHOẢN",
                 font=("Segoe UI", 15, "bold"), bg=BG_DARK, fg=TEXT_PRIMARY).pack(pady=(4, 2))
        tk.Label(outer, text=f"Đang chỉnh sửa: {self.old['username']}",
                 font=FONT_SMALL, bg=BG_DARK, fg=ACCENT).pack(pady=(0, 16))

        # Current info card
        info_card = tk.Frame(outer, bg=BG_SURFACE, padx=16, pady=12)
        info_card.pack(fill="x", pady=(0, 14))

        tk.Label(info_card, text="THÔNG TIN HIỆN TẠI",
                 font=("Segoe UI", 9, "bold"), bg=BG_SURFACE, fg=ACCENT2).pack(anchor="w")
        tk.Frame(info_card, bg=ACCENT2, height=1).pack(fill="x", pady=(4, 8))

        info_pairs = [
            ("👤 Tên đăng nhập", self.old["username"]),
            ("🔒 Mật khẩu",      "●" * len(self.old["password"])),
            ("📛 Họ tên",        self.old["hoten"]),
        ]
        for k, v in info_pairs:
            row = tk.Frame(info_card, bg=BG_SURFACE)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=k, font=FONT_SMALL, bg=BG_SURFACE,
                     fg=TEXT_SECONDARY, width=16, anchor="w").pack(side="left")
            tk.Label(row, text=v, font=FONT_SMALL, bg=BG_SURFACE,
                     fg=TEXT_PRIMARY, anchor="w").pack(side="left")

        # New info card
        edit_card = tk.Frame(outer, bg=BG_SURFACE, padx=16, pady=16)
        edit_card.pack(fill="x")

        tk.Label(edit_card, text="THÔNG TIN MỚI",
                 font=("Segoe UI", 9, "bold"), bg=BG_SURFACE, fg=WARNING).pack(anchor="w")
        tk.Frame(edit_card, bg=WARNING, height=1).pack(fill="x", pady=(4, 10))

        fields = [
            ("TÊN ĐĂNG NHẬP MỚI",  "entry_username", None,  self.old["username"]),
            ("MẬT KHẨU MỚI",       "entry_password", "●",   self.old["password"]),
            ("HỌ VÀ TÊN MỚI",      "entry_hoten",    None,  self.old["hoten"]),
        ]
        for label, attr, show, default in fields:
            tk.Label(edit_card, text=label, font=("Segoe UI", 9, "bold"),
                     bg=BG_SURFACE, fg=TEXT_SECONDARY, anchor="w").pack(fill="x", pady=(0, 3))
            entry = StyledEntry(edit_card, show=show, width=36)
            entry.set(default)
            entry.pack(fill="x", pady=(0, 10))
            setattr(self, attr, entry)

        # Show password
        self._show_pass = tk.BooleanVar()
        tk.Checkbutton(edit_card, text="Hiển thị mật khẩu",
                       variable=self._show_pass, command=self._toggle_pass,
                       bg=BG_SURFACE, fg=TEXT_SECONDARY,
                       selectcolor=BG_INPUT, activebackground=BG_SURFACE,
                       font=FONT_SMALL, cursor="hand2").pack(anchor="e", pady=(0, 4))

        # Hint text
        tk.Label(edit_card,
                 text="• Tên đăng nhập và mật khẩu không được để trống",
                 font=FONT_SMALL, bg=BG_SURFACE, fg=BORDER, anchor="w").pack(fill="x")

        # Buttons
        btn_frame = tk.Frame(outer, bg=BG_DARK)
        btn_frame.pack(fill="x", pady=(16, 0))

        GlowButton(btn_frame, text="💾 LƯU THAY ĐỔI", command=self.save_changes,
                   style_type="success", width=18).pack(side="left", padx=(0, 8))
        GlowButton(btn_frame, text="🔄 KHÔI PHỤC", command=self.reset_form,
                   style_type="warning", width=14).pack(side="left", padx=(0, 8))
        GlowButton(btn_frame, text="❌ HỦY", command=self.cancel,
                   style_type="secondary", width=10).pack(side="left")

    def _toggle_pass(self):
        show = "" if self._show_pass.get() else "●"
        self.entry_password.config_show(show)

    def reset_form(self):
        self.entry_username.set(self.old["username"])
        self.entry_password.set(self.old["password"])
        self.entry_hoten.set(self.old["hoten"])

    def save_changes(self):
        new_u = self.entry_username.get().strip()
        new_p = self.entry_password.get().strip()
        new_h = self.entry_hoten.get().strip()

        if not new_u or not new_p:
            messagebox.showwarning("⚠️ Lỗi", "Tên đăng nhập và mật khẩu không được trống!")
            return

        if new_u == self.old["username"] and new_p == self.old["password"] and new_h == self.old["hoten"]:
            messagebox.showinfo("ℹ️ Thông báo", "Không có thay đổi nào!")
            return

        try:
            self.qualy_tk.update("username", self.old["username"],
                                 ["username", "password", "hoten"],
                                 [new_u, new_p, new_h])
            messagebox.showinfo("✅ Thành công", "Đã cập nhật tài khoản thành công!")
            self.app_manager.show_quanlytk_page()
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Không thể cập nhật: {e}")

    def cancel(self):
        cur_u = self.entry_username.get().strip()
        cur_p = self.entry_password.get().strip()
        cur_h = self.entry_hoten.get().strip()
        changed = (cur_u != self.old["username"] or cur_p != self.old["password"] or cur_h != self.old["hoten"])
        if changed:
            if messagebox.askyesno("⚠️ Xác nhận", "Hủy bỏ các thay đổi chưa lưu?"):
                self.app_manager.show_quanlytk_page()
        else:
            self.app_manager.show_quanlytk_page()
