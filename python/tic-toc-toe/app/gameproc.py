"""class contains games ligics"""
import tkinter as tk
from tkinter import messagebox

import loggings
import menus
import minimax
import windows


class Gameprocesse:
    """
    class Gameprocesse

    methods:
        menu,draw,update_status,event,ai_turn,write_log,play_with_ai,play_with_human
    """

    def __init__(self, height, width) -> None:
        self.place = []
        self.counter = 0
        self.log = loggings.Loging()
        self.process = minimax.Minimax()
        self.frame = windows.Window(height, width)
        self.withAI = False
        self.start = False
        self.name1 = "Игрок_1"
        self.name2 = "Игрок_2"

    def menu(self):
        """create windows menu"""

        menu = tk.Menu(self.frame.window)
        submenu = tk.Menu(menu)
        submenu.add_command(label="На двоих", command=lambda: self.play_with_human())
        submenu.add_command(label="Против AI", command=lambda: self.play_with_ai())
        menu.add_cascade(label="Начать", menu=submenu)

        self.frame.window.config(menu=menu)
        menu.add_command(
            label="Просмотреть лог побед", command=lambda: menus.Menu.readlog()
        )
        menu.add_command(
            label="Очистить лог побед", command=lambda: menus.Menu.dellog()
        )
        menu.add_command(label="Выход", command=lambda: menus.Menu.exit())

    def draw(self):
        """create gameplace"""
        for row in range(3):
            line = []
            for col in range(3):
                button = tk.Button(
                    self.frame.window,
                    text=" ",
                    width=4,
                    height=2,
                    bd=5,
                    font=("Verdana", 30, "bold"),
                    background="lavender",
                    activebackground="yellow",
                    command=lambda row=row, col=col: self.event(self.place, row, col),
                )
                button.grid(row=row, column=col, sticky="nsew")
                line.append(button)
            self.place.append(line)

    def show_winner(self, place, counter, status):
        """show winner in mb and refresh status"""
        if counter > 4:
            if self.process.check_win(place):
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

    def update_status(self):
        """choose next stepplayer"""
        if self.counter % 2 == 0:
            self.frame.text_place.set(f"Ходит {self.name1}")
        else:
            self.frame.text_place.set(f"Ходит {self.name2}")

    def event(self, place, row, col):
        """check processe on gameplace"""
        if self.start is True:
            if self.withAI is False:
                if self.show_winner(place, self.counter, self.start):
                    return
                if self.counter % 2 == 0:
                    if place[row][col]["text"] == " ":
                        place[row][col]["text"] = "X"
                    self.counter += 1
                    if self.show_winner(place, self.counter, self.start):
                        self.write_log()
                        return
                    self.update_status()
                else:
                    if self.counter % 2 != 0:
                        if place[row][col]["text"] == " ":
                            place[row][col]["text"] = "O"
                        self.counter += 1
                        if self.show_winner(place, self.counter, self.start):
                            self.write_log()
                            return
                        self.update_status()

            else:
                if self.show_winner(place, self.counter, self.start):
                    return
                if self.counter % 2 != 0:
                    if place[row][col]["text"] == " ":
                        place[row][col]["text"] = "O"
                    self.counter += 1
                    if self.show_winner(place, self.counter, self.start):
                        self.write_log()
                        return
                    self.update_status()
                    self.frame.window.update()
                    if self.withAI is True:
                        self.ai_turn()
                        self.update_status()

    def ai_turn(self):
        """return ai move"""
        move = self.process.ai_moving(self.place)
        for i, value in enumerate(self.place):
            for j, val in enumerate(value):
                if val == move:
                    self.place[i][j]["text"] = "X"
        self.counter += 1
        if self.show_winner(self.place, self.counter, self.start):
            self.write_log()
        self.update_status()

    def write_log(self):
        """write log with winner name"""
        winner = self.process.check_win(self.place)
        if winner == "X":
            return self.log.log_win(self.name1)
        elif winner == "O":
            return self.log.log_win(self.name2)
        else:
            return self.log.log_win("Ничья")

    def play_with_ai(self):
        """cgoose game with ai"""
        self.start = True
        self.withAI = True
        self.new_game(self.place)
        self.counter = 0
        self.update_status()
        self.frame.window.update()
        self.ai_turn()

    def play_with_human(self):
        """cgoose game for two players"""
        self.start = True
        self.withAI = False
        self.process.new_game(self.place)
        self.counter = 0
        self.update_status()

    @staticmethod
    def new_game(place):
        """update self.place (work place)"""
        for i, value in enumerate(place):
            for j, val in enumerate(value):
                place[i][j]["text"] = " "
