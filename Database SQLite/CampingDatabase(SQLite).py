import shutil
import sqlite3
from datetime import datetime

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

def insert_campsite(name, state, rating, description, url):
    try:
        with conn: #commits the function in the with statement
            c.execute("""INSERT INTO campsite (name, state, rating, description, url) 
            VALUES (:name, :state, :rating, :description, :url)""",
                      {'name': name, 'state': state, 'rating': rating, 'description': description, 'url': url})
    #error handling
    except sqlite3.IntegrityError as e:
        print(f'Integrity Error: {e}')
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
        print(f'Integrity Error: {e}')
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

def create_item(type): #inputs for mountain information

    if not validate_type(type): #checks the type
        return

    while True:
        name = input(f'Enter {type} name: ').strip()
        if name: #makes sure that the name isn't left blank
            break
        else:
            print(f'Please enter a valid {type} name.')
            continue

    while True:
        global US_States #grabs the set of states
        state = input(f'Enter {type} state: ').strip().title()
        #takes away extra spaces at the start and end of the string.
        # Then capitalizes the first letter of each word (aka title format).
        # This makes it match with the set of states more.
        try:
            if state in US_States: #checks if the state matches the set
                break
            else:
                raise ValueError
        except ValueError:
            print('Please enter a valid state')
            continue

    while True:
        rating = input(f'Enter {type} rating: ').strip()
        try: #making sure correct values are implemented
            rating = float(rating)
            if 0 <= rating <= 5:
                break
            else:
                raise ValueError
        except ValueError:
            print('Please a value from 0 to 5')
            continue

    if type == 'mountain':
        while True:
            elevation = input('Enter mountain elevation: ').strip()
            try:
                elevation = float(elevation)
                if elevation >= 0: break
                else:
                    raise ValueError
            except ValueError:
                print('Please enter a valid elevation')
                continue

        while True:
            ascension = input('Enter total feet ascended: ').strip()
            try:
                ascension = float(ascension)
                if ascension >= 0: break
                else:
                    raise ValueError
            except ValueError:
                print('Please enter a valid input')
                continue

        while True:
            time = input('Enter time to complete (HH:MM): ').strip()
            try:
                hours, minutes = map(int, time.split(':')) #parsing the data of date
                if 0 <= hours <= 24 and 0 <= minutes <= 59: #checking hours and minutes individually
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Please enter a valid time')
                continue

    while True:
        description = input(f'Enter {type} description: ').strip()
        if description:
            break
        else:
            print('Please enter a valid description')
            continue

    if type == 'mountain':
        while True:
            date = input('Enter date of completion (YYYY-MM-DD): ').strip()
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
                break
            except ValueError:
                print('Please enter a valid date')
                continue

    while True:
        url = input(f'Enter {type} URL: ').strip()
        try:
            if url.startswith(('https://', 'http://')): #checks if url starts with valid address
                break
            else:
                raise ValueError
        except ValueError:
            print('Please input a valid URL')
            continue

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

def all_items(type): #displays all items
    try:
        if not validate_type(type): return

        c.execute(f"SELECT * from {type}")
        rows = c.fetchall()

        for row in rows:
            if type == 'campsite':
                formatted_output = campsite_format(row[1],row[2],row[3],row[4],row[5])
            else:
                formatted_output = mountain_format(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            print(formatted_output)

    #error handling:
    except sqlite3.Error as e:
        print(f"Database Error: {e}")


def remove_item(name, type): #removes item from database
    if not validate_type(type): return #checking type

    name = name.strip()
    if not name:
        print('Name cannot be empty\n')
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
        print('Name cannot be empty\n')
        return

    try:
        with conn:
            c.execute(f"SELECT * FROM {type} WHERE name=?", (name,))
            results = c.fetchall()
            if results:
                for row in results:
                    if type == 'campsite':
                        print(campsite_format(row[1], row[2], row[3], row[4], row[5]))
                    else:
                        print(mountain_format(row[1], row[2], row[3], row[4], row[5], row[6], row[7],row[8], row[9]))
            else:
                print(f"No {type} has been found with name '{name}'\n")

    except sqlite3.Error as e:
        print(f"Database Error: {e}")


def sort_data(sort, type, order): #displays the data in order by sorted
    if not validate_type(type): return

    try:
        if sort not in type_map[type]['fieldnames']:
            raise ValueError(f'{sort.capitalize()} is not a valid sort type.\n')

        order = order.upper()
        if order not in ['ASC', 'DESC']:
            raise ValueError(f"Invalid order: '{order}' is not correct.\n")

        with conn:
            c.execute(f"SELECT * from {type} ORDER BY {sort} {order}")
            results = c.fetchall()
            if results:
                for row in results:
                    if type == 'campsite':
                        print(campsite_format(row[1], row[2], row[3], row[4], row[5]))
                    else:
                        print(mountain_format(row[1], row[2], row[3], row[4], row[5], row[6], row[7],row[8], row[9]))
            else:
                print(f"No {type}s found to display.\n")

    except ValueError as e:
        print(e)
    except sqlite3.Error as e:
        print(f"Database Error: {e}\n")



def replace_info(name, type, column): #updates info from a column
    if not validate_type(type): return

    try:

        if column not in type_map[type]['fieldnames']:
            raise ValueError('Invalid attribute to replace by.\n')

        new_value = input(f'Enter a new value for {column}: ').strip() #gets input for new value
        if not new_value:
            raise ValueError(f'New value for {column} cannot be empty.\n')

        confirm = input(f'Are you sure want to update {column} to {new_value}? (y/n): ').strip()
        if confirm != 'y':
            print('Update cancelled.\n')
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


def sort_specific(column, value, type, order): #only displays specific data
    if not validate_type(type): return

    value = value.strip().lower()

    if column not in type_map[type]['fieldnames']: #checking the column
        raise ValueError('Invalid attribute to sort by.\n')

    try:
        c.execute(f"SELECT * FROM {type} WHERE LOWER({column})=? ORDER BY {column} {order}", (value,)) #actually sorting
        results = c.fetchall()
        if results:
            for row in results:
                if type == 'campsite':
                    print(campsite_format(row[1], row[2], row[3], row[4], row[5]))
                else:
                    print(mountain_format(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],row[9]))
        else:
            print(f"No {type}s found to display.\n")

    except ValueError as e:
        print(e)
    except sqlite3.Error as e:
        print(f"Database Error: {e}\n")


