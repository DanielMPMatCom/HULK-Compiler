import cmp.visitor as visitor
from hulk_ast import*
from cmp.semantic import*


class TypeBuilder():
    def __init__(self, context, errors=None):
        self.context : Context = context
        self.errors: list = [] if errors is None else errors
        self.current_type = None

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for declaration in node.declarations:
            self.visit(declaration)

    @visitor.when(TypeDeclarationNode)
    def visit(self, node: TypeDeclarationNode):
        try:
            self.current_type = self.context.get_type(node.identifier)
        except SemanticError as error:
            self.errors.append(str(error))
            self.current_type = ErrorType()

        self.current_type.param_names, self.current_type.param_types = self.param_names_and_types(node)
        
        if node.parent in ['Number', 'String', 'Bool']:
            self.errors.append(SemanticError(f'Type {node.identifier} is inheriting from forbidden type {node.parent}.', node.line, node.column))
        elif node.parent is not None:
            try:
                parent : Type = self.context.get_type(node.parent)
                current = parent
                while current is not None:
                    if current.name == self.current_type.name:
                        self.errors.append(SemanticError(f'Circular dependency inheritance {self.current_type.name} : {node.parent} : ... : {current.name}.', node.line, node.column))
                        parent = ErrorType()
                        break
                    current = current.parent
            except SemanticError as error:
                self.errors.append(str(error))
                parent = ErrorType()
            try:
                self.current_type.set_parent(parent)
            except SemanticError as error:
                self.errors.append(str(error))
        else:
            obj_type = self.context.get_type('Object')
            self.current_type.set_parent(obj_type)

        for attr in node.attributes:
            self.visit(attr)
        for method in node.methods:
            self.visit(method)

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode):
        self.param_names, self.param_types = self.param_names_and_types(node)

        if node.return_type is None:
            return_type = UndefinedType()
        else:
            try:
                return_type = self.context.type_protocol_or_vector(node.type)
            except SemanticError as error:
                self.errors.append(str(error))
                return_type = ErrorType()

        try:
            self.context.create_function(node.identifier, self.param_names, self.param_types, return_type)
        except SemanticError as error:
            self.errors.append(str(error))

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node: ProtocolDeclarationNode):
        try:
            self.current_type = self.context.get_protocol(node.identifier)
        except:
            return
        
        if node.parent is not None:
            try:
                parent : Type = self.context.get_protocol(node.parent)
                current = parent
                while current is not None:
                    if current.name == self.current_type.name:
                        self.errors.append(SemanticError(f'Circular dependency inheritance {self.current_type.name} : {node.parent} : ... : {current.name}.', node.line, node.column))
                        parent = ErrorType()
                        break
                    current = current.parent
            except SemanticError as error:
                self.errors.append(str(error))
                parent = ErrorType()
            try:
                self.current_type.set_parent(parent)
            except SemanticError as error:
                self.errors.append(str(error))

        for method in node.signatures:
            self.visit(method)
                
    @visitor.when(MethodNode)
    def visit(self, node: MethodNode):
        param_names, param_types = self.param_names_and_types(node)

        if node.type is None:
            return_type = UndefinedType()
        else:
            try:
                return_type = self.context.type_protocol_or_vector(node.type)
            except SemanticError as error:
                self.errors.append(str(error))
                return_type = ErrorType()
        try:
            self.current_type.define_method(node.identifier, param_names, param_types, return_type)
        except SemanticError as error:
            self.errors.append(str(error))

    @visitor.when(AttributeNode)
    def visit(self, node: AttributeNode):
        if node.type is None:
            attr_type = UndefinedType()
        else:
            try:
                attr_type = self.context.type_protocol_or_vector(node.type)
            except SemanticError as error:
                self.errors.append(str(error))
                attr_type = ErrorType()
        try:
            self.current_type.define_attribute(node.identifier, attr_type)
        except SemanticError as error:
            self.errors.append(str(error))

    @visitor.when(ProtocolMethodSignatureNode)
    def visit(self, node : ProtocolMethodSignatureNode):
        param_names, param_types = self.param_names_and_types(node)
        try:
            return_type = self.context.type_protocol_or_vector(node.type)
        except SemanticError as error:
            self.errors.append(str(error))
            return_type = ErrorType()
        try:
            self.current_type.define_method(node.identifier, param_names, param_types, return_type)
        except SemanticError as error:
            self.errors.append(str(error))



    def param_names_and_types(self, node):
        if node.param_ids is None or node.param_types is None:
            return None, None

        names = []
        types = []
        for param_name in node.param_ids:
            param_type = node.param_types[node.param_types.index(param_name)]
            if param_name in names:
                self.errors.append(SemanticError(f'Parameter {param_name} already declared.', node.line, node.column))
                types[names.index(param_name)] = ErrorType()
            else:
                if param_type is None:
                    param_type = UndefinedType()
                else: 
                    try:
                        param_type = self.context.type_protocol_or_vector(param_type)
                    except SemanticError as error:
                        self.errors.append(str(error))
                        param_type = ErrorType()
                names.append(param_name)
                types.append(self.context.get_type(param_type))
        return names, types