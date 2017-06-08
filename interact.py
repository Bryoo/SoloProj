"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.

Usage:
    interact create_room (office | living) <room_name>...
    interact add_person <fname> <lname> (fellow [[yes|y][no|n]] | staff)
    interact print_room <room_name>...
    interact print_unallocated [--o=filename]
    interact print_allocations [--o=filename]
    interact reallocate_person <fname> <lname> <room_name>
    interact (-i | --interactive)
    interact (-h | --help | --version)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""
import sys
import cmd
from allocator import Dojo
from docopt import docopt, DocoptExit

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):

        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


dojo = Dojo()


class MyInteractive(cmd.Cmd):
    # def __init__(self):
    #     self.
    intro = 'Welcome to my interactive program!' \
            + ' (type help for a list of commands.)'
    prompt = '(dojo_tings) '
    file = None

    @docopt_cmd
    def do_create_room(self, args):
        """Usage:  create_room (office | living) <room_name>..."""
        room_name = args['<room_name>']
        is_office = args['office']

        dojo.create_room(is_office, room_name)

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage:  add_person <fname> <lname> (fellow [[yes|y][n|no]] | staff)"""
        if arg['yes'] | arg['y']:
            need_room = "yes"
        else:
            need_room = "no"

        if arg['fellow']:
            is_fellow = True
        else:
            is_fellow = False

        dojo.create_person(arg['<fname>'], arg['<lname>'], is_fellow, need_room)

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>... """

        rooms = arg['<room_name>']
        result = dojo.print_room(rooms)

        offices = result[0]
        livings = result[1]
        null = result[2]

        if offices:
            print("Offices: ")
            for room in offices:
                people_list = dojo.offices[room]
                print("office ", room)
                for member in people_list:
                    print(member.name, "\t")

        if livings:
            print("Living Spaces: ")
            for room in livings:
                living_people = dojo.livings[room]
                print("Living space ", room)
                for member in living_people:
                    print(member.name, "\t")

        if null:
            print("Non Existent Rooms: ")
            for room in null:
                print("Room", room, "doesn't exist")

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""
        filename = arg['--o']
        dojo.print_unallocated(filename)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]"""
        filename = arg['--o']
        dojo.print_allocations(filename)

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <fname> <lname> <room_name>"""

        dojo.reallocate_person(arg['<fname>'], arg['<lname>'], arg['<room_name>'])

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

if opt['create_room']:
    print(opt['<room_name>'])

print(opt)
