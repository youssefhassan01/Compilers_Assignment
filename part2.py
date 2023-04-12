import part1 as thomNFA
from queue import Queue
from utils import utils
import json
import re


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
                if c in v and len(v[c]) != 0:
                    v[c] = Statenamesdict[v[c]]
                # remove unnecessary key characters
                if c in v and len(v[c]) == 0:
                    del v[c]

    return bigStateDict
# NOTE: when reading output of epsilon closure please read carefully as it outputs key and state in a dictionory


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
        if newState == None:
            return False    # not sure if this is correct
        # get StateGroup of newState
        verynewState_stateGroup = getStateGroup(newState, currStateGroups)
        if newState_stateGroup != verynewState_stateGroup:
            return False
    return True

# checks if there is another group to merge with
# returns the group to merge with


def checkOtherGroups(state, originalStateGroup, currStateGroups, alphabet):
    for stateGroup in currStateGroups:
        if stateGroup == originalStateGroup:
            continue
        # take any state from the group
        theOtherState = stateGroup["states"][0]
        flag = True
        for c in alphabet:
            newState = getnewState(state, c)
            theOtherStatenNewState = getnewState(theOtherState, c)

            # should the check here be on group or state? idk
            if newState != theOtherStatenNewState:
                flag = False
                break
                # if newState == None:
                #     continue
                # # get StateGroup of newState
                # newState_stateGroup = getStateGroup(newState, currStateGroups)
                # if newState_stateGroup != stateGroup:
                #     # check if there is another group to merge with
                #     for otherGroup in currStateGroups:
                #         if otherGroup != stateGroup:
                #             if checkOtherGroupMembers(newState_stateGroup, otherGroup, currStateGroups, c) == True:
                #                 return True
        if (flag == True):
            return stateGroup
    return None


def minimise(stateGroups, alphabet):
    oldStategroupSize = -1
    while oldStategroupSize != len(stateGroups):
        # StateGroups will be update in the loop so we need to make a copy of it
        # but CurrentStateGroups will not be updated during it
        currStateGroups = stateGroups.copy()
        changedStaeGroupsFlag = False
        for stateGroup in currStateGroups:
            # loop on each state in the state group
            # no need to check single element or empty group
            if (len(stateGroup["states"]) == 1):
                continue
            for state in stateGroup["states"]:
                # lol
                for c in alphabet:
                    newState = getnewState(state, c)
                    if newState == None:
                        continue
                    # get StateGroup of newState
                    newState_stateGroup = getStateGroup(
                        newState, stateGroups)
                    if newState_stateGroup != stateGroup:
                        # check if there is another group to merge with
                        # potentialMergeGroup = checkOtherGroups(
                        #     state, stateGroup, currStateGroups, alphabet)
                        potentialMergeGroup = checkOtherGroups(
                            state, stateGroup, stateGroups, alphabet)
                        if (potentialMergeGroup != None):
                            # merge with the other group
                            potentialMergeGroup["statenames"].append(
                                getStateName(state))
                            potentialMergeGroup["states"].append(state)
                            # remove state from old group
                            stateGroup["statenames"].remove(
                                getStateName(state))
                            stateGroup["states"].remove(
                                state)
                            break
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
                                state)
                            changedStaeGroupsFlag = True
                            break  # break out of the alphabet loop: no need to check for more characters
                # if changedStaeGroupsFlag == True:
                #     break  # break out of the state loop: to go and update the StateGroups
        oldStategroupSize = len(currStateGroups)
    # print("minimized thing is ")
    # print(stateGroups)
    # for thing in stateGroups:
    #     print(thing)
    return stateGroups

# puts minimized DFA in final format


