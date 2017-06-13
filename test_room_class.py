import unittest
from room import Room, Office
from people import Person, Fellow, Staff
from allocator import Dojo
import os


class TestRoomClass(unittest.TestCase):
    def setUp(self):
        self.test_dojo = Dojo()
        self.fellow1 = Fellow("bryan")
        self.is_office = True
        self.need_room = True
        self.is_fellow = True

        self.room1 = Room()
        self.office1 = Office("blue_office")

        # creating multiple offices
        self.test_dojo.create_room(self.is_office, ['Spires', 'Black', 'Yellow'])

        # creating multiple living spaces
        self.test_dojo.create_room(not self.is_office, ['living_spires', 'living_Black', 'living_Yellow'])

        # creation of people
        self.test_dojo.create_person("Martha", "Nyambura", self.is_fellow)

    def test_if_created(self):
        """ test if creation of rooms is successful"""
        self.assertIsInstance(self.room1, Room)
        self.assertIsInstance(self.office1, Office)

    def test_creation_of_offices(self):
        """ test multiple room creation"""
        initial_office_len = len(self.test_dojo.offices)
        initial_living_len = len(self.test_dojo.livings)

        # assign initial offices to initial dojo object
        initial_dojo_offices = self.test_dojo.offices.copy()
        initial_dojo_livings = self.test_dojo.livings.copy()

        # creation of multiple offices
        self.test_dojo.create_room(self.is_office, ['Blue', 'DayKio', 'Plaza'])
        self.assertEqual(3, (len(self.test_dojo.offices) - initial_office_len),
                         msg="Creating three rooms need to increment counter by 3"
                         )
        print("after keys are ", self.test_dojo.offices.keys())
        print("before keys are ", initial_dojo_offices.keys())

        # test whether the offices created exist in dictionary
        self.assertEqual(set(['yellow', 'spires', 'black']), set(initial_dojo_offices.keys())&set(self.test_dojo.offices.keys()),
                        msg="'Blue', 'DayKio', 'Plaza' created should be in room dict")

        # creation of multiple living spaces
        self.test_dojo.create_room( not self.is_office, ['Blue_living', 'DayKio_living', 'Plaza_living'])
        self.assertEqual(3, (len(self.test_dojo.livings) - initial_living_len),
                         msg="Creating three rooms need to increment counter by 3"
                         )
        # test whether the offices created exist in dictionary
        self.assertTrue(bool(set(initial_dojo_livings.keys())&set(self.test_dojo.livings.keys())),
                        msg="'Blue_living', 'DayKio_living', 'Plaza_living' created should be in living room dictionary")

    def test_creation_of_livings(self):

        initial_dojo = Dojo()
        initial_living_len = len(self.test_dojo.livings)

        # assign initial rooms to initial dojo object
        initial_dojo.livings = self.test_dojo.livings

        # creation of multiple offices
        self.test_dojo.create_room(not self.is_office, ['living_Blue', 'living_DayKio', 'living_Plaza'])

        self.assertEqual(3, (len(self.test_dojo.livings) - initial_living_len),
                         msg="Creating three living spaces need to increment living dict by 3"
                         )
        # test whether the rooms created exist in dictionary

        self.assertTrue(bool(set(initial_dojo.livings.keys())&set(self.test_dojo.livings.keys())),
                        msg="'living_Blue', 'living_DayKio', 'living_Plaza' created should be in room dict" )

    def test_create_person(self):
        """ test creation of person and increment of person number"""

        fellow_num = len(self.test_dojo.fellow_list) # before person creation
        self.test_dojo.create_person("bryant", "kiseu", self.is_fellow)
        self.assertEqual(1, len(self.test_dojo.fellow_list) - fellow_num)

        staff_num = len(self.test_dojo.staff_list) # before person creation
        self.test_dojo.create_person("peter", "marangi", not self.is_fellow)
        self.assertEqual(1, len(self.test_dojo.staff_list) - staff_num)

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
            {'black': ['bryant', self.created_fellow]},
            self.test_dojo.offices,
            msg='assign room should add Miriam to black office'
        )
        self.assertDictEqual(
            {'blue_room': ['henry', self.created_fellow]},
            self.test_dojo.livings,
            msg='assign room should add fellow1(Miriam) to blue living space'
        )

        # test addition of staff
        need_room = False
        self.test_dojo.assign_room(self.created_staff, need_room)
        self.assertDictEqual(
            {'black': ['bryant', self.created_fellow, self.created_staff]},
            self.test_dojo.offices,
            msg='assign room should add Rosemary staff to black office'
        )
        self.assertDictEqual(
            {'blue_room': ['henry', self.created_fellow]},
            self.test_dojo.livings,
            msg='addition of staff should not alter the living space dictionary'
        )

    def test_print_room(self):
        # test printing of single office room, existing and non existing
        self.test_dojo.offices.clear()
        self.test_dojo.offices.update({'black_office': ['bryant marangi', 'Meshack Nyambura', 'Lilian muli'],
                                       'blue_office': [],
                                       'dark_office': ['danielle stark']
                                       })

        self.assertEqual([['black_office', 'dark_office'], [], ['non_existing'], ],
                         self.test_dojo.print_room(["black_office", "non_existing", "dark_office"]))

        # test printing of existing and non existing living spaces
        self.test_dojo.livings.clear()
        self.test_dojo.livings.update({'black_living': ['megan doh', 'tony stark', ' ruth bopchy'],
                                       'blue_living': ['ruth mwangi', 'destiny maina']

                                       })
        self.assertEqual([[], ['black_living'], ['absent_living']], self.test_dojo.print_room( ["black_living", "absent_living"]))

    def test_print_unallocated(self):
        """ test data printed on the file"""
        self.test_dojo.fellow_unallocated = [Fellow("bryant awesome"), Fellow("martin king"), Fellow("peter kariuki")]

        # check the existence of the file
        filename = 'data.txt'
        self.test_dojo.print_unallocated(filename)
        self.assertTrue(os.path.exists(filename))

        # check whether the functions outputs the unallocated fellows to data.txt
        with open(filename) as myfile:
            lines = myfile.readlines()
            # line three holds the unallocated fellows
            print("Lines is this mate", lines[2])
            # check if that line matches the people in defined dictionary above
            self.assertTrue("bryant awesome\t\tmartin king\t\tpeter kariuki" in lines[2])
        os.remove(filename)

    def test_print_allocations(self):
        filename = 'allocation.txt'
        """ test the output of the allocated offices"""
        self.test_dojo.offices = {'black': ['peter', 'mushagi', 'kiseu', 'bryan', 'testla', 'rose'],
                                  'blue': ['vandam', 'andrew', 'ritho'],
                                  'white': ['stella', 'shiku', 'hellen']
                                  }
        self.test_dojo.livings = {'black_living': ['bryant marangi', 'Meshack Nyambura', 'Lilian muli'],
                                  'blue_living': [],
                                  'dark_living': ['danielle stark']
                                 }
        self.test_dojo.print_allocations(filename)

    def test_reallocate_person(self):
        """ test whether the person reallocated exists in the new office/living space"""
        self.test_dojo.create_room(self.is_office, ['Bluedom'])
        inital_len = len(self.test_dojo.offices['bluedom'])
        # allocate martha to newly created office
        self.test_dojo.reallocate_person("Martha", "Nyambura", "Bluedom")
        self.assertEqual(1, len(self.test_dojo.offices['bluedom']) - inital_len)

    def test_load_people(self):
        """ test whether load people adds to rooms"""
        fellow_len = len(self.test_dojo.fellow_list)
        staff_len = len(self.test_dojo.staff_list)
        self.test_dojo.load_people('people.txt')
        self.assertEqual(4, len(self.test_dojo.fellow_list) - fellow_len)
        self.assertEqual(3, len(self.test_dojo.staff_list) - staff_len)

    def test_reallocation(self):
        """test whether the reallocation function reallocates to new room"""
        staff_created = Staff('martha jones')
        staff_jen = Staff('jeniffer jenny')
        fellow_akash = Fellow("akash baga")
        fellow_adams = Fellow("adams mister")
        self.test_dojo.offices.clear()
        self.test_dojo.offices.update(
            {
                'black': [staff_created],
                'blue': [staff_jen]
            }
        )
        self.test_dojo.livings.update({
            'bluedom': [fellow_adams, fellow_akash]
        })
        # tests whether staff moves to new room allocated
        self.test_dojo.reallocation([], ['black'], [[self.is_office, 'blue', staff_jen]])
        self.assertEqual({'black': [staff_created, staff_jen],
                          'blue': []
                          }, self.test_dojo.offices,
                         msg="An allocated person needs to exist in the new allocated room"
                         )



if __name__ == '__main__':
    unittest.main()