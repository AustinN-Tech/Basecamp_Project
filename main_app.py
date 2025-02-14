from PyQt6.QtCore import Qt
from UI_design import Ui_MainWindow
import os
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTime, QDate
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QLineEdit, QSizePolicy, QTableWidgetItem, QHeaderView, QTableWidget
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


        self.stackedWidget.currentChanged.connect(self.page_reset)  #resets the page if index changes


        #campsite search functionality:
        self.pushButton_11.clicked.connect(self.search_submit)
        self.lineEdit.returnPressed.connect(self.search_submit)
        #campsite search 2:
        self.pushButton_29.clicked.connect(self.search_submit)
        self.lineEdit_15.returnPressed.connect(self.search_submit) #when return is pressed, it searches


        #campsite display functionality:
        self.comboBox_5.clear()
        self.comboBox_5.addItems(["Name", "State", "Rating"]) #adding items to column comboBox

        self.pushButton_13.clicked.connect(self.display_data) #if apply button clicked
        self.pushButton_20.clicked.connect(self.reset_clicked_display) #resets page if reset clicked


        #campsite create functionality:
        self.pushButton_14.clicked.connect(self.campsite_create_submit) #submit button

        #comboBox:
        self.comboBox.clear() #clears previous entries
        self.comboBox.addItem("") #adds blank entry
        self.comboBox.addItems(sorted(CampingDatabase_SQLite.US_States)) #adding states to comboBox

        self.pushButton_17.clicked.connect(self.reset_clicked_create) #reset button
        #slider:
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(5)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.valueChanged.connect(self.update_rating_label) #updates label next to slider

        #Slider map: (used for correlating labels)
        self.slider_label_map = {
            self.horizontalSlider: self.label_31,
            self.horizontalSlider_2: self.label_52
        }


        #campsite delete functionality:
        self.pushButton_18.clicked.connect(self.delete_clicked) #delete pressed
        self.lineEdit_3.returnPressed.connect(self.delete_clicked) #when enter is pressed


        #campsite modify functionality:
        self.pushButton_21.clicked.connect(self.modify_clicked) #submit clicked
        #column comboBox:
        self.comboBox_2.clear()
        self.comboBox_2.addItem("") #adds blank entry
        self.comboBox_2.addItems(CampingDatabase_SQLite.type_map['campsite']['fieldnames']) #adds proper columns

        #Need to add a fresh dictionary because 'fieldnames' is lowercased


        #mountain search functionality:
        self.pushButton_22.clicked.connect(self.search_submit) #search clicked
        self.lineEdit_8.returnPressed.connect(self.search_submit) #return pressed
        #mountain search 2:
        self.pushButton_31.clicked.connect(self.search_submit)
        self.lineEdit_16.returnPressed.connect(self.search_submit)


        #mountain display functionality:
        self.comboBox_6.clear()
        self.comboBox_6.addItems(["Name", "State", "Rating", "Elevation", "Ascension", "Time Taken", "Date"])  # adding items to column comboBox

        self.pushButton_24.clicked.connect(self.display_data)  # if apply button clicked
        self.pushButton_23.clicked.connect(self.reset_clicked_display)  #if reset clicked


        #mountain create functionality:
        self.pushButton_27.clicked.connect(self.mountain_create_submit) #submit button
        self.pushButton_26.clicked.connect(self.reset_clicked_create) #reset button

        #comboBox:
        self.comboBox_3.clear() #clears previous entries
        self.comboBox_3.addItem("") #adds blank space
        self.comboBox_3.addItems(sorted(CampingDatabase_SQLite.US_States)) #adds states to comboBox

        #slider:
        self.horizontalSlider_2.setMinimum(1)
        self.horizontalSlider_2.setMaximum(5)
        self.horizontalSlider_2.setTickInterval(1)
        self.horizontalSlider_2.setSingleStep(1)
        self.horizontalSlider_2.valueChanged.connect(self.update_rating_label)  # updates label next to slider


        #mountain delete functionality:
        self.pushButton_28.clicked.connect(self.delete_clicked) #if delete clicked
        self.lineEdit_14.returnPressed.connect(self.delete_clicked) #if return pressed


        #mountain modify functionality:
        self.pushButton_30.clicked.connect(self.modify_clicked) #submit button




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


    #displaying info functions:
    def search_submit(self): #search button functionality
        clicked_button = self.sender()

        #These if statements also account for "enter" being pressed in the lineEdits.
        if clicked_button == self.pushButton_11 or clicked_button == self.lineEdit: #if you search on campsite_search
            type = 'campsite'
            self.stackedWidget.setCurrentIndex(1) #sets index to search page w/ tableWidget to show campsite (campsite_search_2)
            name = self.lineEdit.text().strip() #grabs the campsite name from lineEdit
            self.table = self.tableWidget
        elif clicked_button == self.pushButton_29 or clicked_button == self.lineEdit_15: #if you search on campsite_search_2 (results are already shown)
            type = 'campsite'
            name = self.lineEdit_15.text().strip()
            self.table = self.tableWidget
        elif clicked_button == self.pushButton_22 or clicked_button == self.lineEdit_8: #if you search on mountain_search
            type = 'mountain'
            self.stackedWidget.setCurrentIndex(13)
            name = self.lineEdit_8.text().strip()
            self.table = self.tableWidget_3
        elif clicked_button == self.pushButton_31 or clicked_button == self.lineEdit_16:
            type = 'mountain'
            name = self.lineEdit_16.text().strip()
            self.table = self.tableWidget_3
        else:
            print("Button Error")
            return

        if not name: #checks for blank
            print(f"No {type} name entered")
            return

        data = CampingDatabase_SQLite.item_search(name, type) #you gotta be specific when referencing functions from imported code

        self.populate_table(data, self.table)


    def populate_table(self, results, table): #to populate different tables

        table.setColumnCount(1)

        if not results: #if there is no results
            #the whole "No Results" isn't great right now. will require reworking.
            print("No results found") #for extra logging

            table.setRowCount(1)
            #hides the indexes:
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setVisible(False)

            #creates "No Results" item and sets it to bold
            item = QTableWidgetItem("No Results")
            font = item.font()
            font.setBold(True)
            item.setFont(font)

            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable) #makes table not editable
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) #centers
            table.setItem(0, 0, item)


            table.viewport().update() #updates the UI
            table.setRowHeight(0, int(table.viewport().height())) #sets height of "No Results" to table

            #Resizes table:
            table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
            return

        #making sure headers are visible
        table.verticalHeader().setVisible(True)
        table.horizontalHeader().setVisible(True)

        #setting the header to bold:
        header_font = table.horizontalHeader().font()
        header_font.setBold(True)
        table.horizontalHeader().setFont(header_font)
        table.setHorizontalHeaderLabels(["Search Results"]) #sets header of table

        table.setRowCount(len(results))  # sets row count relative to the data
        for row, result in enumerate(results): #goes through each result and displays it
            item = QTableWidgetItem(result)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable) #makes it so it isn't editable

            item.setTextAlignment(Qt.AlignmentFlag.AlignTop) #aligns the results to the top
            table.setWordWrap(True)

            table.setItem(row, 0, item)

        table.resizeRowsToContents()
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch) #resizes the contents of the table to the tableWidget

    def display_data(self):
        clicked_button = self.sender()

        if clicked_button == self.pushButton_13: #so if its campsite display:
            type = 'campsite'
            column = self.comboBox_5.currentText().strip().lower()
            order = self.comboBox_4.currentText().strip()
            value = self.lineEdit_5.text().strip()
            table = self.tableWidget_2
        else: #if its mountain display
            type = 'mountain'

            column = self.comboBox_6.currentText().strip().lower()
            if column == "time taken":
                column = "time" #sort_and_filter only takes "time"

            order = self.comboBox_7.currentText().strip()
            value = self.lineEdit_6.text().strip()
            table = self.tableWidget_4


        data = CampingDatabase_SQLite.sort_and_filter(column, value, order, type)
        #DOESN'T DISPLAY "NO RESULTS" YET

        self.populate_table(data, table) #populates display tableWidget

    def reset_clicked_display(self): #reset for display
        clicked_button = self.sender()

        if clicked_button == self.pushButton_20:
            self.clear_display_campsite()
        elif clicked_button == self.pushButton_23:
            self.clear_display_mountain()

    #creating items functions:
    def campsite_create_submit(self): #when submit is clicked on the create campsite page
        #grabs the info from the page:
        name = self.lineEdit_2.text().strip()
        state = self.comboBox.currentText().strip()
        rating = float(self.horizontalSlider.value())
        description = self.textEdit.toPlainText()
        URL = self.lineEdit_6.text().strip()

        info = [name, state, rating, description, URL] #puts all info into 1 variable

        CampingDatabase_SQLite.create_item('campsite',info)

    def mountain_create_submit(self):
        #grabs the info from the page
        name = self.lineEdit_11.text().strip()
        state = self.comboBox_3.currentText().strip()
        rating = float(self.horizontalSlider_2.value())
        try:
            elevation = float(self.lineEdit_12.text().strip())
        except ValueError: #makes sure elevation is a number
            print("Invalid Input: Elevation must be a number")
            return
        try: #makes sure ascension is a number
            ascension = float(self.lineEdit_13.text().strip())
        except ValueError:
            print("Invalid Input: Ascension must be a number")
            return
        time = self.timeEdit.time().toString("HH:mm")
        description = self.textEdit_2.toPlainText()
        date = self.dateEdit.date().toString("yyyy-MM-dd")
        URL = self.lineEdit_10.text().strip()

        info = [name, state, rating, elevation, ascension, time, description, date, URL] #puts all info into 1 variable

        CampingDatabase_SQLite.create_item('mountain',info)

    def update_rating_label(self, value): #updates label next to slider
        slider = self.sender()

        if slider in self.slider_label_map:
            label = self.slider_label_map[slider]
            label.setText(f"{value:.2f}") #changes it to 2 decimal places

    def reset_clicked_create(self): #this is for create reset
        clicked_button = self.sender()

        #clears inputs
        if clicked_button == self.pushButton_17: #if on campsite create
            self.clear_create_campsite()
        elif clicked_button == self.pushButton_26: #if on mountain create
            self.clear_create_mountain()
        else:
            pass


    #deleting item functions:
    def delete_clicked(self):
        clicked_button = self.sender()

        if clicked_button == self.pushButton_18 or clicked_button == self.lineEdit_3: #if campsite delete was clicked/enter pressed
            type = 'campsite'
            name = self.lineEdit_3.text().strip()
        else: #if mountain delete was clicked/enter pressed
            type = 'mountain'
            name = self.lineEdit_14.text().strip()
            pass

        CampingDatabase_SQLite.remove_item(name, type)


    #modifying item functions:
    def modify_clicked(self):
        clicked_button = self.sender()

        if clicked_button == self.pushButton_21: #if campsite modify was clicked
            type = 'campsite'
            name = self.lineEdit_7.text().strip()
            column = self.comboBox_2.currentText().strip().lower()
            new_value = self.lineEdit_4.text().strip()
        else: #if mountain modify was clicked
            type = 'mountain'
            name = self.lineEdit_17.text().strip()
            column = self.comboBox_11.currentText().strip().lower()
            new_value = self.lineEdit_18.text().strip()

        CampingDatabase_SQLite.replace_info(name, type, column, new_value)


    #page reset function:
    def page_reset(self, index):
        #some of these have functions cause the code is used multiple times others don't
        if index == 0: #campsite search 1
            self.lineEdit.clear()
        elif index == 1: #campsite search 2
            self.lineEdit_15.clear()
            #clearing tableWidget:
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
        elif index == 12: #campsite display
            self.clear_display_campsite()
        elif index == 3: #campsite create
            self.clear_create_campsite()
        elif index == 4: #campsite delete
            self.lineEdit_3.clear()
        elif index == 2: #campsite modify
            self.lineEdit_7.clear()
            self.comboBox_2.setCurrentIndex(0)
            self.lineEdit_4.clear()
        elif index == 8: #mountain search
            self.lineEdit_8.clear()
        elif index == 13: #mountain search 2
            self.lineEdit_16.clear()
            #clearing tableWidget
            self.tableWidget_3.clear()
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.setColumnCount(0)
        elif index == 9: #mountain display
            self.clear_display_mountain()
        elif index == 11: #mountain create
            self.clear_create_mountain()
        else:
            pass

    #clearing functions:
    def clear_display_campsite(self):
        # clearing inputs:
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.lineEdit_5.clear()
        # clearing tableWidget:
        self.tableWidget_2.clear()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(0)
    def clear_display_mountain(self):
        # clearing inputs:
        self.comboBox_6.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        self.lineEdit_9.clear()
        # clearing tableWidget:
        self.tableWidget_4.clear()
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.setColumnCount(0)
    def clear_create_campsite(self):
        self.lineEdit_2.clear()
        self.comboBox.setCurrentIndex(0)
        self.horizontalSlider.setValue(1)
        self.textEdit.clear()
        self.lineEdit_6.clear()
    def clear_create_mountain(self):
        self.lineEdit_11.clear()
        self.comboBox_3.setCurrentIndex(0)
        self.horizontalSlider_2.setValue(1)
        self.lineEdit_12.clear()
        self.lineEdit_13.clear()
        self.timeEdit.setTime(QTime(0, 0))  # resets time to 00:00
        self.textEdit_2.clear()
        self.dateEdit.setDate(QDate(2000, 1, 1))  # resets to default
        self.lineEdit_10.clear()


#NOTE: filtering by rating might be broke check it out


app = QApplication([])
window = Window()

window.show()
app.exec()