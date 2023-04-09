import part1 as thomNFA
from queue import Queue
from utils import utils


def checkUnique(list, elem):
    # check if element is unique
    if (list.count(elem) >= 1):
        return False
    else:
        return True


def stateEquality(stateList1, stateList2):
    # checks if state is unique or not
    if len(stateList1) != len(stateList2):
        return False
    else:
        for i in range(len(stateList1)):
            foundState = False
            state1name = list(stateList1[i].keys())[0]
            # print(state1name)
            for j in range(len(stateList2)):
                state2name = list(stateList2[j].keys())[0]
                if (state1name == state2name):
                    foundState = True
                    break
            if not foundState:
                return False
        return True


# gets epsilon clsoure of passed state using allStates after conversion to json
def epsilonClosure(state, allStates):
    newState = list()
    findEpsilon = Queue(maxsize=0)
    # Split passed state to key and value and add to Queue
    key = list(state.keys())
    key = key[0]
    value = list(state.values())
    value = value[0]
    findEpsilon.put(value)
    newState.append(state)
    while not findEpsilon.empty():
        # walk through each state in epsilon of current state if any epsilon list exists
        x = findEpsilon.get()
        if "epsilon" in x:
            for i in x['epsilon']:
                # since there can be no sets of dictitionary i made a list with a check to make sure it is unique and
                # and not keep returning it to queue or state
                if (checkUnique(newState, {i: allStates.get(i)})):
                    findEpsilon.put(allStates.get(i))
                    newState.append({i: allStates.get(i)})
    # returns all states in this epsilon closure
    return newState


def move(state, char, allStates):
    # allStates is in Required format
    stateList = []
    for key, value in state.items():
        if char in value:
            nextState = value
            for i in nextState[char]:
                stateList = epsilonClosure({i: allStates.get(i)}, allStates)
    return stateList


statecounter = 0


def stateMaker(stateList, alphabet, DFA, isStartState=False):
    global statecounter
    newState = dict()
    newState["stateList"] = stateList
    newState["bigStateName"] = "S" + str(statecounter)
    statecounter += 1

    for c in alphabet:
        newState[c] = ""
    # newState = { : newState}
    # DFA.update(newState)
    # if(isStartState == True):
    #     DFA["startingState"] = "S0"
    # counter+=1
    return newState


def makeDFA(bigStateList):
    statesQueue = Queue(maxsize=0)
    statesQueue.put(bigStateList[0])
    while not statesQueue.empty():
        currState = statesQueue.get()  # currBigState
        currStateList = currState["stateList"]
        for c in alphabet:
            newStateList = []
            for state in currStateList:
                newStateListInput = move(state, c, allStates)
                for x in newStateListInput:
                    if x not in newStateList:
                        newStateList.append(x)
            newStateList = stateMaker(newStateList, alphabet, DFA, False)
            # by this point newStaeList contains the big state
            if len(newStateList["stateList"]) == 0:
                continue
            # assume new
            stateExists = False
            stateToConnectto = newStateList
            for s in bigStateList:  # checks if we found this state before
                if stateEquality(s["stateList"], newStateList["stateList"]) == True:
                    stateExists = True
                    stateToConnectto = s
                    break
            currState[c] = stateToConnectto["bigStateName"]
            if not stateExists:  # checks if we are adding this new state or not
                # newStateList by this point contains the big State
                bigStateList.append(newStateList)
                statesQueue.put(newStateList)


def dfaFormatter(bigStateList):
    counter = 0
    Statenamesdict = dict()
    # sanitize statename
    # print('bigStateList: ', bigStateList)
    for state in bigStateList:
        oldStateName = state['bigStateName']
        Statenamesdict[oldStateName] = "S" + str(counter)
        state['bigStateName'] = "S" + str(counter)
        counter += 1
        # an update all old references to new state name will happen later

        # print(state)

    # marks which states are terminal
    for state in bigStateList:
        currStateList = state['stateList']
        for s in currStateList:
            foundState = False
            for k, v in s.items():
                if v['isTerminalState'] == True:
                    state['isTerminalState'] = True
                    foundState = True
                    break
                else:
                    state['isTerminalState'] = False
            if foundState == True:
                break
    # remove stateList and make stateName the key in the final Dictionary
    bigStateDict = dict()
    # adds startingState to get the right format
    # print(bigStateList)
    for state in bigStateList:
        if state.get('isStartingState') and state['isStartingState'] == True:
            bigStateDict['startingState'] = state['bigStateName']
            break
    for s in bigStateList:
        del s['stateList']
        bigStateDict[s['bigStateName']] = s
    # Removes embbeded statName in the value
    for k, v in bigStateDict.items():
        if k != 'startingState':
            del v['bigStateName']
    # update all old references to new state name
    for k, v in bigStateDict.items():
        if k != 'startingState':
            for c in alphabet:
                if c in v:
                    v[c] = Statenamesdict[v[c]]
    return bigStateDict
