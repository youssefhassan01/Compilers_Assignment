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
        # print('my name is ', self.name)
        # if (state.counter == 0):
        #     self.stateDict["isStartingState"] = 1

        state.counter += 1
        global AllStates
        AllStates.append(self)

    # def __iter__(self):
    #     return self

    # def __next__(self):
    #     if self.currIndex > self.stateNum:
    #         raise StopIteration
    #     else:
    #         return self

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


# [expressions, operations]
# expressions = string | operations(expression)
# operations = functions(expressions)
superstate_stack = []
AllStates = []


# precedence:  * > + > ? > concat >| >
def getPrecedence(operator):
    match(operator):
        case '*':
            return 5
        case '+':
            return 4
        case '?':
            return 2
        case 'ඞ':
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
                    out += '/' + c if c in '?*+|ඞ' else c
                if (i != 0 and c != '-'):
                    # out += '|' + c
                    out += '/' + '|' + c if c in '?*+|ඞ' else '|' + c
                    # differencecounter += 1
        else:
            if (i == 0):
                out += '/' + c if c in '?*+|ඞ' else c

            if (i != 0 and c != '-'):
                # out += '|' + c
                out += '|' + '/' + c if c in '?*+|ඞ' else '|' + c

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

            # print('first part is ', result[:i+rescounter])
            # print('second part is ', result[i+rescounter+bracketendind+1:])
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

# takes raw input


def preprocess(regexInput):
    result = ""+regexInput
    rescounter = 0
    i = 0
    while i < len(regexInput)-1:
        c = regexInput[i]
        v = regexInput[i+1]
        if c == '[':
            bracketendind = getEndofRange(regexInput[i:])
            i += bracketendind-1  # skips bracket
        if c in '*+?)]' and v not in 'ඞ*+?])|':
            # print('found some special character and concatenating')
            # print(result[:i+1+rescounter])
            # +1 for the character itself (the brackets or asterisk or whatever)
            cuttingindex = i+rescounter+1
            result = result[:cuttingindex] + 'ඞ' + result[cuttingindex:]
            rescounter += 1
            # print('result now is ', result)
        # if c is a letter

        # elif c.isalnum() and (v.isalnum() or v in '(['):
        elif (c not in '*+?|ඞ-[(' and v not in '*+?|ඞ-)]'):
            # +1 for the character
            # print('concatenating', c, 'to', v)
            cuttingindex = i+rescounter+1
            result = result[:cuttingindex] + 'ඞ' + result[cuttingindex:]
            rescounter += 1
        i += 1
    # print('first stage of processing result is', result)
    # removes [] from the regex and replaces them with their equivalent ORed values
    result = preprocessrangeclasses(result)
    # print('final result is ', result)
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
    print('preprocessed string is ', regexInput)
    isInClass = False
    for i in range(len(regexInput)):
        c = regexInput[i]
        # # if (c.isalnum()):
        # if (c.isalnum()):
        #     postfix += c
        if (c in '(['):
            stack.append(c)
            if c == '[':
                isInClass = True
        elif (c in ')]'):
            while (stack[-1] != '('):  # stack top
                postfix += stack.pop()
            stack.pop()
            isInClass = False
        elif (c in "*+?|ඞ"):
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
# regex = "AB*[A-HIJKMNL]K(H)"
# print('postfix is ', Shuntyard(regex))


def wildCardLogic():
    global superstate_stack
    # print("Handling the  * logic")
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
    print(newSuperState)
    superstate_stack.append(newSuperState)


def plusLogic():
    global superstate_stack
    # print("Handling the + logic")
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
    global superstate_stack
    # print("Handling ? logic")
    ss = superstate_stack.pop()
    # no bypass from start to end
    # ss.startState.stateDict["epsilon"].append(ss.endState.name)
    # print(ss.startState)
    ss.startState.appendToEpsilon(ss.endState)
    superstate_stack.append(ss)


