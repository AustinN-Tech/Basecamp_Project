import sys
import os
import http.server
import socketserver
import socket
import threading
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtCore import QTime, QDate, QUrl
from PyQt6.QtGui import QPixmap
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QLabel
from UI_design import Ui_MainWindow
import CampingDatabase_SQLite

#=== Server Code ===
"""
In order for the folium maps to be displayed in PyQt6, they must be sent from a local server.
This is because they are html files and PyQt6 views these are security risks.
Getting the file from a local server circumvents this issue.
"""
PORT = 8000 #any number above 1024 is good

server = None #sets the server variable

class HTTPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandler):
        super().__init__(server_address, RequestHandler)
        self.running = True #to detect if the server is running

    def stop(self): #stops the server
        self.running = False
        self.shutdown()
        self.server_close()


#starting a basic HTTP server:
def start_server():
    global server
    script_dir = os.path.dirname(os.path.abspath(__file__)) #gets the directory of the script
    os.chdir(script_dir)

    handler = http.server.SimpleHTTPRequestHandler
    server = HTTPServer(('', PORT), handler)
    print(f"Serving at http://localhost:{PORT}")

    #runs the server forever unless told otherwise
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass #makes so ctrl c does nothing when run code is run in terminal, extra error protection
    finally: #will always make sure the server closes accordingly
        server.server_close()

def port_use(port): #detects if port is in use (shouldn't be a problem locally but just in case)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result =  s.connect_ex(("localhost", port)) == 0
        s.close() #closes the socket
        return result

if not port_use(PORT): #makes sure port isn't in use
    #threading: makes it so the server and the PyQt application can run at the same time
    server_thread = threading.Thread(target=start_server, daemon=True) #'daemon = True' ensures the thread is closed once the program is
    server_thread.start()
else:
    print(f"Server is already running at http://localhost:{PORT}")

def close_server():
    if server and server.running: #makes sure server exists before continuing and its running
        print(f"Shutting down server...")
        server.stop()
        print(f"Server shut down.") #for debugging



