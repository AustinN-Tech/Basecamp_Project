import csv
import shutil
from datetime import datetime


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

US_States = {
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
}


def save_to_csv(filename, fieldnames, data):

    backup_file = filename.replace('.csv','_backup.csv') #renames the backup file
    try:
        shutil.copy(filename, backup_file) #creates backup file
    except FileNotFoundError: #silent error handling
        pass
    except PermissionError:
        pass

    with open(filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0: #checks if file has header
            writer.writeheader()
        writer.writerow(data)


def write_csv(filename, fieldnames, rows): #utility function for writing
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # makes sure to write the header row
        writer.writerows(rows)  # writes the information saved in the list


def to_dict(data): #turns data into dictionaries
    return {key: value for key, value in vars(data).items()}

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
                hours, minutes = map(int, time.split(':'))
                if 0 <= hours <= 24 and 0 <= minutes <= 59:
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

    #makes date and time into formatted string
    if type == 'mountain':
        time = f"{hours:02}:{minutes:02}"
        date = date.strftime('%Y-%m-%d')

        #creates new mountain
        data = Mountain(name, state, rating, elevation, ascension, time, description, date, url)
        data = to_dict(data)

        fieldnames = type_map[type]['fieldnames']

        #adds it to the file
        filename = "mountains.csv"

    elif type == 'campsite':
        new_camp = Campsite(name, state, rating, description, url)
        data = to_dict(new_camp)

        fieldnames = type_map[type]['fieldnames']

        # adds it to the file
        filename = "campsites.csv"

    save_to_csv(filename, fieldnames, data)
    print(f'{type.capitalize()}: {name} saved to {filename}\n')


def all_items(filename, type): #displays all items in a csv file. Can be campsites or mountains.
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)

            if not validate_type(type):  # checks the type
                return

            if reader.fieldnames != type_map[type]['fieldnames']: raise ValueError  #checking CSV header structure

            for row in reader:
                if row: #checks if row is empty, if it exists it prints,
                    print(type_map[type]['format'].format(**row)) #retrieves the values from the type_map and formats them accordingly

    #error handling:
    except FileNotFoundError:
        print('File not found')
        return
    except ValueError:
        print('CSV headers do not match excepted format')
        return
    except PermissionError:
        print('Permission denied')
        return

def remove_item_from_file(filename, name, type):
    rows = [] #saves the information needed
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)

            if not validate_type(type):  # checks the type
                return

            if reader.fieldnames != type_map[type]['fieldnames']: raise ValueError

            for row in reader:
                 if row and row['name'].lower() != name.strip().lower():
                    rows.append(row)

            fieldnames = reader.fieldnames #makes it so that the fieldnames can be easily transferred to a new file

        write_csv(filename, fieldnames, rows) #uses function created earlier for writing

        print(f'{type.capitalize()}: {name} removed from {filename}\n')

    #error handling:
    except FileNotFoundError:
        print('File not found')
        return
    except ValueError:
        print('CSV headers do not match excepted format')
        return
    except PermissionError:
        print('Permission denied')
        return

def item_search(filename, name, type):
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)

            found = False  # sets found as false for default

            if not validate_type(type):  # checks the type
                return

            if reader.fieldnames != type_map[type]['fieldnames']: raise ValueError

            for row in reader:
                if row and row['name'].lower() == name.strip().lower():
                    print(type_map[type]['format'].format(**row))
                    found = True

            if not found:
                print(f'{type.capitalize()} not found')

    #error handling:
    except FileNotFoundError:
        print('File not found')
        return
    except ValueError:
        print('CSV headers do not match excepted format')
    except PermissionError:
        print('Permission denied')
        return


