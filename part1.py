Regex = input("Enter Regex:")

size=len(Regex)

squareCounter = 0
bracketCounter = 0
curlyCounter = 0
invalid = 0
for i in range(size):
    if((Regex[i] == "*") or (Regex[i] == "?") or (Regex[i] == "+")):
        continue
    elif(Regex[i] == "|" or Regex[i] == "^" or Regex[i] == "$"):
        continue
    elif(Regex[i] == "["):
        squareCounter+=1
    elif(Regex[i] == "{"):
        curlyCounter+=1
    elif(Regex[i] == "("):
        bracketCounter+=1
    elif(Regex[i] == "]"):
        squareCounter-=1
    elif(Regex[i] == "}"):
        curlyCounter-=1
    elif(Regex[i] == ")"):
        bracketCounter-=1
    elif(Regex[i].isalnum()):
        continue
    else:
        invalid=1
        break

if( not (squareCounter == 0 and curlyCounter == 0 and bracketCounter == 0 )):
    invalid = 1
    
if(invalid == 1):
    print("Error Invalid Regex")
else:
    for i in range(size):
        
 
        