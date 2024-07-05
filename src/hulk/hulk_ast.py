from abc import ABC
from typing import List, Tuple
from cmp.ast import*
from cmp.semantic import Scope



#----------------------------------------------------------Level0---------------------------------------------------------#

class Node:
    def __init__(self, line=None, column=None):
        self.scope : Scope
        self.line = line
        self.column = column

#----------------------------------------------------------Level1---------------------------------------------------------#

class ProgramNode(Node):
    def __init__(self, declarations, expression):
        Node.__init__(self)
        self.declarations = declarations
        self.expression = expression
    
class DeclarationNode(Node, ABC):
    pass

class ExpressionNode(Node, ABC):
    pass


#----------------------------------------------------------Level2---------------------------------------------------------#

class TypeDeclarationNode(DeclarationNode):
    def __init__(self, identifier, params, type_body, type_parent, type_parent_args=None):
        DeclarationNode.__init__(self)
        if params and len(params) > 0:
            params_ids, params_types = [(param[0], param[1]) for param in params]
        elif params:
            params_ids, params_types = [], []
        else: 
            params_ids, params_types = None, None

        methods = [method for method in type_body if isinstance(method, MethodNode)]
        attributes = [attr for attr in type_body if isinstance(attr, AttributeNode)]
        self.identifier = identifier
        self.params_ids = params_ids
        self.params_types = params_types
        self.methods = methods
        self.attributes = attributes
        self.parent = type_parent
        self.type_parent_args = type_parent_args

class FunctionDeclarationNode(DeclarationNode):
    def __init__(self, identifier, params, expression, type=None):
        DeclarationNode.__init__(self)
        if len(params) > 0:
            params_ids, params_types = [(param[0], param[1]) for param in params]
        else: 
            params_ids, params_types = [], []
        self.params_ids = params_ids
        self.params_types = params_types
        self.identifier = identifier
        self.expression = expression
        self.type = type

class ProtocolDeclarationNode(DeclarationNode):
    def __init__(self, identifier, signatures, parent):
        DeclarationNode.__init__(self)
        self.identifier = identifier
        self.signatures = signatures
        self.parent = parent

class MethodNode(DeclarationNode):
    def __init__(self, identifier, params, expression, type=None):
        DeclarationNode.__init__(self)
        if len(params) > 0:
            params_ids, params_types = [(param[0], param[1]) for param in params]
        else: 
            params_ids, params_types = [], []
        self.params_ids = params_ids
        self.params_types = params_types
        self.identifier = identifier
        self.expression = expression
        self.type = type

class AttributeNode(DeclarationNode):
    def __init__(self, identifier, expression, type=None):
        DeclarationNode.__init__(self)
        self.identifier = identifier
        self.expression = expression
        self.type = type

class ProtocolMethodSignatureNode(DeclarationNode):
    def __init__(self, identifier, params, type):
        DeclarationNode.__init__(self)
        if len(params) > 0:
            params_ids, params_types = [(param[0], param[1]) for param in params]
        else:
            params_ids, params_types = [], []
        self.identifier = identifier
        self.params_ids = params_ids
        self.params_types = params_types
        self.type = type

class VectorNode(ExpressionNode):
    def __init__(self, elements_type):
        DeclarationNode.__init__(self)
        self.elements_type = elements_type
        
class VariableDeclarationNode(DeclarationNode):
    def __init__(self, identifier, expression, type=None):
        DeclarationNode.__init__(self)
        self.identifier = identifier
        self.expression = expression
        self.type = type

class ExpressionBlockNode(ExpressionNode):
    def __init__(self, expressions):
        ExpressionNode.__init__(self)
        self.expressions = expressions

class LetInNode(ExpressionNode):
    def __init__(self, assignment_list, expression):
        ExpressionNode.__init__(self)
        self.assignment_list = assignment_list
        self.expression = expression

class IfElseNode(ExpressionNode):
    def __init__(self, condition_expressions: List[Tuple], else_expression):
        ExpressionNode.__init__(self)
        conditions, expressions = [(element[0], element[1]) for element in condition_expressions]
        self.conditions = conditions
        self.expressions = expressions
        self.else_expression = else_expression

class WhileNode(ExpressionNode):
    def __init__(self, condition, expression):
        ExpressionNode.__init__(self)
        self.condition = condition
        self.expression = expression

class ForNode(ExpressionNode):
    def __init__(self, iterator, iterable_expression, expression):
        ExpressionNode.__init__(self)
        self.iterator = iterator
        self.iterable_expression = iterable_expression
        self.expression = expression

class DestructiveOperationNode(ExpressionNode):
    def __init__(self, destiny, expression):
        ExpressionNode.__init__(self)
        self.destiny = destiny
        self.expression = expression

