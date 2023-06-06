# """
# exec defining classes and functions are updated to locals() every time
# """
# a=open("example.nx",'r').read()
# tokens = a.replace('\n', '').replace("  ","").split("|")

# for token in tokens: 
#     if (len(token) == 2 or len(token) == 1) and ('}' in token or ')' in token):
#         i = tokens.index(token)
#         tokens[i - 1] = tokens[i-1] + tokens[i]  # add the closing brackets to the one before deleting it
#         del tokens[i]
#     # check for brackets opened that aren't closed
#     if ('(' in token and ')' not in token) or ('{' in token and '}' not in token):
#         # these are not closed
#         i = tokens.index(token)
#         if ')' in tokens[i+1] or '}' in tokens[i+1]:
#             # add them together then delete the extra
#             tokens[i] = tokens[i] + tokens[i+1]
#             del tokens[i+1] 
# del tokens[len(tokens)-1]
# print(tokens)
#temp="bp myClass(myClass[arg1,arg2]{set myArg to arg1|set a to arg2|}def a[arg2]{//code', '}def b[arg2]{//code})"
#print(temp.split("{")[1].split("}")[0].split("|"))
a=(1,2,3)
print(str(a))