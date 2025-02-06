from UI_design import Ui_MainWindow
import os
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication
import CampingDatabase_SQLite

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        base_dir = os.getcwd() #gets the directory the code is running in

        #setting the label icons' pixmaps
        self.label_6.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "search.png"))) #campsite search icon
        self.label_14.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "list.png"))) #campsite display icon
        self.label_12.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "pencil.png"))) #campsite modify icon


app = QApplication([])
window = Window()

window.show()
app.exec()