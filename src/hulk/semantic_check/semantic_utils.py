from src.hulk.hulk_grammar import *

class TypeDTONode():
    
    def __init__(self, param_names: list[str] = [], attributes : list[AttributeNode] = [], methods : list[MethodNode] = []):
        self.param_names = param_names
        self.attributes = attributes
        self.methods = methods

    
