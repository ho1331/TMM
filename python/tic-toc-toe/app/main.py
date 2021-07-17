"""game Tic Toc Toe (runing)"""
import gameproc

window = gameproc.Gameprocesse(440, 460)
window.frame.createplace()
window.menu()

window.draw()


if __name__ == "__main__":
    window.frame.show()
