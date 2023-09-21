"""
Language Information:
    Name: Nexus 
    Version: 1.0.0b
    File Extension: .nx
Syntax Creation:
    :NOTE:Each statement ends in |
    Create a class:
        bp myClass(
            myClass[arg1,arg2]{
            code
            }
        )
        public bp myGlobalClass(
            myGlobalClass[arg1,arg2]{
            code
            }
        )
    Derive class:
        bp myClass(
            myClass[arg1,arg2]{
            code
            }
        )
        bp myOtherClass inherits myClass(
            myOtherClass[arg1,arg2]{
            code
            }
        )
    Create a function
        def myFunction[arg1,arg2]{
        code
        }
        public def myGlobalFunction[arg1,arg2]{
        code
        }
    Create a variable
        set a to {val}
        set a to {val} public //global
    :NOTE: Calculations are not saved besides last one to &
    Basic calculations
        set a to 30
        2*5//This is &
        set a to a/&
    Comment
        //This is a comment
    Call function
        call myFunction [arg1,arg2,arg3]
"""
from sys import argv
from os import system
from ast import UAdd,USub,Add,Sub,Mult,Div,Mod,Num,Expression,UnaryOp,BinOp,parse
from typing import Callable as Function
from typing import Any,Literal
locals={"&":None}
globals={}
finalCode="RESERVED=locals['&']\n"#RESERVED holds the & in Nexus
UNARY_OPS = (UAdd, USub)
BINARY_OPS = (Add, Sub, Mult, Div, Mod)
"""
Nexus Errors(manage exit codes):
HELP(1) - Help function
NO_ARGS(2) - No args were given to the interpreter
"""
NEXUS_ERRORS={'HELP':1,'NO_ARGS':2,'CANNOT_READ_FILE':3,'WRONG_FILE_TYPE':4}
print(NEXUS_ERRORS.HELP)
"""
Finished Functions: is_math,helpp,functionToDict,handleLine,pythonizeFunction
Working on: handleLineType,identifyLineType

:TODO:
    1. Finish handleLine()
    2. identifyLineType()
    3. handleLineType()

To clarify:
    saving to & in nexus is a python binding of locals["&"]
    the finished class holds the finished functions
To simplify process:
    class NexusClass:
        ONLY HOLD PYTHON IN CODE VARS   
        NexusClass.name -> class {this}
        NexusClass.args -> constructor args in str(tuple)
        NexusClass.code -> constructor code in str 
        NexusClass.final -> all code for the class
    class NexusFunction(typing.Callable)
        NexusFunction.name->def {this}
        NexusFunction.args->string of the tuple
        NexusFunction.code->finished string
        NexusFunction.final->full pythonized code
    class NexusVariable:
        NexusVariable.name -> var name
        NexusVariable.value -> var value
        NexusVariable.final -> python value
    class ClassString(str):
     def findClose(self,char:Literal['(']|Literal['[']|Literal['{'],startindex:int=-1):pass
     
    Write functions to simplify main block at bottom:
    def writeFile(file):open(file,'w+').write(finalCode)
    def compileFile(file):system(pyinstaller --onefile --distpath ./ file.py)
    Maybe add a way to test functions by simulating flows of data:
        def test(function:Function,args:tuple)->str:pass
        print(test(identifyLineType,("bp myClass(myClass[args]{})|"))->string containing the output ['bp',['myClass',(args),{'myClass':{"args":(args),"code":""}}]]
Conditionals:
if[condition]{
code|
}
while[condition]{
code|
}
for[{} in {var}]{
code|
}
        
        
        
"""
class ClassString(str):
    """
    Nexus Class for possibly making indexing of brackets and parenthases so much easier
    """
    def getSetOfBracketedStatements(self)->list:
        possibleCloses={'(':')','{':'}','[':']'}
        currentIndex=0
        counter=0
        currentBracketType=""
        currentlyOpen=False
        bracketedStatements=[]
        while True:
            try:
                i=self[counter]
                if i in possibleCloses.keys():#this means the open is there and we can take that index
                    if not currentlyOpen:#extra check
                        currentBracketType=i
                        currentIndex=counter
                        currentlyOpen=True
                        counter+=1
                elif i in possibleCloses.values():
                    if currentlyOpen and i==possibleCloses[currentBracketType]:#extra check to make sure there is a new index
                        #counter = final index
                        bracketedStatements.append(self[currentIndex:counter+1])
                        currentIndex=counter
                        currentBracketType=""
                        currentlyOpen=False
                        counter+=1
                        continue
                else:
                    counter+=1
                    continue
            except IndexError:break#the string is over length or is done iterating
        return bracketedStatements
    def findClose(self,char:str,startIndex:int=-1)->int:
        """
        Find the close for the brackets
        :param Literal char: Character to find close for
        :param int startIndex: Where the open character is in the string
        """
        possibleCloses={'(':')','[':']','{':'}'}
        if startIndex == -1:
            """
            Find first occurrence of the char
            """
            firstIndex=0
            if str(char) not in self: raise ValueError("The char is not in the string ")
            counter=0
            while True:
                if self[counter]!=char:
                    counter+=1
                    continue
                firstIndex=counter#this is the open bracket
                break
            counter=firstIndex#set the start index
            while True:
                if self[counter]!=possibleCloses[char]:
                    counter+=1
                    continue
                #if it hits this the close is here
                return counter

