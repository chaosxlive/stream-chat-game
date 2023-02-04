from tkinter import Tk, simpledialog


class Helper:

    def __init__(self):
        self.tk_root = Tk()
        self.tk_root.withdraw()

    def popupGetStr(self, title: str, text: str) -> str:
        return simpledialog.askstring(title=title, prompt=text)
