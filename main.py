import os

file = open('code.txt', 'r')
outputFile = open('output.cpp', 'w')
lines = file.readlines()

returnedTypes = ['int', 'float', 'double', 'string', 'char', 'bool', 'void']

newFunctionName = False
writeReturnLine = False
functionsNames = []
returnedFunctions = []
possibleFunctionName = ""
mainFuncFound = False
for line in lines:  # read file line by line
    for word in line.split(" "):  # read line word by word
        if "(" in word:  # if a '(' is found in the word
            possibleFunctionName = word.split("(")[0] + "("
            if [funcName for funcName in functionsNames if(funcName in possibleFunctionName)]:
                # check if the current word is present in the saved functions names
                outputFile.write("""cout << \"""" + possibleFunctionName[:-1] + """ called\" << endl;\n""")
                returnedFunctions.append("cout << \"" + possibleFunctionName[:-1] + " returned\" << endl;\n")
                writeReturnLine = True
        if newFunctionName:  # if it's an indicator that a new function name could be found
            if "(" in word:  # if it contains parenthesis, then it's a function
                funcName = word.split("(")[0]
                if funcName == "main":
                    mainFuncFound = True
                functionsNames.append(funcName + "(")   # add function name to the list
            newFunctionName = False
        if word in returnedTypes:  # if a return type was found, it could be a function
            newFunctionName = True
    outputFile.write(line)  # write the original line
    if mainFuncFound:
        outputFile.write("freopen(\"log_output.txt\",\"w\",stdout);\n")
        mainFuncFound = False
    outputFile.writelines(returnedFunctions)  # write the returned functions logs
    returnedFunctions = []

file.close()
outputFile.close()
if os.system('g++ output.cpp -o output.out') == 0:
    os.system("./output.out")
else:
    print("Unable to compile and run output file")
