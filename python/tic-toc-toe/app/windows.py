""" creating tkinter window"""

import tkinter as tk


class Window:
    """class Window"""

    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width
        self.window = tk.Tk()
        # status bar
        self.text_place = tk.StringVar()
        self.status = tk.Label(
            self.window,
            textvariable=self.text_place,
            fg="green",
            font="Courier 30",
        )
        self.status.place(x=70, y=360)

    def createplace(self):
        """create main window"""
        self.window.title("Tic toc toe")
        self.window.geometry(f"{self.width}x{self.height}")

    def show(self):
        """show work place"""
        self.window.mainloop()
