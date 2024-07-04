from src.hulk.hulk_ast import *
from src.cmp.semantic import *
from src.cmp.visitor import visitor


class CodeGenVisitor:
    def __init__(self, context):
        self.context : Context = context
        self.new_block = ""
        self.block_definitions = ""
        self.variable_id = 0
        self.new_block_id = 0
        self.block_definitions_id = 0
        
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(NewTypeNode)
    def visit(self, node : NewTypeNode):
        variables = node.scope.get_all_variables()
        parameters = "("
        if len(variables) > 0:
            parameters += variables[0].name_for_CodeGen
            for var in variables[1:]:
                parameters += ", " + var.name_for_CodeGen
        parameters += ")"
        new_block = f"Object* newBlock{str(self.new_block_id)}("
        temp_id = self.new_block_id
        self.new_block_id += 1
        if len(variables) > 0:
            new_block += f"Object* {variables[0].name_for_CodeGen}"
            for var in variables[1:]:
                new_block += f", Object* {var.name_for_CodeGen}"
        new_block += ")"
        self.block_definitions += f"{new_block};\n"
        new_block += " {\n"
        define_variables = ""
        code = f"   return new{node.identifier}("
        class_ = self.context.get_type(node.identifier)
        arguments = node.args
        while class_ is not None and class_.name != "Object":
            for param in class_.param_names:
                variable = f"var{self.variable_id}"
                self.variable_id += 1
                define_variables += f"   Object* {variable} = {self.visit(arguments[class_.param_names.index(param)])};\n"
                # class_.node.scope.children
        
