import itertools as itt
from collections import OrderedDict
from hulk.hulk_ast import*
from typing import List

#region Errors
class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]
    
#endregion
    
#region Structures

class Attribute:
    def __init__(self, name, typex, current_node=None):
        self.name = name
        self.type = typex
        self.current_node = current_node

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class Method:
    def __init__(self, name, param_names, params_types, return_type, current_node=None):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type
        self.current_node = current_node

    def can_be_replaced_by(self, other):
        if self.name != other.name:
            return False
        if not other.return_type.conforms_to(self.return_type):
            return False
        if len(self.param_types) != len(other.param_types):
            return False
        for self_param_type, other_param_type in zip(self.param_types, other.param_types):
            if not self_param_type.conforms_to(other_param_type):
                return False
        return True

    def __str__(self):
        try:
            params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
        except:
            print([t for t in self.param_types])
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Type:
    def __init__(self, name:str, current_node=None):
        self.name = name
        self.attributes : list[Attribute] = []
        self.methods : list[Method] = []
        self.param_names = []
        self.param_types = []
        self.parent = None
        self.current_node = current_node

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex, current_node=None):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex, current_node)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name:str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name:str, param_names:list, param_types:list, return_type, current_node=None):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')
        method = Method(name, param_names, param_types, return_type, current_node)
        self.methods.append(method)
        return method

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain
    
    def set_parameters(self):
        param_names, param_types = self.get_parameters()
        self.param_names = param_names
        self.param_types = param_types

    def get_parameters(self):
        if (self.param_names is None or self.param_types is None) and self.parent is not None:
            param_names, param_types = self.parent.get_parameters()
        else:
            param_names = self.param_names
            param_types = self.param_types
        return param_names, param_types

    def conforms_to(self, other):
        if isinstance(other, Type):
            return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)
        elif isinstance(other, Protocol):
            try:
                return all(method.can_be_replaced_by(self.get_method(method.name)) for method in other.methods)
            except SemanticError    :
                return False

    def bypass(self):
        return False

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)
class Function:
    def __init__(self, name, param_names, param_types, return_type, current_node=None, body=None):
        self.name = name
        self.param_names = param_names
        self.param_types = param_types
        self.return_type = return_type
        self.body : ExpressionNode = body
        self.current_node = current_node

    def __eq__(self, other):
        return other.name == self.name and other.return_type == self.return_type and other.param_types == self.param_types

    
class Protocol:
    def __init__(self, name, current_node=None):
        self.name = name
        self.methods : "list[Method]" = []
        self.parent = None
        self.current_node = current_node

    def get_method(self, name: str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            
    def define_method(self, name:str, param_names:list, param_types:list, return_type, current_node=None):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')
        method = Method(name, param_names, param_types, return_type, current_node)
        self.methods.append(method)
        return method

    def conforms_to(self, other):
        if other == ObjectType():
            return True
        elif isinstance(other, Type):
            return False
        return self == other or (self.parent is not None and self.parent.conforms_to(
            other)) or self._has_not_ancestor_that_conforms_to(other)
    
    def _has_not_ancestor_that_conforms_to(self, other):
        if not isinstance(other, Protocol):
            return False
        try:
            return all(method.can_be_replaced_by(self.get_method(method.name)) for method in other.methods)
        except SemanticError:
            return False
    
#endregion
    
#region Types
    
class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)
    
class ObjectType(Type):
    def __init__(self):
        Type.__init__(self, 'Object')

    def __eq__(self, other):
        return isinstance(other, ObjectType) or self.name == other.name
    
class NumberType(Type):
    def __init__(self):
        Type.__init__(self, 'Number')
        self.set_parent(ObjectType())

    def __eq__(self, other):
        return isinstance(other, NumberType) or self.name == other.name
    
class StringType(Type):
    def __init__(self):
        Type.__init__(self, 'String')
        self.set_parent(ObjectType())

    def __eq__(self, other):
        return isinstance(other, StringType) or self.name == other.name
    
