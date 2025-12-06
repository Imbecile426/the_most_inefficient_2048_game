import random
import keyboard
a=[0,0,0,0]
b=[0,0,0,0]
c=[0,0,0,0]
d=[0,0,0,0]
rows=[a,b,c,d]
def addstuff(direction):
    freeChoices=[0,1,2,3]
    shuffledRows = [a,b,c,d]
    random.shuffle(shuffledRows)
    if direction == 'l':# adds a random 2 or 4 in a random row of the right edge
        if 0 in [a[3],b[3],c[3],d[3]]:
            for row in shuffledRows:
                if row[3] == 0:
                    row[3] = random.choice([2,4])
                    break
                else:
                    continue


    if direction == 'r':# adds a random 2 or 4 in a random row of the left edge
        if 0 in [a[0],b[0],c[0],d[0]]:
            for row in shuffledRows:
                if row[0] == 0:
                    row[0] = random.choice([2,4])
                    break           
                else:
                    continue


    if direction == 'd':# adds a random 2 or 4 in a random coloumn at the top
        if 0 not in a:
            pass
        else:
            randomColoumn=random.choice(freeChoices)
            while a[randomColoumn] != 0:
                freeChoices.remove(randomColoumn)
                if not (len(freeChoices)):
                    break
                randomColoumn=random.choice(freeChoices)
            a[randomColoumn] = random.choice([2,4])


    if direction == 'u':# adds a random 2 or 4 in a random coloumn at the bottom
        if 0 not in d:
            pass
        else:
            randomColoumn=random.choice(freeChoices)
            while a[randomColoumn] != 0:
                freeChoices.remove(randomColoumn)
                if not (len(freeChoices)):
                    break
                randomColoumn=random.choice(freeChoices)
            d[randomColoumn] = random.choice([2,4])
def render():
    for row in rows:
        for unit in range(4):
            if row[unit]==0:
                print('☐',end='    ')
            elif len(str(row[unit]))==1:
                print(row[unit],end='    ')
            elif len(str(row[unit]))==2:
                print(row[unit],end='   ')
            elif len(str(row[unit]))==3:
                print(row[unit],end='  ')
            elif len(str(row[unit]))==4:
                print(row[unit],end=' ')
        print()
    print('\n\n\n\n')
