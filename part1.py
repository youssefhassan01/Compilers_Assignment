import re


class state:
    # here class varialbe only (static)
    counter = 0  # counter of created states

    def __init__(self, tState=False):
        self.stateDict = dict()
        self.stateDict["isTerminalState"] = tState
        self.name = "S" + str(state.counter)
        print('my name is ', self.name)
        # if (state.counter == 0):
        #     self.stateDict["isStartingState"] = 1

        state.counter += 1
        global AllStates
        AllStates.append(self)

    def addTransition(self, otherstate, transitionString):
        self.stateDict[otherstate.name] = transitionString

    def removeTransition(self, otherstate):
        self.stateDict.pop(otherstate.name)

    def __str__(self):
        print("{", self.name, ":")
        print(self.stateDict)
        print("}")
        return ''


class superstate:
    # counter = 0  # counter of created states
    def __init__(self, startState, endState):
        self.startState = startState
        self.endState = endState
        self.endState.stateDict["isTerminalState"] = True

    def __str__(self):
        print(self.startState)
        print(self.endState)
        return ''


recursioncounter = 0

# gets string in form of something "(something)"


def getIndexEndingBrack(stringInput, bracket):
    if (bracket == '('):
        OpenBracket = '('
        ClosingBracket = ')'
    else:
        OpenBracket = '['
        ClosingBracket = ']'
    counter = 1
    index = 1
    while (counter != 0):
        if (stringInput[index] == OpenBracket):
            counter += 1
        elif (stringInput[index] == ClosingBracket):
            counter -= 1
        index += 1
    return index-1


def ClassRangeLogic(regexInput):
    pass


# [expressions, operations]

# expressions = string | operations(expression)
# operations = functions(expressions)
superstate_stack = []
AllStates = []


def concatLogic():
    global superstate_stack

    if (len(superstate_stack) > 1):
        print("Concatenated")
        ss2 = superstate_stack.pop()
        ss1 = superstate_stack.pop()
        # either this
        # ss1.endState.stateDict["isTerminalState"] = False
        # ss1.endState.addTransition(ss2.startState, "epsilon")
        # newSuperState = superstate(ss1.startState, ss2.endState)

        # or this (in slides)
        # ss2.startState = dict()
        ss1.endState.addTransition(
            ss2.endState, ss2.startState.stateDict[ss2.endState.name])
        # ss1.endState.removeTransition(ss2.startState)
        AllStates.remove(ss2.startState)
        ss2.startState = dict()
        newSuperState = superstate(ss1.startState, ss2.endState)
        superstate_stack.append(newSuperState)


# makeNFAcurrIndex = 0


def makeNFA(regexInput, contextindex=0):
    global makeNFAcurrIndex
    global NFA
    global superstate_stack
    global recursioncounter
    # if (regexInput == ""):
    #     return NFA
    if (contextindex == len(regexInput)):
        return NFA
    c = regexInput[contextindex]
    # Grouping
    if (c == "("):
        # print('extracted string in brackets is', regexInput[contextindex:])
        # passes string of form    "(something)"
        index = getIndexEndingBrack(regexInput[contextindex:], '(')
        # print(regexInput[1:index])
        recursioncounter += 1

        # get expression inside bracket
        # print('index is ', index, 'therefore the new regex ...')
        # mfee4 -1, excluded by default
        newregexInput = regexInput[contextindex+1:index]

        # print("new input is ", newregexInput)
        # parese new expression
        makeNFA(newregexInput)
        # parse from the beginning of the ending bracket
        # print(regexInput[index:])
        makeNFA(regexInput[index+1:])  # skip the bracket
        return
    if (c == "|"):
        # call next expression first
        makeNFA(regexInput, contextindex+1)
        # handle pipe logic
        print("found | at contextindex= ", contextindex)
        ss2 = superstate_stack.pop()
        ss1 = superstate_stack.pop()

        newStartState = state()
        newStartState.stateDict["epsilon"] = [ss1.startState.name]
        newStartState.stateDict["epsilon"].append(ss2.startState.name)

        newEndState = state()
        ss1.endState.stateDict["epsilon"] = newEndState.name
        ss2.endState.stateDict["epsilon"] = newEndState.name
        ss1.endState.stateDict["isTerminalState"] = False
        ss2.endState.stateDict["isTerminalState"] = False

        newSuperState = superstate(newStartState, newEndState)
        superstate_stack.append(newSuperState)
        # concatLogic()

    if (c == '*'):
        makeNFA(regexInput[1:])
        print("found *")

    if (c == '+'):
        makeNFA(regexInput[1:])
        print("found +")

    if (c == '?'):
        makeNFA(regexInput[1:])
        print("found ?")

    # range or group
    if (c == '['):
        index = getIndexEndingBrack(regexInput, '[')
        # print(regexInput[1:index])
        recursioncounter += 1
        newregexInput = regexInput[1:index-1]
        # print(newregexInput)
        ClassRangeLogic(newregexInput)
        makeNFA(regexInput[index:])
        return
    # makeNFA(regexInput[], NFA)
    if (c.isalnum()):  # do we need to add other characters here ?
        print("found letter/num")
        # make 2 states
        firstState = state()
        secondState = state()
        firstState.addTransition(secondState, c)
        # print("namaywa", firstState.name)
        # print(NFA)
        Superstate = superstate(firstState, secondState)
        superstate_stack.append(Superstate)
        if (contextindex != 0):
            previous_c = regexInput[contextindex-1]
            # print(previous_c)
            if (previous_c.isalnum()):
                concatLogic()
        makeNFA(regexInput, contextindex+1)

# how does our function handle abc? (da m3nah concatenation)
# abc
# (abc|[a-z])


# alpha.(   && alpha .[
# ).alpha|(
# myind = getIndexEndingBrack("(cd)", "(")
# print("myind is ", myind)

NFA = {}
# NFA = makeNFA("((ab|d)|c)", NFA)
# makeNFA("(((a)(b)|(d))|(c))")
# makeNFA("abc")  # works
# makeNFA("ab|cd")
makeNFA("(ab)|(cd)")  # error
# makeNFA("(abc|3)")
# print(superstate_stack[0].startState)
# print(superstate_stack[0].endState)
# print(superstate_stack[0])
# print(AllStates)
for s in AllStates:
    print(s)
# print(superstate_stack[1])

# A[1:3] starts from 1 really but excludes the 3
# A = "Joseph"
# print(A[1:])
# print(A[1:3])
# Regex = input("Enter Regex:")

# size=len(Regex)

# Regex = '[(hi)-z]'

# try:
#     re.compile(Regex)
# except re.error:
#     print("Non valid regex pattern")
#     exit()

# 1. Required scope for the input regular expressions:
#   - Alternation a|b
#   - Concatenation ab
#   - 1 or more a*
#   - 0 or more a+
#   - Optional a?
#   - Character/number classes [abc] or [345]
#   - Ranges [a-c] or [0-5]
#   - Brackets for grouping ()
# 2. You can use any third-party library to check the validity of the input regular expression.
# 3. You can use any third-party library to help you draw a diagram of your FSM and deal with it as you like, as long as the JSON output file is as expected and stated in the assignment document.
