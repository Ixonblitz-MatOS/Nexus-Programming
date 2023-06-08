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
    def findOpens(self,char:str,startIndex:int=0)->list[int,]:
        """
        :param str char: the open character to be found
        :param int startIndex: the index to start looking at
        :returns list[int,]: returns list of indexs where opens of that character are found 
        """
        counter=startIndex
        final=[]
        try:
            while True:
                if self[counter]==char:final.append(counter)
                counter+=1
        except IndexError:return final
    def findNextOpen(self,char:str,startIndex:int)->int:
        counter=startIndex
        try:
            while True:
                if self[counter]==char:return counter
                counter+=1
        except IndexError:raise SyntaxError("The proper function syntax has not been met according to findNextOpen() check for next open brackets")
        
    def findAllOccurrencesOfFunctions(self)->list[int,]:
        """
        :returns list[int,]: list of indexs where def are found

        """
        counter=0
        while True:
            if self[counter:counter+3]=="def":
                #we know this counter - counter +3 has def but there are brackets of args and {} of code from it
                pass
            counter+=1
    def findFunctionStrings(self)->list[str]:pass
print("defww"[0:3])