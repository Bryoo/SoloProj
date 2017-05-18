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

            if non_duplicates:  # if there are no duplicates

                for room in non_duplicates:
                    create_office = Office(room)
                    self.offices[create_office.name] = []
                    print("Office", room, "has been created")

                if office_duplicates:
                    for room in office_duplicates:
                        print("Room", room, "already exists \n")

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

                if living_duplicates:
                    for room in living_duplicates:
                        print("Living room", room, "already exists \n")
            else:
                print("All living spaces imputted exist hence no room created\n")

    def create_person(self, fname, lname, is_fellow, need_room='No'):
        names = fname.lower() + " " + lname.lower()
        if is_fellow:
            created_fellow = Fellow(names)
            self.fellow_list.append(created_fellow)

            if need_room == 'No':
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
            random_offices = random.choice(list(empty_office_dict))
            self.offices[random_offices].append(person.name)
            print(person.name, " has been assigned to office", random_offices)

        except BaseException as error:
            if isinstance(person, Fellow):
                self.fellow_unallocated.append(person)
                print("Fellow", person.name, "added but there are no rooms to allocate ")
            else:
                self.staff_unallocated.append(person)
                print("Staff", person.name, "added but there are no offices to allocate ")

        # Assigning living room
        if need_room:
            try:
                empty_living_dict = self.check_vacant_room(self.livings, 4)
                random_living = random.choice(list(empty_living_dict))

                # append created person to dictionary
                self.livings[random_living].append(person.name)
                print(person.name, " has been assigned to living space", random_living)

            except BaseException as error:
                if error.__class__.__name__ == "IndexError":
                    print("Person added but not allocated to a living space")  # (if staff dont print)
                else:
                    print(error.__class__.__class__, ": ", error)

                    # to create a new room and assign the person to that room

    def check_vacant_room(self, existing_dict, max):
        """if type is office, use office dict else listing to get spaces dict
            it then returns the offices that are not full
        """
        semi_full_dict = {}

        for i in existing_dict.keys():

            if len(existing_dict[i]) < max:
                semi_full_dict[i] = existing_dict[i]

        return semi_full_dict

    def print_room(self, is_office, rooms):
        """ Prints out rooms and occupants"""
        if is_office:
            # get offices that are not in existing office dict
            null_offices = [rm for rm in rooms if rm not in list(self.offices.keys())]
            # get offices that are in existing office dict
            existing_offices = [rm for rm in rooms if rm in list(self.offices.keys())]
            is_office = True
            all_offices = [null_offices, existing_offices, is_office]
            return all_offices

        else:
            # get offices that are not in existing living dict
            null_living = [rm for rm in rooms if rm not in list(self.livings.keys())]
            # get offices that are in existing living dict
            existing_living = [rm for rm in rooms if rm in list(self.livings.keys())]
            is_office = False
            all_livings = [null_living, existing_living, is_office]
            return all_livings

    def print_unallocated(self, filename):
        if not filename:
            print("Unallocated Fellows")
            print('-' * 50)
            if self.fellow_unallocated:
                for room in self.fellow_unallocated:
                    print(room.name)
            else:
                print("All fellows are allocated to rooms")

            print("\nUnallocated Staff")
            print('-' * 50)
            if self.staff_unallocated:
                for room in self.staff_unallocated:
                    print(room.name)
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

            if self.staff_unallocated:
                for room in self.staff_unallocated:
                    data.write(room.name)
            else:
                data.write("All fellows are allocated to rooms\n")

            data.close()

    def print_allocations(self, myfile):
        """ loops through dictionary and prints out parameters to screen or inputted file"""
        if not myfile:
            for office in self.offices:
                print(office, '=>', ', '.join(self.offices[office]))

            for living in self.livings:
                print(living, '=>', ', '.join(self.livings[living]))

        else:
            data = open(myfile, "w")
            for office in self.offices:
                data.write(office)
                data.write('=>')
                data.write(', '.join(str(elem) for elem in self.offices[office]))
                data.write('\n')

            for living in self.livings:
                data.write(living)
                data.write('=>')
                data.write(', '.join(str(elem) for elem in self.livings[living]))
            data.close()

            # create_room office blue_office black_office
            # create_room living blue_living black_living
            # create_person bryoo muthama fellow yes
            # create_person james mitu fellow yes
            # create_person peter marangi staff
            # print_room office blue_office
            # print_room office blue_office black_office yellow_office
            # print_room living blue_living black_living
            # print_room living blue_living black_living yellow_living
            # print_allocations
            # print_allocations --o=file.txt
            # print_unallocated --o=data.txt
"""
office and living space names
has been assigned to 'living space' black_office


assigning a fellow without accomodation

error message for staff acomodation

print  offices and living spaces with same name

show types on allocations
"""