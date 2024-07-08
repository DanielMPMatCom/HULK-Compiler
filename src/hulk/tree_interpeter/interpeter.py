from hulk.hulk_ast import *
from cmp.semantic import *
import cmp.visitor as visitor

import math
import random
import copy


def Print(x):
    print(x)
    return x


class RuntimeError(Exception):
    @property
    def text(self):
        message = ""
        for arg in self.args:
            message += str(arg) + " "
        return message

    def __str__(self) -> str:
        return self.text


def rangeWrapperInit(min, max):
    iterable = []
    for i in range(min, max):
        iterable.append(i)
    return iterable


# region Base
built_in_func = {
    "range": lambda x: rangeWrapperInit(int(x[0]), int(x[1])),
    "print": lambda x: Print(*x),
    "sqrt": lambda x: math.sqrt(*x),
    "sin": lambda x: math.sin(*x),
    "cos": lambda x: math.cos(*x),
    "exp": lambda x: math.exp(*x),
    "log": lambda x: math.log(*reversed(x)),
    "rand": lambda: random.random(),
    "parse": lambda x: float(*x),
}

binary_operators = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "%": lambda x, y: x % y,
    "@": lambda x, y: str(x) + str(y),
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
    "@@": lambda x, y: str(x) + " " + str(y),
}

unary_operators = {"!": lambda x: not x, "-": lambda x: -x}
# endRegion


