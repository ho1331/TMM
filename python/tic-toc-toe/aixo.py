"""class of game XO"""
import logging
import os
import sys

import texttable


class Menu:
    """class Menu"""

    def menu(self):
        """Show console menu"""
        print("-------------------------------Menu----------------------------------")
        menu = [
            "1.player & player |",
            "2.player & AI |",
            "3.Просмотреть лог побед |",
            "4.Очистить лог побед |",
            "5.Выход",
        ]

        for sub in menu:
            print(f"{sub}", end="  ")
        print()

    def readlog(self):
        """returne logfile"""
        try:
            with open("xolog.log", "r") as file:
                lines = file.readlines()
                for i in lines:
                    print(i)
        except FileNotFoundError:
            print("Not exist")
        self.menu()

    def dellog(self):
        """delete logfile"""
        if os.path.exists("xolog.log"):
            os.remove("xolog.log")
        else:
            print("Not found")
        self.menu()

    def exit(self):
        """exit game"""
        sys.exit()


class Gamer:
    """class Gamer"""

    def __init__(self) -> None:
        self.name1 = input("Введите имя 1-го игрока: ")
        self.name2 = input("Введите имя 2-го игрока: ")

    def log_win(self, name):
        """write logfile of winners"""
        logging.basicConfig(
            format="%(asctime)s - %(message)s", level=logging.INFO, filename="xolog.log"
        )
        logger = logging.getLogger()
        logger.info(f"{name} победил!")


class XO:
    """
    Class XO
    It's main class
    """

    def __init__(self) -> None:
        self.place = list(range(9))
        # create menu
        self.menu = Menu()
        self.AI = "X"
        self.PLAYER = "O"
        self.oponent = None

    def key_event(self):
        """check path of menu"""
        event = int(input("Select menu item: "))
        if event == 1:
            oponent = self.oponent_human
            self.oponent = oponent
            self.gamer = Gamer()
            self.game_processing(oponent)

        if event == 2:
            oponent = self.oponent_ai
            self.oponent = oponent
            self.gamer = Gamer()
            self.game_processing(oponent)
        elif event == 3:
            self.menu.readlog()
        elif event == 4:
            self.menu.dellog()
        elif event == 5:
            self.menu.exit()

    def draw(self):
        """draw gameplace"""
        table = texttable.Texttable()
        table.set_cols_align(["c", "c", "c", "c"])
        table.add_rows(
            [
                ["coordinates", "-1-", "-2-", "-3-"],
                ["a", self.place[0], self.place[1], self.place[2]],
                ["b", self.place[3], self.place[4], self.place[5]],
                ["c", self.place[6], self.place[7], self.place[8]],
            ]
        )
        # Display table
        print(table.draw())

    def take_input(self, playertype):
        """check input of players"""
        while True:
            answer = input(f"Поставьтe {playertype}:").lower()
            coordinates = {
                "a1": 0,
                "a2": 1,
                "a3": 2,
                "b1": 3,
                "b2": 4,
                "b3": 5,
                "c1": 6,
                "c2": 7,
                "c3": 8,
            }
            if answer.isdigit():
                if int(answer) in range(9):
                    if str(self.place[int(answer)]) not in "XO":
                        self.place[int(answer)] = playertype
                        break
                    else:
                        print("Занято")
                else:
                    print(
                        "Некорректный ввод. Введите число от 0 до 8 или координату (a1,b3...)"
                    )
            # if input is coordinate
            elif answer in coordinates:
                self.place[coordinates[answer]] = playertype
                break
            else:
                print(
                    "Некорректный ввод. Введите число от 0 до 8 или координату (a1,b3...)"
                )

    def check_win(self, place):
        """check is player win"""
        curplace = place
        # win combinations
        combinates = (
            (2, 4, 6),  # diagonal
            (0, 4, 8),  # diagonal
            (1, 4, 7),
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (2, 5, 8),
        )
        # if tuple of combinations are same - player will win
        for i in combinates:
            if curplace[i[0]] == curplace[i[1]] == curplace[i[2]]:
                return curplace[i[0]]
        return False

    # MINIMAX
    #################################
    def freecolumn(self, place):
        """return free spots"""
        # получает все пустые ячейки
        isfree = [i for i in place if i not in [self.AI, self.PLAYER]]
        return isfree

    def minimax(self, gameplace, player):
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
                place[i] = player
                mass = self.minimax(place, self.PLAYER)
                place[i] = i
                score = max(score, mass)

        else:
            score = 500
            for i in freestep:
                place[i] = player
                mass = self.minimax(place, self.AI)
                place[i] = i
                score = min(score, mass)

        return score

    def ai_moving(self, place):
        move = None
        best_score = -500
        testplace = place
        freestep = self.freecolumn(testplace)
        for i in freestep:
            testplace[i] = self.AI
            mass = self.minimax(testplace, self.PLAYER)
            testplace[i] = i
            if mass > best_score:
                best_score = mass
                move = i

        return move

    #####################################

    def newgame(self):
        """start game"""
        if self.place != list(range(9)):
            choise = input("Сыграть снова? (д/н)  ").lower()
            if choise in ["y", "д"]:
                self.place = list(range(9))
                self.game_processing(self.oponent)
            else:
                self.place = list(range(9))
                self.menu.menu()
        else:
            self.key_event()

    def oponent_ai(self):
        """initiated oponent == ai"""
        move = self.ai_moving(self.place)
        self.place[move] = self.AI

    def oponent_human(self):
        """initiated oponent == humen"""
        self.take_input("X")

    def game_processing(self, oponent):
        """
        processing of game
        1. show gameplace
        2. check whose typing (with take_input func)
        3. check is player win (with check_win func)
        4. write logfile of winners (with log_win func)
        """
        # number of moves
        counter = 0
        while True:
            self.draw()
            if counter % 2 == 0:
                print(f"{self.gamer.name2} ходит")
                ####################
                oponent()
                ####################
            else:
                print(f"{self.gamer.name1} ходит")
                self.take_input(self.PLAYER)  # X =playertype
            counter += 1

            if counter > 4:
                winner = self.check_win(self.place)
                if winner:
                    playerwin = {
                        winner == self.AI: self.gamer.name2,
                        winner == self.PLAYER: self.gamer.name1,
                    }[True]
                    print(f"{playerwin} победил!!!!!")
                    self.gamer.log_win(playerwin)
                    self.draw()
                    break
            if counter == 9:
                print("Ничья!")
                self.draw()
                break


# ------------------GAME------------------------------------
def main():
    """running all processing of module"""
    game = XO()
    game.menu.menu()
    while True:
        game.newgame()


if __name__ == "__main__":
    main()
