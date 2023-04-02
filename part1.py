import re
# import NFAdrawer from nfadrawer
from utils import utils
# import NFAdrawer from nfadrawer
# nfadrawer.NFAdrawer.drawNFA({})


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

    def appendToEpsilonbyName(self, otherstatename):
        if (self.stateDict.get("epsilon")):
            self.stateDict["epsilon"].append(otherstatename)
            return
        self.stateDict["epsilon"] = [otherstatename]

    def setStartStateFalse(self):
        self.stateDict["isStartState"] = False


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


def wildCardLogic():
    print("found *")
    ss = superstate_stack.pop()
    newStartState = state()
    newEndState = state()
    newStartState.stateDict["isStartState"] = True
    newStartState.appendToEpsilon(ss.startState)
    # bypass from start to end (0 times)

    newStartState.appendToEpsilon(newEndState)

    # del ss.startState.stateDict["isStartState"]
    ss.startState.setStartStateFalse()
    ss.endState.appendToEpsilon(newStartState)
    ss.endState.appendToEpsilon(newEndState)

    ss.endState.stateDict["isTerminalState"] = False
    newSuperState = superstate(newStartState, newEndState)
    superstate_stack.append(newSuperState)


def plusLogic():
    print("found +")
    ss = superstate_stack.pop()
    newStartState = state()
    newEndState = state()
    newStartState.stateDict["isStartState"] = True

    # newStartState.stateDict["epsilon"] = [ss.startState.name]
    newStartState.appendToEpsilon(ss.startState)
    # no bypass from start to end
    # del ss.startState.stateDict["isStartState"]
    ss.startState.setStartStateFalse()
    ss.endState.appendToEpsilon(newStartState)
    ss.endState.appendToEpsilon(newEndState)
    ss.endState.stateDict["isTerminalState"] = False
    newSuperState = superstate(newStartState, newEndState)
    superstate_stack.append(newSuperState)


def optionalLogic():
    print("found ?")
    ss = superstate_stack.pop()
    # no bypass from start to end
    # ss.startState.stateDict["epsilon"].append(ss.endState.name)
    # print(ss.startState)
    ss.startState.appendToEpsilon(ss.endState)
    superstate_stack.append(ss)


def charLogic(c):
    print("found letter/num", c)
    # make 2 states
    firstState = state()
    secondState = state()
    firstState.stateDict["isStartState"] = True

    firstState.addTransition(secondState, c)
    # print("namaywa", firstState.name)
    # print(NFA)
    Superstate = superstate(firstState, secondState)
    superstate_stack.append(Superstate)


def pipeLogic():
    ss2 = superstate_stack.pop()
    ss1 = superstate_stack.pop()

    newStartState = state()
    newStartState.appendToEpsilon(ss1.startState)
    newStartState.appendToEpsilon(ss2.startState)
    newStartState.stateDict["isStartState"] = True

    newEndState = state()
    ss1.startState.setStartStateFalse()
    ss2.startState.setStartStateFalse()
    ss1.endState.appendToEpsilon(newEndState)
    ss2.endState.appendToEpsilon(newEndState)
    ss1.endState.stateDict["isTerminalState"] = False
    ss2.endState.stateDict["isTerminalState"] = False

    newSuperState = superstate(newStartState, newEndState)
    superstate_stack.append(newSuperState)


def RangeLogic(regexInput, notFirstRange):
    print("Handling range", regexInput)

    firstState = state()
    firstState.stateDict["isStartState"] = True
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
    # ya3ny law howa da or da haykammel
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
        # del ss1.startState.stateDict["isStartState"]
        # ss1.startState.setStartStateFalse()

        # this line assumes only 2 states in the other stack.. if it's bigger
        # then we just add the start state transitions
        if (ss2.startState.stateDict.get(ss2.endState.name)):
            ss1.endState.addTransition(
                ss2.endState, ss2.startState.stateDict[ss2.endState.name])
        # remove the isTerminalstatus
        ss1.endState.stateDict["isTerminalState"] = False

        # before removing ss2.startState, we need to check if it had epsilon transitions
        # if it did, we need to add them to ss1.endState
        if (ss2.startState.stateDict.get("epsilon")):
            for epsilonState in ss2.startState.stateDict["epsilon"]:
                ss1.endState.appendToEpsilonbyName(epsilonState)
        # ss1.endState.removeTransition(ss2.startState)
        AllStates.remove(ss2.startState)
        ss2.startState = dict()
        newSuperState = superstate(ss1.startState, ss2.endState)
        superstate_stack.append(newSuperState)


