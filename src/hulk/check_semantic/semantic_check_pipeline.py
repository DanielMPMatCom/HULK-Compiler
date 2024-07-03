from src.hulk.check_semantic.type_collector import TypeCollector
from src.hulk.check_semantic.type_builder import TypeBuilder
from src.hulk.check_semantic.type_checker import TypeChecker

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
        for error in errors:
            print('\t', error)
        print(']')
        print('Context:')
        print(context)
        print("============== CHECKING TYPES =================")
    type_checker = TypeChecker(context, errors)
    scope = type_checker.visit(ast)
    if verbose:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('Context:')
        print(context)
        print('Scope:')
        print(scope)
    return ast, errors, context, scope