render()
def move(direction):
    somethingHappened=0
    firsttime=1
    for coloumn in range(4):
        if direction=='u':
            for row in range(2,0,-1):
                while(rows[row][coloumn] !=0 and (rows[row][coloumn]== rows[row+1][coloumn] or rows[row][coloumn]==rows[row-1][coloumn] or rows[row-1][coloumn] == 0) or (rows[row+1][coloumn]!=0 and rows[row][coloumn]==0)):
                    if rows[row][coloumn]==rows[row-1][coloumn] and rows[row][coloumn]!=0:
                        rows[row-1][coloumn] = rows[row][coloumn]*2
                        rows[row][coloumn]=0
                    elif rows[row][coloumn]== rows[row+1][coloumn] and rows[row][coloumn]!=0:
                        rows[row][coloumn]= rows[row+1][coloumn]*2
                        rows[row+1][coloumn]=0
                    elif rows[row-1][coloumn] == 0 and rows[row][coloumn]!=0:
                        rows[row-1][coloumn]= rows[row][coloumn]
                        rows[row][coloumn]=0
                    elif (rows[row+1][coloumn]!=0 and rows[row][coloumn]==0):
                        rows[row][coloumn]= rows[row+1][coloumn]
                        rows[row+1][coloumn]=0
                    else:
                        continue
                    somethingHappened=1
        if direction=='d':
            for row in range(1,3):
                while(rows[row][coloumn] !=0 and (rows[row][coloumn]== rows[row+1][coloumn] or rows[row][coloumn]==rows[row-1][coloumn] or rows[row+1][coloumn] == 0) or (rows[row-1][coloumn]!=0 and rows[row][coloumn]==0)):
                    print('thinking',row,coloumn)
                    if rows[row][coloumn]==rows[row-1][coloumn] and rows[row][coloumn]!=0:#checks if upper block is equal
                        rows[row][coloumn] = rows[row-1][coloumn]*2#adds itself to upper row
                        rows[row-1][coloumn]=0
                    elif rows[row][coloumn]== rows[row+1][coloumn] and rows[row][coloumn]!=0:#checks if lower block wants to add
                        rows[row+1][coloumn]= rows[row][coloumn]*2#adds lower block to itself
                        rows[row][coloumn]=0
                    elif rows[row+1][coloumn] == 0 and rows[row][coloumn]!=0:#checks if lower block is empty
                        rows[row+1][coloumn]= rows[row][coloumn]#moves itself to lower block
                        rows[row][coloumn]=0
                    elif (rows[row-1][coloumn]!=0 and rows[row][coloumn]==0):#checks if upper cell wants down
                        rows[row][coloumn]= rows[row-1][coloumn]
                        rows[row-1][coloumn]=0
                    else:
                        continue
                    somethingHappened=1#makes move valid

        if direction =='r':
            for row in rows:
                for unit in range(1,3):
                    while(row[unit]!=0 and (row[unit+1]==row[unit] or row[unit-1]==row[unit] or row[unit+1]==0) or (row[unit]==0 and row[unit-1]!=0)):
                        if row[unit]!=0 and row[unit+1]==row[unit]:#checks if right block is equal
                            row[unit+1]=row[unit]*2#adds itself with the right block
                            row[unit]=0
                        elif row[unit]!=0 and row[unit-1]==row[unit]:#checks if left block is equal
                            row[unit]=row[unit-1]*2#adds left block with itself
                            row[unit-1]=0
                        elif row[unit]!=0 and row[unit+1]==0:#checks if right block is empty
                            row[unit+1]=row[unit]#moves itself to the right block
                            row[unit]=0
                        elif (row[unit]==0 and row[unit-1]!=0):#checks if left block wants to move
                            row[unit]=row[unit-1]#moves left block to itself
                            row[unit-1]=0
                        else:
                            continue
                        somethingHappened=1 #makes move valid
        if direction =='l':
            for row in rows:
                for unit in range(2,0,-1):
                    while(row[unit]!=0 and (row[unit+1]==row[unit] or row[unit-1]==row[unit] or row[unit-1]==0) or (row[unit]==0 and row[unit+1]!=0)):
                        if row[unit]!=0 and row[unit+1]==row[unit]: #checks if the right unit is same
                            row[unit]=row[unit+1]*2 #adds value of right unit to itself
                            row[unit+1]=0
                        elif row[unit]!=0 and row[unit-1]==row[unit]:#checks if left unit is same
                            row[unit-1]=row[unit]*2#adds itself to left unit
                            row[unit]=0
                        elif row[unit]!=0 and row[unit-1]==0:#checks if it is free to move left
                            row[unit-1]=row[unit]
                            row[unit]=0
                        elif (row[unit]==0 and row[unit+1]!=0):#checks if right unit wants to move in
                            row[unit]=row[unit+1]
                            row[unit+1]=0
                        else:
                            continue
                        somethingHappened=1 #makes the move valid to add a new block
    
    if somethingHappened: #checks if move was valid
        addstuff(direction)
    render()
    return True
addstuff(random.choice(['l','r','u','d']))#adds a random block at start
render()
while True:
    if keyboard.is_pressed('s'):
        while keyboard.is_pressed('s'):
            continue
        if move('d'):
            continue
    if keyboard.is_pressed('d'):
        while keyboard.is_pressed('d'):
            continue
        if move('r'):
            continue
    if keyboard.is_pressed('a'):
        while keyboard.is_pressed('a'):
            continue
        if move('l'):
            continue
    if keyboard.is_pressed('w'):
        while keyboard.is_pressed('w'):
            continue
        if move('u'):
            continue
    if keyboard.is_pressed('q'):
        break