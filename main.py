import os
from anytree import Node
from anytree import find as find_node
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
main_dynamic_node = Node("main", occurrences=0)  # add main function as it's the starting point (for dynamic tree)
main_context_node = Node("main", occurrences=0)  # add main function as it's the starting point (for context tree)
dynamic_stack_trace = [main_dynamic_node]  # add it to the stacktrace to know which function is executing
context_stack_trace = [main_context_node]  # add it to the stacktrace to know which function is executing

for line in lines:  # loop over lines
    func_name = line.split(" ")[0]  # get function name
    func_type = line.split(" ")[1]  # get type (called or returned)
    if func_type.strip() == 'called':  # if it's called, then a new node needs to be created
        dynamic_node = Node(func_name, parent=dynamic_stack_trace[-1],
                            occurrences=1)  # create new node with the right parent
        dynamic_stack_trace.append(dynamic_node)  # add the node to the top of the stacktrace
        # gets the full path of the current node
        path = str(dynamic_node.path[-1])[
               str(dynamic_node.path[-1]).index("(") + 1: str(dynamic_node.path[-1]).index(",")]
        # find the node with the same path
        same_node = find_node(main_context_node, lambda node: str(node.path[-1])[
                                                              str(node.path[-1]).index("(") + 1: str(
                                                                  node.path[-1]).index(",")] == path)
        if same_node is not None:  # if a node with the same path has been found
            same_node.occurrences += 1  # increment the number of occurrences of the node
            context_stack_trace.append(same_node)  # add the node to the top of the stack
        else:  # new node to be added
            context_node = Node(func_name, parent=context_stack_trace[-1],
                                occurrences=1)  # create new node with the right parent
            context_stack_trace.append(context_node)

    else:  # the function returned
        dynamic_stack_trace.pop()  # pop the top most function
        context_stack_trace.pop()  # pop the top most function

most_frequent_path = None
frequent_path_count = 0

most_frequent_sub_path = None
frequent_sub_path_count = 0


def edge_attr_func(node, child):
    global frequent_path_count
    global frequent_sub_path_count
    global most_frequent_path
    global most_frequent_sub_path
    if child.is_leaf:
        if child.occurrences > frequent_path_count:
            frequent_path_count = child.occurrences
            most_frequent_path = child
    if child.occurrences > frequent_sub_path_count:
        frequent_sub_path_count = child.occurrences
        most_frequent_sub_path = child
    return 'label="x%d"' % child.occurrences


# visualize the main_node (root) of the tree
UniqueDotExporter(main_dynamic_node).to_picture("pictures_output/dynamic.png")
UniqueDotExporter(main_context_node, edgeattrfunc=edge_attr_func).to_picture("pictures_output/context.png")
main_path_node = None
for ancestor in most_frequent_path.ancestors:
    main_path_node = Node(ancestor.name, parent=main_path_node)

Node(most_frequent_path.name, parent=main_path_node)
UniqueDotExporter(main_path_node.root).to_picture("pictures_output/most_frequent_path.png")

print(most_frequent_sub_path)
main_sub_path_node = Node(most_frequent_sub_path.parent.name)
Node(most_frequent_sub_path.name, parent=main_sub_path_node)
UniqueDotExporter(main_sub_path_node.root).to_picture("pictures_output/most_frequent_sub_path.png")

log_output_file.close()