class BoolType(Type):
    def __init__(self):
        Type.__init__(self, 'Boolean')
        self.set_parent(ObjectType())

    def __eq__(self, other):
        return isinstance(other, BoolType) or self.name == other.name
    
class VectorType(Type):
    def __init__(self, element_type):
        Type.__init__(f'{element_type.name}[]')
        self.set_parent(ObjectType())
        self.define_method('size', [], [], NumberType())
        self.define_method('next', [], [], BoolType())
        self.define_method('current', [], [], element_type)

    def element_types(self):
        return self.get_method('current').return_type

    def conforms_to(self, other):
        return ((not isinstance(other, VectorType)) and Type.conforms_to(other)) or \
    (isinstance(other, VectorType) and self.element_types().conforms_to(other.element_types()))

    def __eq__(self, other):
        return isinstance(other, VectorType) and self.name == other.name

    def __str__(self):
        return f'type Vector : {self.element_types().name}'

    def __repr__(self):
        return str(self)
    
class UndefinedType(Type):
    def __init__(self):
        Type.__init__(self, '<undefined>')

    def __eq__(self, other):
        return isinstance(other, UndefinedType) or self.name == other.name
    
class AutoReferenceType(Type):
    def __init__(self, self_type: Type = None):
        Type.__init__(self, 'Self')
        self.self_type = self_type

    def get_attribute(self, name: str):
        if self.self_type:
            return self.self_type.get_attribute(name)
        return Type.get_attribute(name)

    def __eq__(self, other):
        return isinstance(other, AutoReferenceType) or self.name == other.name
      
#endregion

#region Context
class Context:
    def __init__(self):
        self.types = {}
        self.functions = {}
        self.protocols = {}
        # self.id_to_type = {}

    def create_type(self, name:str, current_node=None):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        if name in self.protocols:
            raise SemanticError(f'Protocol with the same name ({name}) already in context.')
        type_ = self.types[name] = Type(name, current_node)
        return type_

    def get_type(self, name:str, params_amount=None):
        try:
            type_type = self.types[name]
            if isinstance(type_type, ErrorType) and params_amount is not None:
                type_type = ErrorType()
                type_type.param_names = [f'Error' for _ in range(params_amount)]
                type_type.param_types = [ErrorType() for _ in range(params_amount)]
            return type_type
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')
    
    def create_function(self, name:str, param_names:"list[str]", param_types:list, return_type, current_node=None, body : list = []):
        if name in self.types:
            raise SemanticError(f'Function with the same name ({name}) already in context.')
        function = self.functions[name] = Function(name, param_names, param_types, return_type, current_node=current_node, body=body)
        return function
    
    def get_function_by_name(self, name:str):
        try:
            return self.functions[name]
        except KeyError:
            raise SemanticError(f'Function "{name}" is not defined.')
        
    def create_protocol(self, name:str):
        if name in self.protocols:
            raise SemanticError(f'Protocol with the same name ({name}) already in context.')
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        protocol = self.protocols[name] = Protocol(name)
        return protocol
    
    def get_protocol(self, name:str) -> Protocol:
        try:
            return self.protocols[name]
        except KeyError:
            raise SemanticError(f'Protocol "{name}" is not defined.')
        
    def type_protocol_or_vector(self, type_):
        if isinstance(self.types[type_], VectorType):
            vector_element_type = self.type_protocol_or_vector(type_.element_type)
            return VectorType(vector_element_type)
        else:
            try:
                return self.get_type(type_)
            except SemanticError:
                return self.get_protocol(type_)
    
    # def save_id_type(self, node : TypeDeclarationNode):
    #     self.id_to_type[node.identifier] = node

    #     if node.parent:
    #         try:
    #             parent_node : TypeDeclarationNode = self.id_to_type[node.parent]
    #         except:
    #             print(f"Bug inherit {node.identifier} from {node.parent}, before parent declaration")
    #             return
            
    #         # attributes
    #         node_attr_id = [attr.identifier for attr in node.attributes]
    #         node.attributes += [attr for attr in parent_node.attributes if attr.identifier not in node_attr_id]
            
    #         # methods
    #         for p_method in parent_node.methods:
    #             for method in node.methods:
    #                 if method.identifier == p_method.identifier:
    #                     method.scope.define_function(
    #                         fname='base',
    #                         params=p_method.params_ids,
    #                         return_type=p_method.type,
    #                         body=p_method.expression
    #                     )
    #                     break
    #         node_methods_ids = [m.identifier for m in node.methods]
    #         node.methods += [m for m in parent_node.methods if m.identifier not in node_methods_ids ]


    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)
