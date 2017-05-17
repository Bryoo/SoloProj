import unittest
from room import Room, Office
from people import Person, Fellow, Staff
from allocator import Dojo

class TestRoomClass(unittest.TestCase):
    def setUp(self):
        self.test_dojo = Dojo()
        self.fellow1 = Fellow("bryan")
        self.is_office = True
        self.need_room = True
        self.is_fellow = True

        self.room1 = Room()
        self.office1 = Office("blue_office")
        #
        """ creating multiple offices"""
        self.test_dojo.create_room(self.is_office, ['Spires', 'Black', 'Yellow'])

        """ creating multiple living spaces"""
        self.test_dojo.create_room(not self.is_office, ['living_spires', 'living_Black', 'living_Yellow'])

    def test_if_created(self):
        """ test if creation of rooms is successful"""
        self.assertIsInstance(self.room1, Room)
        self.assertIsInstance(self.office1, Office)

        """check whether room number increases"""
    def test_creation_of_offices(self):
        """ test multiple room creation"""
        initial_dojo = Dojo()

        initial_office_len = len(self.test_dojo.offices)
        initial_living_len = len(self.test_dojo.livings)

        #assign initial rooms to initial dojo object
        initial_dojo.offices = self.test_dojo.offices

        # creation of multiple offices
        self.test_dojo.create_room(self.is_office, ['Blue', 'DayKio', 'Plaza'])

        self.assertEqual(3, (len(self.test_dojo.offices) - initial_office_len),
                         msg="Creating three rooms need to increment counter by 3"
                         )
        # test whether the rooms created exist in dictionary

        self.assertTrue(bool(set(initial_dojo.offices.keys())&set(self.test_dojo.offices.keys())),
                        msg="'Blue', 'DayKio', 'Plaza' created should be in room dict" )


    def test_creation_of_livings(self):

        initial_dojo = Dojo()
        initial_living_len = len(self.test_dojo.livings)

        #assign initial rooms to initial dojo object
        initial_dojo.livings = self.test_dojo.livings

        # creation of multiple offices
        self.test_dojo.create_room(not self.is_office, ['living_Blue', 'living_DayKio', 'living_Plaza'])

        self.assertEqual(3, (len(self.test_dojo.livings) - initial_living_len),
                         msg="Creating three living spaces need to increment living dict by 3"
                         )
        # test whether the rooms created exist in dictionary

        self.assertTrue(bool(set(initial_dojo.livings.keys())&set(self.test_dojo.livings.keys())),
                        msg="'living_Blue', 'living_DayKio', 'living_Plaza' created should be in room dict" )

    def test_duplicate_error(self):
        """ test for duplicate rooms. raise NameError on duplicate"""
        with self.assertRaises(NameError):
            self.test_dojo.create_room(self.is_office, ['Blue'])

        # test for duplicate rooms regardless of how the room name was written. raise NameError on duplicate
        with self.assertRaises(NameError):
            self.test_dojo.create_room(self.is_office, ['BluE'])

    def test_create_person(self):
        """ test creation of person and increment of person number"""

        people_num = len(self.test_dojo.fellow_list) # before person creation
        self.test_dojo.create_person("bryant", "kiseu", self.is_fellow)
        self.assertEqual(1, len(self.test_dojo.fellow_list) - people_num)

        # test if names inputted are strings
        with self.assertRaises(TypeError):
            self.test_dojo.create_person( "bryant", 3453, self.is_fellow)

    def test_check_vacant(self):
        """ check whether a dictionary of only the non full rooms (less than 6) is returned"""
        self.test_dojo.offices = {'black': ['peter', 'mushagi', 'kiseu', 'bryan', 'testla', 'rose'],
                                  'blue': ['vandam', 'andrew', 'ritho'],
                                  'white': ['stella', 'shiku', 'hellen']
                                 }
        self.test_dojo.livings = {'white_living': ['mary', 'john', 'cosmos', 'ruth'],
                                  'blue_living': ['Ernest', 'Peter', 'Waititu', 'Mwambela'],
                                  'black_living': ['Louise', 'Bethany', 'Annabelle', 'Neymar']
                                 }
        self.assertDictEqual(
            {'blue': ['vandam', 'andrew', 'ritho'],
             'white': ['stella', 'shiku', 'hellen']
            },
            self.test_dojo.check_vacant_room(self.test_dojo.offices, 6),
            msg='should only return the offices with less than 6 people'
        )
        # test returning empty dictionay when all rooms are full
        self.assertDictEqual(
            {},
            self.test_dojo.check_vacant_room(self.test_dojo.livings, 4),
            msg='should return empty dictionary if all the living spaces are full'
        )

    def test_assign_room(self):
        """ test whether a person is assigned to a room"""
        self.created_fellow = Fellow("Miriam")
        self.created_staff = Staff("Rosemary")

        self.test_dojo.offices.clear()
        self.test_dojo.livings.clear()
        self.test_dojo.offices.update({'black': ['bryant']})
        self.test_dojo.livings.update({'blue_room': ['henry']})

        # test addition of fellow who needs a room
        self.test_dojo.assign_room(self.created_fellow, self.need_room)
        self.assertDictEqual(
            {'black': ['bryant', 'Miriam']},
            self.test_dojo.offices,
            msg='assign room should add Mirriam to black office'
        )
        self.assertDictEqual(
            {'blue_room': ['henry', 'Miriam']},
            self.test_dojo.livings,
            msg='assign room should add fellow1(Miriam) to blue living space'
        )

        # test addition of staff
        need_room = False
        self.test_dojo.assign_room(self.created_staff, need_room)
        self.assertDictEqual(
            {'black': ['bryant', 'Miriam', 'Rosemary']},
            self.test_dojo.offices,
            msg='assign room should add Rosemary staff to black office'
        )
        self.assertDictEqual(
            {'blue_room': ['henry', 'Miriam']},
            self.test_dojo.livings,
            msg='addition of staff should not alter the living space dictionary'
        )


if __name__ == '__main__':
    unittest.main()


