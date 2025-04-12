from menu import StartMenu
from PyQt5.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    menu = StartMenu()
    menu.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
