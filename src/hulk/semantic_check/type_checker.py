import cmp.visitor as visitor
from hulk.hulk_ast import*
from cmp.semantic import*

class TypeChecker():
    def __init__(self, context, errors=None):
        self.context : Context = context
        self.errors: list[SemanticError] = [] if errors is None else errors
        self.current_type : Type = None
        self.current_method : Method = None

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.expression)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node : TypeDeclarationNode):
        self.current_type : Type = self.context.get_type(node.identifier)
        if isinstance(self.current_type, ErrorType):
            return
        for attr in node.attributes:
            self.visit(attr)
        for method in node.methods:
            self.visit(method)
        if isinstance(node.parent, ErrorType):
            return
        parent_params = self.current_type.parent.param_types
        parent_args = [self.visit(arg) for arg in node.type_parent_args]
        if len(parent_params) != len(parent_args):
            self.errors.append(SemanticError(f'{self.current_type.parent.name} expects {len(parent_params)} arguments but {len(parent_args)} were given', node.line, node.column))
            return ErrorType()
        for i in range(len(parent_params)):
            if not parent_args[i].conforms_to(parent_params[i]):
                self.errors.append(SemanticError(f'{parent_args[i].name} does not conform to {parent_params[i].name}', node.line, node.column))
        self.current_type = None

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node : FunctionDeclarationNode):
        func : Function = self.context.get_function_by_name(node.identifier)
        inferred_return_type : Type = self.visit(node.expression)
        if not inferred_return_type.conforms_to(func.return_type):
            self.errors.append(SemanticError(f'{inferred_return_type.name} does not conform to {func.return_type}', node.line, node.column))
            return ErrorType()
        return func.return_type
    
    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node : ProtocolDeclarationNode):
        self.current_type = self.context.get_protocol(node.identifier)
        for method in node.signatures:
            self.visit(method)
        self.current_type = None

    @visitor.when(MethodNode)
    def visit(self, node : MethodNode):
        self.current_method = self.current_type.get_method(node.identifier)
        inferred_return_type : Type = self.visit(node.expression)
        if not inferred_return_type.conforms_to(self.current_method.return_type):
            self.errors.append(SemanticError(f'{inferred_return_type.name} does not conform to {self.current_method.return_type}', node.line, node.column))
        return_type = self.current_method.return_type
        if self.current_type.parent is None or isinstance(self.current_type.parent, ErrorType):
            return return_type
        try:
            ancestor_method : Method = self.current_type.parent.get_method(node.identifier)
        except SemanticError:
            return return_type
        if ancestor_method.return_type != return_type:
            self.errors.append(SemanticError(f'Method {self.current_method.name} already defined in ancestor with different signature (return type)', node.line, node.column))
        elif len(ancestor_method.param_types) != len(self.current_method.param_types):
            self.errors.append(SemanticError(f'Method {self.current_method.name} already defined in ancestor with different signature (number of arguments)', node.line, node.column))
        else:
            for ancestor_param_type in ancestor_method.param_types:
                param_type = self.current_method.param_types[ancestor_method.param_types.index(param_type)]
                if ancestor_param_type != param_type:
                    self.errors.append(SemanticError(f'Method {self.current_method.name} already defined in ancestor with different signature (argument type)', node.line, node.column))
        self.current_method = None
        return return_type
    
    @visitor.when(AttributeNode)
    def visit(self, node : AttributeNode):
        inferred_type : Type = self.visit(node.expression)
        attr_type = self.current_type.get_attribute(node.identifier).type
        if not inferred_type.conforms_to(attr_type):
            self.errors.append(SemanticError(f'{inferred_type.name} does not conform to {attr_type}', node.line, node.column))
        return attr_type
    
    @visitor.when(ProtocolMethodSignatureNode)
    def visit(self, node : ProtocolMethodSignatureNode):
        if isinstance(self.current_type, ErrorType):
            return ErrorType()
        self.current_method = self.current_type.get_method(node.identifier)
        return_type = self.current_method.return_type
        if self.current_type.parent is None or isinstance(self.current_type.parent, ErrorType):
            return return_type
        try:
            ancestor_method : Method = self.current_type.parent.get_method(node.identifier)
        except SemanticError:
            return return_type
        if ((ancestor_method.name != self.current_method.name) or\
        (not ancestor_method.return_type.conforms_to(self.current_method.return_type)) or\
        (len(ancestor_method.param_types) != len(self.current_method.param_types)) or\
        (not method_type.conforms_to(implicit_type) for method_type, implicit_type in zip(ancestor_method.param_types, self.current_method.param_types))):
            self.errors.append(SemanticError(f'Method {self.current_method.name} already defined in ancestor with different signature', node.line, node.column))
        self.current_method = None
        return return_type
    
    @visitor.when(VectorNode)
    def visit(self, node : VectorNode):
        try:
            elements_type = self.context.get_type(node.elements_type)
        except SemanticError:
            self.errors.append(SemanticError(f'{node.elements_type} is not a valid type', node.line, node.column))
            elements_type = ErrorType()
        return elements_type

    @visitor.when(VariableDeclarationNode)
    def visit(self, node : VariableDeclarationNode):
        scope = node.scope
        inferred_type : Type = self.visit(node.expression)
        variable_info = scope.get_global_variable_info(node.identifier)
        variable_type = variable_info.type
        if variable_type.name == "<undefined>":
            variable_info.type = inferred_type
        if not inferred_type.conforms_to(variable_type):
            self.errors.append(SemanticError(f'{inferred_type.name} does not conform to {variable_type.name}', node.line, node.column))
            variable_type = ErrorType()
        return variable_type
    
    @visitor.when(ExpressionBlockNode)
    def visit(self, node : ExpressionBlockNode):
        expression_type = ErrorType()
        for expr in node.expressions:
            expression_type = self.visit(expr)
        return expression_type
    
    @visitor.when(LetInNode)
    def visit(self, node : LetInNode):
        for assignment in node.assignment_list:
            self.visit(assignment)
        return self.visit(node.expression)

    @visitor.when(IfElseNode)
    def visit(self, node : IfElseNode):
        condition_types = [self.visit(condition) for condition in node.conditions]
        for condition_type in condition_types:
            if condition_type != BoolType():
                self.errors.append(SemanticError(f'{condition_type.name} does not conform to Boolean', node.line, node.column))
        expression_types = [self.visit(expression) for expression in node.expressions]
        else_type = self.visit(node.else_expression)
        return lowest_common_ancestor(expression_types + [else_type])

    @visitor.when(WhileNode)
    def visit(self, node : WhileNode):
        condition_type = self.visit(node.condition)
        if condition_type != BoolType():
            self.errors.append(SemanticError(f'{condition_type.name} does not conform to Boolean', node.line, node.column))
        return self.visit(node.expression)
    
    @visitor.when(ForNode)
    def visit(self, node : ForNode):
        iterable_type : Type = self.visit(node.iterable_expression)
        protocol_iterable = self.context.get_protocol('Iterable')
        if not iterable_type.conforms_to(protocol_iterable):
            self.errors.append(SemanticError(f'{iterable_type.name} does not conform to {protocol_iterable.name}', node.line, node.column))
        return self.visit(node.expression)
    
    @visitor.when(DestructiveOperationNode)
    def visit(self, node : DestructiveOperationNode):
        current_type : Type = self.visit(node.destiny)
        new_type = self.visit(node.expression)
        if current_type.name == 'Self':
            self.errors.append(SemanticError(f'You cannot reassign a Self variable', node.line, node.column))
            return ErrorType()
        if not new_type.conforms_to(current_type):
            self.errors.append(SemanticError(f'{new_type.name} does not conform to {current_type.name}', node.line, node.column))
            return ErrorType()
        return current_type
        
    @visitor.when(NewTypeNode)
    def visit(self, node : NewTypeNode):
        try:
            new_type = self.context.get_type(node.identifier, len(node.args))
        except SemanticError as error:
            self.errors.append(SemanticError(error, node.line, node.column))
            return ErrorType()
        argument_types = [self.visit(argument) for argument in node.args]
        if len(argument_types) != len(new_type.param_types):
            self.errors.append(SemanticError(f'{new_type.name} expects {len(new_type.param_types)} arguments but {len(argument_types)} were given', node.line, node.column))
            return ErrorType()
        for argument_type, param_type in zip(argument_types, new_type.param_types):
            if not argument_type.conforms_to(param_type):
                self.errors.append(SemanticError(f'{argument_type.name} does not conform to {param_type.name}', node.line, node.column))
                return ErrorType()
        return new_type
    
    @visitor.when(IsNode)
    def visit(self, node : IsNode):
        self.visit(node.expression)
        boolean_type = self.context.get_type('Boolean')
        try:
            self.context.type_protocol_or_vector(node.type.lexeme)
        except SemanticError:
            self.errors.append(SemanticError(f"{node.type.lexeme} is not defined", node.line, node.column))
        return boolean_type
    
    @visitor.when(AsNode)
    def visit(self, node : AsNode):
        expr_type : Type = self.visit(node.expression)
        try:
            as_type = self.context.type_protocol_or_vector(node.type.lexeme)
        except SemanticError:
            self.errors.append(SemanticError(f"{node.type.lexeme} is not defined", node.line, node.column))
            return ErrorType()
        if not expr_type.conforms_to(as_type) and not as_type.conforms_to(expr_type):
            self.errors.append(SemanticError(f'{expr_type.name} does not conform to {as_type.name}', node.line, node.column))
            return ErrorType()
        return as_type
    
    @visitor.when(FunctionCallNode)
    def visit(self, node : FunctionCallNode):
        argument_types = [self.visit(argument) for argument in node.args]
        try:
            function : Function = self.context.get_function_by_name(node.identifier)
        except SemanticError as error:
            self.errors.append(SemanticError(error, node.line, node.column))
            for arg in node.args:
                self.visit(arg)
            return ErrorType()
        if len(argument_types) != len(function.param_types):
            self.errors.append(SemanticError(f'{function.name} expects {len(function.param_types)} arguments but {len(argument_types)} were given', node.line, node.column))
            return ErrorType()
        for argument_type, param_type in zip(argument_types, function.param_types):
            if not argument_type.conforms_to(param_type):
                self.errors.append(SemanticError(f'{argument_type.name} does not conform to {param_type.name}', node.line, node.column))
                return ErrorType()
        return function.return_type
    
    @visitor.when(MethodCallNode)
    def visit(self, node : MethodCallNode):
        argument_types = [self.visit(argument) for argument in node.args]
        object_type : Type = self.visit(node.object_identifier)
        if isinstance(object_type, ErrorType):
            return ErrorType()
        try:
            if object_type == AutoReferenceType():
                method = self.current_type.get_method(node.method_identifier)
            else:
                method = object_type.get_method(node.method_identifier)
        except SemanticError as error:
            self.errors.append(SemanticError(error, node.line, node.column))
            for arg in node.args:
                self.visit(arg)
            return ErrorType()
        if len(argument_types) != len(method.param_types):
            self.errors.append(SemanticError(f'{method.name} expects {len(method.param_types)} arguments but {len(argument_types)} were given', node.line, node.column))
            return ErrorType()
        for argument_type, param_type in zip(argument_types, method.param_types):
            if not argument_type.conforms_to(param_type):
                self.errors.append(SemanticError(f'{argument_type.name} does not conform to {param_type.name}', node.line, node.column))
                return ErrorType()
        return method.return_type
    
    @visitor.when(AttributeCallNode)
    def visit(self, node : AttributeCallNode):
        object_type : Type = self.visit(node.object_identifier)
        if isinstance(object_type, ErrorType):
            return ErrorType()
        if object_type == AutoReferenceType():
            try:
                attribute = self.current_type.get_attribute(node.attribute_identifier)
                return attribute.type
            except SemanticError as error:
                self.errors.append(SemanticError(error, node.line, node.column))
                return ErrorType()
        else:
            self.errors.append(SemanticError('You cannot access an attribute from a non-self object', node.line, node.column))
            return ErrorType()
        
    @visitor.when(BaseCallNode)
    def visit(self, node : BaseCallNode):
        if self.current_method is None:
            self.errors.append(SemanticError('You cannot use base outside a method', node.line, node.column))
            for argument in node.args:
                self.visit(argument)
            return ErrorType()
        try:
            method : Method = self.current_type.parent.get_method(self.current_method.name)
            node.method_name = self.current_method.name
            node.parent_type = self.current_type.parent
        except SemanticError:
            self.errors.append(SemanticError('You cannot use base in a method that is not overriding', node.line, node.column))
            for argument in node.args:
                self.visit(argument)
            return ErrorType()
        argument_types = [self.visit(argument) for argument in node.args]
        if len(argument_types) != len(method.param_types):
            self.errors.append(SemanticError(f'{method.name} expects {len(method.param_types)} arguments but {len(argument_types)} were given', node.line, node.column))
            return ErrorType()
        for argument_type, param_type in zip(argument_types, method.param_types):
            if not argument_type.conforms_to(param_type):
                self.errors.append(SemanticError(f'{argument_type.name} does not conform to {param_type.name}', node.line, node.column))
                return ErrorType()
        return method.return_type
    
    @visitor.when(IndexNode)
    def visit(self, node : IndexNode):
        num_type = self.context.get_type('Number')
        index_type : Type = self.visit(node.index)
        if not index_type.conforms_to(num_type):
            self.errors.append(SemanticError(f'{index_type.name} does not conform to {num_type.name}', node.line, node.column))
            return ErrorType()
        object_type : Type = self.visit(node.object)
        if isinstance(object_type, ErrorType):
            return ErrorType()
        if not isinstance(object_type, VectorType):
            self.errors.append(SemanticError(f'Invalid operation []. {object_type.name} is not a Vector', node.line, node.column))
            return ErrorType()
        return object_type.element_types()
    
    @visitor.when(InitializeVectorNode)
    def visit(self, node : InitializeVectorNode):
        elements_types = [self.visit(element) for element in node.elements]
        low_com_anc = lowest_common_ancestor(elements_types)
        if isinstance(low_com_anc, ErrorType):
            return ErrorType()
        return VectorType(low_com_anc)
    
    @visitor.when(InitializeVectorListComprehensionNode)
    def visit(self, node : InitializeVectorListComprehensionNode):
        
        vector_iterable_type : Type = self.visit(node.iterable_expression)
        protocol_iterable = self.context.get_protocol('Iterable')
        return_type = self.visit(node.operation)
        # if node.variable_identifier:
        #     node.scope.define_variable(node.variable_identifier, UndefinedType())
        if not vector_iterable_type.conforms_to(protocol_iterable):
            self.errors.append(SemanticError(f'{vector_iterable_type.name} does not conform to {protocol_iterable.name}', node.line, node.column))
            return ErrorType()
        if isinstance(return_type, ErrorType):
            return ErrorType()
        return VectorType(return_type)
        
    @visitor.when(NumNode)
    def visit(self, node : NumNode):
        return self.context.get_type('Number')
    
    @visitor.when(StringNode)
    def visit(self, node : StringNode):
        return self.context.get_type('String')
    
    @visitor.when(BoolNode)
    def visit(self, node : BoolNode):
        return self.context.get_type('Boolean')
    
    @visitor.when(IDNode)
    def visit(self, node : IDNode):
        scope = node.scope
        if not scope.is_var_globally_defined(node.lexeme):
            self.errors.append(SemanticError(f'Variable {node.lexeme} is not defined', node.line, node.column))
            return ErrorType()
        variable = scope.get_global_variable_info(node.lexeme)
        return variable.type

    @visitor.when(BoolBinaryOpNode)
    def visit(self, node : BoolBinaryOpNode):
        boolean_type = self.context.get_type('Boolean')
        left_type : Type = self.visit(node.left_expression)
        right_type : Type = self.visit(node.right_expression)
        if not left_type.conforms_to(boolean_type) or not right_type.conforms_to(boolean_type):
            self.errors.append(SemanticError(f'Cannot perform boolean operation with {left_type.name} and {right_type.name}', node.line, node.column))
            return ErrorType()
        return boolean_type
    
    @visitor.when(EqualityBinaryOpNode)
    def visit(self, node : ArithmeticBinaryOpNode):
        left_type : Type = self.visit(node.left_expression)
        right_type : Type = self.visit(node.right_expression)
        if not left_type.conforms_to(right_type) and not right_type.conforms_to(left_type):
            self.errors.append(SemanticError(f'Invalid operation {node.operator} between {left_type.name} and {right_type.name}', node.line, node.column))
            return ErrorType()
        return self.context.get_type('Boolean')
    
    @visitor.when(InequalityBinaryOpNode)
    def visit(self, node : ArithmeticBinaryOpNode):
        left_type : Type = self.visit(node.left_expression)
        right_type : Type = self.visit(node.right_expression)
        if left_type.name == "<undefined>": 
            left_type = NumberType()
        if right_type.name == "<undefined>":
            right_type = NumberType()
        if left_type != NumberType() or right_type != NumberType():
            self.errors.append(SemanticError(f'Invalid operation {node.operator} between {left_type.name} and {right_type.name}', node.line, node.column))
            return ErrorType()
        return self.context.get_type('Boolean')

    @visitor.when(StringBinaryOpNode)
    def visit(self, node : StringBinaryOpNode):
        string_type = self.context.get_type('String')
        object_type = self.context.get_type('Object')
        left_type : Type = self.visit(node.left_expression)
        right_type : Type = self.visit(node.right_expression)
        if not left_type.conforms_to(object_type) or not right_type.conforms_to(object_type):
            self.errors.append(SemanticError(f'Invalid operation {node.operator} between {left_type.name} and {right_type.name}', node.line, node.column))
            return ErrorType()
        return string_type
    
    @visitor.when(ArithmeticBinaryOpNode)
    def visit(self, node : ArithmeticBinaryOpNode):
        num_type = self.context.get_type('Number')
        left_type : Type = self.visit(node.left_expression)
        right_type : Type = self.visit(node.right_expression)
        if left_type.name == "<undefined>": 
            left_type = NumberType()
        if right_type.name == "<undefined>":
            right_type = NumberType()
        if left_type != num_type or right_type != num_type:
            self.errors.append(SemanticError(f'Invalid operation {node.operator} between {left_type.name} and {right_type.name}', node.line, node.column))
            return ErrorType()
        return num_type
    
    @visitor.when(SignUnaryOpNode)
    def visit(self, node : SignUnaryOpNode):
        expression_type : Type = self.visit(node.expression)
        if expression_type.name == "<undefined>":
            expression_type = NumberType()
        if expression_type != NumberType():
            self.errors.append(SemanticError(f'Invalid operation {node.operator} with {expression_type.name}', node.line, node.column))
            return ErrorType()
        return self.context.get_type('Number')
    
    @visitor.when(NotUnaryOpNode)
    def visit(self, node : NotUnaryOpNode):
        boolean_type = self.context.get_type('Boolean')
        expression_type : Type = self.visit(node.expression)
        if expression_type.name == "<undefined>":
            expression_type = BoolType()
        if expression_type != boolean_type:
            self.errors.append(SemanticError(f'Invalid operation {node.operator} with {expression_type.name}', node.line, node.column))
            return ErrorType()
        return boolean_type