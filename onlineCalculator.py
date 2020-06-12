from flask import Flask, request, render_template, session
import re, jinja2, secrets

app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)

# Setup for Jinja
loader = jinja2.FileSystemLoader('./templates/index.html')
env = jinja2.Environment(loader=loader)
template = env.get_template('')
history = []

@app.route("/")
def main():
    return template.render(hist = history)
    
@app.route("/", methods=['POST'])
def main_post():
    input = request.form['calc']
    result = str(evaluate(input))
    if (len(history) == 10):
        history.pop(0)
    history.append(str(input) + " = " + result)
    return template.render(hist = history)


# Functions below used for parsing and evaluating input
# Validation function
def is_number(char):
    try:
        int(char)
        return True
    except ValueError:
        return False
 
 # Categorization functions
def peek(stack):
    if (stack):
        return stack[-1] 
    else: 
        return None
 
def greater_precedence(op1, op2):
    precedences = {'+' : 0, '-' : 0, '*' : 1, '/' : 1}
    return precedences[op1] > precedences[op2]
    
def apply_operator(operators, values):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    values.append(eval("{0}{1}{2}".format(left, operator, right)))
 
# Computation functions
def evaluate(expression):
    tokens = re.findall("[+/*()-]|\d+", expression)
    values = []
    operators = []
    for t in tokens:
        if is_number(t): # Token is a digit
            values.append(int(t))
        elif t == '(':
            operators.append(t)
        elif t == ')':
            top = peek(operators)
            while top is not None and top != '(':
                apply_operator(operators, values)
                top = peek(operators)
            operators.pop()
        else: # Token is an operator
            top = peek(operators)
            while top is not None and top not in "()" and greater_precedence(top, t):
                apply_operator(operators, values)
                top = peek(operators)
            operators.append(t)
    while peek(operators) is not None:
        apply_operator(operators, values)
    try:
        return values[0]
    except IndexError:
        return "That's not a real equation, silly."