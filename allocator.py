from people import Fellow, Staff
from room import Office, LivingSpace
import random

class Dojo(object):
    def __init__(self):
        self.room_name = []
        self.offices = {}
        self.livings = {}

        self.staff_list = []
        self.fellow_list = []

    def create_room(self, is_office, room_type):
        rooms = room_type
        # check if its staff or fellow and create person by calling staff and fellow objects

        if is_office:
            for room in rooms:
                create_office = Office(room)
                self.offices[create_office.name] = []
                print("Office ", room, " has been created")

        else:
            for room in rooms:
                create_living = LivingSpace(room)
                self.livings[create_living.name] = []
                print("Living space ", room, " has been created")


    def create_person(self, fname, lname, is_fellow, need_room='No'):
        names = fname + " " + lname
        if is_fellow:
            create_fellow = Fellow(names)
            self.fellow_list.append(create_fellow)

            if need_room == 'No':
                need_room = False
                self.assign_room(create_fellow, need_room)
            else:
                need_room = True
                self.assign_room(create_fellow, need_room)

        else:
            create_staff = Staff(names)
            self.staff_list.append(create_staff)
            self.assign_room(create_staff, need_room)

        # append created person to list

        # call assign rom function to give them a room

    def assign_room(self, person, need_room):
        # check for vacant rooms by looping either the office or living spaces
        empty_office_dict = self.check_vacant_room(self.offices, 6)
        # if  (empty_office_dict)
        random_offices = random.choice(list(empty_office_dict))

        self.offices[random_offices].append(person.name)
        print(person.name, " has been assigned to ", random_offices)

        if need_room:
            try:
                empty_living_dict = self.check_vacant_room(self.livings, 4)
                random_living = random.choice(list(empty_living_dict))

                self.livings[random_living].append(person.name)
                print(person.name, " has been assigned to ", random_living)

            except BaseException as error:
                # return
                print(error.__class__.__class__, ": ", error)
                # create a new room and assign the person to that room


    def check_vacant_room(self, existing_dict, max):
        """if type is office, use office dict else listing to get spaces dict
            it then returns the offices that are not full
        """
        semi_full_dict = {}

        for i in existing_dict.keys():

            if len(existing_dict[i]) < max:
                semi_full_dict[i] = existing_dict[i]

        return semi_full_dict


    # create_room office blue_office black_office
    # create_room living blue_livingce black_living
    # create_person bryoo muthama fellow yes