def ClassRangeLogic(regexInput):

    # find - (the dash) and remove it together with surrounding characters
    notFirstRange = False
    # bootstrap the while loop by setting it to something other than -1
    dashIndex = 1
    # remove all ranges
    while (dashIndex != -1):
        dashIndex = regexInput.find('-')
        if (dashIndex != -1):
            RangeLogic(regexInput[dashIndex-1:dashIndex+2], notFirstRange)
            regexInput = regexInput[:dashIndex-1] + regexInput[dashIndex+2:]
            notFirstRange = True
            print('new replaced regex input is ', regexInput)
    # what remains is the class logic
    if (len(regexInput) == 0):
        return
    counter = 0
    for i in range(1, len(regexInput)):  # from second position to before last character
        # print('lol', i)
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


# precedence:  * > + > ? > concat >| >
def getPrecedence(operator):
    match(operator):
        case '*':
            return 5
        case '+':
            return 4
        case '?':
            return 2
        case '.':
            return 1
        case '|':
            return 0
        case _:
            return -1


stack = []
postfix = ""

# adds dots to the regex input

# gets string in form of "a-c" and returns the range in form of "(a|b|c)"


def convertRange(stringInput):
    out = '('
    for i in range(ord(stringInput[0]), ord(stringInput[2])+1):
        # for character and then either a pipe or closing bracket
        out += chr(i)
        # if not last character
        out += '|' if i != ord(stringInput[2]) else ')'
    return out

# gets string in form of "ZYa-cA-CHGF" and returns the range in form of "(Z|Y|a|b|c|A|B|C|H|G|F)"


def convertRangeClass(stringInput):
    out = '('
    i = 0
    # counts the difference between the original string and new string
    # disregarding the brackets
    # differencecounter = 0
    while i < len(stringInput):
        c = stringInput[i]
        if i != len(stringInput)-1:
            v = stringInput[i+1]
            if (v == '-'):
                RangeInput = stringInput[i:i+3]  # 'A-Z'
                if (i != 0):
                    out += '|'
                    # differencecounter += 1
                # convertedRange, extradiff = convertRange(RangeInput)
                convertedRange = convertRange(RangeInput)
                out += convertedRange
                # differencecounter += extradiff
                # differencecounter -= 1  # for the dash
                i += 2
            else:
                if (i == 0):
                    out += c
                if (i != 0 and c != '-'):
                    out += '|' + c
                    # differencecounter += 1
        else:
            if (i == 0):
                out += c
            if (i != 0 and c != '-'):
                out += '|' + c
                # differencecounter += 1

        i += 1
    # -2 for the brackets that are ommitted outside
    differencecounter = len(out) - len(stringInput) - 2
    return out + ')', differencecounter
# gets string in form of "[something]dasdsada" and returns the index of the closing bracket


def getEndofRange(stringInput):
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
    # -1 because of add 1 in the end of while loop
    return index-1

# removes [] from the regex and replaces them with their equivalent ORed values


def preprocessrangeclasses(regexInput):
    result = ""+regexInput
    rescounter = 0
    # isinClass = False
    i = 0
    while i < len(regexInput)-1:
        c = regexInput[i]
        v = regexInput[i+1]
        if c == '[':
            bracketendind = getEndofRange(regexInput[i:])
            convertedexp, newdiff = convertRangeClass(
                regexInput[i+1:i+bracketendind])

            print('first part is ', result[:i+rescounter])
            print('second part is ', result[i+rescounter+bracketendind+1:])
            # remove the first[
            result = result[:i+rescounter] + convertedexp + \
                result[i+rescounter+bracketendind+1:]  # +1 for ]
            rescounter += newdiff+1
            # why was there a minus 1 here ?
            # remove the first [
            i += bracketendind-1
            # an extra one to parse ) at the end?
            # rescounter += bracketendind-1
        i += 1
    return result

# new appraoch: Separate preprocessing into 2 stages to make it easier:
# handle the concatenation first and then handle the rangeclasses


def preprocess(regexInput):
    result = ""+regexInput
    rescounter = 0
    # isinClass = False
    i = 0
    while i < len(regexInput)-1:
        c = regexInput[i]
        v = regexInput[i+1]
        if c == '[':
            bracketendind = getEndofRange(regexInput[i:])
            i += bracketendind-1  # skips bracket
        if c in '*+?)]' and v not in '.*+?])|':
            print('found some special character and concatenating')
            # print(result[:i+1+rescounter])
            # +1 for the character itself (the brackets or asterisk or whatever)
            cuttingindex = i+rescounter+1
            result = result[:cuttingindex] + '.' + result[cuttingindex:]
            rescounter += 1
            print('result now is ', result)
        # if c is a letter

        elif c.isalnum() and (v.isalnum() or v in '(['):
            # +1 for the character
            cuttingindex = i+rescounter+1
            result = result[:cuttingindex] + '.' + result[cuttingindex:]
            rescounter += 1
        i += 1
    print('first stage of processing result is', result)
    # removes [] from the regex and replaces them with their equivalent ORed values
    result = preprocessrangeclasses(result)
    print('final result is ', result)
    return result

