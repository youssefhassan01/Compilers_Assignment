import part1 as thomNFA
from queue import Queue
from utils import utils

def epsilonClosure(state,AllStates):
    newState = set()
    findEpsilon = Queue(maxsize=0)
    findEpsilon.put(state)
    while not findEpsilon.empty():
        x = findEpsilon.get()
        if "epsilon" in x.stateDict:
            for i in x.stateDict['epsilon']:
                y = AllStates.get("")
                findEpsilon.put(i)
        newState.add(x)
    return newState


regex="a|b"
adam=thomNFA.makeNFA(regex)

alphabet = []

allStates = utils.convertAllstates(thomNFA.AllStates)
utils.drawNFA(allStates,"NFA")

for s,k in allStates:
    print(s)

for c in regex:
    if(c.isalnum()):
        alphabet.append(c)

startingStates = []
for s,k in allStates.items():
    if("isStartState" in k.stateDict):
        if(s.stateDict['isStartState'] == True):
            startingStates.append(s)

initState=epsilonClosure(startingStates)

print(initState)