def statistics(type):
    if not validate_type(type): return

    state_total = 0

    try:
       c.execute(f"SELECT * from {type}")
       total = c.fetchone()[0]

       c.execute(f"SELECT state, COUNT(*) AS count FROM {type} GROUP BY state")
       state_counts = c.fetchall()

       state_total = len(state_counts) #works cause "state_counts" is a tuple

       print(f'Total {type}s found:', total,'\nTotal states:', (state_total))
       print(f'\n{type.capitalize()}s by state:')

       for state, count in state_counts:
           print(f'{state}: {count}')

    # error handling:
    except sqlite3.Error as e:
        print (f"Database Error: {e}")


def menu(type): #menu for both mountains or campsites
    #inputs for functions are checked before and in the function itself for errors.
    #the "type" is hardcoded into the main_menu() and also checked in the functions
    if not validate_type(type):
        return

    while True:
        print(f'     {type.capitalize()} Menu\n\nEnter 1 for all {type}s.\nEnter 2 to search for a specific {type}.\nEnter 3 for sorting {type}s.\nEnter 4 to add a new {type}.\nEnter 5 to delete a {type}.\nEnter 6 to modify a {type}.\nEnter 7 for statistics.\nEnter 0 to exit to main menu.')
        x = input('Enter here: ')
        print('\n')

        if x == '1': #display all items
            all_items(type)
        elif x == '2': #search for a specific item
            name = input('Search: ')
            print('\n')
            item_search(name, type)
        elif x == '3': #sort items
            print(f' Sort Options:\n1. Sort all {type}s\n2. Sort specific {type}s\n')
            while True: #loop for checking sort options
                option = input('Enter here: ')
                if option in ['1','2']: break
                else:
                    print('Invalid option')
                    continue

            if option == '1':
                while True: #loop for checking if sort attribute is correct
                    sort = input('Enter option to sort by: ')
                    if sort not in type_map[type]['fieldnames']:
                        print('Invalid attribute to sort by.')
                        continue
                    else:
                        break

                while True: #order displayed
                    order = input('Enter sort order (asc/desc): ').strip().upper()

                    if order in ['ASC', 'DESC']:
                        break
                    else:
                        print('Invalid option.')
                        continue

                print('\n')
                sort_data(sort, type, order)

            elif option == '2':
                while True: #loop for checking if column is correct
                    column = input('Enter column to filter by: ')
                    if column not in type_map[type]['fieldnames']:
                        print('Invalid attribute to filter by.')
                        continue
                    else:
                        break

                value = input(f'Enter value for {column}: ')

                while True: #order displayed
                    order = input('Enter sort order (asc/desc): ').strip().upper()

                    if order in ['ASC','DESC']:
                        break
                    else:
                        print('Invalid option.')
                        continue

                print('\n')
                sort_specific(column, value, type, order)

        elif x == '4': #add new item
            create_item(type)
        elif x == '5': #delete old item
            name = input(f'Enter the name of {type} to delete: ')
            print('\n')
            remove_item(name, type)
        elif x == '6': #modify column on an item
            name = input('Search: ')
            while True: #checking the column input
                column = input('Enter column to modify: ')
                if column in type_map[type]['fieldnames']:
                    break
                else:
                    print('Invalid attribute to modify by.')
                    continue

            print('\n')
            replace_info(name, type, column)
        elif x == '7': #statistics of data
            statistics(type)
        elif x == '0': #ending code
            print(f'Exiting {type.capitalize()} Menu...')
            break

        else:
            print('Invalid input')
        print('\n')

def main_menu():
    while True:
        print('     Main Menu:\nEnter 1 for the campsite menu.\nEnter 2 for the mountain menu.\nEnter 0 to exit.')
        x = input('Enter here: ')
        if x == '1': #campsite menu
            print('\n')
            menu('campsite')
            print('\n')
        elif x == '2': #mountain menu
            print('\n')
            menu('mountain')
            print('\n')
        elif x == '0': #ending code
            print('\nExiting...')
            conn.close() #closes the connection to the database
            break
        else:
            print('Invalid input')

main_menu()