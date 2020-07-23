import subprocess as sp
from random import randint

minepos = []
dug = set()
alive = True


def nextto(pos, mines):
    """Count adjacent mines.
    
    pos -- (x, y): coordinates of the position
    mines -- list of all mine positions
    """
    count = 0
    x, y = pos
    for X, Y in mines: 
        if abs(x - X) <= 1 and abs(y - Y) <= 1: 
            count += 1
    return count


def setup(start):
    """Generate mine positions.
    
    start -- first selected space (x,y), which mines will not generate on or around
    """
    minelimit = 10
    while minelimit > 0:
        for x in range(1,11):
            for y in range(1,9):
                fakeminelist = [(-1,-1),(x,y)]
                if randint(1,8) == 1 and minelimit > 0 and (x,y) not in minepos and nextto(start, fakeminelist) < 1:
                    minepos.append((x,y))
                    minelimit += -1
    dug.add(start)
    return minepos


def clear():
    """Does the chain reaction of clearing empty space"""
    global dug
    changed = True
    counter = 0
    while changed:
        counter += 1
        changed = False
        empty_dug = set()
        for x, y in dug:
            if nextto((x, y), minepos) == 0:
                empty_dug.add((x, y))
        print('round', counter, empty_dug)
        for x in range(1, 11):
            for y in range(1, 9):
                if (x, y) not in dug and nextto((x, y), empty_dug) > 0:
                    print('\t', x, y)
                    dug.add((x, y))
                    changed = True
    print(counter)


def build(minepos, dug):
    """Print board to stdout
    
    minepos -- list of (x, y) coordinates for all mines
    dug -- list of (x, y) coordintes for positions that have be dug
    """
    global alive
    clear()
    sp.call('clear',shell=True)
    for y in range(1,9):
        y = y * -1 + 9
        print(y,'|',end='')
        for x in range(1,11):
            if x > 0:
                print(' ',end='')
            if (x,y) not in dug: 
               print('\u25a0',end='')
            elif (x,y) in minepos:
                alive = False
                print('\u25c9',end='')
            else:
                count = nextto((x,y), minepos)
                if count == 0:
                    print(' ',end='')
                else:
                    print(str(count),end='')
        print('')
    print('    - - - - - - - - - - \n    1 2 3 4 5 6 7 8 9 10')


def enter(minimum, maximum, name):
    """Retrieves input for a square to dig and filters it to be a 
    number and in the right range between minimum and maximum

    name -- name of value you are getting
    """
    validinput = 0
    while validinput == 0:
        validinput = 1
        try:
            entry = 0
            while entry < minimum or entry > maximum:
                entry = int(input(str('Enter ' + name + ' coordinate: ')))
                validinput = 1
                if entry < minimum or entry > maximum:
                    print('Enter a number between', minimum, 'and', maximum)
                    validinput = 0
        except ValueError: 
            print('Enter a number')
            validinput = 0
    return entry


def getcoordinates():
    entryX = enter(1, 10, 'X')
    entryY = enter(1, 8, 'Y')
    return (entryX, entryY)


if __name__ == '__main__':
    build(minepos, dug)
    minepos = setup(getcoordinates())
    build(minepos, dug)
    while alive:
        if len(dug) == 70:
            print('You win!')
            quit()
        dug.add(getcoordinates())
        build(minepos, dug)
    print('You lost...')