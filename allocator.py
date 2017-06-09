from people import Fellow, Staff
from room import Office, LivingSpace
import random


class Dojo(object):
    def __init__(self):
        self.room_name = []
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
            office_duplicates = [rm for rm in rooms if rm in list(self.offices.keys())]
            non_duplicates = [rm for rm in rooms if rm not in list(self.offices.keys())]

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
            not_living_duplicates = [rm for rm in rooms if rm not in list(self.livings.keys())]
            living_duplicates = [rm for rm in rooms if rm in list(self.livings.keys())]

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
                self.assign_room(created_fellow, need_room)
            else:
                need_room = True
                self.assign_room(created_fellow, need_room)

        else:
            created_staff = Staff(names)
            self.staff_list.append(created_staff)
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
        existing_offices = [rm for rm in rooms if rm in list(self.offices.keys())]

        existing_living = [rm for rm in rooms if rm in list(self.livings.keys())]

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
                print("All fellows are allocated to rooms")

            print("\nUnallocated Staff")
            print('-' * 40)
            if self.staff_unallocated:
                for staff in self.staff_unallocated:
                    print(staff.name)
            else:
                print("All Staff are allocated to rooms")

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
                data.write("All fellows are allocated to rooms\n")

            data.write("Unallocated Staff")
            data.write('-' * 40)
            if self.staff_unallocated:
                for room in self.staff_unallocated:
                    data.write(room.name)
            else:
                data.write("All Staff are allocated to rooms\n")

            data.close()

    def print_allocations(self, myfile):
        """ loops through dictionary and prints out parameters to screen or inputted file"""
        if not myfile:

            if any(self.offices):
                print("Offices")
                for office in self.offices:
                    people_list = self.offices[office]
                    print('office ', office)
                    for person in people_list:
                        print(person.name, "\t")
            else:
                print("No offices currently exist")
            if any(self.livings):
                print("Living Spaces")
                for living in self.livings:
                    living_people = self.livings[living]
                    print("Living ", living)
                    for person in living_people:
                        print(person.name, "\t")
            else:
                print("No living spaces currently exist")

        else:
            data = open(myfile, "w")
            data.write("Offices\n")
            for office in self.offices:

                data.write(office)
                data.write('=>')
                data.write(', '.join(str(elem) for elem in self.offices[office]))
                data.write('\n')

            data.write("Living Spaces\n")
            for living in self.livings:
                data.write(living)
                data.write('=>')
                data.write(', '.join(str(elem) for elem in self.livings[living]))
                data.write('\n')
            data.close()

    def reallocate_person(self, fname, lname, room_name):
        names = fname.lower() + " " + lname.lower()
        room = room_name.lower()
        name_exists = []
        office_exists = []
        living_exists = []
        if room in list(self.offices.keys()):
            office_exists.append(room)
        if room in list(self.livings.keys()):
            living_exists.append(room)

        if len(office_exists + living_exists) < 1:
            print("No room named", room_name, "was not found")
            return

        elif len(office_exists + living_exists) == 1:
            is_office = True
            for office, persons in self.offices.items():
                for person in persons:
                    if person.name == names:
                        name_exists.append([is_office, office, person])
            for living, people in self.livings.items():
                for person in people:
                    if person.name == names:
                        name_exists.append([not is_office, living, person])
            for i in name_exists:
                print(i[2].name)
            print("length is ",len(name_exists))
            if len(name_exists) == 1:
                details = name_exists[0]
                current_room = details[1]
                person_found = details[2]

                #add person to allocated room
                if living_exists:
                    living_name = living_exists[0]
                    self.livings[living_name].append(person_found)
                elif office_exists:
                    office_name = office_exists[0]
                    self.offices[office_name].append(person_found)

                # remove person from current room

                if details[0]:
                    self.offices[current_room].remove(person_found)
                else:
                    self.livings[current_room].remove(person_found)

            elif len(name_exists) < 1:
                print("Sorry, the person doesn't exist")
            else:
                print("Multiple names found")

    def load_people(self, filename='people.txt'):
        with open(filename, 'r') as f:
            content = f.readlines()
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
                return
            self.create_person(fname, lname, is_fellow, need_room)

    

"""
create_room office black
create_room office blue
create_room living bluedom
add_person bryo kiseu fellow yes
add_person peter marangi fellow yes
add_person gift otieno staff
add_person selsa patash staff
"""