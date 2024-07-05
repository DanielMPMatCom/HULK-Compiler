from src.hulk.hulk_ast import *
from src.cmp.semantic import *
from src.cmp.visitor import visitor

import math
import random
import copy


def Print(x):
    print(x)
    return x


built_in_func = {
    "print": lambda x: Print(x),
    "sqrt": lambda x: math.sqrt(x),
    "sin": lambda x: math.sin(x),
    "cos": lambda x: math.cos(x),
    "exp": lambda x: math.exp(x),
    "log": lambda y, x: math.log(x, y),
    "rand": lambda: random.random(),
    "parse": lambda x: float(x),
}

binary_operators = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "%": lambda x, y: x % y,
    "@": lambda x, y: x + y,
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
    "^": lambda x, y: x**y,
    "|": lambda x, y: x or y,
    "&": lambda x, y: x and y,
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    ">=": lambda x, y: x >= y,
    "<=": lambda x, y: x <= y,
    "**": lambda x, y: x**y,
    "@@": lambda x, y: x + " " + y,
}

unary_operators = {"!": lambda x: not x, "-": lambda x: -x}


class Interpeter:
    def __init__(self, context, errors=[]):
        self.context: Context = context
        self.errors: list = errors

    def binary_operation(self, node: BinaryExpressionNode):
        left_value = self.visit(node.left_expression)
        right_value = self.visit(node.right_expression)

        return binary_operators[node.operator](left_value, right_value)

    def unary_operation(self, node: UnaryExpressionNode):
        value = self.visit(node.expression)

        return unary_operators[node.operator](value)

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for declaration in node.declarations:
            self.visit(declaration)

# TypeDeclarationNode(DeclarationNode):
    @visitor.when(TypeDeclarationNode)
    def visit(self, node: TypeDeclarationNode):
        return node

# FunctionDeclarationNode(DeclarationNode):
    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode):
        # function = node.scope.get_local_function_info(
        #     node.identifier, len(node.params_ids)
        # )
        function = self.context.get_function_by_name(node.identifier)
        function.body = node.expression
        return

# ProtocolDeclarationNode(DeclarationNode):
    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node : ProtocolDeclarationNode):
        return
       
# MethodNode(DeclarationNode):
    @visitor.when(MethodNode)
    def visit(self, node: MethodNode):
        return

# AttributeNode(DeclarationNode):
    @visitor.when(AttributeNode)
    def visit(self, node: AttributeNode):
        node.scope.define_variable(f'self.{node.identifier}')
        value = self.visit(node.expression)
        var = node.scope.get_local_variable_info(f'self.{node.identifier}')
        var.update(value)

# ProtocolMethodSignatureNode(DeclarationNode):
    @visitor.when(ProtocolMethodSignatureNode)
    def visit(self, node: ProtocolMethodSignatureNode):
       return

# VectorNode(ExpressionNode):
    @visitor.when(VectorNode)
    def visit(self, node: VectorNode):
       return
    
# VariableDeclarationNode(DeclarationNode):
    @visitor.when(VariableDeclarationNode)
    def visit(self, node: VariableDeclarationNode):
        variable = node.scope.get_local_variable_info(node.identifier)
        value = self.visit(node.expression)
        variable.update(value)
        return

# ExpressionBlockNode(ExpressionNode):
    @visitor.when(ExpressionBlockNode)
    def visit(self, node: ExpressionBlockNode):
        evaluation = None
        for expression in node.expressions:
            evaluation = self.visit(expression)
        return evaluation

# LetInNode(ExpressionNode):
    @visitor.when(LetInNode)
    def visit(self, node: LetInNode):
        for declaration in node.assignment_list:
            self.visit(declaration)
        return self.visit(node.expression)

# IfElseNode(ExpressionNode):
    @visitor.when(IfElseNode)
    def visit(self, node: IfElseNode):
        for i, condition in enumerate(node.conditions):
            if self.visit(condition):
                return self.visit(node.expressions[i])
        return self.visit(node.else_expression)

# WhileNode(ExpressionNode): Explotar si evaluation es None
    @visitor.when(WhileNode)
    def visit(self, node: WhileNode):
        evaluation = None
        while self.visit(node.condition):
            evaluation = self.visit(node.expression)
        return evaluation    
    
# ForNode(ExpressionNode):
    @visitor.when(ForNode)
    def visit(self, node: ForNode):
        evaluation = None
        iterator = node.scope.get_local_variable_info(node.iterator)
        for variable in self.visit(node.iterable_expression):
            iterator.update(variable)
            evaluation = self.visit(node.expression)
        return evaluation

