"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.

Usage:
    interact create_room (office | living) <room_name>...
    interact create_person <fname> <lname> (fellow [[yes|y][y|n]] | staff)
    interact print_room (office | living) <room_name>...
    interact print_unallocated [--o=filemane]
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
    def do_create_person(self, arg):
        """Usage:  create_person <fname> <lname> (fellow [[yes|y][n|no]] | staff)"""
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
        """Usage: print_room (office | living) <room_name>... """

        rooms = arg['<room_name>']
        if arg['office']:
            is_office = True
        else:
            is_office = False

        result = dojo.print_room(is_office, rooms)
        null  = result[0]
        existing = result[1]

        print("Existing ", existing)
        print("Null ", null)

        for room in existing:
            print(room, ":=>", dojo.offices[room])

        if null:
            for room in null:
                print("Room", room, "doesn't exist")

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filemane]"""
        filename = arg['--o']
        dojo.print_unallocated(filename)

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
