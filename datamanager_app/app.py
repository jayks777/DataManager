import tkinter as tk

from datamanager_app.ui.browser import DBBrowser


def main():
    root = tk.Tk()
    app = DBBrowser(root)
    root.mainloop()


if __name__ == "__main__":
    main()
