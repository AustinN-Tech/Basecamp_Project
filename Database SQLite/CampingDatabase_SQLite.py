import os
import sys
import shutil
import sqlite3
import folium
import logging
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)

if getattr(sys, 'frozen', False): #checks if running as exe
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(__file__)

db_path = os.path.join(base_dir, 'ProjectDatabase.db') #proper pathing for db

conn = sqlite3.connect(db_path)
c = conn.cursor()

## table for campsites:
# c.execute("""
#     CREATE TABLE campsite (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL COLLATE NOCASE,
#             state TEXT NOT NULL COLLATE NOCASE,
#             rating REAL NOT NULL CHECK (rating BETWEEN 0 AND 5),
#             description TEXT,
#             url TEXT,
#             longitude REAL,
#             latitude REAL
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
#             url TEXT,
#             longitude REAL,
#             latitude REAL
#             )
#         """)

def error_popup(error_type, error): #popup for errors.
    logger.error(f"{error_type}: {error}")
    pop = QMessageBox()
    pop.setWindowTitle("Error")
    pop.setText(f"{error_type}: {error}")
    pop.setIcon(QMessageBox.Icon.Critical)
    pop.exec()

def no_delete(type, name): #popup for if delete doesn't work
    logger.warning(f"No {type} has been found with name '{name}'")
    pop = QMessageBox()
    pop.setWindowTitle("Deletion Unsuccessful")
    pop.setText(f"No {type} has been found with name: '{name}'.")
    pop.setIcon(QMessageBox.Icon.Warning)
    pop.exec()

def no_modify(type, name):
    logger.warning(f"No {type} found with name: {name}.")
    pop = QMessageBox()
    pop.setWindowTitle("Edit Unsuccessful")
    pop.setText(f"No {type} found with name: {name}.")
    pop.setIcon(QMessageBox.Icon.Warning)
    pop.exec()



def insert_campsite(name, state, rating, description, url, longitude, latitude):
    try:
        with conn: #commits the function in the with statement
            c.execute("""INSERT INTO campsite (name, state, rating, description, url, longitude, latitude) 
            VALUES (:name, :state, :rating, :description, :url, :longitude, :latitude)""",
                      {'name': name, 'state': state, 'rating': rating, 'description': description, 'url': url, 'longitude': longitude, 'latitude': latitude})
    #error handling
    except sqlite3.IntegrityError as e:
        error_type = "Integrity Error"
        error = f"{e}"
        error_popup(error_type, error)
    except sqlite3.Error as e:
        logger.error(f'Database Error: {e}')

def insert_mountain(name, state, rating, elevation, ascension, time_completed, description, date, url, longitude, latitude):
    try:
        with conn:
            c.execute("""INSERT INTO mountain (name, state, rating, elevation, ascension, time_completed, description, date, url, longitude, latitude)
            VALUES (:name, :state, :rating, :elevation, :ascension, :time_completed, :description, :date, :url, :longitude, :latitude)""",
                      {'name': name, 'state': state, 'rating': rating, 'elevation': elevation, 'ascension': ascension, 'time_completed': time_completed, 'description': description,'date':date, 'url': url, 'longitude': longitude, 'latitude': latitude})
    #error handling
    except sqlite3.IntegrityError as e:
        error_type = "Integrity Error"
        error = f"{e}"
        error_popup(error_type, error)
    except sqlite3.Error as e:
        logger.error(f'Database Error: {e}')

type_map= {
    'campsite': {
        'fieldnames':['name','state','rating','description','url', 'longitude', 'latitude'],
        'numeric_fields':['rating'],
        'format':"Name: {name}\nState: {state}\nRating: {rating}\nDescription: {description}\nURL: {url}\n"
    },
    'mountain': {
        'fieldnames':['name','state','rating','elevation','ascension','time','description','date','url', 'longitude', 'latitude'],
        'numeric_fields':['rating','elevation','ascension'],
        'format':"Name: {name}\nState: {state}\nRating: {rating}\nElevation: {elevation}\nTotal Feet Ascended: {ascension}\nTime to Complete: {time}\nDescription: {description}\nDate Completed: {date}\nURL: {url}\n"
    }
}

def campsite_format(name, state, rating, description, url, longitude, latitude):
    formatted_output = (
        f"Name: {name}\nState: {state}\nRating: {rating}\nDescription: {description}\nURL: {url}\nCoordinates: {latitude},{longitude}\n"
    )
    return formatted_output

