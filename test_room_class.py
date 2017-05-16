import unittest
from room import Room
from people import Person, Fellow, Staff
from allocator import Dojo


class TestRoomClass(unittest.TestCase):
    def setUp(self):
        self.test_dojo = Dojo()
        self.fellow1 = Fellow()
        self.is_office = True
        self.is_fellow = True

        """ creating multiple offices"""
        self.three_rooms = self.test_dojo.create_room(self.is_office, ['Blue', 'Black', 'Yellow'])

        """ creating an office"""
        self.one_room = self.test_dojo.create_room(self.is_office, ['Spires'])

        """ Add a person"""
        one_person = self.test_dojo.create_person("bryant", "neymar", self.is_fellow)

        """ test if creation of rooms is successful"""
    def test_if_created(self):
        self.assertEqual(self.Object, self.room1)
        self.assertEqual(self.Object, self.office1)

        """ test if created room is added in list"""
    def test_room_name_creation(self):
        self.assertIn('Blue', self.three_rooms.room_name, msg="Blue should be in the room names list in dojo")

        """check whether room number increases"""
    def test_create_room_func(self):
        initial_len = len(self.three_rooms.room_name)
        initial_office_len = len(self.three_rooms.office_num)
        initial_living_len = len(self.three_rooms.living_num)
        self.dojo_create = self.three_rooms.create_room(self.is_office, ['Blue', 'Black', 'Yellow'])

        """ test multiple room creation"""

        self.assertEqual(3, len(self.dojo_create.room_name) - initial_len,
                         msg="Creating three rooms need to increment counter by 3"
                         )
        """ test whether the rooms created exist in list"""

        self.assertTrue(bool(set(self.three_rooms.room_name)&set(self.dojo_create.room_name)),
                        msg="'Blue', 'Black', 'Yellow' created should be in room_names list" )

        """ test increase in offices count on creation of offices """
        self.assertEqual(1, len(self.one_room.office_num)- initial_office_len)
        self.assertEqual(0, len(self.one_room.living_num)- initial_living_len)

        """ test for duplicate rooms. raise NameError on duplicate"""
    def test_duplicate_error(self):
        with self.assertRaises(NameError):
            self.one_room.create_room(self.is_office, ['Blue'])

        """ test for duplicate rooms regardless of how the room name was written. raise NameError on duplicate"""
        with self.assertRaises(NameError):
            self.one_room.create_room(self.is_office, ['BluE'])

        """ test for duplicate rooms. raise TypeError on duplicate"""
    def test_create_person(self):
        """ test creation of person and increment of person number"""

        people_num = len(self.test.dojo.people) # before person creation
        self.test_dojo.create_person("bryant", 3453, self.is_fellow)
        self.assertEqual(1, len(self.test.dojo.people) - people_num)

        """" test if names inputted are strings"""
        with self.assertRaises(TypeError):
            self.one_room.create_person( "bryant", 3453, self.is_fellow)

    def test_assign_room(self):
        """ test whether the assigment of object"""
        initial_offices = len(self.test.dojo.office_num)

        self.test_dojo.assign_room(self.fellow1, True)

        self.assertEqual(1, len(self.test.dojo.office_num)- initial_offices)






if __name__ == '__main__':
    unittest.main()


