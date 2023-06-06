# Nexus-Programming
A Python based interpreted programming language
Name:  Nexus
Author: Ixonblitz-MatOS
Version:  1.0.0b

Basic Information:
    Nexus is my first programming language attempt to make it through development. The file extensions is .nx. 

Syntax: 

    Creating a comment: 
        //This is a comment

    Creating a class:
        bp myClass(
            myClass[classArgs,args]{
                //code goes here
            }
        )

    Creating a global class:
        public bp myClass(
            myClass[classArgs,args]{
                //code goes here
            }
        )

    Creating a function:
        def myFunction[args]{
            //code goes here
        }

    Creating a global function:
        public def myFunction[args]{
            //code goes here
        }
    Calling a function:
        call myFunction [arg1,arg2,arg3]

    Defining a variable:
        set a to 1|         //a = 1
        set b to "yes"|     //b = "yes"

    Creating a global variable: 
        set a to 1 global   //global a ; a=1

    Using basic calculations:
        Basic calculations can be done and the most previous one will be saved to &
            set a to 30|
            2*5|            //This becomes &
            set a to a/&|   //a ends up with the value of 3;(30/(2*5))
            
