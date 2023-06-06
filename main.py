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
from shutil import move
import ast,os
locals={"&":None}
globals={}
finalCode="RESERVED=locals['&']\n"#RESERVED holds the & in Nexus
UNARY_OPS = (ast.UAdd, ast.USub)
BINARY_OPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod)
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
def handleLine(line:str)->str:
    """
    returns the python version of each line given
    """
    code=""
    if not line.endswith("|"):raise SyntaxError("There is no | character at the end of the line.")
    if 'set' in line:code+=f"{line.split()[1]}={line.split()[3]}"
    if is_math(line):
        locals["&"]=eval(line)
        code+=f"RESERVED={eval(line)}"
    if '//' in line:code+=f"#{line[2:]}"
    if '(' in line and ')' in line:
        if 
        pass
    return code
def pythonizeFunction(function:dict)->str:
    "converts the Nexus function to python"
    code=f"def {function.keys()[0]}{str(function[function.keys()[0]]['args'])}:\n"
    for i in function[function.keys()[0]]["code"]:code+=handleLine(i)+"\n\t"
    return code
def handleLineType(t:str,args:list)->None:
    """
    Handles what to do with the line
    Returns nothing because it will be handled here before moving on
    :NOTE: functions always be passed as dictionaries like: 
    a={
        functionname:
            {
                'args':(arg,arg),
                'code';[code,code,code]
            }
    }
    and are referenced like 
    a[functionname][args] or a[functionname][code]
    """
    match t:
        case "bp":
            """
            :param: classname:str ; This includes the inherit statement if specified
            :param: constructorParams:tuple
            :param: functions:dict format
            """
            classname=args[0]
            if "inherits" in classname:
                classnameActual=classname.split()[0]
                inherited=classname.split()[2]
                classname=f"{classnameActual}({inherited}):"
            else:classname=f"{classname}:"
            constructorParams=args[1]
            finalConstructorParams=""
            for i in constructorParams:finalConstructorParams+=i+","
            finalConstructorParams=finalConstructorParams.rstrip(finalConstructorParams[-1])
            functions=args[2]
            initCode=functions[classnameActual]["code"]
            finalInit=""
            for i in initCode:finalInit+=handleLine(i)+";"
            code=f"class {classname}\n\tdef __init__(self,{finalConstructorParams}):\n\t\t{finalInit}"


            finalCode+=code+"\n"
        case "func":
            """
            :param: func:dict format
            """
            code=f""
            finalCode+=code+"\n"
        case "var":
            """
            :param: name:str
            :param: value:type|Any
            :param: scope:bool; True:global False:local
            """

            code=f""
            finalCode+=code+"\n"
        case "calc":
            """
            :param: value:int|float|Any

            Whenever & is called technically it is the RESERVED variable because & isn't supported as python variable name
            """
            value=eval(args[0])
            locals["&"]=value#update locals value
        case "comment":
            """
            :param: text
            """
            code=f"#{args[0]}"
            finalCode+=code+"\n"
def identifyLineType(line:str)->tuple[str,list]:
    """
    Tells if the line in question is:
        - Class definition
        - Function definition
        - Variable definition
        - Basic Calculations
        - Comment
    """
    if 'bp' in line:
        """
        it is a class definition with the syntax:
        bp myClass(
            myClass[arg1,arg2]{
            code
            }
        )
        Ways to throw errors:
            Uses special characters as name
            missing open or close parenthases
            missing contructor definition
            
        return
            :type: type(bp)
            :param: classname:str ; This includes the inherit statement if specified
            :param: constructorParams:tuple
            :param: functions:dict format
        """
        #bp Myclass inherits Class(Myclass[]{})
        classname=line.split("(")[0].split()#["bp,"Myclass","inherits","Class"]
        Actualname=classname[1]
        if "inherits" in classname:classname=classname[1]+classname[2]+classname[3]#"Myclass inherits Class"
        else:classname=classname[1]
        #one liners vs multi line matter now for text processing of Constructor params and constructor code
        if "(" in line and ")" in line:
            """
            One liners should be handled like :
                bp Myclass inherits Class(Myclass[]{})
            """
            #bp myClass(myClass[arg1]{set myArg to arg1}def a[arg2]{//code', '}def b[arg2]{//code})
            constructorParams=line.split("(")[1].replace(Actualname,"").split("]")[0].replace("[","").split(",") #shows list of init params
            codeLines=line.split("{")[1].split("}")[0].split("|") #[cod,code,code]
        else:raise SyntaxError("Missing Parenthases")
        functions={
            functionToDict(Actualname,tuple(constructorParams),codeLines),#This is init function 
            }
        funcs=[]# holds(functionname:str,params:tuple,codelines:list)
        #bp myClass(myClass[arg1]{set myArg to arg1}def a[arg2]{//code', '}def b[arg2]{//code})
        numFuncs=line.split("def")[1:]#[" a[arg2]{//code', '}", ' b[arg2]{//code})']
        for i in numFuncs:funcs.append((i.split("[")[0],i.split("[")[1].split("]")[0],i.split("{")[1].split("}")[0].split("|")))
        for i in funcs:functions.add(functionToDict(i[0],i[1],i[2]))
        return ("bp",[classname,constructorParams,functions])
        
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
    with open(filename+'.py',"w+") as writer:
        writer.write(finalCode)
        writer.close()
    os.system(f"pyinstaller --onefile {filename+'.py'}")
    os.remove(filename+'.py')
    move(f"./dist/{filename+'.exe'}",f"./{filename+'.exe'}")
    os.rmdir("./dist")
    exec(f"./{filename+'.exe'}")
    """
    Essentially compile the python file, delete the python file, move exe from dist and delete dist
    """