#=== PyQt Code ===

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Camping Database") #sets title of the whole application window

        self.stackedWidget.setCurrentIndex(0) #sets the index to campsite search on startup

        base_dir = os.getcwd() #gets the directory the code is running in

        #setting the label icons' Pixmap
        self.label_3.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "menu-burger.png")))  #hamburger icon

        self.label_76.setPixmap(QPixmap(os.path.join(base_dir, "Icons", "map.png"))) #map icon

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

        #ok I updated to PyQt6 6.8 (previously worked on 6.4) and now in order for the buttons to be invisible, I have to change the background of them
        button_list = [self.pushButton_25, self.pushButton, self.pushButton_5, self.pushButton_32,
                       self.pushButton_3, self.pushButton_4, self.pushButton_6, self.pushButton_7,
                       self.pushButton_8, self.pushButton_9, self.pushButton_10, self.pushButton_15,
                       self.pushButton_16, self.pushButton_19, self.pushButton_2]
        for button in button_list:
            button.setStyleSheet("background: transparent; border: none;")


        #could make a function that takes the label and the name of the .png file to optimize the code a bit

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
            "map_page": self.pushButton_25,

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
        self.lineEdit_19.setPlaceholderText("Latitude")
        self.lineEdit_20.setPlaceholderText("Longitude")

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
        self.comboBox_2.addItems(["Name","State","Rating","Description", "URL", "Latitude", "Longitude"]) #adds proper columns


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
        self.lineEdit_21.setPlaceholderText("Latitude")
        self.lineEdit_22.setPlaceholderText("Longitude")

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
        self.comboBox_11.clear()
        self.comboBox_11.addItem("")  # adds blank entry
        self.comboBox_11.addItems(["Name", "State", "Rating", "Elevation", "Ascension", "Time Taken", "Description", "Date", "URL", "Latitude", "Longitude"])  # adds proper columns

        #statistics functionality:
        self.stackedWidget.currentChanged.connect(self.statistics) #checks the index if it's the right page and if so it runs the stats

        #map page functionality:
        self.stackedWidget.currentChanged.connect(self.load_main_map)



    def page_click(self):
        clicked_button = self.sender()

        #dictionary for page indexes
        page_map = {
            "campsite_search": 0,
            "campsite_display": 13,
            "campsite_create": 3,
            "campsite_delete": 4,
            "campsite_modify": 2,

            "mountain_search": 9,
            "mountain_display": 10,
            "mountain_create": 12,
            "mountain_delete": 8,
            "mountain_modify": 6,

            "campsite_statistics": 11,
            "mountain_statistics": 5,
            "map_page": 7,

            #campsite_search_2 = 1,
            #mountain_search_2 = 14,
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
            name = self.lineEdit.text().strip() #grabs the campsite name from lineEdit
            self.table = self.tableWidget

            data = CampingDatabase_SQLite.item_search(name, type)
            if data: #if data is empty, doesn't change index
                self.stackedWidget.setCurrentIndex(1) #sets index to search w/ tableWidget to show campsite (campsite_search_2)

        elif clicked_button == self.pushButton_29 or clicked_button == self.lineEdit_15: #if you search on campsite_search_2 (results are already shown)
            type = 'campsite'
            name = self.lineEdit_15.text().strip()
            self.table = self.tableWidget
        elif clicked_button == self.pushButton_22 or clicked_button == self.lineEdit_8: #if you search on mountain_search
            type = 'mountain'
            name = self.lineEdit_8.text().strip()
            self.table = self.tableWidget_3

            data = CampingDatabase_SQLite.item_search(name, type)
            if data:  # if data is empty, doesn't change index
                self.stackedWidget.setCurrentIndex(14)
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

        data = CampingDatabase_SQLite.item_search(name, type) #you have to be specific when referencing functions from imported code

        header_title = "Search Results"

        self.populate_table(data, self.table, header_title, type)
        if not data: self.no_results() #if data empty, runs no results popup


    def populate_table(self, results, table, header_title, type): #to populate different tables

        table.setColumnCount(1)

        if not results: #if there is no results
            print("No results found") #for extra logging

            #hides the indexes:
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setVisible(False)

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
        table.setHorizontalHeaderLabels([header_title]) #sets header of table

        #row size: changes depending on data type
        if type == "campsite":
            table.verticalHeader().setMaximumSectionSize(150)
        else:
            table.verticalHeader().setMaximumSectionSize(225)


        table.setRowCount(len(results))  # sets row count relative to the data
        for row, result in enumerate(results): #goes through each result and displays it

            #Result Display:
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

        header_title = "Search Results"

        self.populate_table(data, table, header_title, type) #populates display tableWidget
        if not data: self.no_results() #if data is empty, runs no results popup

    def no_results(self): #no results pop-up
        pop = QMessageBox(self)
        pop.setText("No results found")
        pop.setWindowTitle("No Results")
        pop.setIcon(QMessageBox.Icon.Information)
        pop.exec()

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
        longitude = self.lineEdit_20.text().strip()
        latitude = self.lineEdit_19.text().strip()

        info = [name, state, rating, description, URL, longitude, latitude] #puts all info into 1 variable

        done = CampingDatabase_SQLite.create_item('campsite',info)

        if done: #checks if it success
            self.notification("Campsite Created") #success notification

    def mountain_create_submit(self):
        #grabs the info from the page
        name = self.lineEdit_11.text().strip()
        state = self.comboBox_3.currentText().strip()
        rating = float(self.horizontalSlider_2.value())
        elevation = self.lineEdit_12.text().strip()
        ascension = self.lineEdit_13.text().strip()
        time = self.timeEdit.time().toString("HH:mm")
        description = self.textEdit_2.toPlainText()
        date = self.dateEdit.date().toString("yyyy-MM-dd")
        URL = self.lineEdit_10.text().strip()
        longitude = self.lineEdit_22.text().strip()
        latitude = self.lineEdit_21.text().strip()

        info = [name, state, rating, elevation, ascension, time, description, date, URL, longitude, latitude] #puts all info into 1 variable

        done = CampingDatabase_SQLite.create_item('mountain',info)

        if done:
            self.notification("Mountain Created") #success notification

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

        delete = self.delete_confirm(type, name)
        if delete: #if confirmed, delete happens
            done = CampingDatabase_SQLite.remove_item(name, type)
            if done: self.notification(f"{type.title()}: {name} deleted") #success notification


    def delete_confirm(self, type, name): #confirm delete pop-up
        #setting visuals:
        pop = QMessageBox(self)
        pop.setText(f"Are you sure you want to delete {type}: {name}?")
        pop.setWindowTitle("Confirm Delete")
        pop.setIcon(QMessageBox.Icon.Warning)

        pop.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel) #sets the buttons

        clicked_button = pop.exec() #checks which button was clicked

        if clicked_button == QMessageBox.StandardButton.Yes: #if yes selected, delete continues
            return True
        else: #if not then delete stops.
            return False

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
            if column == "time taken":
                column = "time" #replace_info function only takes time
            new_value = self.lineEdit_18.text().strip()

        modify = CampingDatabase_SQLite.replace_info(name, type, column, new_value)
        if modify: #to check if edit worked or not
            self.notification(f"{type.capitalize()} {name}: {column.capitalize()} has been updated to {new_value}")


    #stat functions:
    def statistics(self, index):
        if index == 11:
          type = 'campsite'
          table = self.tableWidget_5
        elif index == 5:
          type = 'mountain'
          table = self.tableWidget_6
        else:
            return

        state_total, total, formatted_text, average_ascension, average_elevation = CampingDatabase_SQLite.statistics(type)

        header_title = "Campsites by State"

        if type == 'campsite':
            #updating info:
            self.label_60.setText(str(total)) #label displaying camp total
            self.label_61.setText(str(state_total)) #label displaying total states
            self.populate_table(formatted_text, table, header_title, type) #adds data to table
        elif type == 'mountain':
            #updating info
            self.label_64.setText(str(total))
            self.label_68.setText(str(state_total))
            self.label_72.setText(str(average_ascension))
            self.label_70.setText(str(average_elevation))
            #need to add elevation average
            self.populate_table(formatted_text, table, header_title, type)


    #map page functions:
    def load_main_map(self, index):
        if index == 7:
            if not hasattr(self, "main_web_view"): #checks if main_web_view already exists
                self.main_web_view = QWebEngineView()
                self.gridLayout_17.addWidget(self.main_web_view)

            CampingDatabase_SQLite.make_main_map()
            file_url = QUrl("http://localhost:8000/main_map.html")
            self.main_web_view.load(file_url)


    def notification(self, message):
        label = QLabel(message)
        label.setStyleSheet("fontsize: 14; font-weight: bold;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.statusBar().clearMessage()
        self.statusBar().addWidget(label, 1)

        QTimer.singleShot(3000, lambda: self.statusBar().removeWidget(label))

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
        elif index == 13: #campsite display
            self.clear_display_campsite()
        elif index == 3: #campsite create
            self.clear_create_campsite()
        elif index == 4: #campsite delete
            self.lineEdit_3.clear()
        elif index == 2: #campsite modify
            self.lineEdit_7.clear()
            self.comboBox_2.setCurrentIndex(0)
            self.lineEdit_4.clear()
        elif index == 9: #mountain search
            self.lineEdit_8.clear()
        elif index == 14: #mountain search 2
            self.lineEdit_16.clear()
            #clearing tableWidget
            self.tableWidget_3.clear()
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.setColumnCount(0)
        elif index == 10: #mountain display
            self.clear_display_mountain()
        elif index == 12: #mountain create
            self.clear_create_mountain()
        elif index == 8: #mountain delete
            self.lineEdit_14.clear()
        elif index == 6: #mountain modify
            self.lineEdit_17.clear()
            self.comboBox_11.setCurrentIndex(0)
            self.lineEdit_18.clear()
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
        self.lineEdit_19.clear()
        self.lineEdit_20.clear()
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
        self.lineEdit_21.clear()
        self.lineEdit_22.clear()

app = QApplication(sys.argv) #"sys.argv" allows for proper initialization
app.setApplicationName("CampingDatabaseApp")
window = Window()

window.show()
app.aboutToQuit.connect(close_server) #closes the server before quiting
app.exec()