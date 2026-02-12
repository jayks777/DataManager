class Theme:
    def __init__(self):
        self.current = "dark"
        self.COLORS = {
            "dark": {
                "bg": "#0b0d11",
                "panel": "#111826",
                "card": "#0f1624",
                "fg": "#e8f0ff",
                "muted": "#8ea6c8",
                "border": "#1d2b3f",
                "accent": "#4cc2ff",
                "accent_hover": "#6fd0ff",
                "accent_dark": "#2aa4f2",
                "button_bg": "#16324a",
                "button_fg": "#4cc2ff",
                "button_border": "#2b4a6b",
                "button_hover": "#f4fbff",
                "button_pressed": "#0f2a42",
                "input_bg": "#0c1420",
                "input_fg": "#e8f0ff",
                "input_border": "#2b4a6b",
                "input_focus": "#4cc2ff",
                "tree_bg": "#0d1422",
                "tree_alt": "#0f1828",
                "tree_fg": "#e8f0ff",
                "select_bg": "#1d3b5a",
                "select_fg": "#4cc2ff",
            },
        }


theme = Theme()