class VariableInfo:
    def __init__(self, name, vtype, value = None):
        self.name = name
        self.type = vtype
        self.name_for_CodeGen = None
        self.value = value
    
    def set_name_for_CodeGen(self, name):
        self.name_for_CodeGen = name
        
    def update(self, new_value = None): 
        self.value = new_value
    
#endregion


#region Scope
class Scope:
    def __init__(self, parent=None):
        self.local_vars : list[VariableInfo] = []
        self.local_funcs : list[Function]= []
        self.parent : Scope = parent
        self.children : list[Scope] = []
        self.var_index_at_parent = 0 if parent is None else len(parent.local_vars)
        self.func_index_at_parent = 0 if parent is None else len(parent.local_funcs)
        
    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope

    def define_variable(self, vname, vtype):
        if not self.is_var_globally_defined(vname):
            self.local_vars.append(VariableInfo(vname, vtype))
            return True
        return False
    
    def define_function(self, fname, params, return_type, body = None):
        if not self.is_func_locally_defined(fname, len(params)):
            self.local_funcs.append(Function(fname, params, return_type, body))
        
        
    def is_var_locally_defined(self, vname):
        return self.get_local_variable_info(vname) is not None
    
    def is_func_locally_defined(self, fname, n):
        return self.get_local_function_info(fname, n) is not None
    
    def is_var_globally_defined(self, vname):
        return self.get_global_variable_info(vname) is not None        
    
    def is_func_globally_defined(self, fname, n):
        return self.get_global_function_info(fname, n) is not None

    def get_local_variable_info(self, vname) -> VariableInfo:
        for var in self.local_vars:
            if var.name == vname:
                return var
        return None
    
    def get_local_function_info(self, fname, n) -> Function:
        for func in self.local_funcs:
            if func.name == fname and len(func.params) == n:
                return func
        return None
    
    def get_global_variable_info(self, vname) -> VariableInfo:
        local = self.get_local_variable_info(vname)
        if local is None:
            if self.parent is not None:
                return self.parent.get_global_variable_info(vname)
        return local

    def get_global_function_info(self, fname, n) -> Function:
        local = self.get_local_function_info(fname, n)
        if local is None:
            if self.parent is not None:
                return self.parent.get_global_function_info(fname, n)
        return local
    
    def get_all_variables(self):
        variables = [var for var in self.local_vars]
        if self.paret is not None:
            variables.extend(self.parent.get_all_variables())
        return variables

#endregion

#region Auxiliary Functions

def lowest_common_ancestor(types):
    if types is None or any_equivalent_type(types, ErrorType):
        return ErrorType()
    if any_equivalent_type(types, UndefinedType):
        return UndefinedType()
    low_com_anc = types[0]
    for other_type in types[1:]:
        low_com_anc = _lowest_common_ancestor_rec(low_com_anc, other_type)
    return low_com_anc

def _lowest_common_ancestor_rec(type1 : Type, type2 : Type):
    if type1 is None or type2 is None:
        return ObjectType()
    if type1 == type2:
        return type1
    if type1.conforms_to(type2):
        return type2
    if type2.conforms_to(type1):
        return type1
    return _lowest_common_ancestor_rec(_lowest_common_ancestor_rec(type1.parent, type2), _lowest_common_ancestor_rec(type1, type2.parent))

def any_equivalent_type(types, type_):
    for type1 in types:
        if isinstance(type1, type_): return True
        elif type1 == type_: return True
    return False

#endregion