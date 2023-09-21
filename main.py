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
keywords=["if","while","for",'set','call','public','def','bp','throw']
globals={}
finalCode="RESERVED=locals['&']\n"#RESERVED holds the & in Nexus
UNARY_OPS = (UAdd, USub)
BINARY_OPS = (Add, Sub, Mult, Div, Mod)
def updateReserved(new:Any):
    locals['&']=new
    finalCode=
"""
Nexus Errors(manage exit codes):
HELP(1) - Help function
NO_ARGS(2) - No args were given to the interpreter
CANNOT_READ_FILE(3) - Cannot read the nexus file specified
WRONG_FILE_TYPE(4) - Not a nexus file
TESTING(5) - developmental quits
DEBUG(6) - developmental quits
IDENTIFY_UNRECOGNIZED(7) - identifyLineType() doesn't recognize the list
MISSING_ARGS_TESTING(8) - Classes are missing args during testing
IDENTIFY_NO_CODE(9) - Throwing errors for self.code not existing
"""
NEXUS_ERRORS={'HELP':1,'NO_ARGS':2,'CANNOT_READ_FILE':3,'WRONG_FILE_TYPE':4,'TESTING':5,'DEBUG':6,'IDENTIFY_UNRECOGNIZED':7,
              'MISSING_ARGS_TESTING':8,'IDENTIFY_NO_CODE':9,"RESERVED_NAME":10}
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
"""
Finished Functions: is_math,helpp,functionToDict,handleLine,pythonizeFunction
Working on: handleLineType,identifyLineType
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
    line=line.removesuffix("|")
    if 'set' in line:
        if forVar:raise SyntaxError("There cannot be a variable declaration within a variable declaration")
        if line.__contains__("&"):line.replace("&","RESERVED")
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
        except Exception:raise SyntaxError("The line could not be processed: ".join(line.split('(')[1].split(')')[0]))
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
    def __init__(self,name:str,args:tuple,code:list,isclass:bool,public:bool)->None:
        """
        :param str name: Name of the Function
        :param tuple args: args for the function declaration
        :param list code: list of nexus code to be pythonized
        :param bool isclass: if is in a class for indentation purposes
        """
        self.name=name
        self.args=str(args)
        self.nexuscode="".join(i for i in code)
        print("nexus code:" +self.nexuscode)
        self.code=str()
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
    def __call__(self,name:str,args:tuple,code:list,isclass:bool):self.__init__(name=name,args=args,code=code,isclass=isclass)
    def test(self)->str:
        return f"NAME:{self.name}\nARGS:{self.args}\nCODE:{self.code}\nFINAL:{self.final}"
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
        if name in keywords:
            print("Cannot name variables Keywords.")
            quit(NEXUS_ERRORS['RESERVED_NAME'])
        self.name=name
        self.value=handleLine(str(value))
        self._finalize()
    def _finalize(self)->None:self.final=f"{self.name}={str(self.value)}"

   
def functionToDict(functionname:str,args:tuple,code:list)->dict:
        """
        code is in nexus form not python
        """
        return {functionname:{"args":args,"code":code}}
def pythonizeFunction(function:dict)->str:
        "converts the Nexus function to python"
        code=f"def {list(function.keys())[0]}({str(function[list(function.keys())[0]]['args'])}):\n\t"
        for i in function[list(function.keys())[0]]["code"]:code+=handleLine(i)+"\n\t"
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
            finalCode+=args[0].final
        case 'def':
            """
            function identification
            args:
                [NexusFunction Function]
            instructions:
                add Function.final -> finalCode
            """
            finalCode+=args[0].final
        case 'set':
            """
            variable identification
            args:
                [NexusVariable Variable]
            instructions:
                add Variable.final -> finalCode
            """
            finalCode+=args[0].final
        case 'calc':
            """
            regular calculation(save to &)
            args:
                [str expression]
            instructions:
                eval(expression)->&
            """
def identifyLineType(line:str,extra:dict)->tuple[str,Any]:
    """
    :param dict: extra {"isClass":True|False}
    Tells if the line in question is:
        'bp' - Class definition
        'def' - Function definition
        'set' - Variable definition
        'calc' - Basic Calculations
        'call' - Call existing class function or variabl
    """
    operators=['+','-','*','/','^']
    if line.startswith('//'):return None#comments
    elif 'bp' in line:
        """
        This is a class definition
        return:
            ['bp',NexusClass Class]
        """
        classname=line.split('bp')[1].split('(')[0]
        args=tuple(line.split('[')[1].split(']')[0].split(','))
        """
        "bp myClass(myClass[arg1]{set myArg to arg1|}def a[arg2]{//code|}def b[arg2]{//code|})|"
        """
        code=line.split('{')[1].split('}')[0].split('|')
        for i in code:i+="|"
        functions=[]
        indx=line.find("}")
        final=line[indx+1:len(line)-2]
        #def a[arg2]{//code|}def b[arg2]{//code|}
        lists=final.split('}')
        for i in lists:
            i+="}"
            functions.append(identifyLineType(i,{'isClass':True})[1])
        try:
            return ['bp',NexusClass(name=classname,args=args,code=code,functions=functions)]
        except (TypeError,AttributeError) as e:
            if e.args[0].__contains__('AttributeError'):
                print("Nexus No Code Provided: ".join(e.args[0]))
                quit(NEXUS_ERRORS['IDENTIFY_NO_CODE'])
            else:
                print("Missing args: ".join(e.args[0]))
                quit(NEXUS_ERRORS['MISSING_ARGS_TESTING'])
    elif 'def' in line:
        """
        This is a function definition
        return:
            ['def',NexusFunction Function]
        """
        #def a[arg2]{//code|}
        functionname=line.split("def")[1].split("[")[0].strip()
        args=[i for i in line.split('[')[1].split(']')[0].split(',')]
        openIndex,closeIndex=line.find('{')+1,line.find("}")        
        code=[i for i in line[openIndex:closeIndex].split('|')]
        print(f"Code: {code}")
        finalcode=[]
        for i in code:finalcode.append(i+'|')
        return ['def',NexusFunction(name=functionname,args=tuple(args),code=finalcode,isclass=extra['isClass'])]
    elif 'set' in line:
        """
        This is a variable definition
        return:
            ['set',NexusVariable Variable]
        """
        if 'to' not in line:raise SyntaxError("There is no to keyword to set name to.")
    elif any(op in line for op in operators):
        """
        This is a calculation
        return:
            ['calc',string expression]
        """
        return ('calc',line)
    else:
        print("Unrecognized Line")
        quit(NEXUS_ERRORS['IDENTIFY_UNRECOGNIZED'])
"""
Class definition
        - Function definition
        - Variable definition
        - Basic Calculations
        - Comment

identifyLineType(line:str)->tuple[str,Any](tuple of the string of keyword, list of arguments to pass to handleLineType based on that keyword)
if line contains bp:
    return ['bp',Class:NexusClass]
if line contains def:
    return ['def', Function:NexusFunction]
if line contains set:
    return ['set', Variable:NexusVariable]
if line contains if/while/for:

if line contains call:

"""
def testFunction():
    """
    Tested:
        identifyLineType():
            - Calculations(1+1,1^1) | WORKING
            - Comments("//This is a comment to be ignored") | WORKING
            - bp("bp myClass(myClass[arg1]{set myArg to arg1|}def a[arg2]{//code|}def b[arg2]{//code|})|") | NOT WORKING> Need to break down functions for Nexus Class
            - def() | UNCODED
            - set() | UNCODED
    """
    a={"a":1,"b":2}
    print(list(a.keys())[1])
    # f=identifyLineType("def a[arg2]{1+1|set a to &|}",extra={'isClass':True})[1]
    # print(f.test())
    # quit(NEXUS_ERRORS['TESTING'])
    print(pythonizeFunction(functionToDict("myFunction",("arg1"),["1+1|","set a to &|"])))
testFunction()
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