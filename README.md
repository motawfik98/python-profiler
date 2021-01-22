#**_Requirements_**
This script reads the C++ code given in the code.txt file and generates an output.cpp file which is then compiled to produce output.out executable  
C++ code must be well formatted for the python script to be able to parse it correctly  
##**_~~NOT Valid~~_**  
Function return another function, example:

    int f0() {
        return f1();
    }
Output example:  
    
    int f0() {
    cout << "f1 called" << endl;
        return f1();
    cout << "f1 returned" << endl;
    }
As this will generate the instrumentation code AFTER the return line which won't get printed  
Function's curley brackets are at the same line, example:  
`int f0() { return 5; }`  
Output example:  

    cout << "f0 called" << endl;
    int f0() { return 5; }
    cout << "f0 returned" << endl;
    
As this will generate instrumentation code outside the function scope (brackets)  
Function is called without spaces before or after any special characters, example:  
`int x=f0();`  
Output example:

    cout << "x=f0 called" << endl;
    int x=f0();
    cout << "x=f0 returned" << endl;
As `x=f0` will be considered a new function instead of `f0` only  

No brackets in a single line if-condition or for-loop

    if(condition)
        f1();

Output example:

    if(condition)
        f1();
    cout << "f1 returned" << endl;
    
##**_Corrections_**
First case:

    int f0() {
        int x = f1();
        return x;
    }
Second Case:  

    int f0() {
        return 5;
    }

Third Case:

    int x = f0();

Last Case:

    if(condition) {
        f1();
    }