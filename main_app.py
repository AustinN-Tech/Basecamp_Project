from PyQt6.QtCore import Qt

from UI_design import Ui_MainWindow
import os
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QLineEdit, QSizePolicy, QTableWidgetItem, QHeaderView
import CampingDatabase_SQLite



class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0) #sets the index to campsite search on startup

        base_dir = os.getcwd() #gets the directory the code is running in

        #setting the label icons' pixmaps
        self.label_3.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "menu-burger.png")))  #hamburger icon

        self.label_6.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "search.png"))) #campsite search icon
        self.label_14.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "list.png"))) #campsite display icon
        self.label_8.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "add.png")))  #campsite create icon
        self.label_10.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "cross.png")))  #campsite delete icon
        self.label_12.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "pencil.png"))) #campsite modify icon

        self.label_16.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "search.png")))  #mountain search icon
        self.label_18.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "list.png")))  #mountain display icon
        self.label_20.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "add.png")))  #mountain create icon
        self.label_22.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "cross.png")))  #mountain delete icon
        self.label_24.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "pencil.png")))  #mountain modify icon

        self.label_36.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "campfire.png")))  #campsite stats icon
        self.label_38.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "mountains.png")))  #mountain stats icon

        self.label_40.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "power.png")))  #exit icon

        #dictionary for button names
        self.buttons = {
            "campsite_search": self.pushButton,
            "campsite_display": self.pushButton_5,
            "campsite_create": self.pushButton_32,
            "campsite_delete": self.pushButton_3,
            "campsite_modify": self.pushButton_4,

            "mountain_search": self.pushButton_6,
            "mountain_display": self.pushButton_7,
            "mountain_create": self.pushButton_8,
            "mountain_delete": self.pushButton_9,
            "mountain_modify": self.pushButton_10,

            "campsite_statistics": self.pushButton_15,
            "mountain_statistics": self.pushButton_16,

            #"exit": self.pushButton_19
        }

        #closing application with exit button (pushButton_19)
        self.pushButton_19.clicked.connect(self.close)

        for btn in self.buttons.values():
            btn.clicked.connect(self.page_click)

        #campsite search functionality:
        self.pushButton_11.clicked.connect(self.campsite_search_submit)
        #campsite search 2:
        self.pushButton_29.clicked.connect(self.campsite_search_submit)

    def page_click(self):
        clicked_button = self.sender()

        #dictionary for page indexs
        page_map = {
            "campsite_search": 0,
            "campsite_display": 12,
            "campsite_create": 3,
            "campsite_delete": 4,
            "campsite_modify": 2,

            "mountain_search": 8,
            "mountain_display": 9,
            "mountain_create": 11,
            "mountain_delete": 7,
            "mountain_modify": 6,

            "campsite_statistics": 10,
            "mountain_statistics": 5,

            #campsite_search_2 = 1,
            #mountain_search_2 = 13,
            }

        for key, button in self.buttons.items(): #changing the page index according to the button clicked
            if button == clicked_button:
                self.stackedWidget.setCurrentIndex(page_map[key])
                break


    def campsite_search_submit(self): #search button functionality (for campsites)
        clicked_button = self.sender()

        if clicked_button == self.pushButton_11: #if you search on campsite_search
            self.stackedWidget.setCurrentIndex(1) #sets index to search page w/ tableWidget to show campsite (campsite_search_2)
            campsite_name = self.lineEdit.text().strip() #grabs the campsite name from lineEdit
        elif clicked_button == self.pushButton_29: #if you search on campsite_search_2 (results are already shown)
            campsite_name = self.lineEdit_15.text().strip()
        else:
            print("Button Error")
            return

        if not campsite_name: #checks for blank
            print("No campsite name entered")
            return

        data = CampingDatabase_SQLite.item_search(campsite_name, 'campsite') #you gotta be specific when referencing functions from imported code

        if not data: #checks if data exists
            print("No data found.")
            return

        self.populate_table(data, self.tableWidget)

    def populate_table(self, results, table): #to populate different tables

        if not results: #checking if results exist
            print("No results found")
            return

        table.setRowCount(len(results)) #sets row count relative to the data
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["Search Results"]) #sets header of table

        for row, result in enumerate(results): #goes through each result and displays it
            item = QTableWidgetItem(result)

            item.setTextAlignment(Qt.AlignmentFlag.AlignTop)

            table.setItem(row, 0, item)

        table.resizeRowsToContents()
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch) #resizes the contents of the table to the tableWidget





app = QApplication([])
window = Window()

window.show()
app.exec()