def sort_data(filename, sort, type, reverse=False):

    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)

            if not validate_type(type):  # checks the type
                return

            if reader.fieldnames != type_map[type]['fieldnames']: raise ValueError

            data = list(reader) #makes data read into a list

            if sort not in reader.fieldnames: #making sure thing to sort is valid
                print('Invalid attribute to sort by.')
                return

            if sort in type_map[type]['numeric_fields']: #making numeric fields back into numbers
                for row in data:
                    row[sort] = float(row[sort])

            elif sort == 'time': #handles time sorting
                for row in data:
                    try:
                        row[sort] = datetime.strptime(row[sort], '%H:%M').time()
                    except ValueError:
                        print(f'Invalid time: {row[sort]}. Enter in (HH:MM) format.')
                        return

            elif sort == 'date': #handles date sorting
                for row in data:
                    try:
                        row[sort] = datetime.strptime(row[sort], '%Y-%m-%d').date()
                    except ValueError:
                        print(f'Invalid date: {row[sort]}. Enter in (YYYY-MM-DD) format.')
                        return


            sorted_data = sorted(data, key=lambda x: x[sort], reverse=reverse)

            for row in sorted_data:
                print(type_map[type]['format'].format(**row))

    #error handling:
    except FileNotFoundError:
        print('File not found')
    except ValueError:
        print('CSV headers did not match excepted format')
    except PermissionError:
        print('Permission denied')

def replace_info(filename, name, type, column):
    try:

        if not validate_type(type):  # checks the type
            return

        with open(filename, 'r') as file:
            reader = csv.DictReader(file)

            if reader.fieldnames != type_map[type]['fieldnames']: #checking CSV header structure
                raise ValueError('CSV headers do not match excepted format')

            if column not in reader.fieldnames: #checks if column is in the list of columns in the file
                raise ValueError('Invalid attribute to replace by.')

            rows = list(reader) #converts data to list for easier modification

        found = False  # sets found as false for default
        for row in rows:
            if row and row['name'].lower() == name.strip().lower():
                found = True #if the campsite searched matches in the file, found is True
                new_value = input(f'Enter a new value for {column}: ').strip() #gets input for new value

                try:
                    if column == 'rating':
                        new_value = float(new_value)
                        if not (0 <= new_value <= 5): #checking if rating value is correct
                            raise ValueError('\nRating must be between 0 and 5.')

                    elif column in ['elevation','ascension']: #checks mountain's elevation & ascension columns
                        new_value = float(new_value)
                        if not new_value >= 0:
                            raise ValueError(f'\n{column.capitalize()} must be greater than or equal to 0.')

                    elif column == 'time':
                        hours, minutes = map(int, new_value.split(':'))
                        if not (0 <= hours <= 24 and 0 <= minutes <= 59):
                            ValueError(f'\nTime must be in (HH:MM) format.')

                    elif column == 'date':
                        try:
                            column = datetime.strptime(new_value, '%Y-%m-%d')
                            column = column.strftime('%Y-%m-%d')
                            break
                        except ValueError:
                            print('Invalid date format. Use (YYYY-MM-DD).')

                except ValueError as e: #handling multiple errors
                    print(e)
                    return

                row[column] = str(new_value)
                print(f'{column} for {type.capitalize()} {name} saved to {filename}\n')
                break

        if not found:  # if founds is not True, this runs
            print(f'{type.capitalize()} not found.')
            return

        #Creating backup file:
        backup_file = filename.replace('.csv', '_backup.csv')  # renames the backup file
        try:
            shutil.copy(filename, backup_file)  # creates backup file
        except FileNotFoundError:  # silent error handling
            pass
        except PermissionError:
            pass

        write_csv(filename, reader.fieldnames, rows)

    except FileNotFoundError:
        print('File not found')
    except ValueError as e:
        print(e)
    except PermissionError:
        print('Permission denied')