class NewTypeNode(ExpressionNode):
    def __init__(self, identifier, args):
        ExpressionNode.__init__(self)
        self.identifier = identifier
        self.args = args

class IsNode(ExpressionNode):
    def __init__(self, expression, type):
        ExpressionNode.__init__(self)
        self.expression = expression
        self.type = type

class AsNode(ExpressionNode):
    def __init__(self, expression, type):
        ExpressionNode.__init__(self)
        self.expression = expression
        self.type = type

class FunctionCallNode(ExpressionNode):
    def __init__(self, identifier, args):
        ExpressionNode.__init__(self)
        self.identifier = identifier
        self.args = args

class MethodCallNode(ExpressionNode):
    def __init__(self, object_identifier, method_identifier, args):
        ExpressionNode.__init__(self)
        self.object_identifier = object_identifier
        self.method_identifier = method_identifier
        self.args = args

class AttributeCallNode(ExpressionNode):
    def __init__(self, object_identifier, attribute_idetifier):
        ExpressionNode.__init__(self)
        self.object_identifier = object_identifier
        self.attribute_identifier = attribute_idetifier

class BaseCallNode(ExpressionNode):
    def __init__(self, args):
        ExpressionNode.__init__(self)
        self.args = args
        self.method_name = None
        self.parent_type = None

class IndexNode(ExpressionNode):
    def __init__(self, object, index):
        ExpressionNode.__init__(self)
        self.object = object
        self.index = index

class UnaryExpressionNode(ExpressionNode, ABC):
    def __init__(self, expression):
        ExpressionNode.__init__(self)
        self.expression = expression
        self.operator = None

class BinaryExpressionNode(ExpressionNode, ABC):
    def __init__(self, left_expression, right_expression):
        ExpressionNode.__init__(self)
        self.left_expression = left_expression
        self.right_expression = right_expression
        self.operator = None

class InitializeVectorNode(ExpressionNode):
    def __init__(self, elements):
        ExpressionNode.__init__(self)
        self.elements = elements

class InitializeVectorListComprehensionNode(ExpressionNode):
    def __init__(self, operation, variable_identifier, iterable_expression):
        ExpressionNode.__init__(self)
        self.operation = operation
        self.variable_identifier = variable_identifier
        self.iterable_expression = iterable_expression

class AtomNode(ExpressionNode, ABC):
    def __init__(self, lexeme):
        ExpressionNode.__init__(self)
        self.lexeme = lexeme


#-------------------------------------------------------Level3------------------------------------------------------------#


class NumNode(AtomNode):
    pass

class StringNode(AtomNode):
    pass

class BoolNode(AtomNode):
    pass

class IDNode(AtomNode):
    pass

class BoolBinaryOpNode(BinaryExpressionNode, ABC):
    pass

class EqualityBinaryOpNode(BinaryExpressionNode, ABC):
    pass

class InequalityBinaryOpNode(BinaryExpressionNode, ABC):
    pass

class StringBinaryOpNode(BinaryExpressionNode, ABC):
    pass

class ArithmeticBinaryOpNode(BinaryExpressionNode, ABC):
    pass

class SignUnaryOpNode(UnaryExpressionNode, ABC):
    pass

class NotUnaryOpNode(UnaryExpressionNode, ABC):
    pass


#-------------------------------------------------------Level4------------------------------------------------------------#

class OrNode(BoolBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '|'

class AndNode(BoolBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '&'

class EqualNode(EqualityBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '=='

class NonEqualNode(InequalityBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '!='

class LessThanNode(InequalityBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '<'

class LessEqualNode(InequalityBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '<='

class GreaterThanNode(InequalityBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '>'

class GreaterEqualNode(InequalityBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '>='

class ConcatNode(StringBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '@'

class SpacedConcatNode(StringBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '@@'

class PlusNode(ArithmeticBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '+'

class MinusNode(ArithmeticBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '-'

class StarNode(ArithmeticBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '*'

class DivNode(ArithmeticBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '/'

class ModNode(ArithmeticBinaryOpNode):
    def __init__(self, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = '%'

class PowNode(ArithmeticBinaryOpNode):
    def __init__(self, operator, left_expression, right_expression):
        BinaryExpressionNode.__init__(left_expression, right_expression)
        self.operator = operator

class MinusNode(SignUnaryOpNode):
    def __init__(self, expression):
        UnaryExpressionNode.__init__(expression)
        self.operator = '-'

class NotNode(NotUnaryOpNode):
    def __init__(self, expression):
        UnaryExpressionNode.__init__(expression)
        self.operator = '!'