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

    def appendToEpsilon(self, otherstate):
        if (self.stateDict.get("epsilon")):
            self.stateDict["epsilon"].append(otherstate.name)
            return
        self.stateDict["epsilon"] = [otherstate.name]


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

# [expressions, operations]
# expressions = string | operations(expression)
# operations = functions(expressions)
superstate_stack = []
AllStates = []


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


def pipeLogic():
    ss2 = superstate_stack.pop()
    ss1 = superstate_stack.pop()

    newStartState = state()
    newStartState.appendToEpsilon(ss1.startState)
    newStartState.appendToEpsilon(ss2.startState)

    newEndState = state()
    ss1.endState.appendToEpsilon(newEndState)
    ss2.endState.appendToEpsilon(newEndState)
    ss1.endState.stateDict["isTerminalState"] = False
    ss2.endState.stateDict["isTerminalState"] = False

    newSuperState = superstate(newStartState, newEndState)
    superstate_stack.append(newSuperState)


def RangeLogic(regexInput, notFirstRange):
    print("Handling range", regexInput)

    firstState = state()
    secondState = state()
    firstState.addTransition(secondState, regexInput)
    # print("namaywa", firstState.name)
    # print(NFA)
    Superstate = superstate(firstState, secondState)
    superstate_stack.append(Superstate)

    # insert pipelogic here
    if (notFirstRange):
        pipeLogic()


def concatLogic(previouscharacter):
    if (not previouscharacter.isalnum() and not previouscharacter in ')]+*?'):
        return
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


