
import json
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import font as tkfont

from datamanager_app.db.manager import db_manager
from datamanager_app.ui.theme import theme


class RoundedButton(tk.Canvas):
    def __init__(
        self,
        parent,
        text,
        command,
        icon_image=None,
        icon_text="",
        radius=12,
        padding=(14, 8),
        font=("Segoe UI", 10, "bold"),
    ):
        super().__init__(parent, highlightthickness=0, bd=0, bg=self._resolve_bg(parent))
        self._command = command
        self._text = text
        self._icon_image = icon_image
        self._icon_text = icon_text
        self._radius = radius
        self._padding = padding
        self._font = font
        self._state = "normal"
        self._colors = {}
        self._rect_id = None
        self._text_id = None
        self._draw()
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _resolve_bg(self, parent):
        try:
            bg = parent.cget("background")
        except tk.TclError:
            bg = ""
        if not bg:
            try:
                bg = parent.winfo_toplevel().cget("bg")
            except tk.TclError:
                bg = "#000000"
        return bg

    def _measure(self):
        font = tkfont.Font(font=self._font)
        full_text = f"{self._icon_text} {self._text}".strip()
        text_width = font.measure(full_text)
        text_height = font.metrics("linespace")
        width = text_width + (self._padding[0] * 2)
        height = text_height + (self._padding[1] * 2)
        if self._icon_image is not None:
            width += self._icon_image.width() + 6
        return max(width, 64), max(height, 32)

    def _rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r,
            y1,
            x2 - r,
            y1,
            x2,
            y1,
            x2,
            y1 + r,
            x2,
            y2 - r,
            x2,
            y2,
            x2 - r,
            y2,
            x1 + r,
            y2,
            x1,
            y2,
            x1,
            y2 - r,
            x1,
            y1 + r,
            x1,
            y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _draw(self):
        width, height = self._measure()
        self.config(width=width, height=height)
        self.delete("all")
        self._rect_id = self._rounded_rect(
            1,
            1,
            width - 1,
            height - 1,
            self._radius,
            fill=self._colors.get("bg", "#2b4a6b"),
            outline=self._colors.get("border", "#2b4a6b"),
            width=1,
        )

        text_x = width // 2
        if self._icon_image is not None:
            icon_x = self._padding[0] + (self._icon_image.width() // 2)
            self.create_image(icon_x, height // 2, image=self._icon_image)
            text_x = icon_x + (self._icon_image.width() // 2) + 8
            anchor = "w"
        else:
            anchor = "center"

        display_text = f"{self._icon_text} {self._text}".strip()
        self._text_id = self.create_text(
            text_x,
            height // 2,
            text=display_text,
            fill=self._colors.get("fg", "#ffffff"),
            font=self._font,
            anchor=anchor,
        )

    def set_colors(self, colors):
        self._colors = colors
        self.configure(bg=colors.get("surface", self._resolve_bg(self.master)))
        self._draw()

    def set_text(self, text):
        self._text = text
        self._draw()

    def _on_enter(self, _event):
        if self._state != "disabled":
            self.itemconfig(self._rect_id, fill=self._colors.get("hover", "#1b3f5c"))

    def _on_leave(self, _event):
        if self._state != "disabled":
            self.itemconfig(self._rect_id, fill=self._colors.get("bg", "#16324a"))

    def _on_press(self, _event):
        if self._state != "disabled":
            self.itemconfig(self._rect_id, fill=self._colors.get("press", "#0f2a42"))

    def _on_release(self, _event):
        if self._state != "disabled":
            self.itemconfig(self._rect_id, fill=self._colors.get("hover", "#1b3f5c"))
            if self._command:
                self._command()


class DBBrowser:
    COLUMN_LAYOUT = [
        ("Nome", 140),
        ("Tipo", 90),
        ("PK", 40),
        ("AI", 40),
        ("NN", 40),
        ("UNQ", 55),
        ("Default", 110),
        ("FK Tabela", 110),
        ("FK Coluna", 110),
        ("On Delete", 110),
        ("On Update", 110),
        ("", 80),
    ]
    I18N = {
        "pt": {
            "app_title": "DataManager",
            "app_subtitle": "SQLite Browser",
            "btn_create_db": "Criar DB",
            "btn_open_sqlite": "Abrir SQLite",
            "btn_create_table": "Criar Tabela",
            "btn_drop_table": "Excluir Tabela",
            "btn_insert": "Inserir",
            "btn_edit": "Editar",
            "btn_delete": "Excluir",
            "db_none_open": "Nenhum banco aberto",
            "sidebar_tables": "Tabelas",
            "footer_credit": "By Jayks <3",
            "menu_options": "Opcoes",
            "menu_file": "Arquivo",
            "menu_theme": "Tema",
            "menu_language": "Idioma",
            "menu_create_db": "Criar DB",
            "menu_open_db": "Abrir DB",
            "theme_dark": "Escuro",
            "theme_divas": "For Divas",
            "lang_pt": "Portugues",
            "lang_en": "English",
            "lang_kg": "Kaingang",
        },
        "en": {
            "app_title": "DataManager",
            "app_subtitle": "SQLite Browser",
            "btn_create_db": "Create DB",
            "btn_open_sqlite": "Open SQLite",
            "btn_create_table": "Create Table",
            "btn_drop_table": "Drop Table",
            "btn_insert": "Insert",
            "btn_edit": "Edit",
            "btn_delete": "Delete",
            "db_none_open": "No database open",
            "sidebar_tables": "Tables",
            "footer_credit": "By Jayks <3",
            "menu_options": "Options",
            "menu_file": "File",
            "menu_theme": "Theme",
            "menu_language": "Language",
            "menu_create_db": "Create DB",
            "menu_open_db": "Open DB",
            "theme_dark": "Dark",
            "theme_divas": "For Divas",
            "lang_pt": "Portuguese",
            "lang_en": "English",
            "lang_kg": "Kaingang",
        },
        "kg": {
            "app_title": "DataManager",
            "app_subtitle": "Abedenego`s version",
            "btn_create_db": "Criar DB",
            "btn_open_sqlite": "Abrir SQLite",
            "btn_create_table": "Criar Tabela",
            "btn_drop_table": "Excluir Tabela",
            "btn_insert": "Inserir",
            "btn_edit": "Editar",
            "btn_delete": "Excluir",
            "db_none_open": "Nenhum banco aberto",
            "sidebar_tables": "Tabelas",
            "footer_credit": "By Jayks <3",
            "menu_options": "Opcoes",
            "menu_file": "Arquivo",
            "menu_theme": "Tema",
            "menu_language": "Idioma",
            "menu_create_db": "Criar DB",
            "menu_open_db": "Abrir DB",
            "theme_dark": "Escuro",
            "theme_divas": "For Divas",
            "lang_pt": "Portugues",
            "lang_en": "English",
            "lang_kg": "Kaingang",
        },
    }
    SUPPORTED_LANGUAGES = ("pt", "en", "kg")

    def __init__(self, root):
        self.root = root
        self.root.title("DataManager")
        self.root.geometry("1180x700")
        self.root.minsize(980, 620)
        self.theme_options = ("dark", "for_divas")
        self.current_table = None
        self.columns = []
        self.rounded_buttons = []
        self._icon_cache = {}
        self._egg_overlay = None
        self._egg_after_id = None
        self._settings_path = self._get_settings_path()
        self._load_theme_preference()
        self._load_language_preference()
        self.theme_var = tk.StringVar(value=theme.current)
        self.language_var = tk.StringVar(value=self.language)
        self._set_window_icon()
        self.create_ui()
        self._bind_shortcuts()
        self.apply_theme()
        self.root.after(0, self._try_open_last_sqlite)

    # ========================================================
    # UI
    # ========================================================

    def create_ui(self):
        self.main = ttk.Frame(self.root)
        self.main.pack(fill="both", expand=True)
        self.create_topbar()
        self.create_body()
        self.create_footer()
        self._apply_ui_texts()

    def create_topbar(self):
        self.topbar = ttk.Frame(self.main, style="Topbar.TFrame")
        self.topbar.pack(fill="x")

        self.title_label = ttk.Label(
            self.topbar,
            text="DataManager",
            style="Title.TLabel",
        )
        self.title_label.pack(side="left", padx=(16, 8), pady=10)

        self.subtitle_label = ttk.Label(
            self.topbar,
            text="",
            style="Subtitle.TLabel",
        )
        self.subtitle_label.pack(side="left", pady=10)

        self.file_menu_button = ttk.Menubutton(
            self.topbar,
            text="",
            style="Topbar.TMenubutton",
        )
        self.file_menu_button.pack(side="left", padx=(12, 4), pady=8)

        self.options_menu_button = ttk.Menubutton(
            self.topbar,
            text="",
            style="Topbar.TMenubutton",
        )
        self.options_menu_button.pack(side="left", padx=(4, 8), pady=8)

        self.actions = ttk.Frame(self.topbar, style="Topbar.TFrame")
        self.actions.pack(side="right", padx=12, pady=8)

        self.table_button = RoundedButton(
            self.actions,
            text="",
            command=self.create_table,
            icon_image=self._load_icon("table_add"),
            icon_text="▤",
            radius=14,
        )
        self.table_button.pack(side="left", padx=6)
        self.rounded_buttons.append(self.table_button)

        self.drop_button = RoundedButton(
            self.actions,
            text="",
            command=self.drop_table,
            icon_image=self._load_icon("table_remove"),
            icon_text="▧",
            radius=14,
        )
        self.drop_button.pack(side="left", padx=6)
        self.rounded_buttons.append(self.drop_button)

        self.db_label = ttk.Label(
            self.topbar,
            text="",
            style="Topbar.TLabel",
        )
        self.db_label.pack(side="right", padx=12)
        self._create_menu()

    def create_body(self):
        body = ttk.Frame(self.main)
        body.pack(fill="both", expand=True, padx=14, pady=(4, 14))
        self.create_sidebar(body)
        self.create_table_area(body)

    def create_footer(self):
        self.footer = ttk.Frame(self.main, style="Topbar.TFrame")
        self.footer.pack(fill="x")
        self.credit_label = ttk.Label(
            self.footer,
            text="",
            style="Topbar.TLabel",
        )
        self.credit_label.pack(side="right", padx=12, pady=(0, 8))

    def create_sidebar(self, parent):
        self.sidebar = ttk.Frame(parent, width=260, style="Sidebar.TFrame")
        self.sidebar.pack(side="left", fill="y", padx=(0, 12))

        self.sidebar_label = ttk.Label(
            self.sidebar,
            text="",
            style="Sidebar.TLabel",
        )
        self.sidebar_label.pack(anchor="w", padx=12, pady=(12, 6))

        self.tables_list = tk.Listbox(self.sidebar, activestyle="none", bd=0)
        self.tables_list.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.tables_list.bind("<<ListboxSelect>>", self.on_table_select)

    def create_table_area(self, parent):
        self.area = ttk.Frame(parent)
        self.area.pack(side="right", fill="both", expand=True)

        self.toolbar = ttk.Frame(self.area)
        self.toolbar.pack(fill="x", pady=(0, 8))

        self.insert_button = RoundedButton(
            self.toolbar,
            text="",
            command=self.insert_row,
            icon_image=self._load_icon("row_add"),
            icon_text="+",
            radius=12,
        )
        self.insert_button.pack(side="left", padx=4)
        self.rounded_buttons.append(self.insert_button)

        self.edit_button = RoundedButton(
            self.toolbar,
            text="",
            command=self.edit_row,
            icon_image=self._load_icon("edit"),
            icon_text="✎",
            radius=12,
        )
        self.edit_button.pack(side="left", padx=4)
        self.rounded_buttons.append(self.edit_button)

        self.delete_button = RoundedButton(
            self.toolbar,
            text="",
            command=self.delete_row,
            icon_image=self._load_icon("trash"),
            icon_text="×",
            radius=12,
        )
        self.delete_button.pack(side="left", padx=4)
        self.rounded_buttons.append(self.delete_button)

        self.table_card = ttk.Frame(self.area, style="Card.TFrame")
        self.table_card.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(self.table_card)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)
    # ========================================================
    # DATABASE
    # ========================================================

    def _get_settings_path(self):
        appdata = os.getenv("APPDATA")
        if appdata:
            base_dir = os.path.join(appdata, "DataManager")
        else:
            base_dir = os.path.join(os.path.expanduser("~"), ".datamanager")
        os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, "settings.json")

    def _load_settings(self):
        if not os.path.exists(self._settings_path):
            return {}
        try:
            with open(self._settings_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _save_settings(self, settings):
        os.makedirs(os.path.dirname(self._settings_path), exist_ok=True)
        with open(self._settings_path, "w", encoding="utf-8") as fh:
            json.dump(settings, fh, ensure_ascii=True, indent=2)

    def _save_last_db_path(self, path):
        settings = self._load_settings()
        settings["last_db_path"] = path
        self._save_settings(settings)

    def _save_theme_preference(self):
        settings = self._load_settings()
        settings["theme"] = theme.current
        self._save_settings(settings)

    def _save_language_preference(self):
        settings = self._load_settings()
        settings["language"] = self.language
        self._save_settings(settings)

    def _load_theme_preference(self):
        settings = self._load_settings()
        saved_theme = settings.get("theme")
        if saved_theme in theme.COLORS:
            theme.current = saved_theme
        else:
            theme.current = "dark"

    def _load_language_preference(self):
        settings = self._load_settings()
        saved_language = settings.get("language")
        if saved_language in self.SUPPORTED_LANGUAGES:
            self.language = saved_language
        else:
            self.language = "pt"

    def _clear_last_db_path(self):
        settings = self._load_settings()
        if "last_db_path" in settings:
            settings.pop("last_db_path", None)
            self._save_settings(settings)

    def _open_sqlite_path(self, path, persist_last=True):
        conn = db_manager.connect_sqlite(path)
        self.db_label.config(text=conn.name)
        self.refresh_tables()
        if persist_last:
            self._save_last_db_path(path)

    def _try_open_last_sqlite(self):
        settings = self._load_settings()
        last_db_path = settings.get("last_db_path")
        if not last_db_path:
            return
        if not os.path.exists(last_db_path):
            self._clear_last_db_path()
            return
        try:
            self._open_sqlite_path(last_db_path, persist_last=False)
        except Exception:
            self._clear_last_db_path()

    def open_sqlite(self):
        try:
            path = filedialog.askopenfilename(filetypes=[("SQLite", "*.db *.sqlite")])
            if not path:
                return
            self._open_sqlite_path(path)
        except Exception as exc:
            self._show_error("Erro ao abrir", str(exc))

    def create_sqlite(self):
        try:
            path = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("SQLite", "*.db *.sqlite")],
            )
            if not path:
                return
            conn = db_manager.create_sqlite(path)
            self.db_label.config(text=conn.name)
            self.refresh_tables()
            self._save_last_db_path(path)
        except Exception as exc:
            self._show_error("Erro ao criar banco", str(exc))

    def create_table(self):
        if not db_manager.current:
            self._show_warning("Aviso", "Abra ou crie um banco antes de criar tabela.")
            return
        try:
            result = self.open_table_form()
            if result is None:
                return
            table_name, columns = result
            db_manager.create_table(table_name, columns)
            self.refresh_tables()
        except Exception as exc:
            self._show_error("Erro ao criar tabela", str(exc))

    def drop_table(self):
        if not db_manager.current:
            self._show_warning("Aviso", "Abra ou crie um banco antes de excluir tabela.")
            return
        if not self.current_table:
            self._show_warning("Aviso", "Selecione uma tabela para excluir.")
            return

        colors = theme.COLORS[theme.current]
        form = tk.Toplevel(self.root)
        form.title("Excluir tabela")
        form.transient(self.root)
        form.grab_set()
        form.configure(bg=colors["panel"])
        form.resizable(False, False)

        header = tk.Label(
            form,
            text="Excluir tabela",
            bg=colors["panel"],
            fg=colors["fg"],
            font=("Segoe UI", 12, "bold"),
        )
        header.pack(anchor="w", padx=18, pady=(14, 6))

        message = tk.Label(
            form,
            text=f"Tem certeza que deseja excluir a tabela '{self.current_table}'?\nEssa acao nao pode ser desfeita.",
            bg=colors["panel"],
            fg=colors["muted"],
            font=("Segoe UI", 9),
            justify="left",
        )
        message.pack(anchor="w", padx=18, pady=(0, 12))

        footer = tk.Frame(form, bg=colors["panel"])
        footer.pack(fill="x", padx=18, pady=(0, 16))

        def on_cancel():
            form.destroy()

        def on_confirm():
            try:
                db_manager.drop_table(self.current_table)
                self.current_table = None
                self.tree.delete(*self.tree.get_children())
                self.refresh_tables()
                form.destroy()
            except Exception as exc:
                self._show_error("Erro ao excluir tabela", str(exc), parent=form)

        cancel_button = RoundedButton(
            footer,
            text="Cancelar",
            command=on_cancel,
            radius=12,
        )
        cancel_button.pack(side="right", padx=(6, 0))

        confirm_button = RoundedButton(
            footer,
            text="Excluir",
            command=on_confirm,
            radius=12,
        )
        confirm_button.pack(side="right", padx=(0, 6))

        self._apply_rounded_button_theme(cancel_button, colors, secondary=True)
        self._apply_rounded_button_theme(confirm_button, colors, secondary=False)

        form.bind("<Escape>", lambda _event: on_cancel())
        form.bind("<Return>", lambda _event: on_confirm())

        form.update_idletasks()
        self._center_window(form)
        form.wait_window()

    def refresh_tables(self):
        try:
            self.tables_list.delete(0, tk.END)
            for table in db_manager.get_tables():
                self.tables_list.insert(tk.END, table)
        except Exception as exc:
            self._show_error("Erro ao listar tabelas", str(exc))

    def on_table_select(self, event):
        selection = self.tables_list.curselection()
        if not selection:
            return
        table = self.tables_list.get(selection[0])
        self.current_table = table
        self.load_table()

    def load_table(self):
        try:
            cols, rows = db_manager.select_all(self.current_table)
            self.columns = cols
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = cols
            self.tree["show"] = "headings"
            for col in cols:
                self.tree.heading(col, text=col, anchor="center")
                self.tree.column(col, anchor="center", width=120, minwidth=80)
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as exc:
            self._show_error("Erro ao carregar tabela", str(exc))
    # ========================================================
    # CRUD
    # ========================================================

    def insert_row(self):
        if not self.current_table:
            self._show_warning("Aviso", "Selecione uma tabela para inserir.")
            return
        try:
            data = self.open_form("Inserir registro", self.columns, {})
            if data is None:
                return
            db_manager.insert(self.current_table, data)
            self.load_table()
        except Exception as exc:
            self._show_error("Erro ao inserir", str(exc))

    def edit_row(self):
        selected = self.tree.focus()
        if not selected:
            self._show_warning("Aviso", "Selecione um registro para editar.")
            return
        values = list(self.tree.item(selected)["values"])
        pk_name = self.columns[0]
        pk_value = values[0]
        initial = {col: values[i] for i, col in enumerate(self.columns)}
        try:
            data = self.open_form("Editar registro", self.columns, initial)
            if data is None:
                return
            db_manager.update(self.current_table, pk_name, pk_value, data)
            self.load_table()
        except Exception as exc:
            self._show_error("Erro ao editar", str(exc))

    def delete_row(self):
        selected = self.tree.focus()
        if not selected:
            self._show_warning("Aviso", "Selecione um registro para excluir.")
            return
        values = self.tree.item(selected)["values"]
        pk_name = self.columns[0]
        pk_value = values[0]
        try:
            db_manager.delete(self.current_table, pk_name, pk_value)
            self.load_table()
        except Exception as exc:
            self._show_error("Erro ao excluir", str(exc))

    def open_form(self, title, columns, initial_values):
        colors = theme.COLORS[theme.current]
        form = tk.Toplevel(self.root)
        form.title(title)
        form.transient(self.root)
        form.grab_set()
        form.configure(bg=colors["panel"])
        form.resizable(False, False)

        header = tk.Label(
            form,
            text=title,
            bg=colors["panel"],
            fg=colors["fg"],
            font=("Segoe UI", 12, "bold"),
        )
        header.pack(anchor="w", padx=18, pady=(14, 8))

        body = tk.Frame(form, bg=colors["panel"])
        body.pack(fill="both", padx=18, pady=(0, 12))
        body.grid_rowconfigure(1, weight=1)

        entries = {}
        for row, col in enumerate(columns):
            label = tk.Label(
                body,
                text=col,
                bg=colors["panel"],
                fg=colors["muted"],
                font=("Segoe UI", 9, "bold"),
            )
            label.grid(row=row, column=0, sticky="w", pady=6)

            entry = tk.Entry(
                body,
                bg=colors["input_bg"],
                fg=colors["input_fg"],
                insertbackground=colors["input_focus"],
                relief="flat",
                highlightthickness=1,
                highlightbackground=colors["input_border"],
                highlightcolor=colors["input_focus"],
                width=42,
                font=("Segoe UI", 10),
            )
            entry.grid(row=row, column=1, sticky="ew", padx=(12, 0), pady=6)
            entry.insert(0, initial_values.get(col, ""))
            entries[col] = entry

        body.grid_columnconfigure(1, weight=1)

        footer = tk.Frame(form, bg=colors["panel"])
        footer.pack(fill="x", padx=18, pady=(0, 16))

        result = {"data": None}

        def on_cancel():
            result["data"] = None
            form.destroy()

        def on_save():
            try:
                payload = {col: entries[col].get() for col in columns}
                result["data"] = payload
                form.destroy()
            except Exception as exc:
                self._show_error("Erro no formulario", str(exc), parent=form)

        cancel_button = RoundedButton(
            footer,
            text="Cancelar",
            command=on_cancel,
            radius=12,
        )
        cancel_button.pack(side="right", padx=(6, 0))

        save_button = RoundedButton(
            footer,
            text="Salvar",
            command=on_save,
            radius=12,
        )
        save_button.pack(side="right", padx=(0, 6))

        self._apply_rounded_button_theme(cancel_button, colors, secondary=True)
        self._apply_rounded_button_theme(save_button, colors, secondary=False)

        form.bind("<Escape>", lambda _event: on_cancel())
        form.bind("<Return>", lambda _event: on_save())

        form.update_idletasks()
        self._center_window(form)
        form.wait_window()
        return result["data"]

    def open_table_form(self):
        colors = theme.COLORS[theme.current]
        form = tk.Toplevel(self.root)
        form.title("Criar tabela")
        form.transient(self.root)
        form.grab_set()
        form.configure(bg=colors["panel"])
        form.resizable(False, False)

        header = tk.Label(
            form,
            text="Criar tabela",
            bg=colors["panel"],
            fg=colors["fg"],
            font=("Segoe UI", 12, "bold"),
        )
        header.pack(anchor="w", padx=18, pady=(14, 8))

        body = tk.Frame(form, bg=colors["panel"])
        body.pack(fill="both", padx=18, pady=(0, 12))

        name_label = tk.Label(
            body,
            text="Nome da tabela",
            bg=colors["panel"],
            fg=colors["muted"],
            font=("Segoe UI", 9, "bold"),
        )
        name_label.grid(row=0, column=0, sticky="w", pady=6)

        name_entry = tk.Entry(
            body,
            bg=colors["input_bg"],
            fg=colors["input_fg"],
            insertbackground=colors["input_focus"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=colors["input_border"],
            highlightcolor=colors["input_focus"],
            width=42,
            font=("Segoe UI", 10),
        )
        name_entry.grid(row=0, column=1, sticky="ew", padx=(12, 0), pady=6)

        cols_label = tk.Label(
            body,
            text="Colunas",
            bg=colors["panel"],
            fg=colors["muted"],
            font=("Segoe UI", 9, "bold"),
        )
        cols_label.grid(row=1, column=0, sticky="nw", pady=6)

        columns_frame = tk.Frame(body, bg=colors["panel"])
        columns_frame.grid(row=1, column=1, sticky="nsew", padx=(12, 0), pady=6)
        columns_frame.grid_columnconfigure(0, weight=1)
        columns_frame.grid_rowconfigure(1, weight=1)

        header = tk.Frame(columns_frame, bg=colors["panel"])
        header.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        self._apply_column_grid(header)

        for idx, (text, _width) in enumerate(self.COLUMN_LAYOUT):
            tk.Label(
                header,
                text=text,
                bg=colors["panel"],
                fg=colors["muted"],
                font=("Segoe UI", 9, "bold"),
            ).grid(row=0, column=idx, padx=4, sticky="w")

        canvas = tk.Canvas(
            columns_frame,
            bg=colors["panel"],
            highlightthickness=0,
            bd=0,
        )
        canvas.configure(height=240)
        canvas.grid(row=1, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            columns_frame,
            orient="vertical",
            command=canvas.yview,
            style="Vertical.TScrollbar",
        )
        scrollbar.grid(row=1, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        rows_container = tk.Frame(canvas, bg=colors["panel"])
        rows_window = canvas.create_window((0, 0), window=rows_container, anchor="nw")

        def on_frame_configure(_event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas.itemconfig(rows_window, width=event.width)

        rows_container.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        def _on_mousewheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        form_state = {
            "colors": colors,
            "rows_container": rows_container,
            "column_rows": [],
        }

        self._add_column_row(form_state)
        self._add_column_row(form_state)
        self._add_column_row(form_state)

        body.grid_columnconfigure(1, weight=1)

        footer = tk.Frame(form, bg=colors["panel"])
        footer.pack(fill="x", padx=18, pady=(0, 16))

        result = {"data": None}

        def on_cancel():
            result["data"] = None
            form.destroy()

        def on_save():
            table_name = name_entry.get().strip()
            column_rows = form_state["column_rows"]
            if not table_name or not column_rows:
                self._show_error(
                    "Dados incompletos",
                    "Informe o nome da tabela e pelo menos uma coluna.",
                    parent=form,
                )
                return
            columns = []
            for row in column_rows:
                name = row["name"].get().strip()
                if not name:
                    continue
                col_type = row["type"].get()
                pieces = [name, col_type]
                if row["pk"].get():
                    pieces.append("PRIMARY KEY")
                if row["ai"].get():
                    pieces.append("AUTOINCREMENT")
                if row["nn"].get():
                    pieces.append("NOT NULL")
                if row["unq"].get():
                    pieces.append("UNIQUE")
                default_val = row["default"].get().strip()
                if default_val:
                    pieces.append(f"DEFAULT {default_val}")
                fk_table = row["fk_table"].get().strip()
                fk_col = row["fk_col"].get().strip()
                if fk_table and fk_col:
                    pieces.append(f"REFERENCES {fk_table}({fk_col})")
                    on_delete = row["on_delete"].get().strip()
                    on_update = row["on_update"].get().strip()
                    if on_delete:
                        pieces.append(f"ON DELETE {on_delete}")
                    if on_update:
                        pieces.append(f"ON UPDATE {on_update}")
                columns.append(" ".join(pieces))
            if not columns:
                self._show_error(
                    "Dados incompletos",
                    "Informe pelo menos uma coluna valida.",
                    parent=form,
                )
                return
            result["data"] = (table_name, columns)
            form.destroy()

        add_button = RoundedButton(
            footer,
            text="Adicionar coluna",
            command=lambda: self._add_column_row(form_state),
            icon_image=self._load_icon("column_add"),
            icon_text="+",
            radius=12,
        )
        add_button.pack(side="left")

        cancel_button = RoundedButton(
            footer,
            text="Cancelar",
            command=on_cancel,
            radius=12,
        )
        cancel_button.pack(side="right", padx=(6, 0))

        save_button = RoundedButton(
            footer,
            text="Criar",
            command=on_save,
            radius=12,
        )
        save_button.pack(side="right", padx=(0, 6))

        self._apply_rounded_button_theme(cancel_button, colors, secondary=True)
        self._apply_rounded_button_theme(save_button, colors, secondary=False)
        self._apply_rounded_button_theme(add_button, colors, secondary=True)

        form.bind("<Escape>", lambda _event: on_cancel())
        form.bind("<Return>", lambda _event: on_save())

        form.update_idletasks()
        self._center_window(form)
        form.wait_window()
        return result["data"]
    # ========================================================
    # THEME
    # ========================================================

    def apply_theme(self):
        colors = theme.COLORS[theme.current]

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=colors["bg"])
        style.configure("Topbar.TFrame", background=colors["panel"])
        style.configure("Sidebar.TFrame", background=colors["panel"])
        style.configure("Card.TFrame", background=colors["card"])
        style.configure("TLabel", background=colors["bg"], foreground=colors["fg"])
        style.configure(
            "Title.TLabel",
            background=colors["panel"],
            foreground=colors["fg"],
            font=("Segoe UI", 14, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=colors["panel"],
            foreground=colors["muted"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Topbar.TLabel",
            background=colors["panel"],
            foreground=colors["muted"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Topbar.TMenubutton",
            background=colors["panel"],
            foreground=colors["fg"],
            borderwidth=1,
            relief="flat",
            focusthickness=0,
            padding=(10, 4),
            arrowcolor=colors["fg"],
        )
        style.map(
            "Topbar.TMenubutton",
            background=[("active", colors["accent_dark"])],
            foreground=[("active", colors["fg"])],
        )
        style.configure(
            "Sidebar.TLabel",
            background=colors["panel"],
            foreground=colors["muted"],
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "TButton",
            background=colors["button_bg"],
            foreground=colors["button_fg"],
            borderwidth=0,
            focusthickness=0,
            padding=(12, 6),
        )
        style.map(
            "TButton",
            background=[("active", colors["accent_hover"])],
            foreground=[("disabled", colors["muted"])],
        )
        style.configure(
            "Treeview",
            background=colors["tree_bg"],
            foreground=colors["tree_fg"],
            fieldbackground=colors["tree_bg"],
            bordercolor=colors["border"],
            rowheight=26,
        )
        style.map(
            "Treeview",
            background=[("selected", colors["select_bg"])],
            foreground=[("selected", colors["select_fg"])],
        )
        style.configure(
            "Treeview.Heading",
            background=colors["panel"],
            foreground=colors["fg"],
            relief="flat",
        )
        style.map(
            "Treeview.Heading",
            background=[("active", colors["accent_dark"])],
        )
        style.configure(
            "TCombobox",
            fieldbackground=colors["input_bg"],
            background=colors["input_bg"],
            foreground=colors["input_fg"],
            bordercolor=colors["input_border"],
            lightcolor=colors["input_border"],
            darkcolor=colors["input_border"],
            arrowcolor=colors["input_focus"],
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", colors["input_bg"])],
            foreground=[("readonly", colors["input_fg"])],
        )
        self.root.option_add("*TCombobox*Listbox.background", colors["input_bg"])
        self.root.option_add("*TCombobox*Listbox.foreground", colors["input_fg"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", colors["select_bg"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", colors["select_fg"])
        style.configure(
            "Vertical.TScrollbar",
            background=colors["panel"],
            troughcolor=colors["card"],
            bordercolor=colors["border"],
            lightcolor=colors["card"],
            darkcolor=colors["card"],
            arrowcolor=colors["muted"],
        )

        self.root.configure(bg=colors["bg"])

        self.tables_list.configure(
            bg=colors["panel"],
            fg=colors["fg"],
            selectbackground=colors["select_bg"],
            selectforeground=colors["select_fg"],
            highlightthickness=0,
        )

        for button in self.rounded_buttons:
            self._apply_rounded_button_theme(button, colors, secondary=False)
        self._apply_menu_theme()

    def _apply_rounded_button_theme(self, button, colors, secondary=False):
        if secondary:
            palette = {
                "bg": colors["panel"],
                "hover": colors["card"],
                "press": colors["button_pressed"],
                "border": colors["border"],
                "fg": colors["fg"],
                "surface": colors["panel"],
            }
        else:
            palette = {
                "bg": colors["button_bg"],
                "hover": colors["button_hover"],
                "press": colors["button_pressed"],
                "border": colors["button_border"],
                "fg": colors["button_fg"],
                "surface": colors["panel"],
            }
        button.set_colors(palette)

    def _center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def _apply_column_grid(self, container):
        for idx, (_label, minsize) in enumerate(self.COLUMN_LAYOUT):
            container.grid_columnconfigure(idx, minsize=minsize, weight=0)

    def _add_column_row(self, form_state):
        colors = form_state["colors"]
        rows_container = form_state["rows_container"]
        column_rows = form_state["column_rows"]

        type_options = ["INTEGER", "TEXT", "REAL", "BLOB", "NUMERIC"]
        action_options = ["NO ACTION", "CASCADE", "SET NULL", "SET DEFAULT", "RESTRICT"]

        def make_entry(parent, width=14):
            entry = tk.Entry(
                parent,
                bg=colors["input_bg"],
                fg=colors["input_fg"],
                insertbackground=colors["input_focus"],
                relief="flat",
                highlightthickness=1,
                highlightbackground=colors["input_border"],
                highlightcolor=colors["input_focus"],
                width=width,
                font=("Segoe UI", 9),
            )
            return entry

        def make_combobox(parent, values, width=10):
            combo = ttk.Combobox(parent, values=values, width=width, state="readonly")
            combo.set(values[0])
            return combo

        row_frame = tk.Frame(rows_container, bg=colors["panel"])
        self._apply_column_grid(row_frame)
        row_frame.pack(fill="x", pady=3)

        name_entry = make_entry(row_frame, width=16)
        name_entry.grid(row=0, column=0, padx=4, sticky="w")

        type_combo = make_combobox(row_frame, type_options, width=10)
        type_combo.grid(row=0, column=1, padx=4, sticky="w")

        pk_var = tk.IntVar(value=0)
        ai_var = tk.IntVar(value=0)
        nn_var = tk.IntVar(value=0)
        unq_var = tk.IntVar(value=0)

        pk_check = tk.Checkbutton(
            row_frame,
            variable=pk_var,
            bg=colors["panel"],
            fg=colors["fg"],
            selectcolor=colors["panel"],
            activebackground=colors["panel"],
            activeforeground=colors["fg"],
        )
        pk_check.grid(row=0, column=2, padx=6)

        ai_check = tk.Checkbutton(
            row_frame,
            variable=ai_var,
            bg=colors["panel"],
            fg=colors["fg"],
            selectcolor=colors["panel"],
            activebackground=colors["panel"],
            activeforeground=colors["fg"],
        )
        ai_check.grid(row=0, column=3, padx=6)

        nn_check = tk.Checkbutton(
            row_frame,
            variable=nn_var,
            bg=colors["panel"],
            fg=colors["fg"],
            selectcolor=colors["panel"],
            activebackground=colors["panel"],
            activeforeground=colors["fg"],
        )
        nn_check.grid(row=0, column=4, padx=6)

        unq_check = tk.Checkbutton(
            row_frame,
            variable=unq_var,
            bg=colors["panel"],
            fg=colors["fg"],
            selectcolor=colors["panel"],
            activebackground=colors["panel"],
            activeforeground=colors["fg"],
        )
        unq_check.grid(row=0, column=5, padx=6)

        default_entry = make_entry(row_frame, width=12)
        default_entry.grid(row=0, column=6, padx=4, sticky="w")

        fk_table_entry = make_entry(row_frame, width=12)
        fk_table_entry.grid(row=0, column=7, padx=4, sticky="w")

        fk_col_entry = make_entry(row_frame, width=12)
        fk_col_entry.grid(row=0, column=8, padx=4, sticky="w")

        on_delete_combo = make_combobox(row_frame, action_options, width=10)
        on_delete_combo.grid(row=0, column=9, padx=4, sticky="w")

        on_update_combo = make_combobox(row_frame, action_options, width=10)
        on_update_combo.grid(row=0, column=10, padx=4, sticky="w")

        remove_button = RoundedButton(
            row_frame,
            text="x",
            command=lambda: self._remove_column_row(form_state, row_frame),
            icon_image=self._load_icon("remove"),
            icon_text="",
            radius=10,
        )
        remove_button.grid(row=0, column=11, padx=6)
        self._apply_rounded_button_theme(remove_button, colors, secondary=True)

        column_rows.append(
            {
                "frame": row_frame,
                "name": name_entry,
                "type": type_combo,
                "pk": pk_var,
                "ai": ai_var,
                "nn": nn_var,
                "unq": unq_var,
                "default": default_entry,
                "fk_table": fk_table_entry,
                "fk_col": fk_col_entry,
                "on_delete": on_delete_combo,
                "on_update": on_update_combo,
            }
        )

    def _remove_column_row(self, form_state, row_frame):
        column_rows = form_state["column_rows"]
        for idx, row in enumerate(column_rows):
            if row["frame"] == row_frame:
                row_frame.destroy()
                column_rows.pop(idx)
                break

    def _icons_dir(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        return os.path.join(base_dir, "assets", "icons")

    def _icons_dirs(self):
        dirs = [
            self._icons_dir(),
            os.path.join(os.path.dirname(__file__), "..", "assets", "icons"),
            os.path.join(os.path.dirname(__file__), "assets", "icons"),
            os.path.join(os.getcwd(), "datamanager_app", "assets", "icons"),
            os.path.join(os.getcwd(), "assets", "icons"),
        ]
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            dirs.insert(0, os.path.join(meipass, "datamanager_app", "assets", "icons"))
            dirs.insert(1, os.path.join(meipass, "assets", "icons"))
        return dirs

    def _find_icon_file(self, name, exts):
        for icons_dir in self._icons_dirs():
            for ext in exts:
                path = os.path.abspath(os.path.join(icons_dir, f"{name}.{ext}"))
                if os.path.exists(path):
                    return path
        return None

    def _load_icon(self, name):
        if name in self._icon_cache:
            return self._icon_cache[name]
        path = self._find_icon_file(name, ("png", "gif"))
        if path:
            try:
                image = tk.PhotoImage(file=path)
            except tk.TclError:
                image = None
            if image is not None:
                self._icon_cache[name] = image
                return image
        self._icon_cache[name] = None
        return None

    def _set_window_icon(self):
        ico_path = self._find_icon_file("app", ("ico",))
        if ico_path is not None:
            try:
                self.root.iconbitmap(ico_path)
                return
            except tk.TclError:
                pass
        icon = self._load_icon("app")
        if icon is not None:
            try:
                self.root.iconphoto(True, icon)
            except tk.TclError:
                pass

    def _bind_shortcuts(self):
        self.root.bind_all("<Control-Alt-j>", self._on_easter_egg_shortcut)
        self.root.bind_all("<Control-Alt-J>", self._on_easter_egg_shortcut)

    def _t(self, key):
        bundle = self.I18N.get(self.language, self.I18N["pt"])
        return bundle.get(key, key)

    def _create_menu(self):
        self.file_menu = tk.Menu(self.root, tearoff=0)
        self.options_menu = tk.Menu(self.root, tearoff=0)
        self.theme_menu = tk.Menu(self.options_menu, tearoff=0)
        self.language_menu = tk.Menu(self.options_menu, tearoff=0)

        self.file_menu.add_command(label=self._t("menu_create_db"), command=self.create_sqlite)
        self.file_menu.add_command(label=self._t("menu_open_db"), command=self.open_sqlite)

        self.theme_menu.add_radiobutton(
            label=self._t("theme_dark"),
            variable=self.theme_var,
            value="dark",
            command=self._on_theme_selected,
        )
        self.theme_menu.add_radiobutton(
            label=self._t("theme_divas"),
            variable=self.theme_var,
            value="for_divas",
            command=self._on_theme_selected,
        )

        self.language_menu.add_radiobutton(
            label=self._t("lang_pt"),
            variable=self.language_var,
            value="pt",
            command=self._on_language_selected,
        )
        self.language_menu.add_radiobutton(
            label=self._t("lang_en"),
            variable=self.language_var,
            value="en",
            command=self._on_language_selected,
        )
        self.language_menu.add_radiobutton(
            label=self._t("lang_kg"),
            variable=self.language_var,
            value="kg",
            command=self._on_language_selected,
        )

        self.options_menu.add_cascade(label=self._t("menu_theme"), menu=self.theme_menu)
        self.options_menu.add_cascade(label=self._t("menu_language"), menu=self.language_menu)
        self.file_menu_button.config(text=self._t("menu_file"), menu=self.file_menu)
        self.options_menu_button.config(text=self._t("menu_options"), menu=self.options_menu)
        self._apply_menu_theme()

    def _apply_ui_texts(self):
        self.root.title(self._t("app_title"))
        self.title_label.config(text=self._t("app_title"))
        self.subtitle_label.config(text=self._t("app_subtitle"))

        self.table_button.set_text(self._t("btn_create_table"))
        self.drop_button.set_text(self._t("btn_drop_table"))

        self.insert_button.set_text(self._t("btn_insert"))
        self.edit_button.set_text(self._t("btn_edit"))
        self.delete_button.set_text(self._t("btn_delete"))

        if not db_manager.current:
            self.db_label.config(text=self._t("db_none_open"))
        self.sidebar_label.config(text=self._t("sidebar_tables"))
        self.credit_label.config(text=self._t("footer_credit"))

    def _on_theme_selected(self, _event=None):
        selected_theme = self.theme_var.get()
        if selected_theme not in theme.COLORS:
            return
        theme.current = selected_theme
        self._save_theme_preference()
        self.apply_theme()

    def _on_language_selected(self):
        selected_language = self.language_var.get()
        if selected_language not in self.SUPPORTED_LANGUAGES:
            return
        self.language = selected_language
        self._save_language_preference()
        self._create_menu()
        self._apply_ui_texts()
        if selected_language == "kg":
            self._show_info("Modo Kaingang", "Traducao experimental para zoeira.")

    def _on_easter_egg_shortcut(self, _event=None):
        egg_image = self._load_icon("egg")
        if egg_image is None:
            return "break"

        if self._egg_after_id:
            self.root.after_cancel(self._egg_after_id)
            self._egg_after_id = None
        if self._egg_overlay and self._egg_overlay.winfo_exists():
            self._egg_overlay.destroy()

        self._egg_overlay = tk.Label(self.root, image=egg_image, bd=0, highlightthickness=0)
        self._egg_overlay.image = egg_image
        self._egg_overlay.place(relx=0.5, rely=0.5, anchor="center")
        self._egg_overlay.lift()
        self._egg_after_id = self.root.after(100, self._hide_easter_egg)
        return "break"

    def _hide_easter_egg(self):
        self._egg_after_id = None
        if self._egg_overlay and self._egg_overlay.winfo_exists():
            self._egg_overlay.destroy()
        self._egg_overlay = None

    def _show_error(self, title, message, parent=None):
        messagebox.showerror(title, message, parent=parent or self.root)

    def _show_warning(self, title, message, parent=None):
        messagebox.showwarning(title, message, parent=parent or self.root)

    def _show_info(self, title, message, parent=None):
        messagebox.showinfo(title, message, parent=parent or self.root)

    def _apply_menu_theme(self):
        if not hasattr(self, "file_menu"):
            return
        colors = theme.COLORS[theme.current]
        common = {
            "bg": colors["panel"],
            "fg": colors["fg"],
            "activebackground": colors["accent_dark"],
            "activeforeground": colors["fg"],
        }
        self.file_menu.config(**common)
        self.options_menu.config(**common)
        self.theme_menu.config(**common)
        self.language_menu.config(**common)
