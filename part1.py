import re


class state:
    isTerminalState = None
    inputCharacters = None

    def __init__(self, tState=False, inChar={}):
        self.isTerminalState = tState
        self.inputCharacters = inChar


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


def makeNFA(regexInput, NFA):
    global recursioncounter
    if (regexInput == ""):
        return NFA
    c = regexInput[0]
    # Grouping
    if (c == "("):
        index = getIndexEndingBrack(regexInput, '(')
        # print(regexInput[1:index])
        recursioncounter += 1
        newregexInput = regexInput[1:index-1]
        print(newregexInput)
        makeNFA(newregexInput, NFA)
        makeNFA(regexInput[index:], NFA)
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
        if ('-' in newregexInput):
            # Range logic
            pass
        else:
            # Classes logic
            pass
        print(newregexInput)
        makeNFA(regexInput[index:], NFA)
        pass
    # makeNFA(regexInput[], NFA)
    makeNFA(regexInput[1:], NFA)

# abc


NFA = {}
# NFA = makeNFA("((ab|d)|c)", NFA)
NFA = makeNFA("(((a)(b)|(d))|(c))", NFA)


# Regex = input("Enter Regex:")

# size=len(Regex)


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
