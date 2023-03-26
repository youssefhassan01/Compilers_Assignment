import re


class state:
    # here class varialbe only (static)
    counter = 0  # counter of created states

    def __init__(self, tState=False):
        self.stateDict = dict()
        self.stateDict["isTerminalState"] = tState
        self.name = "S" + str(state.counter)
        print('my name is ', self.name)
        if (state.counter == 0):
            self.stateDict["isStartingState"] = 1

        state.counter += 1

    def addTransition(self, otherstate, transitionString):
        self.stateDict[otherstate.name] = transitionString


recursioncounter = 0


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
    return index


def ClassRangeLogic(regexInput):
    pass


# [expressions, operations]

# expressions = string | operations(expression)
# operations = functions(expressions)


def makeNFA(regexInput):
    global NFA
    global recursioncounter
    if (regexInput == ""):
        return NFA
    c = regexInput[0]
    # Grouping
    if (c == "("):
        index = getIndexEndingBrack(regexInput, '(')
        # print(regexInput[1:index])
        recursioncounter += 1

        # get expression inside bracket
        newregexInput = regexInput[1:index-1]
        print(newregexInput)
        makeNFA(newregexInput)
        makeNFA(regexInput[index:])
        return
    if (c == "|"):
        print("found |")
    if (c == '*'):
        print("found *")
    if (c == '+'):
        print("found +")
    if (c == '?'):
        print("found ?")
    # range or group
    if (c == '['):
        index = getIndexEndingBrack(regexInput, '[')
        # print(regexInput[1:index])
        recursioncounter += 1
        newregexInput = regexInput[1:index-1]
        print(newregexInput)
        ClassRangeLogic(newregexInput)
        makeNFA(regexInput[index:], NFA)
        return
    # makeNFA(regexInput[], NFA)
    if (c.isalnum()):  # do we need to add other characters here ?
        # make state
        mystate = state()
        # print("namaywa", mystate.name)
        print(NFA)
        NFA[mystate.name] = mystate.stateDict
        if (len(regexInput) > 1 and regexInput[1].isalnum()):
            mystate.addTransition()
        pass
    makeNFA(regexInput[1:])

# how does our function handle abc? (da m3nah concatenation)
# abc
# (abc|[a-z])


NFA = {}
# NFA = makeNFA("((ab|d)|c)", NFA)
makeNFA("(((a)(b)|(d))|(c))")
makeNFA("(abc|3)")


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
