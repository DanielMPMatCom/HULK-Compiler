from src.hulk.hulk_ast import *
from src.cmp.semantic import *
from src.cmp.visitor import visitor

import math
import random

built_in_func = {
    'print': lambda x: print(x),
    'sqrt': lambda x: math.sqrt(x),
    'sin': lambda x: math.sin(x),
    'cos': lambda x: math.cos(x),
    'exp': lambda x: math.exp(x),
    'log': lambda y, x: math.log(x, y),
    'rand': lambda : random.random(),
    'parse': lambda x: float(x)
}

binary_operators = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '%': lambda x, y: x % y,
    '@': lambda x, y: x + y,
    '>': lambda x, y: x > y,
    '<': lambda x, y: x < y,
    '^': lambda x, y: x ** y,
    '|': lambda x, y: x or y,
    '&': lambda x, y: x and y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y,
    # '@@': lambda x, y:
    # '=>': lambda x, y:
    # '**': lambda x, y:

}

unary_operators = {
    '!': lambda x: not x,
    '-': lambda x: -x
}


class Interpeter():
    def __init__(self, context, errors=[]):
        self.context:Context = context
        self.errors:list = errors
        
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode):
        for declaration in node.declarations:
            self.visit(declaration)

    @visitor.when(FunctionCallNode)
    def visit(self, node:FunctionCallNode):
        if node.identifier in built_in_func:
            return built_in_func[node]
                
        function = node.scope.get_global_function_info(node.identifier, len(node.args))
        scope:Scope = function.body.scope

        params = [self.visit(param) for param in node.args]

        for i, name in enumerate(function.param_names):
            variable = scope.get_local_variable_info('name')
            variable.update(params[i])

        return self.visit(function.body)

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node:FunctionDeclarationNode):
        function = node.scope.get_local_function_info(node.identifier, len(node.params_ids))
        function.body = node.expression
        return
    
    @visitor.when(VariableDeclarationNode)
    def visit(self, node:VariableDeclarationNode):
        variable = node.scope.get_local_variable_info(node.identifier)
        variable.value = self.visit(node.expression)
        return

    @visitor.when(LetInNode)
    def visit(self, node:LetInNode):
        for declaration in node.assignment_list:
            self.visit(declaration)
        return self.visit(node.expression)

    @visitor.when(IfElseNode)
    def visit(self, node:IfElseNode):
        for i, condition in enumerate(node.conditions):
            if self.visit(condition):
                return self.visit(node.expressions[i])
            return self.visit(node.else_expression)
        
    @visitor.when(WhileNode)
    def visit(self, node:WhileNode):
        evaluation = None
        while self.visit(node.condition):
            evaluation = self.visit(node.expression)
        return evaluation

    @visitor.when(ForNode)
    def visit(self, node:ForNode):
        evaluation = None
        for variable in self.visit(node.iterable_expression):
            iterator = node.scope.get_local_variable_info()
            iterator.update(variable)
            evaluation = self.visit(node.expression)
        return evaluation
    
    @visitor.when(NumNode)
    def visit(self, node:NumNode):
        try:
            return int(node.lexeme)
        except:
            return float(node.lexeme)
        
    @visitor.when(StringNode)
    def visit(self, node:StringNode):
        return node.lexeme[1:-1]
    
    @visitor.when(BoolNode)
    def visit(self, node:BoolNode):
        if node.lexeme == 'True':
            return True
        else:
            return False
            
    @visitor.when(IDNode)
    def visit(self, node:IDNode):
        return node.lexeme
    
    def binary_operation(self, node:BinaryExpressionNode):
        left_value = self.visit(node.left_expression)
        right_value = self.visit(node.right_expression)

        return binary_operators[node.operator](left_value, right_value)

    def unary_operation(self, node:UnaryExpressionNode):
        value = self.visit(node.expression)

        return unary_operators[node.operator](value)
    
    @visitor.when(BoolBinaryOpNode)
    def visit(self, node:BoolBinaryOpNode):
        return self.binary_operation(node)

    @visitor.when(EqualityBinaryOpNode)
    def visit(self, node:EqualityBinaryOpNode):
        return self.binary_operation(node)
    
    @visitor.when(InequalityBinaryOpNode)
    def visit(self, node:InequalityBinaryOpNode):
        return self.binary_operation(node)
        
    
    @visitor.when(StringBinaryOpNode)
    def visit(self, node:StringBinaryOpNode):
        return self.binary_operation(node)


    @visitor.when(ArithmeticBinaryOpNode)
    def visit(self, node:ArithmeticBinaryOpNode):
        return self.binary_operation(node)

    @visitor.when(SignUnaryOpNode)
    def visit(self, node:SignUnaryOpNode):
        return self.unary_operation(node)
    
    @visitor.when(NotUnaryOpNode)
    def visit(self, node:NotUnaryOpNode):
        return self.unary_operation(node)
    
    @visitor.when(ExpressionBlockNode)
    def visit(self, node:ExpressionBlockNode):
        evaluation = None
        for expression in node.expressions:
            evaluation = self.visit(expression)
        return evaluation
        
    

    

    
    
    