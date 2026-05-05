import tkinter as tk
from tkinter import messagebox, ttk
import csv, os
from common.theme import *
from common.widgets import GlowButton


class QuanLyTKPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.config()
        self.view()
        self.load_accounts()

    def config(self):
        self.master.title("📋 Quản lý tài khoản")
        self.master.geometry("900x560")
        self.master.configure(bg=BG_DARK)

    def view(self):
        # ── Top accent bar ───────────────────────────────────────────────
        tk.Frame(self.master, bg=ACCENT2, height=4).pack(fill="x")

        # ── Header ──────────────────────────────────────────────────────
        header = tk.Frame(self.master, bg=BG_CARD, pady=14)
        header.pack(fill="x")

        tk.Label(header, text="  📋  QUẢN LÝ TÀI KHOẢN",
                 font=("Segoe UI", 16, "bold"),
                 bg=BG_CARD, fg=TEXT_PRIMARY).pack(side="left", padx=20)

        # Live count badge
        self.badge_var = tk.StringVar(value="0 tài khoản")
        tk.Label(header, textvariable=self.badge_var,
                 bg=ACCENT2, fg="#fff",
                 font=("Segoe UI", 10, "bold"),
                 padx=10, pady=2).pack(side="left", padx=8)

        # ── Toolbar ─────────────────────────────────────────────────────
        toolbar = tk.Frame(self.master, bg=BG_SURFACE, pady=10)
        toolbar.pack(fill="x")

        btn_defs = [
            ("🔄 Làm mới",     self.load_accounts,  "info"),
            ("➕ Tạo mới",     self.create_account, "success"),
            ("✏️ Sửa",         self.edit_account,   "warning"),
            ("🗑️ Xóa",         self.delete_account, "danger"),
        ]
        for label, cmd, stype in btn_defs:
            GlowButton(toolbar, text=label, command=cmd, style_type=stype, width=14).pack(side="left", padx=6, pady=0)

        GlowButton(toolbar, text="🚪 Đăng xuất", command=self.back_to_login,
                   style_type="secondary", width=14).pack(side="right", padx=6)

        # ── Search bar ──────────────────────────────────────────────────
        search_frame = tk.Frame(self.master, bg=BG_DARK, pady=8)
        search_frame.pack(fill="x", padx=20)

        tk.Label(search_frame, text="🔍", font=("Segoe UI", 12),
                 bg=BG_DARK, fg=TEXT_SECONDARY).pack(side="left", padx=(0, 6))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                bg=BG_INPUT, fg=TEXT_PRIMARY,
                                insertbackground=ACCENT, relief="flat", bd=0,
                                font=FONT_BODY, width=36)
        search_entry.pack(side="left", ipady=6, ipadx=8)

        tk.Label(search_frame, text="Tìm kiếm theo tên / username...",
                 bg=BG_DARK, fg=TEXT_SECONDARY, font=FONT_SMALL).pack(side="left", padx=8)

        # ── Table ───────────────────────────────────────────────────────
        table_frame = tk.Frame(self.master, bg=BG_DARK)
        table_frame.pack(expand=True, fill="both", padx=20, pady=(0, 8))

        # Custom ttk style for dark treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview",
                        background=BG_CARD,
                        foreground=TEXT_PRIMARY,
                        rowheight=34,
                        fieldbackground=BG_CARD,
                        bordercolor=BORDER,
                        borderwidth=0,
                        font=FONT_BODY)
        style.configure("Dark.Treeview.Heading",
                        background=BG_SURFACE,
                        foreground=ACCENT,
                        relief="flat",
                        font=("Segoe UI", 10, "bold"))
        style.map("Dark.Treeview",
                  background=[("selected", ACCENT2)],
                  foreground=[("selected", "#fff")])
        style.map("Dark.Treeview.Heading",
                  background=[("active", BG_CARD)])

        cols = ("stt", "username", "password", "hoten", "sdt", "chucvu")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings",
                                 style="Dark.Treeview", height=12)

        col_cfg = [
            ("stt",      "STT",           52,  "center"),
            ("username", "Tên đăng nhập", 180, "center"),
            ("password", "Mật khẩu",      150, "center"),
            ("hoten",    "Họ và tên",     200, "w"),
            ("sdt",      "SĐT",           120, "center"),
            ("chucvu",   "Chức vụ",       140, "center"),
        ]
        for col_id, heading, width, anchor in col_cfg:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width, anchor=anchor, minwidth=50)

        # Alternating row tags
        self.tree.tag_configure("odd",  background=BG_CARD)
        self.tree.tag_configure("even", background=BG_SURFACE)

        vscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vscroll.set)

        self.tree.pack(side="left", expand=True, fill="both")
        vscroll.pack(side="right", fill="y")

        # Bind double-click to edit
        self.tree.bind("<Double-1>", lambda e: self.edit_account())

        # ── Status bar ──────────────────────────────────────────────────
        self.status_var = tk.StringVar(value="Sẵn sàng")
        status = tk.Label(self.master, textvariable=self.status_var,
                          bg=BG_SURFACE, fg=TEXT_SECONDARY,
                          font=FONT_SMALL, anchor="w", pady=4, padx=12)
        status.pack(fill="x", side="bottom")

    # ── Data methods ────────────────────────────────────────────────────

    def load_accounts(self):
        self._all_rows = []
        for item in self.tree.get_children():
            self.tree.delete(item)

        db = "database/tk.csv"
        if not os.path.exists(db):
            self.status_var.set("⚠️  Chưa có dữ liệu")
            return

        with open(db, encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        for idx, row in enumerate(rows, 1):
            if len(row) >= 5:
                tag = "odd" if idx % 2 else "even"
                masked_pw = "●" * len(row[1])
                display = (idx, row[0], masked_pw, row[2], row[3], row[4])
                self.tree.insert("", "end", values=display, tags=(tag,), iid=str(idx - 1))
                self._all_rows.append(row)

        count = len(rows)
        self.badge_var.set(f"{count} tài khoản")
        self.status_var.set(f"✅  Đã tải {count} tài khoản")

    def _on_search(self, *_):
        kw = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)

        display_idx = 1
        for i, row in enumerate(self._all_rows):
            if kw in row[0].lower() or kw in row[2].lower():
                tag = "odd" if display_idx % 2 else "even"
                masked_pw = "●" * len(row[1])
                self.tree.insert("", "end", values=(display_idx, row[0], masked_pw, row[2], row[3], row[4]),
                                 tags=(tag,), iid=str(i))
                display_idx += 1

    def _get_selected_username(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("⚠️ Chưa chọn", "Vui lòng chọn một tài khoản!")
            return None
        vals = self.tree.item(sel[0], "values")
        return vals[1]  # username

    def delete_account(self):
        username = self._get_selected_username()
        if not username:
            return
        if messagebox.askyesno("🗑️ Xác nhận xóa",
                               f"Bạn có chắc muốn xóa tài khoản\n'{username}' không?"):
            db = "database/tk.csv"
            tmp = "database/tk_temp.csv"
            with open(db, encoding="utf-8") as f, open(tmp, "w", encoding="utf-8", newline="") as g:
                for row in csv.reader(f):
                    if row and row[0] != username:
                        csv.writer(g).writerow(row)
            os.replace(tmp, db)
            self.load_accounts()
            self.status_var.set(f"🗑️  Đã xóa tài khoản '{username}'")

    def edit_account(self):
        username = self._get_selected_username()
        if not username:
            return
        db = "database/tk.csv"
        with open(db, encoding="utf-8") as f:
            for row in csv.reader(f):
                if row and row[0] == username:
                    pw   = row[1] if len(row) > 1 else ""
                    ht   = row[2] if len(row) > 2 else ""
                    sdt  = row[3] if len(row) > 3 else ""
                    cv   = row[4] if len(row) > 4 else ""
                    self.app_manager.show_suatk_page(username, pw, ht, sdt, cv)
                    return

    def create_account(self):
        self.app_manager.show_taotk_page()

    def back_to_login(self):
        self.app_manager.show_login_page()
