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


        self.stackedWidget.currentChanged.connect(self.page_reset)  #resets the page if index changes


        #campsite search functionality:
        self.pushButton_11.clicked.connect(self.campsite_search_submit)
        self.lineEdit.returnPressed.connect(self.campsite_search_submit)
        #campsite search 2:
        self.pushButton_29.clicked.connect(self.campsite_search_submit)
        self.lineEdit_15.returnPressed.connect(self.campsite_search_submit) #when return is pressed, it searches


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

        self.pushButton_17.clicked.connect(self.reset_clicked_create)
        #slider:
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(5)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.valueChanged.connect(self.update_rating_label) #updates label next to slider

        #Slider map: (used for correlating labels)
        self.slider_label_map = {
            self.horizontalSlider: self.label_31
        }


        #campsite delete functionality:
        self.pushButton_18.clicked.connect(self.delete_clicked) #delete pressed
        self.lineEdit_3.returnPressed.connect(self.delete_clicked) #when enter is pressed


        #campsite modify functionality:
        self.pushButton_21.clicked.connect(self.modify_clicked) #submit clicked



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
    def campsite_search_submit(self): #search button functionality (for campsites)
        clicked_button = self.sender()

        #These if statements also account for "enter" being pressed in the lineEdits.
        if clicked_button == self.pushButton_11 or clicked_button == self.lineEdit: #if you search on campsite_search
            self.stackedWidget.setCurrentIndex(1) #sets index to search page w/ tableWidget to show campsite (campsite_search_2)
            campsite_name = self.lineEdit.text().strip() #grabs the campsite name from lineEdit
        elif clicked_button == self.pushButton_29 or clicked_button == self.lineEdit_15: #if you search on campsite_search_2 (results are already shown)
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

        #setting the header to bold:
        header_font = table.horizontalHeader().font()
        header_font.setBold(True)
        table.horizontalHeader().setFont(header_font)

        table.setHorizontalHeaderLabels(["Search Results"]) #sets header of table

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
        else: #TO DO
            type = 'mountain'
            pass


        data = CampingDatabase_SQLite.sort_and_filter(column, value, order, type)
        #DOESN'T DISPLAY "NO RESULTS" YET

        self.populate_table(data, self.tableWidget_2) #populates display tableWidget

    def reset_clicked_display(self): #reset for display
        # clearing inputs:
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.lineEdit_5.clear()
        # clearing tableWidget:
        self.tableWidget_2.clear()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(0)

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

    def update_rating_label(self, value): #updates label next to slider
        slider = self.sender()

        if slider in self.slider_label_map:
            label = self.slider_label_map[slider]
            label.setText(f"{value:.2f}") #changes it to 2 decimal places

    def reset_clicked_create(self): #this is for create reset
        #clears inputs
        self.lineEdit_2.clear()
        self.comboBox.setCurrentIndex(0)
        self.horizontalSlider.setValue(1)
        self.textEdit.clear()
        self.lineEdit_6.clear()


    #deleting item functions:
    def delete_clicked(self):
        clicked_button = self.sender()

        if clicked_button == self.pushButton_18 or clicked_button == self.lineEdit_3: #if campsite delete was clicked/enter pressed
            type = 'campsite'
            name = self.lineEdit_3.text().strip()
        else: #TO DO
            type = 'mountain'
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
        else: #TO DO
            type = 'mountain'
            pass

        CampingDatabase_SQLite.replace_info(name, type, column, new_value)


    #page reset functions:
    def page_reset(self, index):
        if index == 0: #campsite search 1
            self.lineEdit.clear()
        elif index == 1: #campsite search 2
            self.lineEdit_15.clear()
            #clearing tableWidget:
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
        elif index == 12: #campsite display
            self.reset_clicked_display()
        elif index == 3: #campsite create
            self.reset_clicked_create()
        elif index == 4: #campsite delete
            self.lineEdit_3.clear()
        elif index == 2: #campsite modify
            self.lineEdit_7.clear()
            self.comboBox.setCurrentIndex(0)
            self.lineEdit_4.clear()
        else:
            pass


#NOTE: filtering by rating might be broke check it out


app = QApplication([])
window = Window()

window.show()
app.exec()