import re

class state:
    isTerminalState = None
    inputCharacters = None
    def __init__(self,tState=False,inChar={}):
        self.isTerminalState = tState
        self.inputCharacters=inChar

def makeNFA(regexInput,NFA):
    if(regexInput == ""):
        return NFA
    c=regexInput[0]
    # Grouping
    if(c == "("):
        counter=1
        index=0
        print("indexed is")
        print(regexInput[index])
        while (counter != 0):
            if(regexInput[index] == "("):
                counter+=1
            elif(regexInput[index] == ")"):
                counter-=1
            index+=1
        print(regexInput[1:index])
        NFA=makeNFA(regexInput[1:index],NFA)

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

NFA = {}
NFA = makeNFA("((ab|d)|c)",NFA)