# NOTE: when reading output of epsilon closure please read carefully as it outputs key and state in a dictionory

# region old code
# def minimise(DFAlist, alphabet):
#     minimiseQueue = Queue(maxsize=0)
#     if len(currStates) != 0:
#         minimiseQueue.put(currStates[0])
#     counter = 0
#     splitState = []
#     while not minimiseQueue.empty():
#         # split nonsimilar states into seperate entites
#         currState = minimiseQueue.get()
#         for c in alphabet:
#             value = list(currState.values())[0]
#             if c in value:
#                 comparisonState = value[c]
#                 for s in currStates:
#                     for k, v in s.items():
#                         if c in v:
#                             if comparisonState != v[c]:
#                                 splitState.append(currState)
#                                 currStates.remove(currState)
#                                 counter = 0
#                                 minimiseQueue.put(currStates[counter])
#     # update starting state before merging
#     newStartingState = ""
#     for state in currStates:
#         # print('mysate is ', state)
#         foundStart = False
#         for k, v in state.items():
#             if k == DFA['startingState']:
#                 newStartingState = list(currStates[0].keys())[0]
#                 foundStart = True
#                 break
#         if foundStart == True:
#             break
#     # update connection of split states before merging merged states
#     for state in splitState:
#         for k, v in state.items():
#             for c in alphabet:
#                 if c in v:
#                     reqState = v[c]
#                 for s in currStates:
#                     for i, j in s.items():
#                         if reqState == i:
#                             v[c] = list(currStates[0].keys())[0]
#     mergedState = currStates[0]
#     return mergedState, splitState, newStartingState

# def minimise(DFAlist, alphabet):
#     stateQueue = []
#     counter = 0
#     stateQueue.append(DFAlist[counter])
#     change = True
#     while stateQueue and change:
#         currState = stateQueue.pop(0)
#         currStateValue = currState[1]
#         similarStates = []
#         for state in DFAlist:
#                 areSameState = True
#                 for c in alphabet:
#                     if state[0] == currState[0]:
#                         break
#                     elif state[1][c] != currStateValue[c] or state[1]['isTerminalState'] != currStateValue['isTerminalState']:
#                         areSameState = False
#                         break
#                 if areSameState == True:
#                     similarStates.append(state)
#                 else:
#                     if not state in stateQueue:
#                         stateQueue.append(state)
#         if similarStates:
#             if len(similarStates) > 1:
#                 for s in DFAlist:
#                     if s in similarStates:
#                         DFAlist.remove(s)
#                 newValue = dict()
#                 statesToBeConverted = []
#                 for s in similarStates:
#                     statesToBeConverted.append(s[0])
#                 for c in alphabet:
#                     for state in DFAlist:
#                         if state[1][c] in statesToBeConverted:
#                             stateQueue.remove(state)
#                             state[1][c] = similarStates[0][0]
#                             stateQueue.append(state)
#                     for s in similarStates:
#                         if s[1][c] in statesToBeConverted:
#                             s[1][c] = similarStates[0][0]
#                 for c in alphabet:
#                     newValue[c] = similarStates[0][1][c]
#                 newValue['isTerminalState'] = similarStates[0][1]['isTerminalState']
#                 if "isStartingState" in similarStates[0][1]:
#                     newValue['isStartingState'] = similarStates[0][1]['isStartingState']
#                 newState = (similarStates[0][0],newValue)
#                 DFAlist.append(newState)
# endregion


def getStatefromName(stateName):
    global DFA
    for k, v in DFA.items():
        if k == stateName:
            return {k: v}
    return None

# does this actually work ?


def getnewState(state, char):
    global allStates
    for k, v in state.items():
        if k != 'isStartingState' and k != 'isTerminalState' and char in v:
            stateName = v[char]
            return getStatefromName(stateName)

    return None