def mountain_format(name, state, rating, elevation, ascension, time_completed, description, date, url, longitude, latitude):
    formatted_output = (
        f"Name: {name}\nState: {state}\nRating: {rating}\nElevation: {elevation}\nTotal Feet Ascended: {ascension}\nTime to complete: {time_completed}\nDescription: {description}\nDate Completed: {date}\nURL: {url}\nCoordinates: {latitude},{longitude}\n"
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
        logger.info(f"Backup created: {backup_file}")
    except FileNotFoundError:  # error handling
        logger.error(f"Database Error: '{filename}' not found\n")
    except PermissionError:
        logger.error("Database Error: permission denied\n")
    except Exception as e:
        logger.error(f'Unexpected error: {e}')

def validate_type(type): #utility function for validating types
    if type not in type_map:
        logger.error(f'Invalid type: {type}.')
        return False
    return True

#info = ['name, state, rating, description, URL, longitude, latitude']
#info_m = ['name, state, rating, elevation, ascension, time, description, date, URL, longitude, latitude']

def create_item(type, info): #inputs for mountain information

    done = False

    if not validate_type(type): #checks the type
        return
    if not info:
        logger.error("Missing Info.")
        return done

    name = info[0].strip()
    if not name: #makes sure that the name isn't left blank
        error_type = "Invalid Input"
        error = f"{type.title()} name cannot be empty."
        error_popup(error_type, error)
        return done

    global US_States #grabs the set of states
    state = info[1].strip().title()
    try:
        if not (state in US_States): #checks if the state matches the set
            raise ValueError
    except ValueError:
        error_type = "Invalid Input"
        error = "State cannot be empty."
        error_popup(error_type, error)
        return done

    rating = info[2]
    try: #making sure correct values are implemented
        rating = float(rating)
        if not (1 <= rating <= 5):
            raise ValueError
    except ValueError:
        error_type = "Invalid Input"
        error = "Enter a value from 1 to 5."
        error_popup(error_type, error)
        return done

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
            return done

        ascension = info[4]
        try:
            ascension = float(ascension)
            if not ascension >= 0:
                raise ValueError
        except ValueError:
            error_type = "Invalid Input"
            error = "Ascension must be a number."
            error_popup(error_type, error)
            return done

        time = info[5].strip()
        try:
            hours, minutes = map(int, time.split(':')) #parsing the data of date
            if not (0 <= hours < 24 and 0 <= minutes <= 59): #checking hours and minutes individually
                raise ValueError
        except ValueError:
            error_type = "Invalid Input"
            error = "Please enter a valid time."
            error_popup(error_type, error)
            return done

    if type == 'campsite':
        description = info[3].strip()
    else:
        description = info[6].strip()
    if not description: #checks if description exists
        error_type = "Invalid Input"
        error = "Description cannot be empty."
        error_popup(error_type, error)
        return done

    if type == 'mountain':
        date = info[7].strip()
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            error_type = "Invalid Input"
            error = "Please enter a valid date."
            error_popup(error_type, error)
            return done

    if type == 'campsite':
        url = info[4].strip()
    else:
        url = info[8].strip()
    if not url or not url.startswith(('https://', 'http://')):#checks if url starts with valid address
        error_type = "Invalid Input"
        error = "URL must begin with 'https://' or 'http://'."
        error_popup(error_type, error)
        return done

    if type == 'campsite':
        longitude = info[5].strip()
    else:
        longitude = info[9].strip()
    try:
        longitude = float(longitude)
    except ValueError:
        error_type = "Invalid Input"
        error = "Longitude must be a number."
        error_popup(error_type, error)
        return done

    if type == 'campsite':
        latitude = info[6].strip()
    else:
        latitude = info[10].strip()
    try:
        latitude = float(latitude)
    except ValueError:
        error_type = "Invalid Input"
        error = "Latitude must be a number."
        error_popup(error_type, error)
        return done

    create_backup()

    if type == 'mountain':
        # makes date and time into formatted string
        time_completed = f"{hours:02}:{minutes:02}"
        date = date.strftime('%Y-%m-%d')
        #adding mountain to database
        insert_mountain(name, state, rating, elevation, ascension, time_completed, description, date, url, longitude, latitude)

    elif type == 'campsite':
        #adding campsite to database
        insert_campsite(name, state, rating, description, url, longitude, latitude)

    logger.info(f'{type.capitalize()}: {name} is saved\n')
    done = True
    return done


def remove_item(name, type): #removes item from database
    if not validate_type(type): return #checking type

    done = False

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
                done = True
                return done
            else:
                no_delete(type, name)
                return done

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
                        data.append(campsite_format(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                    else:
                        data.append(mountain_format(row[1], row[2], row[3], row[4], row[5], row[6], row[7],row[8], row[9], row[10], row[11]))

                return data #returns the data (as a list)

            else:
                logger.error(f"No {type} has been found with name '{name}'\n")
                return [] #returns empty list if no results found

    except sqlite3.Error as e:
        logger.error(f"Database Error: {e}")
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

        #input error handling:
        if not new_value: #checks for empty new_value
            error_type = "Invalid Input"
            error = "New value cannot be empty."
            error_popup(error_type, error)
            return

        if column == "state" and new_value not in US_States: #checks if state is valid
            error_type = "Invalid Input"
            error = "Enter a valid US state."
            error_popup(error_type, error)
            return

        if column in ["ascension", "elevation", "rating", "longitude", "latitude"]: #checks if all number columns are numbers.
            try:
                new_value = float(new_value)
            except ValueError:
                error_type = "Invalid Input"
                error = f"{column.title()} must be a number."
                error_popup(error_type, error)
                return

        if column == "url" and not new_value.startswith(("https://", "http://")):
            error_type = "Invalid Input"
            error = "URL must begin with 'https://' or 'http://'."
            error_popup(error_type, error)
            return

        if column == "time_completed":
            try:
                hours, minutes = map(int, new_value.split(':'))  # parsing the data of date
                if not (0 <= hours < 24 and 0 <= minutes <= 59):  # checking hours and minutes individually
                    raise ValueError
            except ValueError:
                error_type = "Invalid Input"
                error = "Please enter a valid time. Time must be in __:__ format."
                error_popup(error_type, error)
                return

        if column == "date":
            try:
                test = datetime.strptime(new_value, '%Y-%m-%d') #checks if new_value is in the right format
            except ValueError:
                error_type = "Invalid Input"
                error = "Please enter a valid date. Date must be in YYYY-MM-DD format."
                error_popup(error_type, error)
                return


        create_backup()

        with conn:
            c.execute(f"UPDATE {type} SET {column}=? WHERE name =?", (new_value, name))
            if c.rowcount > 0:
                logger.info(f'{type.capitalize()} {name}: {column.capitalize()} has been updated to {new_value}\n')
                return True
            else:
                no_modify(type, name)
                return False

    except ValueError as e:
        logger.error(e)
    except sqlite3.Error as e:
        logger.error(f'Database Error: {e}\n')


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
                    data.append(campsite_format(row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                else:
                    data.append(mountain_format(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))

            return data

    except ValueError as e:
        logger.error(e)
    except sqlite3.Error as e:
        logger.error(f"Database Error: {e}")

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

       logger.info(f'Total {type}s found: {total}, Total states: {state_total}')

       formatted_text = []
       for state, count in state_counts:
           formatted_text.append(f'{state}: {count}')

       return state_total, total, formatted_text, average_ascension, average_elevation


       #error handling: returns empty values if error
    except sqlite3.Error as e:
        logger.error(f"Database Error: {e}")
        return 0, 0, []
    except Exception as e:
        logger.error(f"Error: {e}")
        return 0, 0, []

def make_main_map(): #main map creation
    try:
        main_map = folium.Map(
            location = [39.8283,-98.5795],
            zoom_start = 5,
            tiles = 'https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png',
            attr = "Stadia.Outdoors"
        )

        c.execute("SELECT * from campsite")
        results = c.fetchall()

        if not results:
            logger.info("No campsites found in database.")
        for row in results:
            folium.Marker(
                location = [row[7], row[6]],
                tooltip = f"""
                <span style="font-size:14px; font-weight:bold;">{row[1]}</span><br>
                <b>Rating:</b> {row[3]} <br>
                <b>Description:</b><br>
                <p>{row[4]}</p>
                """, #has to be html formatted not python
                popup = f"<b>{row[1]}</b>",
                icon=folium.Icon(icon="campground", prefix="fa", color="green"),  #icon for campsites
            ).add_to(main_map)

        c.execute("SELECT * from mountain")
        results = c.fetchall()

        if not results:
            logger.info("No mountains found in database.")
        for row in results:
            folium.Marker(
                location = [row[11], row[10]],
                tooltip = f"""
                <span style="font-size:14px; font-weight:bold;">{row[1]}</span><br>
                <b>Rating:</b> {row[3]} <br>
                <b>Elevation:</b> {row[4]} <br>
                <b>Ascension:</b> {row[5]} <br>
                <b>Description:</b><br>
                <p>{row[7]}</p>
                """, #has to be html formatted not python
                popup = f"<b>{row[1]}</b>",
                icon=folium.Icon(icon="mountain", prefix="fa", color="gray")  #icon for mountains
            ).add_to(main_map)

        if getattr(sys, 'frozen', False): #checks if running as exe
            save_dir = os.path.dirname(sys.executable)
        else:
            save_dir = os.path.dirname(os.path.abspath(__file__))

        map_path = os.path.join(save_dir, 'main_map.html') #defines where to save the map at

        main_map.save(map_path)
        logger.info("Main map created.")
    except sqlite3.Error as e:
        logger.error(f"Database Error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")