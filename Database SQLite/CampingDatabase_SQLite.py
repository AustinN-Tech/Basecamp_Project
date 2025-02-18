import shutil
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox

conn = sqlite3.connect('ProjectDatabase.db')
c = conn.cursor()

## table for campsites:
# c.execute("""
#     CREATE TABLE campsite (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL COLLATE NOCASE,
#             state TEXT NOT NULL COLLATE NOCASE,
#             rating REAL NOT NULL CHECK (rating BETWEEN 0 AND 5),
#             description TEXT,
#             url TEXT
#             )
#         """)

# # table for mountains:
# c.execute("""
#     CREATE TABLE mountain (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL COLLATE NOCASE,
#             state TEXT NOT NULL COLLATE NOCASE,
#             rating REAL NOT NULL CHECK (rating BETWEEN 0 AND 5),
#             elevation REAL NOT NULL CHECK (elevation >= 0),
#             ascension REAL NOT NULL CHECK (ascension >= 0),
#             time_completed TEXT NOT NULL CHECK (time_completed LIKE '__:__'),
#             description TEXT,
#             date TEXT NOT NULL CHECK (date LIKE '____-__-__'),
#             url TEXT
#             )
#         """)

def error_popup(error_type, error): #popup for errors.
    print(f"{error_type}: {error}")
    pop = QMessageBox()
    pop.setWindowTitle("Error")
    pop.setText(f"{error_type}: {error}")
    pop.setIcon(QMessageBox.Icon.Critical)
    pop.exec()


def insert_campsite(name, state, rating, description, url):
    try:
        with conn: #commits the function in the with statement
            c.execute("""INSERT INTO campsite (name, state, rating, description, url) 
            VALUES (:name, :state, :rating, :description, :url)""",
                      {'name': name, 'state': state, 'rating': rating, 'description': description, 'url': url})
    #error handling
    except sqlite3.IntegrityError as e:
        error_type = "Integrity Error"
        error = f"{e}"
        error_popup(error_type, error)
    except sqlite3.Error as e:
        print(f'Database Error: {e}')

def insert_mountain(name, state, rating, elevation, ascension, time_completed, description, date, url):
    try:
        with conn:
            c.execute("""INSERT INTO mountain (name, state, rating, elevation, ascension, time_completed, description, date, url)
            VALUES (:name, :state, :rating, :elevation, :ascension, :time_completed, :description, :date, :url)""",
                      {'name': name, 'state': state, 'rating': rating, 'elevation': elevation, 'ascension': ascension, 'time_completed': time_completed, 'description': description,'date':date, 'url': url})
    #error handling
    except sqlite3.IntegrityError as e:
        error_type = "Integrity Error"
        error = f"{e}"
        error_popup(error_type, error)
    except sqlite3.Error as e:
        print(f'Database Error: {e}')




class Campsite:

    def __init__(self, name, state, rating, description, url):
        self.name = name
        self.state = state
        self.rating = rating
        self.description = description
        self.url = url


    def stats(self):
        return '{}:\nState - {}\nRating - {}\nDescription:\n  {}\nURL - {}'.format(self.name, self.state, self.rating, self.description, self.url)


class Mountain:

    def __init__(self, name, state, rating, elevation, ascension, time, description, date, url):
        self.name = name
        self.state = state
        self.rating = rating
        self.elevation = elevation
        self.ascension = ascension
        self.time = time
        self.description = description
        self.date = date
        self.url = url


    def stats(self):
        return '{}:\nState - {}\nRating - {}\nElevation - {}\nTotal elevation gain - {}\nTime taken - {}\nDescription: {}\nDate completed: {}\nURL - {}'.format(self.name, self.state, self.rating, self.elevation, self.ascension, self.time, self.description, self.date, self.url)

type_map= {
    'campsite': {
        'fieldnames':['name','state','rating','description','url'],
        'numeric_fields':['rating'],
        'format':"Name: {name}\nState: {state}\nRating: {rating}\nDescription: {description}\nURL: {url}\n"
    },
    'mountain': {
        'fieldnames':['name','state','rating','elevation','ascension','time','description','date','url'],
        'numeric_fields':['rating','elevation','ascension'],
        'format':"Name: {name}\nState: {state}\nRating: {rating}\nElevation: {elevation}\nTotal Feet Ascended: {ascension}\nTime to Complete: {time}\nDescription: {description}\nDate Completed: {date}\nURL: {url}\n"
    }
}

def campsite_format(name, state, rating, description, url):
    formatted_output = (
        f"Name: {name}\nState: {state}\nRating: {rating}\nDescription: {description}\nURL: {url}\n"
    )
    return formatted_output

