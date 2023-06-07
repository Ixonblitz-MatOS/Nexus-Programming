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
from ast import UAdd,USub,Add,Sub,Mult,Div,Mod
from typing import Callable as Function
from typing import Any
locals={"&":None}
globals={}
finalCode="RESERVED=locals['&']\n"#RESERVED holds the & in Nexus
UNARY_OPS = (UAdd, USub)
BINARY_OPS = (Add, Sub, Mult, Div, Mod)
"""
Finished Functions: is_math,helpp,functionToDict
Working on: handleLine,pythonizeFunction,handleLineType,identifyLineType

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

    Write functions to simplify main block at bottom:
    def writeFile(file):open(file,'w+').write(finalCode)
    def compileFile(file):system(pyinstaller --onefile --distpath ./ file.py)
    Maybe add a way to test functions by simulating flows of data:
        def test(function:Function,args:tuple)->str:pass
        print(test(identifyLineType,("bp myClass(myClass[args]{})|"))->string containing the output ['bp',['myClass',(args),{'myClass':{"args":(args),"code":""}}]]
"""
def handleLine(line:str)->str:
    """
    returns the python version of each line given
    class or function definitions cannot be given to this function(they get predefined and interpretted separately by their respective objects)
    Possible lines given:
        1. set a to value
        2. 2*5
        3. 
    """
    code=""
    if not line.endswith("|"):raise SyntaxError("There is no | character at the end of the line.")
    if 'set' in line:code+=f"{line.split()[1]}={line.split()[3]}"
    if is_math(line):
        locals["&"]=eval(line)
        code+=f"RESERVED={eval(line)}"
    if '//' in line:code+=f"#{line[2:]}"
    if '(' in line and ')' in line:
        
        pass
    return code
class NexusClass:
    """
    Python class for holding Nexus Class info
    """
class NexusFunction(Function):
    """
    Python class for holding Nexus Function info
    """
    name:str
    args:str
    code:str
    final:str
    def __init__(self,name:str,args:tuple,code:list)->None:
        """
        :param str: Name of the Function
        :param tuple: args for the function declaration
        :param list: list of nexus code to be pythonized
        """
        self.name=name
        self.args=str(args)
        self._handleCode(code)#update self.code
        self.final=self._finalize()#update self.final
    def _code(self,code:list)->str:
        """
        Pythonize all code and then add to self.code
        *REQUIRES handleLine() TO BE FUNCTIONAL*
        """
        for i in code:self.code+=f"\t{handleLine(i)}\n"
    def _finalize(self)->None:
        """
        Used to save the whole code block to self.final
        def myFunction[arg,arg2]{               def myFunction(arg,arg2):
            code                        ->          code
        }
        """
        self.final=f"def {self.name}{self.args}:\n{self.code}"
class NexusVariable:
    """
    Python class for holding Nexus Variable Info
    """
class finished:
    def is_math(s):
        def _is_arithmetic(node):
            if isinstance(node, ast.Num):
                return True
            elif isinstance(node, ast.Expression):
                return _is_arithmetic(node.body)
            elif isinstance(node, ast.UnaryOp):
                valid_op = isinstance(node.op, UNARY_OPS)
                return valid_op and _is_arithmetic(node.operand)
            elif isinstance(node, ast.BinOp):
                valid_op = isinstance(node.op, BINARY_OPS)
                return valid_op and _is_arithmetic(node.left) and _is_arithmetic(node.right)
            else:
                raise ValueError('Unsupported type {}'.format(node))

        try:
            return _is_arithmetic(ast.parse(s, mode='eval'))
        except (SyntaxError, ValueError):
            return False
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
    return ['bp',[classname:str,constructorParams:tuple,functions:NexusFunction]]
if line contains def:

if line contains set:

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
    quit()
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
    file=args[0]
    if not file.endswith(".nx"):
        print("Nexus files end in .nx. Aborting...")
        quit(1)
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
        quit(1)
    #file has text in it as list of lines
    for i in file:handleLineType(identifyLineType(i))
    """
    FIXING SOON
    """