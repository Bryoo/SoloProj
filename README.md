# Dojo Room Allocation

## Status

|    **Item**    | **Status** |
|----------------|------------|
| Finished-ness  | :thumbsup: |
| Happiness      | :bowtie:   |
| Markdowny-ness | :octocat:  |

## Problem Description
**For your homework, you will be creating a readme document to introduce yourself to the class and experiment with the range of Markdown features.**

When a new Fellow joins Andela they are assigned an office space and an optional living space
if they choose to opt in. When a new Staff joins they are assigned an office space only.
In this exercise you will be required to digitize and randomize a room allocation system for one of Andela Kenya’s facilities called The Dojo.


## Installation
```
$ https://github.com/Bryoo/SoloProj

```
Navigate to the root folder
```
$ cd SoloProj

```
Install the required prerequisites in your virtual environment
```
$ pip install -r requirements.txt

```

*The header above is "H2" size. The headers below will range from "H2" to "H4" depending on the number of hashtags in front of them*

## Usage

```
$ python interact.py -i

```
```create_room (living|office) <room_name>...```
This creates new rooms by taking in parameters of the type of room and name.
One can create multiple rooms by specifying multiple room names.

```add_person <fname> <lname> (fellow [[yes|y][y|n]] | staff)```
Adds a person to the system and allocates the person to a random room.
If there are no rooms, the person is added to the waiting list.
Only fellows are allocated rooms.

```print_room (office | living) <room_name>...```
Prints  the names of all the people in room_name on the screen.

```print_allocations [--o=filename]...```
Prints a list of allocations onto the screen. Specifying the optional -o option here outputs the registered allocations to a txt file.

```print_unallocated [--o=filename]...```
Prints a list of unallocated people to the screen.
Specifying the -o option here outputs the information to the txt file provided.

## Executing the tests included

```
$ py.test test_room_class.py
```
Alternatively, if you do not have pytest installed but with to, use:

```
$ python3 test_room_class.py
```
You could also use nosetests
```
$ nosetests
```