def mountain_format(name, state, rating, elevation, ascension, time_completed, description, date, url):
    formatted_output = (
        f"Name: {name}\nState: {state}\nRating: {rating}\nElevation: {elevation}\nTotal Feet Ascended: {ascension}\nTime to complete: {time_completed}\nDescription: {description}\nDate Completed: {date}\nURL: {url}\n"
    )
    return formatted_output


US_States = {
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
}

def create_backup(): #creates backup of file. simple function, to be updated later
    #Creating backup file:
    filename = 'ProjectDatabase.db'
    backup_file = filename.replace('.db', '_backup.db')  # renames the backup file
    try:
        shutil.copy(filename, backup_file)  # creates backup file
    except FileNotFoundError:  # error handling
        print(f"Database Error: '{filename}' not found\n")
    except PermissionError:
        print("Database Error: permission denied\n")
    except Exception as e:
        print(f'Unexpected error: {e}')

def validate_type(type): #utility function for validating types
    if type not in type_map:
        print(f'Invalid type: {type}.')
        return False
    return True

#info = ['name, state, rating, description, URL']
#info_m = ['name, state, rating, elevation, ascension, time, description, date, URL']

def create_item(type, info): #inputs for mountain information

    if not validate_type(type): #checks the type
        return
    if not info:
        print("Missing Info.")
        return

    name = info[0].strip()
    if not name: #makes sure that the name isn't left blank
        error_type = "Invalid Input"
        error = f"{type.title()} name cannot be empty."
        error_popup(error_type, error)
        return

    global US_States #grabs the set of states
    state = info[1].strip().title()
    try:
        if not (state in US_States): #checks if the state matches the set
            raise ValueError
    except ValueError:
        error_type = "Invalid Input"
        error = "State cannot be empty."
        error_popup(error_type, error)
        return

    rating = info[2]
    try: #making sure correct values are implemented
        rating = float(rating)
        if not (1 <= rating <= 5):
            raise ValueError
    except ValueError:
        error_type = "Invalid Input"
        error = "Enter a value from 1 to 5."
        error_popup(error_type, error)
        return

    if type == 'mountain':
        elevation = info[3]
        try:
            elevation = float(elevation)
            if elevation < 0:
                raise ValueError
        except ValueError:
            error_type = "Invalid Input"
            error = "Elevation must be a number."
            error_popup(error_type, error)
            return

        ascension = info[4]
        try:
            ascension = float(ascension)
            if not ascension >= 0:
                raise ValueError
        except ValueError:
            error_type = "Invalid Input"
            error = "Ascension must be a number."
            error_popup(error_type, error)
            return

        time = info[5].strip()
        try:
            hours, minutes = map(int, time.split(':')) #parsing the data of date
            if not (0 <= hours < 24 and 0 <= minutes <= 59): #checking hours and minutes individually
                raise ValueError
        except ValueError:
            error_type = "Invalid Input"
            error = "Please enter a valid time."
            error_popup(error_type, error)
            return

    if type == 'campsite':
        description = info[3].strip()
    else:
        description = info[6].strip()
    if not description: #checks if description exists
        error_type = "Invalid Input"
        error = "Description cannot be empty."
        error_popup(error_type, error)
        return

    if type == 'mountain':
        date = info[7].strip()
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            error_type = "Invalid Input"
            error = "Please enter a valid date."
            error_popup(error_type, error)
            return

    if type == 'campsite':
        url = info[4].strip()
    else:
        url = info[8].strip()
    if not url or not url.startswith(('https://', 'http://')):#checks if url starts with valid address
        error_type = "Invalid Input"
        error = "URL must begin with 'https://' or 'http://'."
        error_popup(error_type, error)
        return

    create_backup()

    if type == 'mountain':
        # makes date and time into formatted string
        time_completed = f"{hours:02}:{minutes:02}"
        date = date.strftime('%Y-%m-%d')
        #adding mountain to database
        insert_mountain(name, state, rating, elevation, ascension, time_completed, description, date, url)

    elif type == 'campsite':
        #adding campsite to database
        insert_campsite(name, state, rating, description, url)

    print(f'{type.capitalize()}: {name} is saved\n')


def remove_item(name, type): #removes item from database
    if not validate_type(type): return #checking type

    name = name.strip()
    if not name:
        error_type = "Invalid Input"
        error = "Name cannot be empty."
        error_popup(error_type, error)
        return

    create_backup()

    try:
        with conn:
            c.execute(f"DELETE FROM {type} WHERE name=?", (name,))
            if c.rowcount > 0: #checks if any rows were affected (aka if it worked)
                print(f'{type.capitalize()}: {name} has been removed\n')
            else:
                print(f"No {type} has been found with name '{name}'\n")

    except sqlite3.Error as e:
        print(f"Database Error: {e}")