# region test
# gets string in form of "ZYa-cA-CHGF" and returns the range in form of "(Z|Y|a|b|c|A|B|C|H|G|F)
# print(convertRangeClass("ZYa-cA-CHGF"))
# print(convertRangeClass("Ha-cA-CYB-Z"))
# print(convertRange("a-c"))
# res, diff = convertRangeClass("A-HUI")
# print(res, diff, len(res))
# preprocess('a[b-c]')
# preprocess('a[b-c]d')
# preprocess('a[b-c]d*')
# print(preprocess("AB*[A-H]K(HABCSD)"))
# print(preprocess("AB*[A-H]K(H)"))
# print(preprocess("AB*[A-HIJKMNL]K(H)"))
# print(preprocess("AB*[A-CTYU]K(H)"))
# print(preprocess("AB*[CDE]K(H)"))
# print(preprocess("abcd"))  # works
# print(preprocess("(ab)cd"))  # works
# print(preprocess("[ab]cd"))  # work
# print(preprocess("[a-ghj]cd"))  # work
# print(convertRangeClass("a-g"))

# print(preprocess("[A-CDEFG]a[b-c]"))

# print(preprocess("[A-C]a[b-c]d*"))

# endregion


def Shuntyard(regexInput):
    global postfix
    global stack
    regexInput = preprocess(regexInput)
    # print('preprocessed string is ', regexInput)
    isInClass = False
    for i in range(len(regexInput)):
        c = regexInput[i]
        if (c.isalnum()):
            postfix += c
        elif (c in '(['):
            stack.append(c)
            if c == '[':
                isInClass = True
        elif (c in ')]'):
            while (stack[-1] != '('):  # stack top
                postfix += stack.pop()
            stack.pop()
            isInClass = False
        elif (c in "*+?|."):
            while (stack and getPrecedence(c) <= getPrecedence(stack[-1])):
                postfix += stack.pop()
            stack.append(c)
        elif c == '-':
            final = regexInput[i+1]
            initial = postfix[-1]
            processed_range = ''
            for j in range(ord(initial), ord(final)+1):
                processed_range += chr(j)
                processed_range += '|'
            regexInput = regexInput[:i-1] + processed_range + regexInput[i+2:]
        # normal character
        else:
            postfix += c
            if isInClass:
                postfix += '|'

    while (stack):
        postfix += stack.pop()
    return postfix


# regex = "(AH+.B*)?.(C|D)"
# regex = "[a-cd]*"
# regex = "a|b|c|d"
# regex = "[a-d]"
regex = "AB*[A-HIJKMNL]K(H)"
print('postfix is ', Shuntyard(regex))