def formatminimisedDFA(DFA, alphabet):

    # first Name all the Groupstates
    for i in range(len(DFA)):
        stateGroup = DFA[i]
        stateGroup["stateGroupName"] = 'S'+str(i)

    FinalStatsedict = {}
    for stateGroup in DFA:
        FinalStateform = {}
        for state in stateGroup["states"]:
            # determine if starting State
            stateInfo = list(state.values())[0]
            # for k, v in state.items():
            for k, v in stateInfo.items():
                if k == 'isStartingState':
                    FinalStateform["isStartingState"] = True
                if k == 'isTerminalState':
                    FinalStateform["isTerminalState"] = v

        newName = stateGroup["stateGroupName"]
        for c in alphabet:
            # print(list(stateGroup["states"][0].values()))
            firstState = list(stateGroup["states"][0].values())[0]
            # print(firstState)
            if c not in firstState.keys():
                continue
            newState = getnewState(stateGroup["states"][0], c)
            newStategroup = getStateGroup(newState, DFA)
            # FinalStateform[c] = getStateName(newStategroup)
            FinalStateform[c] = newStategroup["stateGroupName"]
        # del stateGroup["states"]
        # del stateGroup["statenames"]
        FinalStatsedict[newName] = FinalStateform

    # getting startingState
    veryFinalState = {}
    for k, v in FinalStatsedict.items():
        if 'isStartingState' in v.keys():
            veryFinalState['startingState'] = k
            break
    veryFinalState.update(FinalStatsedict)
    # print('printing loler in zewat')
    # for k, v in FinalStatsedict.items():
    #     print(k, v)
    print('printing loler in zewat')
    for k, v in veryFinalState.items():
        print(k, v)
    return veryFinalState


# regex = ""
# regex = input("Enter your regex: ")
regex = "ab(b|c)*d+"

# regex = "(abc|[a-z])"
# regex = "ab?cd?(ef|g)*"
# regex = "abc[g-h]*"
# regex = "ab$_"
# regex = "abc"
# regex = "(((a)(b)|(d))|(c))"
# regex = "ab|cd"
# regex = "((a)(b)|(c)(d))"
# regex = "(ab)|(cd)"
# regex = "(abc|3)"
# regex = "ab|c"
# regex = "(a)b|c"
# regex = "(a)(b)|c"
# regex="(((ab)|d)|c)"
# regex = "[a-h]*"
# regex = "[abc]"
# regex = "ab?"
# regex = "ab?cd?(ef|g)*"
# regex = "(a|b)*"
# regex = "(a|b)*abb"
# regex = "[a-d][a-d]"
# The main Test cases
# # regex = "ab(b|c)*d+"
# regex = "[a-zA-Z_$][a-zA-Z0-9_$]*"
# regex = "0|[1-9A-F][0-9A-F]*|[1-9a-f][0-9a-f]*"
# regex = "https?://(www.)?[a-zA-Z0-9-_].(com|org|net)"
# regex = "[1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]"

# don't forget to add re.compile and output errror

if (len(regex) == 0):
    print("Regex is empty")
    exit()


try:
    re.compile(regex)
except re.error:
    print("Non valid regex pattern")
    exit()


def extractchars(c1, c2):
    processed_range = ""
    for j in range(ord(c1)+1, ord(c2)):  # exclude c1 and c2
        processed_range += chr(j)
    print('processed range is ', processed_range)
    return processed_range


alphabet = []
# rudimentary system to get alphabet of regex
for i in range(len(regex)):
    c = regex[i]
    if (c == '-'):
        newchars = extractchars(regex[i-1], regex[i+1])
        for char in newchars:
            if checkUnique(alphabet, char) == True:
                alphabet.append(char)

    if (c not in '*+?|ඞ-[()]'):
        if checkUnique(alphabet, c) == True:
            alphabet.append(c)


# make NFA from part1
adam = thomNFA.makeNFA(regex)
allStatesJSON = utils.convertAllstates(thomNFA.AllStates)
allStates = utils.convertAllstatestoReq(allStatesJSON)

with open("NFA.json", "w") as outfile:
    json.dump(allStates, outfile, indent=4)


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

with open("DFA.json", "w") as outfile:
    json.dump(allStates, outfile, indent=4)

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
StateGroups = []
if (len(nonTerminalStates["statenames"]) == 0):
    StateGroups = [TerminalStates]
elif (len(TerminalStates["statenames"]) == 0):
    StateGroups = [nonTerminalStates]
elif (len(TerminalStates["statenames"]) != 0 and len(nonTerminalStates["statenames"]) != 0):
    StateGroups = [nonTerminalStates, TerminalStates]


minimisedDFA = minimise(StateGroups, alphabet)

# print('minimized DFA is ')
# for state in minimisedDFA:
#     print(state)


format_minDFA = formatminimisedDFA(minimisedDFA, alphabet)

for state in format_minDFA:
    print(state)

utils.DrawDFA(format_minDFA, alphabet)
with open("MinimizedDFA.json", "w") as outfile:
    json.dump(format_minDFA, outfile, indent=4)
