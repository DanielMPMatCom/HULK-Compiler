import cmp.visitor as visitor
from hulk_ast import*
from cmp.semantic import*


class TypeCollector():
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.context = Context()
    
        obj_type = self.context.create_type('Object')
        num_type = self.context.create_type('Number')
        num_type.set_parent(obj_type)
        bool_type = self.context.create_type('Bool')
        bool_type.set_parent(obj_type)
        str_type = self.context.create_type('String')
        str_type.set_parent(obj_type)
        str_type.define_method('size', [], [], num_type)
        obj_type.define_method('equals', ['other'], [obj_type], bool_type)
        obj_type.define_method('toString', [], [], str_type)

        self.context.create_function('print', ['value'], [obj_type], str_type)
        self.context.create_function('sqrt', ['value'], [num_type], num_type)
        self.context.create_function('sin', ['angle'], [num_type], num_type)
        self.context.create_function('cos', ['angle'], [num_type], num_type)
        self.context.create_function('exp', ['value'], [num_type], num_type)
        self.context.create_function('log', ['base', 'value'], [num_type, num_type], num_type)
        self.context.create_function('rand', [], [], num_type)
        self.context.create_function('parse', ['value'], [str_type], num_type)

        iterable = self.context.create_protocol('Iterable')
        iterable.define_method('next', [], [], bool_type)
        iterable.define_method('current', [], [], obj_type)

        range_type = self.context.create_type('Range')
        range_type.set_parent(obj_type)
        range_type.param_names, range_type.param_types = ['min', 'max'], [num_type, num_type]
        range_type.define_attribute('min', num_type)
        range_type.define_attribute('max', num_type)
        range_type.define_attribute('current', num_type)
        range_type.define_method('next', [], [], bool_type)
        range_type.define_method('current', [], [], num_type)

        self.context.create_function('range', ['min', 'max'], [num_type, num_type], range_type)

        for declaration in node.declarations:
            self.visit(declaration)
        return self.context, self.errors
    
    @visitor.when(TypeDeclarationNode)
    def visit(self, node: TypeDeclarationNode):
        try:
            self.context.create_type(node.identifier)
        except SemanticError as error:
            self.errors.append(str(error))
            if node.identifier in self.context.types:
                self.context.types[node.identifier] = ErrorType()
            else:
                raise SemanticError(f'Type "{node.identifier}" is not defined.', node.line, node.column)

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node: ProtocolDeclarationNode):
        try:
            self.context.create_protocol(node.identifier)
        except SemanticError as error:
            self.errors.append(str(error))
            if node.identifier in self.context.protocols:
                self.context.protocols[node.identifier] = ErrorType()
            else:
                raise SemanticError(f'Protocol "{node.identifier}" is not defined.', node.line, node.column)