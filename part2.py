import part1 as thomNFA
from queue import Queue
from utils import utils

def checkUnique(list,elem):
    if(list.count(elem) >= 1):
        return False
    else:
        return True


# gets epsilon clsoure of passed state using allStates after conversion to json  
def epsilonClosure(state,allStates,isStart=True):
    newState = list()
    findEpsilon = Queue(maxsize=0)
    # Split passed state to key and value and add to Queue
    key = list(state.keys())
    key = key[0]
    value = list(state.values())
    value = value[0]
    findEpsilon.put(value)
    if isStart == True:
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

#TODO: function that accepts all alphabets and check for their epsilon closure
#TODO: function that assembles DFA states !!! don't do this alone ya joe

#NOTE: when reading output of epsilon closure please read carefully as it outputs key and state in a dictionory  

regex="(a|b)"
adam=thomNFA.makeNFA(regex)

alphabet = []

allStates = utils.convertAllstates(thomNFA.AllStates)
utils.drawNFA(allStates,"NFA")

# rudimentary system to get alphabet of regex
# for c in regex:
#     if(c.isalnum()):
#         alphabet.append(c)

startingState = allStates.get("startingState")

initState=epsilonClosure({startingState:allStates.get(startingState)},allStates)

print(initState)