# DestructiveOperationNode(ExpressionNode):
    @visitor.when(DestructiveOperationNode)
    def visit(self, node: DestructiveOperationNode):
        vname = node.destiny # Revisar si esto es el identifier, asumimos que si
        variable = node.scope.get_global_variable_info(vname)
        value = self.visit(node.expression)
        variable.update(value)

# NewTypeNode(ExpressionNode):
    @visitor.when(NewTypeNode)
    def visit(self, node: NewTypeNode):
        type_node = self.context.id_to_type[node.identifier]
        type_node : TypeDeclarationNode = copy.deepcopy(type_node)

        scope = type_node.scope

        for i, vname in enumerate(type_node.params_ids):
            scope.define_variable(vname, None)
            variable = scope.get_global_variable_info(vname)
            value = self.visit(node.args[i])
            variable.update(value)

# IsNode(ExpressionNode):
    @visitor.when(IsNode)
    def visit(self, node: IsNode):
        pass

# AsNode(ExpressionNode):
    @visitor.when(AsNode)
    def visit(self, node: AsNode)

# FunctionCallNode(ExpressionNode):
    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode):
        
        
        params = [self.visit(param) for param in node.args]    
        
        if node.identifier in built_in_func:  
            return built_in_func[node](tuple(params))

        function: Function = self.context.get_function_by_name(node.identifier)
        scope: Scope = function.body.scope

        for i, name in enumerate(function.param_names):
            variable = scope.get_local_variable_info(name)
            variable.update(params[i])

        return self.visit(function.body)

# MethodCallNode(ExpressionNode):

# AttributeCallNode(ExpressionNode):

# BaseCallNode(ExpressionNode):

# IndexNode(ExpressionNode):

# UnaryExpressionNode(ExpressionNode, ABC):

# BinaryExpressionNode(ExpressionNode, ABC):

# InitializeVectorNode(ExpressionNode):

# InitializeVectorListComprehensionNode(ExpressionNode):

# NumNode(AtomNode):
    @visitor.when(NumNode)
    def visit(self, node: NumNode):
        return float(node.lexeme)

# StringNode(AtomNode):
    @visitor.when(StringNode)
    def visit(self, node: StringNode):
        return node.lexeme[1:-1]

# BoolNode(AtomNode):
    @visitor.when(BoolNode)
    def visit(self, node: BoolNode):
        return node.lexeme is "true"

# IDNode(AtomNode):
    @visitor.when(IDNode)
    def visit(self, node: IDNode):
        return node.lexeme

# OrNode(BoolBinaryOpNode):
# AndNode(BoolBinaryOpNode):
    @visitor.when(BoolBinaryOpNode)
    def visit(self, node: BoolBinaryOpNode):
        return self.binary_operation(node)

# EqualNode(EqualityBinaryOpNode):
    @visitor.when(EqualityBinaryOpNode)
    def visit(self, node: EqualityBinaryOpNode):
        return self.binary_operation(node)

# NonEqualNode(InequalityBinaryOpNode):
# LessThanNode(InequalityBinaryOpNode):
# LessEqualNode(InequalityBinaryOpNode):
# GreaterThanNode(InequalityBinaryOpNode):
# GreaterEqualNode(InequalityBinaryOpNode):
    @visitor.when(InequalityBinaryOpNode)
    def visit(self, node: InequalityBinaryOpNode):
        return self.binary_operation(node)

# ConcatNode(StringBinaryOpNode):
# SpacedConcatNode(StringBinaryOpNode):
    @visitor.when(StringBinaryOpNode)
    def visit(self, node: StringBinaryOpNode):
        return self.binary_operation(node)

# PlusNode(ArithmeticBinaryOpNode):
# MinusNode(ArithmeticBinaryOpNode):
# StarNode(ArithmeticBinaryOpNode):
# DivNode(ArithmeticBinaryOpNode):
# ModNode(ArithmeticBinaryOpNode):
# PowNode(ArithmeticBinaryOpNode):
    @visitor.when(ArithmeticBinaryOpNode)
    def visit(self, node: ArithmeticBinaryOpNode):
        return self.binary_operation(node)

# MinusNode(SignUnaryOpNode):
    @visitor.when(SignUnaryOpNode)
    def visit(self, node: SignUnaryOpNode):
        return self.unary_operation(node)

# NotNode(NotUnaryOpNode):
    @visitor.when(NotUnaryOpNode)
    def visit(self, node: NotUnaryOpNode):
        return self.unary_operation(node)