def handleLine(line:str,forVar:bool=False)->str|Any:
    """
    :param str line: line to analyze
    :param bool forVar: for variables calling their assignment to be processed
    returns the python version of each line given
    class or function definitions cannot be given to this function(they get predefined and interpretted separately by their respective objects)
    Possible lines given:
        1. set a to value
        2. 2*5(math)
        3. //comment
        4. (code)
    """
    code=""
    if not line.endswith("|"):raise SyntaxError("There is no | character at the end of the line.")
    if 'set' in line:
        if forVar:raise SyntaxError("There cannot be a variable declaration within a variable declaration")
        code+=f"{line.split()[1]}={line.split()[3]}"
    if is_math(line):
        if forVar:return eval(line)
        locals["&"]=eval(line)
        code+=f"RESERVED={eval(line)}"
    if '//' in line:
        if forVar:
            if line.startswith('//'):raise SyntaxError("Variables cannot equal comments")#there is nothing to do unless this is all there is 
        code+=f"#{line[2:]}"
    if '(' in line and ')' in line:
        #doesnt really matter if forVar cuz we don't process parens unless its mathematical which wouldve been accounted for
        try:handleLine(line.split('(')[1].split(')')[0])
        except Exception:raise SyntaxError("The line could not be processed: "+line.split('(')[1].split(')')[0])
    return code
class NexusClass:
    """
    Python class for holding Nexus Class info
    """
    name:str
    args:str
    code:str
    functions:Function
    final:str
    def __init__(self,name:str,args:tuple,code:list,functions:list,inheritence:str=None) -> None:
        """
        :param str name: Name of the Class
        :param tuple args: arguments of the constructor
        :param list code: code of the init function
        :param list functions: functions within the class using NexusFunction Objects
        :param str inheritence: If the class inherits another(super classes)
        """
        self.name=name
        self.args=str(args)
        if inheritence is not None:self.inheritence=inheritence
        self._handleCode(code)#updates self.code
        self.functions=functions
        self._finalize()
    def _handleCode(self,code:list)->str:
        """
        Pythonize all code and then add to self.code
        *REQUIRES handleLine() TO BE FUNCTIONAL*
        :param list code: List of code for funtion
        """
        for i in code:self.code+=f"\t\t{handleLine(i)}\n"
    def _finalize(self)->None:
        """
        Finishes Python code and puts it to self.final
        """
        if not self.inheritence:self.final=f"class {self.name}:\n\tdef __init__(self,{self.args[1:len(self.args)-1]})->None:\n{self.code}"#This finished init function
        else:self.final=f"class {self.name}({self.inheritence}):\n\tdef __init__(self,{self.args[1:len(self.args)-1]})->None:\n{self.code}"#This finished init function
        for i in self.functions:self.final+=f"{i.final}\n"
class NexusFunction(Function):
    """
    Python class for holding Nexus Function info
    """
    name:str
    args:str
    code:str
    final:str
    def __init__(self,name:str,args:tuple,code:list,isclass:bool)->None:
        """
        :param str name: Name of the Function
        :param tuple args: args for the function declaration
        :param list code: list of nexus code to be pythonized
        :param bool isclass: if is in a class for indentation purposes
        """
        self.name=name
        self.args=str(args)
        self.isclass=isclass
        self._handleCode(code)#update self.code
        self.final=self._finalize()#update self.final
    def _handleCode(self,code:list)->str:
        """
        Pythonize all code and then add to self.code
        *REQUIRES handleLine() TO BE FUNCTIONAL*
        """
        if not self.isclass:
            for i in code:self.code+=f"\t{handleLine(i)}\n"
        else:
            for i in code:self.code+=f"\t\t{handleLine(i)}\n"
    def _finalize(self)->None:
        """
        Used to save the whole code block to self.final
        def myFunction[arg,arg2]{               def myFunction(arg,arg2):
            code                        ->          code
        }
        """
        if not self.isclass:self.final=f"def {self.name}{self.args}:\n{self.code}"
        self.final=f"\tdef {self.name}{self.args}:\n{self.code}"
class NexusVariable:
    """
    Python class for holding Nexus Variable Info
    """
    name:str
    value:Any
    final:str
    def __init__(self,name:str,value:Any)->None:
        """
        :param str name: name of the variable
        :param Any value: value of the variable
        """
        self.name=name
        self.value=handleLine(str(value))
        self._finalize()
    def _finalize(self)->None:self.final=f"{self.name}={str(self.value)}"
