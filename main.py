from typing import Any, List, Union

def tokeniseEquation(equation:str) -> List[Any]: # currently broken for floats and doesnt even work for negative numbers...

    num = 0
    power = 0
    isFloat = False
    tokens = []

    for i, char in enumerate(reversed(equation)):
        if char.isnumeric():
            
            if isFloat:
                num += int(char) * (10** -power)
            else:
                num += int(char) * (10** power)
            power += 1
        elif char == '.':
            
            if len(equation) > i and equation[i+1].isnumeric():
                isFloat = True 
        else:
            
            if num != 0:
                tokens.append(num)
            tokens.append(char)
            num = 0
            power = 0

    if num != 0:
        tokens.append(num)

    return tokens[::-1]

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

    print(stack)

    return stack[-1]

def evalEquation(equation:str)-> Union[float, int]:
    return evalPostFix(infixToPostFix(tokeniseEquation(equation)))

equation = "(5*4+3*2)-1"

print(tokeniseEquation(equation))

print(evalEquation(equation))