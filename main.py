from typing import Any, List, Union

def tokeniseEquation(equation:str) -> List[Any]: 

    num = 0
    tokens = []
    isNegative = False

    for i, char in enumerate(equation):
        
        if char.isnumeric():
            if isNegative:
                num = -(num * 10 + (int(char)))
            else:
                num = num * 10 + (int(char))

        elif char == '-':
            
            if i == 0:
                isNegative = True
            elif i - 1 >= 0:
                if equation[i-1].isnumeric() == False:
                    isNegative = True
                else:
                    if num != 0:    # Not following DRY here at all, but IT WORKS!!!
                        tokens.append(num)
                        num = 0
                        isNegative = False
                    tokens.append(char)
        else:
            if num != 0:
                tokens.append(num)
                num = 0
                isNegative = False
            tokens.append(char)
            
    if num != 0:
        tokens.append(num)

    return tokens


def isNumeric(token:Any):
    return type(token) == float or type(token) == int

def infixToPostFix(equation: List[Any])-> List[Any]: 

    stack = [] #LIFO
    queue = [] #FIFO

    operators = {
        "+" : 0,
        "-" : 0,
        "*" : 1,
        "/" : 1,
        ")" : 2,
        "(" : 2
    }

    for token in equation:
        if isNumeric(token):
            queue.append(token)
        else:
            if token == ')':
                while len(stack) > 0 and stack[-1] !='(':
                    if operators[stack[-1]] < 2:
                        queue.append(stack[-1])
                        stack.pop()
                    else:
                        stack.pop()
            else:
                if len(stack) > 0 and operators[token] <= operators[stack[-1]] and operators[stack[-1]] < 2:

                    queue.append(stack[-1])
                    stack.pop()
                    stack.append(token)
                else:
                    stack.append(token)

    while len(stack) > 0:

        if operators[stack[-1]] < 2:
            queue.append(stack[-1])
            stack.pop()
        else:
            stack.pop()   
    return queue

def evalPostFix(queue:list) -> Union[float, int]:

    stack = []
    lvalue = None
    rvalue = None

    for token in queue:
        if isNumeric(token):
            stack.append(token)
        else:
            
            rvalue = stack[-1]
            stack.pop()
            lvalue = stack[-1]
            stack.pop()

            match token:

                case "+":
                    stack.append(lvalue + rvalue)  
                case "*":
                    stack.append(lvalue * rvalue)
                case "/":
                    stack.append(lvalue / rvalue) 
                case "-":
                    stack.append(lvalue - rvalue)

    return stack[-1]

def evalEquation(equation:str)-> Union[float, int]:
    return evalPostFix(infixToPostFix(tokeniseEquation(equation)))

eq = "(-1+20*3-1)-1"

print(f"Equation {eq}\n" +"-"*32 )
print(f"Tokenised {tokeniseEquation(eq)}\n" +"-"*32 )
print(f"infixToPostFix {infixToPostFix(tokeniseEquation(eq))}\n" +"-"*32 )
print(f"{eq} = {evalEquation(eq)}")
