""" Module contains logic of Tic Toc Toe"""
import logging
import os
import sys
import tkinter as tk
from tkinter import messagebox


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


class Gameprocesse:
    """class Gameprocesse"""

    def __init__(self) -> None:
        self.place = None
        self.AI = "X"
        self.PLAYER = "O"
        self.oponent = None

    @staticmethod
    def new_game(place):
        """update self.place (work place)"""
        for i, value in enumerate(place):
            for j, val in enumerate(value):
                place[i][j]["text"] = " "

    @staticmethod
    def check_win(place):
        """check is player win and return symbol"""
        for i in range(3):
            if place[i][0]["text"] != " ":
                if place[i][0]["text"] == place[i][1]["text"] == place[i][2]["text"]:
                    return place[i][0]["text"]
            if place[0][i]["text"] != " ":
                if place[0][i]["text"] == place[1][i]["text"] == place[2][i]["text"]:
                    return place[i][0]["text"]
        if place[1][1]["text"] != " ":
            if place[0][0]["text"] == place[1][1]["text"] == place[2][2]["text"]:
                return place[0][0]["text"]
            if place[0][2]["text"] == place[1][1]["text"] == place[2][0]["text"]:
                return place[0][2]["text"]
        return False

    def show_winner(self, place, counter, status):
        """show winner in mb and refresh status"""
        if counter > 4:
            if self.check_win(place):
                if counter % 2 == 0:
                    messagebox.showinfo("Игра окончена", "Победил Игрок2")
                    status = False
                    return True
                else:
                    messagebox.showinfo("Игра окончена", "Победил Игрок1")
                    status = False
                    return True

        if counter == 9:
            messagebox.showinfo("Игра окончена", "Ничья")
            status = False
            return True

    # MINIMAX
    #################################
    @staticmethod
    def freecolumn(places):
        """return free spots"""
        # получает все пустые ячейки
        isfree = [j for group in places for j in group if j["text"] == " "]
        return isfree

    def minimax(self, gameplace, player):
        """recursion of to score"""
        place = gameplace
        # Empty index
        freestep = self.freecolumn(place)

        # Check win
        winner = self.check_win(place)
        if winner == self.AI:
            return 10
        if winner == self.PLAYER:
            return -10

        # push score for each index

        if player == self.AI:
            score = -500
            for i in freestep:
                for j, value in enumerate(place):
                    for pos, val in enumerate(value):
                        if val == i:
                            place[j][pos]["text"] = player
                            mass = self.minimax(place, self.PLAYER)
                            place[j][pos]["text"] = " "
                            score = max(score, mass)

        else:
            score = 500
            for i in freestep:
                for j, value in enumerate(place):
                    for pos, val in enumerate(value):
                        if val == i:
                            place[j][pos]["text"] = player
                            mass = self.minimax(place, self.AI)
                            place[j][pos]["text"] = " "
                            score = min(score, mass)

        return score

    def ai_moving(self, place):
        """choise a move"""
        move = None
        best_score = -500
        testplace = place
        freestep = self.freecolumn(testplace)
        for i in freestep:
            for j, value in enumerate(place):
                for pos, val in enumerate(value):
                    if val == i:
                        testplace[j][pos]["text"] = self.AI
                        mass = self.minimax(testplace, self.PLAYER)
                        testplace[j][pos]["text"] = " "
                        if mass > best_score:
                            best_score = mass
                            move = i

        return move


# ------------------------------------------------------------------
class Loging:
    """class Loging"""

    @staticmethod
    def log_win(name):
        """write logfile of winners"""
        logging.basicConfig(
            format="%(asctime)s - %(message)s", level=logging.INFO, filename="xolog.log"
        )
        logger = logging.getLogger()
        logger.info(f"{name} победил!")