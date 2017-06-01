import math
import random
#Read files
input = open('input.dat').read()
scroll = open('Scrolls.dat').read()
path = open('LevelMaps.dat').read()
#Get Vars from Input
splitInput = input.splitlines()
mapNum = int(splitInput[0])
scrollNum = int(splitInput[1])
portalLoc = int(splitInput[3])
actChips = list(splitInput[4])
conChips = list(splitInput[6])
purpleTrolls = []
orangeTrolls = []
#0: Red, 1: Green, 2: Blue
availableActs = []
#1 - 6 is Nx crystals, 7 is purple troll, 8 is orange troll
availableCons = []
totalActNum = len(actChips)
totalConNum = len(conChips)
actOrder = []
solved = False

#Set trolls
tempMap = path.split("MAP: " + str(mapNum))[1].splitlines()
for i in list(tempMap[2]):
    purpleTrolls.append(int(i))
for i in list(tempMap[3]):
    orangeTrolls.append(int(i))

for i in actChips:
    if i == 'R':
        availableActs.append(0)
    elif i == 'G':
        availableActs.append(1)
    elif i == 'B':
        availableActs.append(2)
    else:
        print("Error: Action Token Invalid")
        print(i)
        exit()

for i in conChips:
    if i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6':
        availableCons.append(int(i))
    elif i == 'P':
        availableCons.append(7)
    elif i == 'O':
        availableCons.append(8)
    else:
        print("Error: Condition Token Invalid")
        print(i)
        exit()

#print availableActs
#ADD CONDITION CHECKING!!!!!!!!!!!

#Moves curPos given a certain color. 0: Red, 1: Green, 2: Blue
#Returns -1 if not legal
def move(color, curPos):
    #Get List of legal moves from curPos
    #print color
    if color == 0:
        legalMoves = path.split("MAP: " + str(mapNum))[1].split("ENDOFMAP")[0].split("RED:")[1].split("END")[0].splitlines()
    elif color == 1:
        legalMoves = path.split("MAP: " + str(mapNum))[1].split("ENDOFMAP")[0].split("GREEN:")[1].split("END")[0].splitlines()
    else:
        legalMoves = path.split("MAP: " + str(mapNum))[1].split("ENDOFMAP")[0].split("BLUE:")[1].split("END")[0].splitlines()
    for x in legalMoves:
        if len(list(x)) > 1:
            if int(list(x)[0]) == curPos:
                #print curPos
                #print int(list(x)[1])
                return int(list(x)[1])
    return curPos
#Runs Scroll program
def runProgram(actSequence, conSequence):
    labels = []
    actColor = []
    conProg = []
    crystals = []
    past = []
    visited = 0
    crystalsFound = 0
    for x in range(len(actSequence)):
        actColor.append(availableActs[actSequence[x]])
    for x in range(len(conSequence)):
        conProg.append(availableCons[conSequence[x]])
    if splitInput[5] != "NONE":
        for x in range(len(list(splitInput[5]))):
            crystals.append(list(splitInput[5])[x])
    else:
        crystals = []
    curPos = int(splitInput[2])
    program = scroll.split("SCROLL: " + str(scrollNum))[1].split("ENDSCROLL")[0]
    progActTotal = int(program.split("ACT(")[1].split(")")[0])
    program = program.split("PATH")[1].splitlines()
    if progActTotal != totalActNum:
        print("Invalid # of Action Tokes")
        exit()
    step = 0
    while step < len(program):
        if "LBL" in program[step]:
            labels.append(step)
        step = step + 1
    step = 0
    while step < len(program):
        #print curPos
        #print program[step]

        if curPos in past:
            visited = visited + 1
        if visited >= 50:
            return -1
        if "STOP" in program[step]:
            if len(crystals) == 0:
                return curPos
            else:
                return -1
            return curPos
        elif "ACT" in program[step]:
            #print actColor
            color = actColor[int(program[step].split("ACT")[1])]
            curPos = move(color, curPos)
            if curPos == -1:
                return -1
            past.append(curPos)
            for x in crystals:
                if curPos == int(x):
                    crystals.remove(x)
                    crystalsFound = crystalsFound + 1
                    break
        elif "GOTO" in program[step]:
            step = labels[int(program[step].split("GOTO")[1])]

        elif "CON" in program[step]:
            conditionIndex = int(program[step].split("CON")[1])
            condition = int(conProg[conditionIndex])
            #If no, add one to step
            if condition < 7:
                if crystalsFound < condition:
                    step = step + 1
            elif condition == 7:
                if curPos not in purpleTrolls:
                    step = step + 1
            elif condition == 8:
                if curPos not in orangeTrolls:
                    step = step + 1
        step = step + 1
            #print str(curPos) + ":" + str(color)

counter = 0
actColors = []

def randomizeOrder(length):
    order = []
    for x in range(length):
        futureIndex = random.randrange(0, length)
        while futureIndex in order:
            futureIndex = random.randrange(0, length)
        order.append(futureIndex)
    return order



trialOrderActs = randomizeOrder(len(availableActs))
trialOrderCons = randomizeOrder(len(availableCons))
triedOrderActs = [trialOrderActs]
triedOrderCons = [trialOrderCons]


while not solved:
    #print triedOrderActs
    if runProgram(trialOrderActs, trialOrderCons) == portalLoc:
        solved = True
        #print runProgram(trialOrderActs, trialOrderCons)
    else:
        while trialOrderActs in triedOrderActs or trialOrderCons in triedOrderActs:
            trialOrderActs = randomizeOrder(len(availableActs))
            trialOrderCons = randomizeOrder(len(availableCons))
        triedOrderActs.append(trialOrderActs)
        triedOrderCons.append(trialOrderCons)
        #print triedOrderActs
        #print triedOrderCons

for x in range(len(trialOrderActs)):
    trialElement = availableActs[trialOrderActs[x]]
    string = "Act " + str(x) + " = "
    if trialElement == 0:
        string = string + "Red"
    elif trialElement == 1:
        string = string + "Green"
    else:
        string = string + "Blue"
    print string
for x in range(len(trialOrderCons)):
    trialElement = availableCons[trialOrderCons[x]]
    string = "Con " + str(x) + " = "
    if trialElement < 7:
        string = string + str(trialElement) + "x"
    elif trialElement == 7:
        string = string + "Purple"
    else:
        string = string + "Orange"
    print string