def getStateGroup(state, stateGroups):
    for s in stateGroups:
        for k, v in state.items():
            if k != 'isStartingState' and k != 'isTerminalState' and k in s["statenames"]:
                return s
    return None


def getStateName(state):
    for k, v in state.items():
        if k != 'isStartingState' and k != 'isTerminalState':
            return k


def checkOtherGroupMembers(newState_stateGroup, stateGroup, currStateGroups, character):
    for state in stateGroup["states"]:

        newState = getnewState(state, character)
        # get StateGroup of newState
        verynewState_stateGroup = getStateGroup(newState, currStateGroups)
        if newState_stateGroup != verynewState_stateGroup:
            return False
    return True


def minimise(stateGroups, alphabet):
    oldStategroupSize = -1
    while oldStategroupSize != len(stateGroups):
        # StateGroups will be update in the loop so we need to make a copy of it
        # but CurrentStateGroups will not be updated during it
        currStateGroups = stateGroups.copy()
        for stateGroup in currStateGroups:
            # loop on each state in the state group
            if (len(stateGroup["states"]) == 1):  # no need to check single element
                continue
            for state in stateGroup["states"]:
                for c in alphabet:
                    newState = getnewState(state, c)
                    # get StateGroup of newState
                    newState_stateGroup = getStateGroup(
                        newState, stateGroups)
                    if newState_stateGroup != stateGroup:  # ya rab el 7etta dee t4t8l
                        # first check if the rest of group members go to the same newState_stateGroup
                        # if they do then don't make a new group
                        if (checkOtherGroupMembers(newState_stateGroup, stateGroup, currStateGroups, c) == False):
                            # make new state group
                            newGroupofState = {"statenames": [getStateName(
                                state)], "states": [state]}
                            stateGroups.append(newGroupofState)
                            # remove state from old group
                            stateGroup["statenames"].remove(
                                getStateName(state))
                            stateGroup["states"].remove(
                                state)  # ya rab dee t4t8l
        oldStategroupSize = len(currStateGroups)
    # print("minimized thing is ")
    # print(stateGroups)
    # for thing in stateGroups:
    #     print(thing)
    return stateGroups


regex = "(a|b)*abb"
# regex = "(a|b)*"
# regex = "(a|b)*abb"

alphabet = []
# rudimentary system to get alphabet of regex
for c in regex:
    if (c.isalnum()):
        if checkUnique(alphabet, c) == True:
            alphabet.append(c)

# make NFA from part1
adam = thomNFA.makeNFA(regex)
allStatesJSON = utils.convertAllstates(thomNFA.AllStates)
allStates = utils.convertAllstatestoReg(allStatesJSON)


utils.drawNFA(allStatesJSON, "NFA")
DFA = dict()
startingState = allStates.get("startingState")

# initialise first State
initState = epsilonClosure(
    {startingState: allStates.get(startingState)}, allStates)
initState = stateMaker(initState, alphabet, DFA, True)
# initState by this point contains the big State
initState["isStartingState"] = True
bigStateList = [initState]

makeDFA(bigStateList)
# print('printing after DFA no connection: ')
# for key in bigStateList:
#     print(key)
DFA = dfaFormatter(bigStateList)

# print('intermedietly, bigStateList is: ', bigStateList)
# print('intermedietly, bigStateList is: ', DFA)
# print('intermedietly, bigStateList is: ')
print('printing after DFA Formatter: ')
for key, value in DFA.items():
    print(key, value)


# let state group be of form {states: {{S1:bla bla}, {S2:bla bla}}, statenames: ["S1", "S2"]}

# minimization
nonTerminalStates = {"states": [], "statenames": []}
TerminalStates = {"states": [], "statenames": []}


for k, v in DFA.items():
    if k != 'startingState' and v['isTerminalState'] == True:
        TerminalStates["states"].append({k: v})
        TerminalStates["statenames"].append(k)
    else:
        if k != 'startingState':
            nonTerminalStates["states"].append({k: v})
            nonTerminalStates["statenames"].append(k)

# print('nonTerminalStates is: ', nonTerminalStates)
# print('TerminalStates is: ', TerminalStates)

# keda we have the starting 2 groups

StateGroups = [nonTerminalStates, TerminalStates]

minimisedDFA = minimise(StateGroups, alphabet)

print('minimized DFA is ')
for state in minimisedDFA:
    print(state)


def formatminimisedDFA():
    pass
