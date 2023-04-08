import part1 as thomNFA
from queue import Queue
from utils import utils



def checkUnique(list,elem):
    #check if element is unique
    if(list.count(elem) >= 1):
        return False
    else:
        return True

def stateEquality(stateList1,stateList2):
    #checks if state is unique or not
    if len(stateList1) != len(stateList2):
        return False
    else:
        for i in range(len(stateList1)):
            foundState = False
            state1name = list(stateList1[i].keys())[0]
            print(state1name)
            for j in range(len(stateList2)):
                state2name = list(stateList2[j].keys())[0]
                if(state1name == state2name):
                    foundState = True
                    break
            if not foundState:
                return False
        return True


# gets epsilon clsoure of passed state using allStates after conversion to json  
def epsilonClosure(state,allStates):
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
                if(checkUnique(newState,{i:allStates.get(i)})):
                    findEpsilon.put(allStates.get(i))
                    newState.append({i:allStates.get(i)})
    #returns all states in this epsilon closure
    return newState


def move(state,char,allStates):
    # allStates is in Required format
    stateList=[]
    for key,value in state.items():
        if char in value:
            nextState = value
            for i in nextState[char]:
                stateList = epsilonClosure({i:allStates.get(i)},allStates)
    return stateList

def stateMaker(stateList,alphabet,DFA,isStartState=False):
    # global counter
    newState = dict()
    newState["stateList"]=stateList
    
    for c in alphabet:
        newState[c]=""
    # newState = { : newState}
    # DFA.update(newState)
    # if(isStartState == True):
    #     DFA["startingState"] = "S0"
    # counter+=1
    return newState

def dfaNoConnection(bigStateList):
    statesQueue = Queue(maxsize = 0)
    statesQueue.put(bigStateList[0])
    while not statesQueue.empty():
        currState = statesQueue.get()
        currStateList = currState["stateList"]
        for c in alphabet:
            newStateList = []
            for state in currStateList:
                newStateListInput = move(state,c,allStates)
                for x in newStateListInput:
                    if x not in newStateList:
                        newStateList.append(x)
            newStateList = stateMaker(newStateList,alphabet,DFA,False)
            if len(newStateList["stateList"]) == 0:
                continue
            stateExists = False
            for s in bigStateList: #checks if we found this state before
                if stateEquality(s["stateList"],newStateList["stateList"]) == True:
                    stateExists = True
                    break
            if not stateExists: # checks if we are adding this new state or not
                bigStateList.append(newStateList) # newStateList by this point contains the big State
                statesQueue.put(newStateList)

def dfaConnectorAndFormatter(bigStateList):
    counter = 0
    # Creates New Names for New states
    for state in bigStateList:
        state["stateName"] = "S" + str(counter)
        counter += 1
    # embbeds stateNames into each state for later use 
    bigStateListstates = dict()
    for state in bigStateList:
        currStateList = state["stateList"]
        reqState = list()
        for s in currStateList:
            for k , v in s.items():
                reqState.append(k)
        # this dictionary gives you bigstate as a key and its value are the NFA states contained inside for easier access
        bigStateListstates[state["stateName"]]=reqState
    # find which input allows you to go to a desired state
    for state in bigStateList:
        currStateList = state['stateList']
        for s in currStateList:
            # accesses stateList and splits keys and values to allow access  
            for k,v in s.items():
                for c in alphabet:
                    if c in v:
                        reqState = v[c][0]
                        # finds which input leads to which state
                        for i,j in bigStateListstates.items():
                            if reqState in j:
                                state[c] = i
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
    for s in bigStateList:
        del s['stateList']
        bigStateDict[s['stateName']] = s
    # Removes embbeded statName in the value
    for k,v in bigStateDict.items():
        del v['stateName']
    return bigStateDict
#NOTE: when reading output of epsilon closure please read carefully as it outputs key and state in a dictionory  

def minimise(currStates, DFA, alphabet):
    minimiseQueue = Queue(maxsize=0)
    if len(currStates) != 0:
        minimiseQueue.put(currStates[0])

    counter = 0
    splitState = []
    while not minimiseQueue.empty():
        #split nonsimilar states into seperate entites
        currState = minimiseQueue.get()
        for c in alphabet:
            value=list(currState.values())[0]
            if c in value:
                comparisonState = value[c]
                for s in currStates:
                    for k,v in s.items():
                        if c in v:
                            if comparisonState != v[c]:
                                splitState.append(currState)
                                currStates.remove(currState)
                                counter = 0
                                minimiseQueue.put(currStates[counter])
    #update starting state before merging
    newStartingState = ""
    for state in currStates:
        foundStart = False
        for k,v in state.items():
            if k == DFA['startingState']:
                newStartingState = list(currStates[0].keys())[0]
                foundStart = True
                break
        if foundStart == True:
            break
    #update connection of split states before merging merged states
    for state in splitState:
        for k,v in state.items():
            for c in alphabet:
                if c in v:
                    reqState = v[c]
                for s in currStates:
                    for i,j in s.items():
                        if reqState == i:
                            v[c] = list(currStates[0].keys())[0]
    mergedState=currStates[0]
    return mergedState,splitState,newStartingState

regex="(a|b)"

alphabet = []
# rudimentary system to get alphabet of regex
for c in regex:
    if(c.isalnum()):
        if checkUnique(alphabet,c) == True:
            alphabet.append(c)

# make NFA from part1
adam=thomNFA.makeNFA(regex)
allStatesJSON = utils.convertAllstates(thomNFA.AllStates)
allStates = utils.convertAllstatestoReg(allStatesJSON)


utils.drawNFA(allStatesJSON,"NFA")
DFA = dict()
startingState = allStates.get("startingState")

# initialise first State
initState = epsilonClosure({startingState:allStates.get(startingState)},allStates)
initState = stateMaker(initState,alphabet,DFA,True) # initState by this point contains the big State
bigStateList = [initState]

dfaNoConnection(bigStateList)
DFA=dfaConnectorAndFormatter(bigStateList)

nonTerminalStates = []
TerminalStates = []

for k,v in DFA.items():
    if v['isTerminalState'] == True:
        TerminalStates.append({k:v})
    else:
        nonTerminalStates.append({k:v})

mergedNonTerminal , splitNonTerminal , newStartingStateTerm = minimise(nonTerminalStates,DFA,alphabet)
mergedTerminal , splitTerminal , newStartingStateNonTerm  = minimise(TerminalStates,DFA,alphabet)

minimisedDFA = dict()

if newStartingStateTerm != "":
    minimisedDFA["startingState"] = newStartingStateTerm
elif newStartingStateNonTerm != "":
    minimisedDFA["startingState"] = newStartingStateNonTerm
else:
    minimisedDFA["startingState"] = DFA["startingState"]

for s in splitNonTerminal:
    minimisedDFA.update(s)
for s in splitTerminal:
    minimisedDFA.update(s)

minimisedDFA.update(mergedNonTerminal)
minimisedDFA.update(mergedTerminal)