def ClassRangeLogic(regexInput, previouscharacter):

    # find - (the dash) and remove it together with surrounding characters
    notFirstRange = False
    # bootstrap the while loop by setting it to something other than -1
    dashIndex = 1
    # remove all ranges
    while (dashIndex != -1):
        dashIndex = regexInput.find('-')
        if (dashIndex != -1):
            RangeLogic(regexInput[dashIndex-1:dashIndex+2], notFirstRange)
            # print(regexInput[dashIndex-1:dashIndex+2])
            # regexInput.replace(regexInput[dashIndex-1:dashIndex+2], '')
            regexInput = regexInput[:dashIndex-1] + regexInput[dashIndex+2:]
            notFirstRange = True
            print('new replaced regex input is ', regexInput)
    # what remains is the class logic
    if (len(regexInput) == 0):
        return
    counter = 0
    for i in range(1, len(regexInput)):  # from second position to before last character
        print('lol', i)
        regexInput = regexInput[:i+counter] + '|' + regexInput[i+counter:]
        counter += 1

    # if (notFirstRange):
    #     regexInput = '|'+regexInput
    print('class regexinput is ', regexInput)
    makeNFA(regexInput)

    # or the classes with the ranges
    if (notFirstRange):
        pipeLogic()
    # print(previous_c)
    # if (previouscharacter.isalnum() or previouscharacter in ')]+*?'):
    #     concatLogic()
    # # one more call here because it returns outside
    # concatLogic(previouscharacter)


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
        print('extracted string in brackets is', regexInput[contextindex:])
        # passes string of form    "(something)"
        index = getIndexEndingBrack(regexInput[contextindex:], '(')
        # print(regexInput[1:index])
        recursioncounter += 1

        # get expression inside bracket
        # print('index is ', index, 'therefore the new regex ...')
        # print('regexin is ', regexInput)
        # print('regexin is ', regexInput)
        # mfee4 -1, excluded by default
        newregexInput = regexInput[contextindex+1:contextindex+index]

        # print("new input is ", newregexInput)
        # parese new expression in the brackets
        makeNFA(newregexInput)
        # concatenate the brackets states
        if (contextindex != 0):
            previous_c = regexInput[contextindex-1]
            concatLogic(previous_c)
        # parse from the beginning of the ending bracket
        # print(regexInput[index:])
        makeNFA(regexInput[index+1:])  # skip the bracket
        return

    # range or group
    if (c == '['):
        index = getIndexEndingBrack(regexInput[contextindex:], '[')
        # print(regexInput[1:index])
        recursioncounter += 1
        newregexInput = regexInput[contextindex+1:contextindex+index]
        previouscharacter = regexInput[contextindex -
                                       1] if (contextindex > 0) else ''
        print('previouscharacter is ', previouscharacter)
        # print(newregexInput)
        ClassRangeLogic(newregexInput, previouscharacter)
        if (contextindex != 0):
            previous_c = regexInput[contextindex-1]
            concatLogic(previous_c)
        makeNFA(regexInput[index+1:])  # skip the bracket
        return

    if (c == "|"):
        # call next expression first
        makeNFA(regexInput, contextindex+1)
        # handle pipe logic
        print("found | at contextindex= ", contextindex)
        pipeLogic()
        # CHECKKK
        # not sure 5ales
        if (contextindex != 0):
            previous_c = regexInput[contextindex-1]
            concatLogic(previous_c)
        # ss2 = superstate_stack.pop()
        # ss1 = superstate_stack.pop()

        # newStartState = state()
        # newStartState.appendToEpsilon(ss1.startState)
        # newStartState.appendToEpsilon(ss2.startState)

        # newEndState = state()
        # ss1.endState.appendToEpsilon(newEndState)
        # ss2.endState.appendToEpsilon(newEndState)
        # ss1.endState.stateDict["isTerminalState"] = False
        # ss2.endState.stateDict["isTerminalState"] = False

        # newSuperState = superstate(newStartState, newEndState)
        # superstate_stack.append(newSuperState)
        # concatLogic()

    if (c == '*'):
        print("found *")
        ss = superstate_stack.pop()
        newStartState = state()
        newEndState = state()
        newStartState.appendToEpsilon(ss.startState)
        # bypass from start to end (0 times)

        newStartState.appendToEpsilon(newEndState)

        ss.endState.appendToEpsilon(newStartState)
        ss.endState.appendToEpsilon(newEndState)

        ss.endState.stateDict["isTerminalState"] = False
        newSuperState = superstate(newStartState, newEndState)
        superstate_stack.append(newSuperState)

        # if (contextindex != 0):
        #     previous_c = regexInput[contextindex-1]
        #     # print(previous_c)
        #     # if (previous_c.isalnum() or previous_c in ')]+*?'):
        #     #     concatLogic()
        #     concatLogic(previous_c)
        # makeNFA(regexInput[1:])
        # continue parsing
        if (contextindex != 0):
            previous_c = regexInput[contextindex-1]
            concatLogic(previous_c)
        makeNFA(regexInput, contextindex+1)

    if (c == '+'):
        print("found +")
        ss = superstate_stack.pop()
        newStartState = state()
        newEndState = state()

        # newStartState.stateDict["epsilon"] = [ss.startState.name]
        newStartState.appendToEpsilon(ss.startState)
        # no bypass from start to end

        ss.endState.appendToEpsilon(newStartState)
        ss.endState.appendToEpsilon(newEndState)
        ss.endState.stateDict["isTerminalState"] = False
        newSuperState = superstate(newStartState, newEndState)
        superstate_stack.append(newSuperState)

        if (contextindex != 0):
            previous_c = regexInput[contextindex-1]
            concatLogic(previous_c)

        # continue parsing
        makeNFA(regexInput, contextindex+1)

    if (c == '?'):
        print("found ?")
        ss = superstate_stack.pop()
        # no bypass from start to end
        # ss.startState.stateDict["epsilon"].append(ss.endState.name)
        ss.startState.appendToEpsilon(ss.endState)
        superstate_stack.append(ss)
        if (contextindex != 0):
            previous_c = regexInput[contextindex-1]
            concatLogic(previous_c)

        makeNFA(regexInput, contextindex+1)

    # makeNFA(regexInput[], NFA)
    if (c.isalnum()):  # do we need to add other characters here ?
        print("found letter/num", c)
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
            concatLogic(previous_c)
        makeNFA(regexInput, contextindex+1)
    # concatenate after all
    # if (contextindex != 0):
    #     previous_c = regexInput[contextindex-1]
    #     # print(previous_c)
    #     # if (previous_c.isalnum() or previous_c in ')]+*?'):
    #     #     concatLogic()
    #     concatLogic(previous_c)

# how does our function handle abc? (da m3nah concatenation)
# abc
# (abc|[a-z])


NFA = {}
# Regex = "((a)(b))|((c)(d))"
# try:
#     re.compile(Regex)
# except re.error:
#     print("Non valid regex pattern")
#     exit()
# makeNFA(Regex)

# ERROR CASES
makeNFA("x?[0-9]+")  # gives error hena

# makeNFA("((ab|d)|c)")
# makeNFA("[a-cb]*")
# makeNFA("[abc]")
# makeNFA("a?")
# makeNFA("(((a)(b)|(d))|(c))")
# makeNFA("abc")  # works
# makeNFA("ab|cd")
# makeNFA("((a)(b)|((c)(d))")
# makeNFA("(ab)|(cd)")  # works
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