class finished:
    def is_math(s):
        def _is_arithmetic(node):
            if isinstance(node, Num):return True
            elif isinstance(node, Expression):return _is_arithmetic(node.body)
            elif isinstance(node, UnaryOp):
                valid_op = isinstance(node.op, UNARY_OPS)
                return valid_op and _is_arithmetic(node.operand)
            elif isinstance(node, BinOp):
                valid_op = isinstance(node.op, BINARY_OPS)
                return valid_op and _is_arithmetic(node.left) and _is_arithmetic(node.right)
            else:raise ValueError('Unsupported type {}'.format(node))
        try:return _is_arithmetic(parse(s, mode='eval'))
        except (SyntaxError, ValueError):return False
    def functionToDict(functionname:str,args:tuple,code:list)->dict:
        """
        code is in nexus form not python
        """
        return {functionname:{"args":args,"code":code}}
    def pythonizeFunction(function:dict)->str:
        "converts the Nexus function to python"
        code=f"def {function.keys()[0]}{str(function[function.keys()[0]]['args'])}:\n"
        for i in function[function.keys()[0]]["code"]:code+=handleLine(i)+"\n\t"
        return code
def handleLineType(t:str,args:list)->None:
    """
    Handles each line based on response from identifyLineType()
    """
    match t:
        case None:pass#comments
        case 'bp':
            """
            class identification
            args:
                [NexusClass Class]
            instructions:
                add Class.final -> finalCode
            """
        case 'def':
            """
            function identification
            args:
                [NexusFunction Function]
            instructions:
                add Function.final -> finalCode
            """
        case 'set':
            """
            variable identification
            args:
                [NexusVariable Variable]
            instructions:
                add Variable.final -> finalCode
            """
        case 'calc':
            """
            regular calculation(save to &)
            args:
                [str expression]
            instructions:
                eval(expression)->&
            """
def identifyLineType(line:str)->tuple[str,Any]:
    """
    Tells if the line in question is:
        'bp' - Class definition
        'def' - Function definition
        'set' - Variable definition
        'calc' - Basic Calculations
    """
    
    if '//' in line:return None#comments
    if 'bp' in line:
        """
        This is a class definition
        return:
            ['bp',NexusClass Class]
        """
        classname=line.split('bp')[1].split('(')[0]
        args=tuple(line.split('[')[1].split(']')[0].split(','))
        #bp myClass(myClass[classArgs,args]{//code goes here} def def def def def)|
        code=line.split('{')[1].split('}')[0].split('|')
        for i in code:i+="|"
        return ['bp',NexusClass(classname,args,code,)]
    if 'def' in line:
        """
        This is a function definition
        return:
            ['def',NexusFunction Function]
        """
    if 'set' in line:
        """
        This is a variable definition
        return:
            ['set',NexusVariable Variable]
        """
        if 'to' not in line:raise SyntaxError("There is no to keyword to set name to.")
    if ('+' in line) or ('-' in line) or ('*' in line) or ('/' in line) or ('^' in line):
        """
        This is a calculation
        return:
            ['calc',string expression]
        """
        return ('calc',line)
"""
Class definition
        - Function definition
        - Variable definition
        - Basic Calculations
        - Comment

identifyLineType(line:str)->tuple[str,list](tuple of the string of keyword, list of arguments to pass to handleLineType based on that keyword)
if line contains bp:
    return ['bp',Class:NexusClass]
if line contains def:
    return ['def', Function:NexusFunction]
if line contains set:
    return ['set', Variable:NexusVariable]
if line contains if/while/for:

if line contains call:

"""

def helpp():
    a="""
    Argv:
    file.py target_file 
    Args:
    target_file
      """
    print(a)
    quit(NEXUS_ERRORS['HELP'])
if __name__=="__main__":
    """
    For each script there must be:
    local dictionary:
        holds all local variables,functions,classes in name:object format
    global dictionary:
        can be referenced everywhere and holds globally specified variables,functions,classes; OVERRIDES LOCAL IF SPECIFIED IN BOTH
    """
    args=argv[1:]
    if "?" in args or help in args: helpp()
    try:file=args[0]
    except IndexError:
        helpp()
        quit(NEXUS_ERRORS['NO_ARGS'])
    if not file.endswith(".nx"):
        print("Nexus files end in .nx. Aborting...")
        quit(NEXUS_ERRORS['WRONG_FILE_TYPE'])
    filename=file.replace(".nx","")
    try:
        with open(file,'r') as reader:
            file=reader.read()
            reader.close()
            tokens = file.replace('\n', '').replace("  ","").split("|")

            for token in tokens: 
                if (len(token) == 2 or len(token) == 1) and ('}' in token or ')' in token):
                    i = tokens.index(token)
                    tokens[i - 1] = tokens[i-1] + tokens[i]  # add the closing brackets to the one before deleting it
                    del tokens[i]
                # check for brackets opened that aren't closed
                if ('(' in token and ')' not in token) or ('{' in token and '}' not in token):
                    # these are not closed
                    i = tokens.index(token)
                    if ')' in tokens[i+1] or '}' in tokens[i+1]:
                        # add them together then delete the extra
                        tokens[i] = tokens[i] + tokens[i+1]
                        del tokens[i+1] 
            del tokens[len(tokens)-1]
            file=tokens
    except (FileNotFoundError,Exception):
        print("There was a file reading error.")
        quit(NEXUS_ERRORS['CANNOT_READ_FILE'])
    #file has text in it as list of lines
    for i in file:handleLineType(identifyLineType(i))
    """
    FIXING SOON
    """