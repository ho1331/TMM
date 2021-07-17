"""minimax algoritm"""


class Minimax:
    """class Minimax"""

    def __init__(self) -> None:
        self.place = None
        self.AI = "X"
        self.PLAYER = "O"
        self.oponent = None

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

    # MINIMAX
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
            return -20

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