def item_search(name, type):
    if not validate_type(type): return

    name = name.strip()
    if not name:
        error_type = "Invalid Input"
        error = "Name cannot be empty."
        error_popup(error_type, error)
        return

    try:
        with conn:
            c.execute(f"SELECT * FROM {type} WHERE name=?", (name,))
            results = c.fetchall()
            if results:
                data = [] #creates list to store data

                for row in results:
                    if type == 'campsite':
                        data.append(campsite_format(row[1], row[2], row[3], row[4], row[5]))
                    else:
                        data.append(mountain_format(row[1], row[2], row[3], row[4], row[5], row[6], row[7],row[8], row[9]))

                return data #returns the data (as a list)

            else:
                print(f"No {type} has been found with name '{name}'\n")
                return [] #returns empty list if no results found

    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return []


def replace_info(name, type, column, new_value): #updates info from a column
    if not validate_type(type): return

    try:

        if column not in type_map[type]['fieldnames']:
            raise ValueError('Invalid attribute to replace by.\n')

        if not name: #checks for empty name
            error_type = "Invalid Input"
            error = "Name cannot be empty."
            error_popup(error_type, error)
            return

        if column == "time":
            column = "time_completed"

        new_value = new_value.strip() #gets input for new value

        if not new_value: #checks for empty new_value
            error_type = "Invalid Input"
            error = "New value cannot be empty."
            error_popup(error_type, error)
            return

        create_backup()

        with conn:
            c.execute(f"UPDATE {type} SET {column}=? WHERE name =?", (new_value, name))
            if c.rowcount > 0:
                print(f'{type.capitalize()} {name}: {column.capitalize()} has been updated to {new_value}\n')
            else:
                print(f"No {type} has been found with name: '{name}'.\n")

    except ValueError as e:
        print(e)
    except sqlite3.Error as e:
        print(f'Database Error: {e}\n')


def sort_and_filter(column, value, order, type):
    if not validate_type(type): return

    if column not in type_map[type]['fieldnames']:  # checking the column
        raise ValueError('Invalid attribute to sort by.\n')

    #converts the order value to SQL friendly
    if order == 'Ascending':
        order = "ASC"
    elif order == 'Descending':
        order = "DESC"

    if column == "time":
        column = "time_completed" #the column in the database is named time_completed

    try:
        data = [] #creates list to store data

        query = f"SELECT * FROM {type}" #starts with base query then depending on conditions (like value) more stuff is added to the query
        params = [] #for applying filter

        if value: #if value entered, filter
            query += f" WHERE LOWER({column})=?"
            if isinstance(value, str): #checks if value is a string
                params.append(value.strip().lower())
            else: #if value is a number
                params.append(value)
            #im checking this because if integer/floats are .strip() or .lower() then code breaks

        query += f" ORDER BY {column} {order}" #sorts

        with conn:
            c.execute(query, params)
            results = c.fetchall()

            if not results: #returns data even if no results
                return data

            for row in results:
                if type == 'campsite':
                    data.append(campsite_format(row[1], row[2], row[3], row[4], row[5]))
                else:
                    data.append(mountain_format(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

            return data

    except ValueError as e:
        print(e)
    except sqlite3.Error as e:
        print(f"Database Error: {e}\n")

def statistics(type):
    if not validate_type(type): return 0, 0, [] #returns empty values

    try:
       c.execute(f"SELECT COUNT(*) from {type}")
       total = c.fetchone()[0]

       c.execute(f"SELECT state, COUNT(*) AS count FROM {type} GROUP BY state")
       state_counts = c.fetchall()

       if type == 'mountain': #grabs averages of ascension and elevation if type is mountain
           c.execute(f"SELECT AVG(ascension) from {type}")
           average_ascension = c.fetchone()[0]
           c.execute(f"SELECT AVG(elevation) from {type}")
           average_elevation = c.fetchone()[0]
       else: #still needs values for ascension and elevation even if its campsite, so just leaving it 0
           average_ascension = 0
           average_elevation = 0

       state_total = len(state_counts) #works cause "state_counts" is a tuple

       print(f'Total {type}s found:', total,'\nTotal states:', (state_total))

       formatted_text = []
       for state, count in state_counts:
           formatted_text.append(f'{state}: {count}')

       return state_total, total, formatted_text, average_ascension, average_elevation


       #error handling: returns empty values if error
    except sqlite3.Error as e:
        print (f"Database Error: {e}")
        return 0, 0, []
    except Exception as e:
        print(f"Error: {e}")
        return 0, 0, []