class Interpreter:

    # region Visitor
    def __init__(self, context, errors=[]):
        self.context: Context = context
        self.errors: list = errors

    def binary_operation(self, node: BinaryExpressionNode):
        left_value = self.visit(node.left_expression)
        right_value = self.visit(node.right_expression)
        try:
            return binary_operators[node.operator](left_value, right_value)
        except Exception as e:
            print(
                "💥Runtime Error: "
                + str(RuntimeError(str(e) + " at", node.line, node.column))
            )
            exit(1)

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
        return self.visit(node.expression)

    # TypeDeclarationNode(DeclarationNode):
    @visitor.when(TypeDeclarationNode)
    def visit(self, node: TypeDeclarationNode):
        return node

    # FunctionDeclarationNode(DeclarationNode):
    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode):
        # function = node.scope.get_local_function_info(
        #     node.identifier, len(node.param_ids)
        # )
        function = self.context.get_function_by_name(node.identifier)
        function.body = node.expression
        return

    # ProtocolDeclarationNode(DeclarationNode):
    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node: ProtocolDeclarationNode):
        return

    # MethodNode(DeclarationNode):
    @visitor.when(MethodNode)
    def visit(self, node: MethodNode):
        return

    # AttributeNode(DeclarationNode):
    @visitor.when(AttributeNode)
    def visit(self, node: AttributeNode):
        node.scope.define_variable(f"self.{node.identifier}")
        value = self.visit(node.expression)
        var = node.scope.get_local_variable_info(f"self.{node.identifier}")
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
        variable = node.scope.get_global_variable_info(node.identifier)
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
        iterator: VariableInfo = node.expression.scope.get_global_variable_info(
            node.iterator
        )

        for variable in self.visit(node.iterable_expression):
            iterator.update(variable)
            evaluation = self.visit(node.expression)
        return evaluation

    # DestructiveOperationNode(ExpressionNode):
    @visitor.when(DestructiveOperationNode)
    def visit(self, node: DestructiveOperationNode):
        destiny: IDNode = (
            node.destiny
        )  # Revisar si esto es el identifier, asumimos que si
        variable = node.scope.get_global_variable_info(destiny.lexeme)
        value = self.visit(node.expression)
        variable.update(value)
        return value

    # NewTypeNode(ExpressionNode):
    @visitor.when(NewTypeNode)
    def visit(self, node: NewTypeNode):
        print(" * * * " * 10)
        type_node = self.context.get_type(node.identifier, len(node.args)).current_node
        type_node: TypeDeclarationNode = copy.deepcopy(type_node)

        args = node.args
        parent = type_node

        while parent:
            scope = parent.scope
            for i, vname in enumerate(parent.param_ids):
                scope.define_variable(vname=vname, vtype=None)
                value = self.visit(args[i])
                scope.get_local_variable_info(vname=vname).update(value)

            print("Variables")
            for var in scope.get_all_variables():
                print(var.name, " ", var.value)

            for attr in parent.attributes:
                print(attr, " ", attr.expression)
                scope.define_variable(f"self.{attr.identifier}", None)
                print('Last attr parent scope ', attr.scope.parent)
                attr.scope = parent.scope.create_child_scope()
                
                attr.expression.scope = attr.scope.create_child_scope()

                value = self.visit(attr.expression)
                print(value)
                scope.get_local_variable_info(f"self.{attr.identifier}").update(value)

            print("Variables and attributes")
            for var in scope.get_all_variables():
                print(var.name, " ", var.value)

            for method in parent.methods:
                method: MethodNode
                scope.define_function(
                    method.identifier,
                    method.param_ids,
                    method.param_types,
                    method.type,
                    body=method.expression,
                )

            if len(parent.type_parent_args) > 0:
                args = [self.visit(arg) for arg in parent.type_parent_args]

            if parent.parent:
                oldChild = parent
                parent: TypeDeclarationNode = self.context.get_type(
                    parent.parent, len(parent.type_parent_args)
                ).current_node
                parent = copy.deepcopy(parent)
                scope.parent = parent.scope  # 100% real, simetrico y no fake

                for p_method in parent.methods:
                    for c_method in oldChild.methods:
                        if p_method.identifier == c_method.identifier:
                            c_method.scope.define_function(
                                "base",
                                p_method.param_ids,
                                None,
                                body=p_method.expression,
                            )
            else:
                break
        return type_node

    # IsNode(ExpressionNode):
    @visitor.when(IsNode)
    def visit(self, node: IsNode):
        value = self.visit(node.expression)
        type = self.context.get_type(node.type)
        if isinstance(value, float):
            return type == "Number"
        elif isinstance(value, str):
            return type == "String"
        elif isinstance(value, bool):
            return type == "Bool"
        elif isinstance(value, list):
            return type == "Vector"
        else:
            try:
                value: TypeDeclarationNode
                while value:
                    if value.identifier == node.type:
                        return True
                    if value.parent:
                        value = value.parent
                        value = Context.get_type(
                            value.identifier, len(value.type_parent_args)
                        ).current_node
                    else:
                        value = None
            except:
                return False

        return False

    # AsNode(ExpressionNode):
    @visitor.when(AsNode)
    def visit(self, node: AsNode):
        value = self.visit(node.expression)
        value: TypeDeclarationNode
        tmp = value
        while tmp.identifier != node.type:
            if tmp.parent:
                tmp = self.context.get_type(
                    tmp.parent, len(tmp.type_parent_args)
                ).current_node
            else:
                break
        node.scope = tmp.scope
        return node

    # FunctionCallNode(ExpressionNode):
    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode):

        params = [self.visit(param) for param in node.args]

        if node.identifier in built_in_func:
            return built_in_func[node.identifier](tuple(params))

        function: Function = self.context.get_function_by_name(node.identifier)
        scope: Scope = function.body.scope

        for i, name in enumerate(function.param_names):
            variable = scope.get_global_variable_info(name)
            variable.update(params[i])

        return self.visit(function.body)

    # MethodCallNode(ExpressionNode):
    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode):
        variable_name = node.object_identifier.lexeme
        object_instance: TypeDeclarationNode = node.scope.get_global_variable_info(
            variable_name
        ).value

        if isinstance(object_instance, list):
            if node.method_identifier == "next":
                if len(object_instance) == 0:
                    return False
                return True
            if node.method_identifier == "current":
                return object_instance.pop(0)

        method: Function = object_instance.scope.get_global_function_info(
            node.method_identifier, len(node.args)
        )

        for i, vname in enumerate(method.param_names):
            method.body.scope.define_variable(vname, None)  # no hagas eso
            value = self.visit(node.args[i])
            method.body.scope.get_local_variable_info(vname).update(value)

        return self.visit(method.body)

    # AttributeCallNode(ExpressionNode):
    @visitor.when(AttributeCallNode)
    def visit(self, node: AttributeCallNode):
        object_instance: TypeDeclarationNode = node.scope.get_global_variable_info(
            f"self.{node.attribute_identifier}"
        )

        return object_instance.value

    # BaseCallNode(ExpressionNode):
    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode):
        function: Function = node.scope.get_global_function_info("base").value
        for i, vname in enumerate(function.param_names):
            function.body.scope.define_variable(vname, None)
            value = self.visit(node.args[i])
            function.body.scope.get_local_variable_info(vname).update(value)

        return self.visit(function.body)

    # IndexNode(ExpressionNode):
    @visitor.when(IndexNode)
    def visit(self, node: IndexNode):
        vector = node.scope.get_global_variable_info(node.object).value
        index = self.visit(node.index)
        return vector[index]

    # InitializeVectorNode(ExpressionNode):
    @visitor.when(InitializeVectorNode)
    def visit(self, node: InitializeVectorNode):
        return [self.visit(element) for element in node.elements]

    # InitializeVectorListComprehensionNode(ExpressionNode):
    @visitor.when(InitializeVectorListComprehensionNode)
    def visit(self, node: InitializeVectorListComprehensionNode):
        vector = self.visit(node.iterable_expression)
        evaluation = []
        for i in vector:
            node.operation.scope.define_variable(node.identifier, None)
            node.operation.scope.get_local_variable_info(node.identifier).update(i)
            evaluation.append(self.visit(node.operation))
        return evaluation

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
        return node.lexeme == "true"

    # IDNode(AtomNode):
    @visitor.when(IDNode)
    def visit(self, node: IDNode):
        return node.scope.get_global_variable_info(node.lexeme).value

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

    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode):
        return node.value
