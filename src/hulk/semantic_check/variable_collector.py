import cmp.visitor as visitor
from hulk_ast import*
from cmp.semantic import*

class VariableCollector:
    def __init__(self, context, errors=None):
        self.context: Context = context
        self.errors: list[SemanticError] = [] if errors is None else errors
        self.current_type : Type = None

    @visitor.on('node')
    def visit(self, node, scope : Scope = None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode, scope : Scope = None):
        scope = Scope()
        node.scope = scope
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child_scope())
        self.visit(node.expression, scope.create_child_scope())
        return scope
    
    @visitor.when(TypeDeclarationNode)
    def visit(self, node : TypeDeclarationNode, scope : Scope = None):
        node.scope = scope
        self.current_type = self.context.get_type(node.identifier)
        if isinstance(self.current_type, ErrorType):
            return
        if node.type_parent_args is None and node.params_ids is not None:
            node.type_parent_args = []
        if node.type_parent_args is None and node.params_ids is None:
            self.current_type.set_parameters()
            node.params_ids = self.current_type.param_names
            node.params_types = self.current_type.param_types
            for param_name in self.current_type.param_names:
                node.type_parent_args.append(IDNode(param_name))
        params_scope = scope.create_child_scope()
        for param_name in self.current_type.param_names:
            params_scope.define_variable(param_name, self.current_type.param_types[self.current_type.param_names.index(param_name)])
        for arg in node.type_parent_args:
            self.visit(arg, params_scope.create_child_scope())
        for attr in node.attributes:
            self.visit(attr, params_scope.create_child_scope())
        methods_scope = scope.create_child_scope()
        methods_scope.define_variable("self", AutoReferenceType(self.current_type))
        for method in node.methods:
            self.visit(method, methods_scope.create_child_scope())

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node : FunctionDeclarationNode, scope : Scope = None):
        node.scope = scope
        function : Function = self.context.get_function_by_name(node.identifier)
        function_scope = scope.create_child_scope()
        for param_name in function.param_names:
            function_scope.define_variable(param_name, function.param_types[function.param_names.index(param_name)])
        self.visit(node.expression, function_scope)

    @visitor.when(MethodNode)
    def visit(self, node : MethodNode, scope : Scope = None):
        node.scope = scope
        method : Method = self.current_type.get_method(node.identifier)
        method_scope = scope.create_child_scope()
        for param_name in method.param_names:
            method_scope.define_variable(param_name, method.param_types[method.param_names.index(param_name)])
        self.visit(node.expression, method_scope)

    @visitor.when(AttributeNode)
    def visit(self, node : AttributeNode, scope : Scope = None):
        node.scope = scope
        self.visit(node.expression, scope.create_child_scope())

    @visitor.when(VariableDeclarationNode)
    def visit(self, node : VariableDeclarationNode, scope : Scope = None):
        self.visit(node.expression, scope.create_child_scope())
        node.scope = scope.create_child_scope()
        if node.type is not None:
            try:
                variable_type = self.context.type_protocol_or_vector(node.type)
            except SemanticError as error:
                self.errors.append(error)
                variable_type = ErrorType()
        else:
            variable_type = UndefinedType()
        node.scope.define_variable(node.identifier, variable_type)

    @visitor.when(ExpressionBlockNode)
    def visit(self, node : ExpressionBlockNode, scope : Scope = None):
        expr_block_scope = scope.create_child_scope()
        node.scope = expr_block_scope
        for expression in node.expressions:
            self.visit(expression, expr_block_scope.create_child_scope())

    @visitor.when(LetInNode)
    def visit(self, node : LetInNode, scope : Scope = None):
        node.scope = scope
        previous_scope = scope
        for declaration in node.assignment_list:
            self.visit(declaration, previous_scope)
            previous_scope = declaration.scope
        self.visit(node.expression, previous_scope.create_child_scope())

    @visitor.when(IfElseNode)
    def visit(self, node : IfElseNode, scope : Scope = None):
        node.scope = scope
        for condition in node.conditions:
            self.visit(condition, scope.create_child_scope())
        for expression in node.expressions:
            self.visit(expression, scope.create_child_scope())
        self.visit(node.else_expression, scope.create_child_scope())

    @visitor.when(WhileNode)
    def visit(self, node : WhileNode, scope : Scope = None):
        node.scope = scope
        self.visit(node.condition, scope.create_child_scope())
        self.visit(node.expression, scope.create_child_scope())

    @visitor.when(ForNode)
    def visit(self, node : ForNode, scope : Scope = None):
        node.scope = scope
        expression_scope = scope.create_child_scope()
        expression_scope.define_variable(node.iterator, UndefinedType())
        self.visit(node.iterable_expression, scope.create_child_scope())
        self.visit(node.expression, expression_scope)

    @visitor.when(DestructiveOperationNode)
    def visit(self, node : DestructiveOperationNode, scope : Scope = None):
        node.scope = scope
        self.visit(node.destiny, scope.create_child_scope())
        self.visit(node.expression, scope.create_child_scope())

    @visitor.when(NewTypeNode)
    def visit(self, node : NewTypeNode, scope : Scope = None):
        node.scope = scope
        for arg in node.args:
            self.visit(arg, scope.create_child_scope())

    @visitor.when(IsNode)
    def visit(self, node : IsNode, scope : Scope = None):
        node.scope = scope
        self.visit(node.expression, scope.create_child_scope())

    @visitor.when(AsNode)
    def visit(self, node : AsNode, scope : Scope = None):
        node.scope = scope
        self.visit(node.expression, scope.create_child_scope())

    @visitor.when(FunctionCallNode)
    def visit(self, node : FunctionCallNode, scope : Scope = None):
        node.scope = scope
        for arg in node.args:
            self.visit(arg, scope.create_child_scope())

    @visitor.when(MethodCallNode)
    def visit(self, node : MethodCallNode, scope : Scope = None):
        node.scope = scope
        self.visit(node.object_identifier, scope.create_child_scope())
        for arg in node.args:
            self.visit(arg, scope.create_child_scope())

    @visitor.when(AttributeCallNode)
    def visit(self, node : AttributeCallNode, scope : Scope = None):
        node.scope = scope
        self.visit(node.object_identifier, scope.create_child_scope())

    @visitor.when(BaseCallNode)
    def visit(self, node : BaseCallNode, scope : Scope = None):
        node.scope = scope
        for arg in node.args:
            self.visit(arg, scope.create_child_scope())

    @visitor.when(IndexNode)
    def visit(self, node : IndexNode, scope : Scope = None):
        node.scope = scope
        self.visit(node.object, scope.create_child_scope())
        self.visit(node.index, scope.create_child_scope())

    @visitor.when(UnaryExpressionNode)
    def visit(self, node : UnaryExpressionNode, scope : Scope = None):
        node.scope = scope
        self.visit(node.expression, scope.create_child_scope())

    @visitor.when(BinaryExpressionNode)
    def visit(self, node : BinaryExpressionNode, scope : Scope = None):
        node.scope = scope
        self.visit(node.left_expression, scope.create_child_scope())
        self.visit(node.right_expression, scope.create_child_scope())

    @visitor.when(InitializeVectorNode)
    def visit(self, node : InitializeVectorNode, scope : Scope = None):
        node.scope = scope
        for element in node.elements:
            self.visit(element, scope.create_child_scope())

    @visitor.when(InitializeVectorListComprehensionNode)
    def visit(self, node : InitializeVectorListComprehensionNode, scope : Scope = None):
        node.scope = scope
        operation_scope = scope.create_child_scope()
        operation_scope.define_variable(node.variable_identifier, UndefinedType())
        self.visit(node.operation, operation_scope)
        self.visitn(node.iterable_expression, scope.create_child_scope())

    @visitor.when(NumNode)
    def visit(self, node : NumNode, scope : Scope = None):
        node.scope = scope

    @visitor.when(StringNode)
    def visit(self, node : StringNode, scope : Scope = None):
        node.scope = scope

    @visitor.when(BoolNode)
    def visit(self, node : BoolNode, scope : Scope = None):
        node.scope = scope

    @visitor.when(IDNode)
    def visit(self, node : IDNode, scope : Scope = None):
        node.scope = scope