def charLogic(c):
    global superstate_stack
    # print("Handling the character", c)
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
    global superstate_stack
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


def concatLogic():
    global superstate_stack
    # print("Handling Concat logic")
    ss2 = superstate_stack.pop()
    ss1 = superstate_stack.pop()
    # if (ss2.startState.stateDict.get(ss2.endState.name)):
    #     ss1.endState.addTransition(
    #         ss2.endState, ss2.startState.stateDict[ss2.endState.name])
    # remove the isTerminalstatus
    ss1.endState.appendToEpsilon(ss2.startState)
    ss1.endState.stateDict["isTerminalState"] = False
    ss2.startState.setStartStateFalse()

    # before removing ss2.startState, we need to check if it had epsilon transitions
    # if it did, we need to add them to ss1.endState
    # if (ss2.startState.stateDict.get("epsilon")):
    #     for epsilonState in ss2.startState.stateDict["epsilon"]:
    #         ss1.endState.appendToEpsilonbyName(epsilonState)
    # ss1.endState.removeTransition(ss2.startState)
    # AllStates.remove(ss2.startState)
    # ss2.startState = dict()
    newSuperState = superstate(ss1.startState, ss2.endState)
    superstate_stack.append(newSuperState)


def makeNFA(regexInput):
    global makeNFAcurrIndex
    global superstate_stack

    postfix = Shuntyard(regexInput)
    print('pofix', postfix)
    for i in range(len(postfix)):
        c = postfix[i]
        if (c == "/" and i < len(postfix)-1 and postfix[i+1] in "+*?|ඞ"):
            charLogic(postfix[i+1])
            i += 1
        elif (c == "*"):
            wildCardLogic()
        elif (c == "+"):
            plusLogic()
        elif (c == 'ඞ'):
            concatLogic()
        elif (c == "?"):
            optionalLogic()
        elif (c == "|"):
            pipeLogic()
        else:
            charLogic(c)


# how does our function handle abc? (da m3nah concatenation)
# abc
# (abc|[a-z])
# regex = "ab?cd?(ef|g)*"
# regex = input("Enter your regex: ")
# regex = "abc[g-h]*"
# regex = "ab$_"
# adam = makeNFA(regex)
# makeNFA("(((a)(b)|(d))|(c))")
# makeNFA("abc")
# makeNFA("ab|cd")
# makeNFA("((a)(b)|(c)(d))")
# makeNFA("(ab)|(cd)")
# makeNFA("(abc|3)")
# print(AllStates)
# for s in AllStates:
#     print(s)
# ERROR CASES
# makeNFA("x?[0-9]+")


# makeNFA("[ab][ab]*[!?]?")
# makeNFA("(a)b|c")
# makeNFA("(a)(b)|c")
# makeNFA("(a)(b)|c")
# makeNFA("(((ab)|d)|c)")
# makeNFA("[a-cd]*")
# makeNFA("[abc]")
# makeNFA("ab?")
# makeNFA("ab?cd?(ef|g)*")

# Tha main test cases
# makeNFA("ab(b | c)*d+")
# makeNFA("[a-zA-Z_$][a-zA-Z0-9_$]*")
# makeNFA("0|[1-9A-F][0-9A-F]*|[1-9a-f][0-9a-f]*")
# makeNFA("https?://(www.)?[a-zA-Z0-9-_].(com|org|net)")
# makeNFA("[1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]")
# for s in AllStates:
#     print(s)
# AllStatesJSON = utils.convertAllstates(AllStates)
# utils.drawNFA(AllStatesJSON, "NFA")


# AllStatesJSON = utils.convertAllstates(AllStates)
# utils.drawNFA(AllStatesJSON, "NFA")
# print('AllStatesJSON', AllStatesJSON)
# for mystate in AllStatesJSON.items():
#     print(mystate[0])


# Regex = '[(hi)-z]'