def makeNFA(regexInput, contextindex=0):
    global makeNFAcurrIndex
    global NFA
    global superstate_stack
    global recursioncounter
    if (contextindex == len(regexInput)):
        return NFA
    c = regexInput[contextindex]
    # Grouping
    if (c == "("):
        print('extracted string in brackets is', regexInput[contextindex:])
        # passes string of form    "(something)"
        index = getIndexEndingBrack(regexInput[contextindex:], '(')
        recursioncounter += 1

        # get expression inside bracket
        # mfee4 -1, excluded by default
        newregexInput = regexInput[contextindex+1: contextindex+index]

        # print("new input is ", newregexInput)
        # parese new expression in the brackets
        makeNFA(newregexInput)
        # concatenate the brackets states
        # if (contextindex != 0):
        #     previous_c = regexInput[contextindex-1]
        #     concatLogic(previous_c)

        if (contextindex != 0):
            previous_c = regexInput[contextindex-1]
            # print('regex expression is ', regexInput)
            # el regex expression byb2a kamel hena

            if (contextindex+index+1 != len(regexInput)):
                # if not out of range then check for higher priority logic
                print('next char is ', regexInput[contextindex+index+1])
                if (regexInput[contextindex+index+1] not in '*+?'):
                    # print('lmao gamed')
                    concatLogic(previous_c)
            else:  # do concat logic in case of last character
                concatLogic(previous_c)
        # parse from the beginning of the ending bracket
        # print(regexInput[index:])
        print('index is ', index, 'contextindex is ', contextindex)
        # makeNFA(regexInput[index+1:])  # skip the bracket
        makeNFA(regexInput, contextindex+index+1)  # skip the bracket
        return

    # range or group
    if (c == '['):
        index = getIndexEndingBrack(regexInput[contextindex:], '[')
        # print(regexInput[1:index])
        recursioncounter += 1
        newregexInput = regexInput[contextindex+1: contextindex+index]
        previouscharacter = regexInput[contextindex -
                                       1] if (contextindex > 0) else ''
        print('previouscharacter is ', previouscharacter)
        # print(newregexInput)
        ClassRangeLogic(newregexInput, previouscharacter)
        if (contextindex != 0):
            previous_c = regexInput[contextindex-1]
            concatLogic(previous_c)
        # makeNFA(regexInput[index+1:])  # skip the bracket
        makeNFA(regexInput, contextindex+index+1)  # skip the bracket
        return

    if (c == "|"):
        # call next expression first
        makeNFA(regexInput, contextindex+1)
        # handle pipe logic
        print("found | at contextindex= ", contextindex)
        pipeLogic()
        # CHECKKK
        # not sure 5ales
        if (contextindex != 1):  # heya at least hatkoon tany letter m4 awl letter
            previous_c = regexInput[contextindex-2]
            concatLogic(previous_c)
        if (contextindex+2 != len(regexInput)):
            # if not out of range then check for higher priority logic
            print('next char is ', regexInput[contextindex+2])
            if (regexInput[contextindex+index+1] not in '*+?'):
                # print('lmao gamed')
                concatLogic(previous_c)
        else:  # do concat logic in case of last character
            concatLogic(previous_c)

    if (c == '*'):
        wildCardLogic()
        if (contextindex != 0):
            previous_c = regexInput[contextindex-2]
            concatLogic(previous_c)
        makeNFA(regexInput, contextindex+1)

    if (c == '+'):
        plusLogic()
        # you need to calculate the previous index here
        # like if it is (a|b)+ previous index is 0
        # BAS ETSADA2? MIGHT WORK WITHOUT IT..
        # ESPECIALLY BECAUSE WE CHECK THE superstack size
        if (contextindex != 0):
            previous_c = regexInput[contextindex-2]
            concatLogic(previous_c)

        # continue parsing
        makeNFA(regexInput, contextindex+1)

    if (c == '?'):
        optionalLogic()
        if (contextindex != 0):
            previous_c = regexInput[contextindex-2]
            concatLogic(previous_c)

        makeNFA(regexInput, contextindex+1)

    # makeNFA(regexInput[], NFA)
    if (c.isalnum()):  # do we need to add other characters here ?
        charLogic(c)
        if (contextindex != len(regexInput)-1):
            print('nextchar', regexInput[contextindex+1])

        if (contextindex != 0):
            previous_c = regexInput[contextindex-1]
            if (contextindex != len(regexInput)-1):
                # if not last character then check for higher priority logic
                if (regexInput[contextindex+1] not in '*+?'):
                    concatLogic(previous_c)
            else:  # do concat logic in case of last character
                concatLogic(previous_c)

        makeNFA(regexInput, contextindex+1)

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
# makeNFA("x?[0-9]+")  # gives error hena

# makeNFA("ab|c")
# makeNFA("(a)b|c")
# makeNFA("(a)(b)|c")
# makeNFA("(a)(b)|c")
# makeNFA("(((ab)|d)|c)")
# makeNFA("[a-cd]*")
# makeNFA("[abc]")
# makeNFA("ab?")


# makeNFA("ab?cd?(ef|g)*")


# makeNFA("(((a)(b)|(d))|(c))")
# makeNFA("abc")
# makeNFA("ab|cd")
# makeNFA("((a)(b)|(c)(d))")
# makeNFA("(ab)|(cd)")
# makeNFA("(abc|3)")  # works lol
# print(AllStates)
# for s in AllStates:
#     print(s)

# AllStatesJSON = utils.convertAllstates(AllStates)
# utils.drawNFA(AllStatesJSON, "NFA")
# print('AllStatesJSON', AllStatesJSON)
# for mystate in AllStatesJSON.items():
#     print(mystate[0])

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
#   - 1 or more a+
#   - 0 or more a*
#   - Optional a?
#   - Character/number classes [abc] or [345]
#   - Ranges [a-c] or [0-5]
#   - Brackets for grouping ()
# 2. You can use any third-party library to check the validity of the input regular expression.
# 3. You can use any third-party library to help you draw a diagram of your FSM and deal with it as you like, as long as the JSON output file is as expected and stated in the assignment document.
