import os
from anytree import Node
from anytree.exporter import UniqueDotExporter

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


log_output_file = open("log_output.txt", "r")  # open log output file
lines = log_output_file.readlines()  # read the lines generated
main_node = Node("main")  # add main function as it's the starting point
stack_trace = [main_node]  # add it to the stacktrace to know which function is executing
for line in lines:  # loop over lines
    func_name = line.split(" ")[0]  # get function name
    func_type = line.split(" ")[1]  # get type (called or returned)
    if func_type.strip() == 'called':  # if it's called, then a new node needs to be created
        new_node = Node(func_name, parent=stack_trace[-1])  # create new node with the right parent
        stack_trace.append(new_node)  # add the node to the top of the stacktrace
    else:  # the function returned
        stack_trace.pop()  # pop the top most function

# visualize the main_node (root) of the tree
UniqueDotExporter(main_node).to_picture("pictures_output/dynamic_calling.png")
log_output_file.close()