def sort_specific(filename, column, value, type, reverse=False): #only displays specific sorted values

    try:

        if not validate_type(type):  # checks the type
            return

        with open(filename, 'r') as file:
            reader = csv.DictReader(file)

            if reader.fieldnames != type_map[type]['fieldnames']: #checking CSV header structure
                raise ValueError('CSV headers do not match excepted format')

            if column not in reader.fieldnames:
                raise ValueError('Invalid attribute to sort by.')

            rows = [row for row in reader if row[column].strip().lower() == value.strip().lower()] #goes through and only gets columns that matches the given value


        if column in type_map[type]['numeric_fields']:
            for row in rows:
                row[column] = float(row[column])

        elif column == 'time': #handles time sorting
            for row in rows:
                try:
                    row[column] = datetime.strptime(row[column], '%H:%M').time()
                except ValueError:
                    print(f'Invalid time: {row[column]}. Enter in (HH:MM) format.')
                    return

        elif column == 'date': #handles date sorting
            for row in rows:
                try:
                    row[column] = datetime.strptime(row[column], '%Y-%m-%d').date()
                except ValueError:
                    print(f'Invalid date: {row[column]}. Enter in (YYYY-MM-DD) format.')
                    return

        sorted_specific = sorted(rows, key=lambda x: x[column], reverse=reverse)

        if sorted_specific:
            for row in sorted_specific:
                print(type_map[type]['format'].format(**row))
        else:
            print(f"No {type.capitalize()}s found with {column} = '{value}'")

    #error handling:
    except FileNotFoundError:
        print('File not found')
    except ValueError as e:
        print(e)
    except PermissionError:
        print('Permission denied')

def statistics(filename, type):
    total = 0
    state_counts = {}

    if not validate_type(type):
        return

    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)

            if reader.fieldnames != type_map[type]['fieldnames']:  # checking CSV header structure
                raise ValueError('CSV headers do not match excepted format')

            for row in reader:
                if row:
                    total = total + 1
                    state = row['state'].strip()

                    if state in state_counts:
                        state_counts[state] = state_counts[state] + 1
                    else:
                        state_counts[state] = 1

        print(f'Total {type}s found:', total,'\nTotal states:', len(state_counts))
        print(f'\n{type.capitalize()}s by state:')
        for state in state_counts:
            print(f'{state}: {state_counts[state]}')

    # error handling:
    except FileNotFoundError:
        print('File not found')
    except ValueError as e:
        print(e)
    except PermissionError:
        print('Permission denied')

def menu(type): #menu for both mountains or campsites
    if not validate_type(type):
        return

    #makes the filename the appropriate one depending on the type entered.
    if type == 'campsite':
        filename = "campsites.csv"
    elif type == 'mountain':
        filename = "mountains.csv"

    while True:
        print(f'     {type.capitalize()} Menu\n\nEnter 1 for all {type}s.\nEnter 2 to search for a specific {type}.\nEnter 3 for sorting {type}s.\nEnter 4 to add a new {type}.\nEnter 5 to delete a {type}.\nEnter 6 to modify a {type}.\nEnter 7 for statistics.\nEnter 0 to exit to main menu.')
        x = input('Enter here: ')
        print('\n')

        if x == '1': #display all items
            all_items(filename,type)
        elif x == '2': #search for a specific item
            name = input('Search: ')
            print('\n')
            item_search(filename, name, type)
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
                    order = input('Enter sort order (asc/desc): ').strip().lower()

                    if order =='asc':
                        reverse = False
                        break
                    elif order =='desc':
                        reverse = True
                        break
                    else:
                        print('Invalid option.')
                        continue

                print('\n')
                sort_data(filename, sort, type, reverse=reverse)

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
                    order = input('Enter sort order (asc/desc): ').strip().lower()

                    if order =='asc':
                        reverse = False
                        break
                    elif order =='desc':
                        reverse = True
                        break
                    else:
                        print('Invalid option.')
                        continue

                print('\n')
                sort_specific(filename, column, value, type, reverse=reverse)

        elif x == '4': #add new
            create_item(type)
        elif x == '5': #delete old
            name = input(f'Enter the name of {type} to delete: ')
            print('\n')
            remove_item_from_file(filename, name, type)
        elif x == '6': #modify column on an item
            name = input('Search: ')
            column = input('Enter column to modify: ')
            print('\n')
            replace_info(filename, name, type, column)
        elif x == '7': #statistics of data
            statistics(filename, type)
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
            break
        else:
            print('Invalid input')

main_menu()