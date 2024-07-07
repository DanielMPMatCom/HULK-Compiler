from hulk.semantic_check.type_collector import TypeCollector
from hulk.semantic_check.type_builder import TypeBuilder
from hulk.semantic_check.type_checker import TypeChecker
from hulk.semantic_check.variable_collector import VariableCollector

def formatErrors(vector) :
    for error in vector:
        print("\033[91m::" +"\t❌ Semantic Error: " + str(error) + "\033[0m") 

def semantic_check_pipeline(ast, verbose=False):
    if verbose:
        print("============== COLLECTING TYPES ===============")
    errors = []
    type_collector = TypeCollector(errors)
    type_collector.visit(ast)
    context = type_collector.context
    errors = type_collector.errors
    if verbose:
        print('Errors:', errors)
        print('Context:')
        print(context)
        print("============== BUILDING TYPES =================")
    type_builder = TypeBuilder(context, errors)
    type_builder.visit(ast)
    if verbose:
        print('Errors: [')
        formatErrors(errors)
        print(']')
        print('Context:')
        print(context)
        print("============== COLLECTING VARIABLES =================")
    variable_collector = VariableCollector(context, errors)
    scope = variable_collector.visit(ast)
    if verbose:
        print('Errors: [')
        formatErrors(errors)
        print(']')
        print('Context:')
        print(context)
        print('Scope:')
        print(scope)
        print("============== CHECKING TYPES =================")
    type_checker = TypeChecker(context, errors)
    type_checker.visit(ast)
    if verbose:
        print('Errors: [')
        formatErrors(errors)
        print(']')
        print('Context:')
        print(context)
        print('Scope:')
        print(scope)
    return ast, errors, context, scope