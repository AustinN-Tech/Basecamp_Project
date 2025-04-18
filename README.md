# Basecamp App
Basecamp is an application that manages campsites and mountains in a database for hikers, campers, and anyone who likes the outdoors. It allows users to create campsite/mountain entries, customizing the name, rating, description, location on the map, and more.

## Motivation:
I originally got the idea for this application because I was using a website for finding campsites and it always loaded slowly and didn’t work at all without wifi. I wanted to create an application tailored to my needs and to have the ability to work offline. Additionally, I added mountains in order to track my mountain climbing progress.


## Tech Stack Used:
* Python – Primary programming language.
* PyQt6 – UI framework for making interactive desktop application
* SQLite3 – Lightweight database for offline storage
* Folium – Generates interactive maps for data visualization
* Pyinstaller – Converts the project into a standalone .exe file


## Feature List:
* Track your adventures – Store campsite and mountain details with names, ratings, descriptions, and more.
* Powerful Filtering Tools – Quickly find and display specific campsites or mountains
* Interactive Mapping – Visualize locations directly on a map for better trip planning
* Detailed Statistics –  Find summarized information of campsites/mountains

![Map Page](screenshots/map_page.png)
![Adding a Mountain](screenshots/mountain_create.png)
![Displaying Campsites](screenshots/campsite_display.png)
![Mountain Statistics](screenshots/mountain_stats.png)

## How Its Made:
1. Early Development: CSV File Storage
- First made using .CSV files for data storage and used a terminal-based menu
- Two CSV files were created: one for campsite storage and another for mountain storage.
- CRUD operations were implemented, using dynamic functions.
- Limitations: CSV files were not too scalable and couldn’t be used in applications.
2. Transition to SQLite3
- Second version used SQLite3 for data storage, keeping the terminal-based menu.
- Had to convert all of the functions to be compatible with SQLite3.
- SQLite3 was honestly simpler, as in CSV everything is manual.
- Used one file with two tables, one for campsites and another for mountains. Now both data types could be stored on one file.
3. Building the User Interface (UI) using PyQt6
- After creating the database with SQLite3, I needed a frontend UI for users to use. I decided to use PyQt6, as it is very compatible with Python.
- I used Qt designer to design and construct the majority of the interface, including multiple pages each with inputs of lineEdits, pushButtons, dropdowns, and more.
- I then converted the .UI file into .py, to be used in the code.
4. Connecting the Frontend & Backend
- Imported UI and database code into a single file called main_app.py.
- Connected all of the sidebar buttons to navigate to the appropriate pages.
- Connected logic to the input widgets to ensure compatibility with the database.
- Linked the sqlite3 database logic to the UI.
- **Challenges:** There were many times I had to adjust the UI or modify the functions in the database to get the application working appropriately
5. Adding Mapping Functionality using Folium
- I wanted to add mapping for more advanced camp planning and a visual application of the data.
- I used folium to create the map in a .html file. 
- Added coordinate columns to my database to display the markers of each item.
- Used QWebEngine to display the map in the application.
- **Challenges:** PyQt blocked local html files from loading (as it saw it as a security concern) so I created a local web server to work around this issue.
6. Packaging the Application:
- After finalizing the UI and database, I used Pyinstaller to package all of my code into a .exe file.
- This allows users to run the application as a standalone program without needing Python installed.


## Skills Learned:
1. Managing data using CSV files and later sqlite3.
2. Making functional UI applications with PyQt and Qt designer.
3. Connecting frontend and backend logic to put together an application that allows users to do CRUD operations to a sqlite3 database.
4. Crucial skills for debugging projects and applications.
5. Packaging code together into a .exe file using Pyinstaller.
6. Using github for the first time to log the progress of my project, create a README, and make a finalized release version of my application.


## Known Bugs:
1. Local Server Not Closing Properly (Map Won’t Display):
Sometimes the local server does not close properly when exiting the application. This causes future sessions from displaying the map.
Solution: Check and close the server manually
First check if the server is running using this command below in the command prompt:
```bash
netstat -ano | findstr :8001
```
This will show the list of connections the server is using. Locate the PID number on the far right. Do the following command but replace {CORRESPONDING PID NUMBER} with the actual PID number.
```bash
taskkill /PID {CORRESPONDING PID NUMBER} /F
```
This will close the server and fix the issue, allowing the map to display correctly.

2. Windows 10 UI Differences & Formatting Issue:
- On Windows 10, the UI has visual differences.
- The “Create Mountain” page has incorrect formatting but remains functional.


## Installation & Usage:
1. Clone the repository on github.
2. Install the dependencies using:
4. ```pip install -r requirements.txt```
5. Run the main_app.py file.

**Note:** I’ve excluded the compiled .exe from this repo because some antivirus tools like Windows Defender can mistakenly flag self-compiled executables. If you desire the .exe version, you can compile it yourself using PyInstaller.


## Icon Attribution:
This application uses icons from Flaticon
* https://www.flaticon.com/uicons
