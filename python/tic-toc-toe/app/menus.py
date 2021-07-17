"""main menu"""
import os
import sys
from tkinter import messagebox


class Menu:
    """class Menu"""

    @staticmethod
    def readlog():
        """returne logfile"""
        try:
            with open("xolog.log", "r") as file:
                logs = file.read()
                messagebox.showinfo("История", logs)
        except FileNotFoundError:
            messagebox.showinfo("История", "Пока пусто")

    @staticmethod
    def dellog():
        """delete logfile"""
        if os.path.exists("xolog.log"):
            os.remove("xolog.log")
            messagebox.showinfo("Info", "Файл 'xolog.log' удален")
        else:
            messagebox.showinfo("Info", "Файл 'xolog.log' не найден или не существует ")

    @staticmethod
    def exit():
        """exit game"""
        sys.exit()
