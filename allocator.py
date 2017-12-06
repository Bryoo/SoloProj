from people import Fellow, Staff
from room import Office, LivingSpace
import random
import sqlite3
import os
from sqlite_db import SaveState, LoadState
SaveState = SaveState()
LoadState = LoadState()


class Dojo(object):
    def __init__(self):
        # self.room_name = []
        self.offices = {}
        self.livings = {}
        self.fellow_unallocated = []
        self.staff_unallocated = []
        self.staff_list = []
        self.fellow_list = []

    def create_room(self, is_office, room_names):
        rooms = [item.lower() for item in room_names]
        # check if its staff or fellow and create person by calling staff and fellow objects

        if is_office:
            office_duplicates = [room for room in rooms if room in list(self.offices.keys())]
            non_duplicates = [room for room in rooms if room not in list(self.offices.keys())]

            if non_duplicates:  # if there are no office duplicates

                for room in non_duplicates:
                    create_office = Office(room)
                    self.offices[create_office.name] = []
                    print("Office", room, "has been created")

                print(" ")
                # if there are some office duplicates
                if office_duplicates:
                    for room in office_duplicates:
                        print("Room", room, "already exists")
                    print(" ")
            # if there are no unique entries
            else:
                print("All entries exist hence no room created\n")

        else:
            not_living_duplicates = [room for room in rooms if room not in list(self.livings.keys())]
            living_duplicates = [room for room in rooms if room in list(self.livings.keys())]

            if not_living_duplicates:  # if there are no duplicates
                for room in not_living_duplicates:
                    create_living = LivingSpace(room)
                    self.livings[create_living.name] = []
                    print("Living space", room, "has been created")
                print(" ")

                if living_duplicates:
                    for room in living_duplicates:
                        print("Living room", room, "already exists \n")
            else:
                print("All living spaces inputted exist hence no room created\n")

    def create_person(self, fname, lname, is_fellow, need_room='no'):
        names = fname.lower() + " " + lname.lower()
        if is_fellow:
            created_fellow = Fellow(names)
            self.fellow_list.append(created_fellow)

            if need_room == 'no':
                need_room = False
            else:
                need_room = True
            self.assign_room(created_fellow, need_room)

        else:
            created_staff = Staff(names)
            self.staff_list.append(created_staff)
            if need_room == 'no':
                pass

            else:
                print('Cannot allocate living space to staff')
            need_room = False
            self.assign_room(created_staff, need_room)

    def assign_room(self, person, need_room):
        """ check for vacant rooms by looping either the office or living spaces"""
        # assigning office rooms to all parties
        try:
            # check if there are vacant rooms in dictionary
            empty_office_dict = self.check_vacant_room(self.offices, 6)
            random_office = random.choice(list(empty_office_dict))
            self.offices[random_office].append(person)
            print(person.name, "has been assigned to office", random_office)

        except BaseException as error:
            if isinstance(person, Fellow):
                self.fellow_unallocated.append(person)
                print("Fellow", person.name, "added but there are no rooms to allocate\n")
            else:
                self.staff_unallocated.append(person)
                print("Staff", person.name, "added but there are no offices to allocate\n")

        # Assigning living room
        if need_room:
            try:
                empty_living_dict = self.check_vacant_room(self.livings, 4)
                random_living = random.choice(list(empty_living_dict))

                # append created person to dictionary
                self.livings[random_living].append(person)

                print(person.name, " has been assigned to living space", random_living)
                print(" ")
            except BaseException as error:
                if error.__class__.__name__ == "IndexError":
                    pass
                else:
                    print(error.__class__.__class__, ": ", error)
        else:
            print(" ")

    def check_vacant_room(self, existing_dict, max):
        """if type is office, use office dict else listing to get spaces dict
            it then returns the offices that are not full
        """
        semi_full_dict = {}

        for i in existing_dict.keys():

            if len(existing_dict[i]) < max:
                semi_full_dict[i] = existing_dict[i]

        return semi_full_dict

    def print_room(self, rooms):
        """ Prints out rooms and occupants"""
        existing_offices = [room for room in rooms if room in list(self.offices.keys())]

        existing_living = [room for room in rooms if room in list(self.livings.keys())]

        # get non existent rooms
        null_rooms = []
        for room in rooms:
            if room not in list(self.offices.keys()):
                if room not in list(self.livings.keys()):
                    null_rooms.append(room)

        all_rooms = [existing_offices, existing_living, null_rooms]
        return all_rooms

    def print_unallocated(self, filename):
        if not filename:
            print("Unallocated Fellows")
            print('-' * 40)
            # prints unallocated fellows
            if self.fellow_unallocated:
                for fellow in self.fellow_unallocated:
                    print(fellow.name)
            else:
                print("No unallocated fellows exist")

            print("\nUnallocated Staff")
            print('-' * 40)
            if self.staff_unallocated:
                for staff in self.staff_unallocated:
                    print(staff.name)
            else:
                print("No unallocated staff exist")

        else:
            data = open(filename, "w")
            data.write("Unallocated Fellows\n")
            data.write('-' * 50)
            data.write("\n")
            if self.fellow_unallocated:
                for room in self.fellow_unallocated:
                    data.write(room.name)
                    data.write("\t\t")
                data.write("\n")
            else:
                data.write("No unallocated fellows exist\n")

            data.write("Unallocated Staff")
            data.write('-' * 40)
            if self.staff_unallocated:
                for room in self.staff_unallocated:
                    data.write(room.name)
            else:
                data.write("No unallocated staff exist\n")

            data.close()

    def print_allocations(self, myfile):
        """ loops through dictionary and prints out parameters to screen or inputted file"""
        if not myfile:

            if any(self.offices):
                print(" ")
                for office in self.offices:
                    people_list = self.offices[office]
                    print('office', office)
                    print('='* 30)
                    for person in people_list:
                        print(person.name, '\t', person.id)
                    print(" ")
                print(" ")
            else:
                print("No offices currently exist")
            if any(self.livings):
                for living in self.livings:
                    living_people = self.livings[living]
                    print("Living Space", living)
                    print('=' * 30)
                    for person in living_people:
                        print(person.name, '\t', person.id)
                    print(" ")
                print(" ")
            else:
                print("No living spaces currently exist")

        else:
            data = open(myfile, "w")
            data.write("Offices\n")
            for office in self.offices:

                data.write(office)
                data.write('=>')
                data.write(', '.join(elem.name for elem in self.offices[office]))
                data.write('\n')

            data.write("Living Spaces\n")
            for living in self.livings:
                data.write(living)
                data.write('=>')
                data.write(', '.join(elem.name for elem in self.livings[living]))
                data.write('\n')
            data.close()
            print("Printed allocations to", myfile)

    def reallocate_person(self, fname, lname, room_name, identity=None):
        names = fname.lower() + " " + lname.lower()
        room = room_name.lower()
        name_exists = []
        office_exists = []
        living_exists = []
        if room in list(self.offices.keys()):
            # stores room if input was an office
            office_exists.append(room)
        if room in list(self.livings.keys()):
            # stores room if input was a living space
            living_exists.append(room)

        if len(office_exists + living_exists) < 1:
            print("No room named", room_name, "was found")
            return "Room not found"

        elif len(office_exists + living_exists) >= 1:
            # a room found
            is_office = True
            # checking the rooms and validating
            if len(office_exists + living_exists) > 1:
                # if room name inputted has more than one name
                print("Please specify which of these rooms you'd like to allocate to")
                result = self.print_room([room_name])
                offices = result[0]
                livings = result[1]
                null = result[2]
                if null:
                    print("Non Existent Rooms: ")
                    for room in null:
                        print("Room", room, "doesn't exist")
                if offices:
                    for room in offices:
                        people_list = self.offices[room]
                        print("office ", room)
                        print('=' * 30)
                        for member in people_list:
                            print(member.name, "\t", member.id)
                        print(" ")
                if livings:
                    for room in livings:
                        living_people = self.livings[room]
                        print("Living space ", room)
                        print('=' * 30)
                        for member in living_people:
                            print(member.name, "\t", member.id)
                        print(" ")
                final_room = input("Enter 'office' or 'living space' to select room type: ")
                if final_room == 'living space':
                    # search for person in living spaces
                    for living, people in self.livings.items():
                        #  finds person inputted if in living space dict
                        for person in people:
                            if person.name == names:
                                # appends a list of similar names in living space dict to name_exists list
                                name_exists.append([not is_office, living, person])

                else:
                    # search for person in offices
                    for office, persons in self.offices.items():
                        # finds person inputted if in office dict
                        for person in persons:
                            if person.name == names:
                                # appends all similar names in office dict to name_exists list
                                name_exists.append([is_office, office, person])

            else:
                # only one room found by inputted name in both office and living spaces present
                if office_exists:
                    # if inputted room is an office, search for person in offices
                    for office, persons in self.offices.items():
                        # finds person inputted if in office dict
                        for person in persons:
                            if person.name == names:
                                # appends all similar names in office dict to name_exists list
                                name_exists.append([is_office, office, person])

                if living_exists:
                    # if inputted room is a living space, search for person in living spaces
                    for living, people in self.livings.items():
                        #  finds person inputted if in living space dict
                        for person in people:
                            if person.name == names:
                                # appends a list of similar names in living space dict to name_exists list
                                name_exists.append([not is_office, living, person])

            # checking the names and validating
            if len(name_exists) == 1:
                # only a single person by inputted name
                self.reallocation(living_exists, office_exists, name_exists)

            elif len(name_exists) < 1:
                # no name found
                print("Sorry, the person doesn't exist")
                return "Sorry, the person doesn't exist"

            else:
                if len(name_exists) == 2:
                    # two similar names found
                    ids = []
                    for name in name_exists:
                        ids.append(name[2].id)

                    if ids[0] == ids[1]:
                        # same person
                        self.reallocation(living_exists, office_exists, name_exists)
                        return "successfully reallocated"

                print("Multiple names found. Which id should be reallocated?")
                for name in name_exists:
                    print(name[2].name, '\t', name[2].id)

                if identity is None:
                    identity = int(input('Enter id: '))

                final_identity = []
                for name in name_exists:
                    if name[2].id == identity:
                        final_identity.append(name)
                        break
                if final_identity:
                    self.reallocation(living_exists, office_exists, final_identity)
                else:
                    print("Sorry, that identity doesn't exist")

    def reallocation(self, living_exists, office_exists, name_exists):
        details = name_exists[0]
        is_office = details[0]
        current_room = details[1]
        person_found = details[2]

        # add person to allocated room
        if living_exists:
            living_name = living_exists[0]
            if isinstance(person_found, Staff):
                print("Staff cannot be allocated to a living space")
                return "Staff allocated to living space"
            if len(self.livings[living_name]) >= 4:
                print("the room is already packed. Choose another room")
                return "the room is full"
            else:
                self.livings[living_name].append(person_found)
            print("Successfully reallocated", person_found.name, "to", living_name)
        elif office_exists:
            office_name = office_exists[0]
            if len(self.offices[office_name]) >= 6:
                print("the room is already packed. Choose another room")
                return "the room is full"
            self.offices[office_name].append(person_found)
            print("Successfully reallocated", person_found.name, "to", office_name)

        # remove person from current room
        if is_office:
            self.offices[current_room].remove(person_found)
        else:
            self.livings[current_room].remove(person_found)

    def load_people(self, filename='people.txt'):
        if not os.path.isfile(filename):
            print("File doesn't exist")
            return "file doesn't exist"

        with open(filename, 'r') as f:
            content = f.readlines()
        if not content:
            print("The file specified is empty")
            return "empty file"

        for line in content:
            data = line.split()
            fname = data[0]
            lname = data[1]
            role = data[2].lower()

            if role == 'fellow':
                is_fellow = True
                try:
                    stay = data[3].lower()
                    if stay in ['yes', 'y']:
                        need_room = 'yes'
                    else:
                        need_room = 'no'
                except IndexError:
                    pass
            elif role == 'staff':
                is_fellow = False
            else:
                print("person", fname, lname, "not a staff or fellow")
                return "person not a staff or fellow"
            self.create_person(fname, lname, is_fellow, need_room)

    def save_state(self, database):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        SaveState.create_tables(c, conn)
        # loop through office and living spaces dictionaries

        for office, people in self.offices.items():
            # recreate office room key dictionary
            SaveState.insert_offices(c, conn, office)
            for person in people:
                # add people to key
                if isinstance(person, Fellow):
                    SaveState.insert_people_offices(c, conn, person.id, person.name, office, role='fellow')
                elif isinstance(person, Staff):
                    SaveState.insert_people_offices(c, conn, person.id, person.name, office, role='staff')
        for living, people in self.livings.items():
            # recreate living room key dictionary
            SaveState.insert_livings(c, conn, living)
            for person in people:
                # add people to living key created
                SaveState.insert_people_livings(c, conn, person.id, person.name, living, role='fellow')

        for person in self.staff_unallocated:
            role = 'staff'
            SaveState.insert_unallocated(c, conn, person.id, person.name, role)
        for person in self.fellow_unallocated:
            role = 'fellow'
            SaveState.insert_unallocated(c, conn, person.id, person.name, role)
        print('application state has been saved successfully')
        c.close()
        conn.close()

    def load_state(self, database='dojo.db'):
        """ loads data from database"""
        if not os.path.exists(database):
            print("database doesn't exist")
            return "database doesn't exist"

        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        results = LoadState.load_unallocated(cursor)

        for result in results:
            if result[2] == 'fellow':
                fellow = Fellow(result[1])
                fellow.id = result[0]
                self.fellow_unallocated.append(fellow)
            elif result[2] == 'staff':
                staff = Staff(result[1])
                staff.id = result[0]
                self.staff_unallocated.append(staff)

        offices = LoadState.load_offices(cursor)
        for office in offices:
            room_name = office[0]
            allocations = LoadState.load_office_alloc(cursor, room_name)
            self.offices[room_name] = []

            for person in allocations:
                identity = person[0]
                names = person[1]
                role = person[4]

                if role == 'fellow':
                    fellow_obj = Fellow(names)
                    fellow_obj.id = identity
                    self.offices[room_name].append(fellow_obj)
                elif role == 'staff':
                    staff_obj = Staff(names)
                    staff_obj.id = identity
                    self.offices[room_name].append(staff_obj)

        livings = LoadState.load_livings(cursor)
        for living in livings:
            room_name = living[0]
            allocations = LoadState.load_living_alloc(cursor, room_name)
            self.livings[room_name] = []

            for person in allocations:
                identity = person[0]
                names = person[1]
                role = person[4]

                if role == 'fellow':
                    fellow_obj = Fellow(names)
                    fellow_obj.id = identity
                    self.livings[room_name].append(fellow_obj)
                elif role == 'staff':
                    print("error")
        print("loaded state successfully")

"""
# copy and paste these commands onto project terminal
create_room office black
create_room living red
add_person bryo kiseu fellow yes
add_person gift otieno fellow no
add_person edmond ato staff yes
add_person selsa patash staff
load_people people.txt
save_state --db_name=dojos.db
print_allocations

load_state dojos.db
"""