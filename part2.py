import part1 as thomNFA
from queue import Queue
from utils import utils

counter = 0

def checkUnique(list,elem):
    if(list.count(elem) >= 1):
        return False
    else:
        return True

def stateEquality(stateList1,stateList2):
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
    # newState = {"S" + str(counter) : newState}
    # DFA.update(newState)
    # if(isStartState == True):
    #     DFA["startingState"] = "S0"
    # counter+=1
    return newState
#NOTE: when reading output of epsilon closure please read carefully as it outputs key and state in a dictionory  

regex="(a|b)"

alphabet = []
# rudimentary system to get alphabet of regex
for c in regex:
    if(c.isalnum()):
        alphabet.append(c)

adam=thomNFA.makeNFA(regex)
allStatesJSON = utils.convertAllstates(thomNFA.AllStates)

allStates = utils.convertAllstatestoReg(allStatesJSON)

utils.drawNFA(allStatesJSON,"NFA")

DFA = dict()

startingState = allStates.get("startingState")

initState = epsilonClosure({startingState:allStates.get(startingState)},allStates)
for s in initState:
    print(s)
initState = stateMaker(initState,alphabet,DFA,True) # initState by this point contains the big State
bigStateList = [initState]

statesQueue = Queue(maxsize = 0)
statesQueue.put(initState)

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
            
print("bigStateList is :")


for s in bigStateList:
    print(s)








