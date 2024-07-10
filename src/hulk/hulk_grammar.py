from cmp.pycompiler import Grammar
from hulk.hulk_ast import*
from math import pi as piValue
from math import e as eValue

G =  Grammar()


#---------------------------------------------------Non-Terminals---------------------------------------------------------
Program = G.NonTerminal('Program', startSymbol=True)
Declaration_list, Declaration = G.NonTerminals('Declaration_list Declaration')
Expression, Line_Expression, Program_Expression, Simple_Expression, Non_Empty_Expression_list, Comma_Sep_Expr_List, Non_Empty_Comma_Sep_Expr_List, Expression_Block = G.NonTerminals(
    'Expression Line_Expression Program_Expression Simple_Expression Non_Empty_Expression_list Comma_Sep_Expr_List Non_Empty_Comma_Sep_Expr_List Expression_Block'
    )
Atom = G.NonTerminal('Atom')
Arithmetic_Expression_p_m, Arithmetic_Expression_s_d_mod = G.NonTerminals(
    'Arithmetic_Expression_p_m Arithmetic_Expression_s_d_mod'
    )
Destructive_Operation, Or_Operation, And_Operation, Not_Operation = G.NonTerminals(
    'Destructive_Operation Or_Operation And_Operation Not_Operation'
    )
Equality_Operation, Inequality_Operation, Is_As_Operation, Concat_Operation, Plus_Minus_Sign_Operation, Pow_Operation = G.NonTerminals(
    'Equality_Operation Inequality_Operation Is_As_Operation Concat_Operation Plus_Minus_Sign_Operation Pow_Operation'
    )
Obj_Indx_Method_Attr_Call = G.NonTerminal('Obj_Indx_Method_Attr_Call')
Type_Declaration, New_Type_Operation, Type_Params, Type_Body, Non_Empty_Type_Body = G.NonTerminals(
    'Type_Declaration New_Type_Operation Type_Params Type_Body Non_Empty_Type_Body'
    )
Protocol_Declaration, Protocol_Methods_Signatures = G.NonTerminals('Protocol_Declaration Protocol_Methods_Signatures')
Func_Declaration, Func_Call = G.NonTerminals('Func_Declaration Func_Call')
Params_list, Params_Typed, Possibly_Empty_Params_list, Possibly_Empty_Param_Type, Attribute, Method = G.NonTerminals(
    'Params_list Params_Typed Possibly_Empty_Params_list Possibly_Empty_Param_Type Attribute Method'
    )
Assignment_list, Type_Var, Possibly_Empty_Type, Non_Empty_Type = G.NonTerminals(
    'Assignment_list Type_Var Possibly_Empty_Type Non_Empty_Type'
    )
Elif_list = G.NonTerminal('Elif_list')
Vector_Initialization = G.NonTerminal('Vector_Initialization')


#------------------------------------------------------Terminals----------------------------------------------------------
semi, colon, comma, dot, opar, cpar, ocurly, ccurly, obrack, cbrack = G.Terminals('; : , . ( ) { } [ ]')
plus, minus, star, div, power, power_star , concat, dobleconcat, arrow, mod = G.Terminals('+ - * / ^ ** @ @@ => %')
eq, neq, le, leq, gr, greq, eqeq, dest_eq = G.Terminals('= != < <= > >= == :=')
and_, or_, not_ = G.Terminals('& | !') 
num_, str_, bool_, id_, let_, in_, is_, as_, if_, elif_, else_, while_, for_, new = G.Terminals('num str bool id let in is as if elif else while for new')
func_, type_, inherits_, protocol_, extends_, base_ = G.Terminals('func type inherits protocol extends base')
bar_bar_ = G.Terminal('||')
pi, e = G.Terminals('PI E')



#-----------------------------------------------------Productions---------------------------------------------------------

#----------------------------------------------------Expressions----------------------------------------------------------

# A Program is a declaration list followed by an expression
Program %= Declaration_list + Program_Expression, lambda h,s: ProgramNode(s[1], s[2]), None, None

# A declaration list is a list of 0 or more declarations
Declaration_list %= Declaration_list +  Declaration, lambda h,s: s[1] + [s[2]], None, None
Declaration_list %= G.Epsilon, lambda h,s: []

# A declaration is a type declaration, a function declaration or a protocol declaration
Declaration %= Type_Declaration, lambda h,s: s[1], None
Declaration %= Func_Declaration, lambda h,s: s[1], None
Declaration %= Protocol_Declaration, lambda h,s: s[1], None

# A program expression is the global program expression
Program_Expression %= Simple_Expression, lambda h,s: s[1], None
Program_Expression %= Line_Expression, lambda h,s: s[1], None

# A line expression is a simple expression followed by a semicolon, an expression block or an expression block followed by a semicolon
Line_Expression %= Expression + semi, lambda h,s: s[1], None, None
Line_Expression %= Expression_Block, lambda h,s: s[1], None

# An expression is a single exrpession or an expression block
Expression %= Expression_Block, lambda h,s: s[1], None
Expression %= Simple_Expression, lambda h,s: s[1], None

# An expression block is a list of expressions enclosed in curly braces. It can't be empty
Expression_Block %= ocurly + Non_Empty_Expression_list + ccurly, lambda h,s: ExpressionBlockNode(s[2]), None, None, None

# A non empty expression list is a line expression or a line expression followed by a non empty expression list
Non_Empty_Expression_list %= Line_Expression, lambda h,s: [s[1]], None
Non_Empty_Expression_list %= Line_Expression + Non_Empty_Expression_list, lambda h,s: [s[1]] + s[2], None, None
Non_Empty_Expression_list %= Simple_Expression, lambda h,s: [s[1]], None

# A list of expressions separated by commas
Comma_Sep_Expr_List %= G.Epsilon, lambda h,s: []
Comma_Sep_Expr_List %= Non_Empty_Comma_Sep_Expr_List, lambda h,s: s[1]

Non_Empty_Comma_Sep_Expr_List %= Expression, lambda h,s: [s[1]], None
Non_Empty_Comma_Sep_Expr_List %= Expression + comma + Non_Empty_Comma_Sep_Expr_List, lambda h,s: [s[1]] + s[3], None, None, None

# A simple expression is a let in expression, an if expression, a while expression, a for expression or a destructive operation
Simple_Expression %= let_ + Assignment_list + in_ + Expression, lambda h,s: LetInNode(s[2], s[4]), None, None, None, None
Simple_Expression %= if_ + opar + Expression + cpar + Expression + Elif_list + else_ + Expression, lambda h,s: IfElseNode([(s[3], s[5])] + s[6], s[8]), None, None, None, None, None, None, None, None
Simple_Expression %= while_ + opar + Expression + cpar + Expression, lambda h,s: WhileNode(s[3], s[5]), None, None, None, None, None
Simple_Expression %= for_ + opar + id_ + in_ + Expression + cpar + Expression, lambda h,s: ForNode(s[3], s[5], s[7]), None, None, None, None, None, None, None
Simple_Expression %= Destructive_Operation, lambda h,s: s[1], None

# Let in assignments
Assignment_list %= Assignment_list + comma + Type_Var, lambda h,s: s[1] + [s[3]], None, None, None
Assignment_list %= Type_Var, lambda h,s: [s[1]], None

Type_Var %= id_ + Possibly_Empty_Type + eq + Expression, lambda h,s: VariableDeclarationNode(s[1], s[4], s[2]), None, None, None, None

Possibly_Empty_Type %= G.Epsilon, lambda h,s: None
Possibly_Empty_Type %= colon + Non_Empty_Type, lambda h,s: s[2], None, None

Non_Empty_Type %= id_, lambda h,s: s[1], None
Non_Empty_Type %= Non_Empty_Type + obrack + cbrack, lambda h,s: VectorNode(s[1]), None, None, None

# Elif list is a list of 0 or more elif statements
Elif_list %= elif_ + opar + Expression + cpar + Expression + Elif_list, lambda h,s: [(s[3], s[5])] + s[6], None, None, None, None, None, None
Elif_list %= G.Epsilon, lambda h,s: []

# Desctructive operation
Destructive_Operation %= Or_Operation + dest_eq + Destructive_Operation, lambda h,s: DestructiveOperationNode(s[1], s[3]), None, None, None
Destructive_Operation %= Or_Operation, lambda h,s: s[1], None

Or_Operation %= Or_Operation + or_ + And_Operation, lambda h,s: OrNode(s[1], s[3]), None, None, None
Or_Operation %= And_Operation, lambda h,s: s[1], None

And_Operation %= And_Operation + and_ + Equality_Operation, lambda h,s: AndNode(s[1], s[3]), None, None, None
And_Operation %= Equality_Operation, lambda h,s: s[1], None

Equality_Operation %= Equality_Operation + eqeq + Inequality_Operation, lambda h,s: EqualNode(s[1], s[3]), None, None, None
Equality_Operation %= Equality_Operation + neq + Inequality_Operation, lambda h,s: NonEqualNode(s[1], s[3]), None, None, None
Equality_Operation %= Inequality_Operation, lambda h,s: s[1], None

Inequality_Operation %= Inequality_Operation + le + Is_As_Operation, lambda h,s: LessThanNode(s[1], s[3]), None, None, None
Inequality_Operation %= Inequality_Operation + leq + Is_As_Operation, lambda h,s: LessEqualNode(s[1], s[3]), None, None, None
Inequality_Operation %= Inequality_Operation + gr + Is_As_Operation, lambda h,s: GreaterThanNode(s[1], s[3]), None, None, None
Inequality_Operation %= Inequality_Operation + greq + Is_As_Operation, lambda h,s: GreaterEqualNode(s[1], s[3]), None, None, None
Inequality_Operation %= Is_As_Operation, lambda h,s: s[1], None

Is_As_Operation %= Is_As_Operation + is_ + Concat_Operation, lambda h,s: IsNode(s[1], s[3]), None, None, None
Is_As_Operation %= Is_As_Operation + as_ + Concat_Operation, lambda h,s: AsNode(s[1], s[3]), None, None, None
Is_As_Operation %= Concat_Operation, lambda h,s: s[1], None

Concat_Operation %= Concat_Operation + concat + Arithmetic_Expression_p_m, lambda h,s: ConcatNode(s[1], s[3]), None, None, None
Concat_Operation %= Concat_Operation + dobleconcat + Arithmetic_Expression_p_m, lambda h,s: SpacedConcatNode(s[1], s[3]), None, None, None
Concat_Operation %= Arithmetic_Expression_p_m, lambda h,s: s[1], None

Arithmetic_Expression_p_m %= Arithmetic_Expression_p_m + plus + Arithmetic_Expression_s_d_mod, lambda h,s: PlusNode(s[1], s[3]), None, None, None
Arithmetic_Expression_p_m %= Arithmetic_Expression_p_m + minus + Arithmetic_Expression_s_d_mod, lambda h,s: MinusNode(s[1], s[3]), None, None, None
Arithmetic_Expression_p_m %= Arithmetic_Expression_s_d_mod, lambda h,s: s[1], None

Arithmetic_Expression_s_d_mod %= Arithmetic_Expression_s_d_mod + star + Plus_Minus_Sign_Operation, lambda h,s: StarNode(s[1], s[3]), None, None, None
Arithmetic_Expression_s_d_mod %= Arithmetic_Expression_s_d_mod + div + Plus_Minus_Sign_Operation, lambda h,s: DivNode(s[1], s[3]), None, None, None
Arithmetic_Expression_s_d_mod %= Arithmetic_Expression_s_d_mod + mod + Plus_Minus_Sign_Operation, lambda h,s: ModNode(s[1], s[3]), None, None, None
Arithmetic_Expression_s_d_mod %= Plus_Minus_Sign_Operation, lambda h,s: s[1], None

Plus_Minus_Sign_Operation %= plus + Pow_Operation, lambda h,s: s[2], None, None
Plus_Minus_Sign_Operation %= minus + Pow_Operation, lambda h,s: NotUnaryOpNode(s[2]), None, None
Plus_Minus_Sign_Operation %= Pow_Operation, lambda h,s: s[1], None

Pow_Operation %= New_Type_Operation + power + Pow_Operation, lambda h,s: PowNode(s[2], s[1], s[3]), None, None, None
Pow_Operation %= New_Type_Operation + power_star + Pow_Operation, lambda h,s: PowNode(s[2], s[1], s[3]), None, None, None
Pow_Operation %= New_Type_Operation, lambda h,s: s[1], None

New_Type_Operation %= new + id_ + opar + Comma_Sep_Expr_List + cpar, lambda h,s: NewTypeNode(s[2], s[4]), None, None, None, None, None
New_Type_Operation %= Not_Operation, lambda h,s: s[1], None

Not_Operation %= not_ + Obj_Indx_Method_Attr_Call, lambda h,s: NotNode(s[2]), None, None
Not_Operation %= Obj_Indx_Method_Attr_Call, lambda h,s: s[1], None

Obj_Indx_Method_Attr_Call %= Obj_Indx_Method_Attr_Call + dot + id_ + opar + Comma_Sep_Expr_List + cpar, lambda h,s: MethodCallNode(s[1], s[3], s[5]), None, None, None, None, None, None
Obj_Indx_Method_Attr_Call %= Obj_Indx_Method_Attr_Call + dot + id_, lambda h,s: AttributeCallNode(s[1], s[3]), None, None, None
Obj_Indx_Method_Attr_Call %= Obj_Indx_Method_Attr_Call + obrack + Expression + cbrack, lambda h,s: IndexNode(s[1], s[3]), None, None, None, None
Obj_Indx_Method_Attr_Call %= Atom, lambda h,s: s[1], None

Func_Call %= id_ + opar + Comma_Sep_Expr_List + cpar, lambda h,s: FunctionCallNode(s[1], s[3]), None, None, None, None

Vector_Initialization %= obrack + Comma_Sep_Expr_List + cbrack, lambda h,s: InitializeVectorNode(s[2]), None, None, None
Vector_Initialization %= obrack + Expression + bar_bar_ + id_ + in_ + Expression + cbrack, lambda h,s: InitializeVectorListComprehensionNode(s[2], s[4], s[6]), None, None, None, None, None, None, None

Atom %= opar + Expression + cpar, lambda h,s: s[2], None, None, None
Atom %= num_, lambda h,s: NumNode(s[1]), None
Atom %= str_, lambda h,s: StringNode(s[1]), None
Atom %= bool_, lambda h,s: BoolNode(s[1]), None
Atom %= id_, lambda h,s: IDNode(s[1]), None
Atom %= Func_Call, lambda h,s: s[1], None
Atom %= base_ + opar + Comma_Sep_Expr_List + cpar, lambda h,s: BaseCallNode(s[3]), None, None, None, None
Atom %= Vector_Initialization, lambda h,s: s[1], None
Atom %= pi, lambda h,s: ConstantNumNode(s[1], piValue)
Atom %= e, lambda h,s: ConstantNumNode(s[1], eValue)
# Atom %= Expression_Block, lambda h,s: s[1], None

#----------------------------------------------Declarations---------------------------------------------------------#

# Type Declarations
Type_Declaration %= type_ + id_ + Type_Params + ocurly + Type_Body + ccurly, lambda h,s: TypeDeclarationNode(s[2], s[3], s[5]), None, None, None, None, None, None
Type_Declaration %= type_ + id_ + Type_Params + inherits_ + id_ + ocurly + Type_Body + ccurly, lambda h,s: TypeDeclarationNode(s[2], s[3], s[7], s[5]), None, None, None, None, None, None, None, None
Type_Declaration %= type_ + id_ + Type_Params + inherits_ + id_ + opar + Comma_Sep_Expr_List + cpar + ocurly + Type_Body + ccurly, lambda h,s: TypeDeclarationNode(s[2], s[3], s[10], s[5], s[7]), None, None, None, None, None, None, None, None, None, None, None

Type_Params %= opar + Possibly_Empty_Params_list + cpar, lambda h,s: s[2], None, None, None
Type_Params %= G.Epsilon, lambda h,s: None

Possibly_Empty_Params_list %= Params_list, lambda h,s: s[1], None
Possibly_Empty_Params_list %= G.Epsilon, lambda h,s: []

Params_list %= id_ + Possibly_Empty_Type, lambda h,s: [(s[1], s[2])], None, None
Params_list %= Params_list + comma + id_ + Possibly_Empty_Type, lambda h,s: s[1] + [(s[3], s[4])], None, None, None, None

Type_Body %= G.Epsilon, lambda h,s: []
Type_Body %= Non_Empty_Type_Body, lambda h,s: s[1], None

Non_Empty_Type_Body %= Non_Empty_Type_Body + Attribute, lambda h,s: s[1] + [s[2]], None, None
Non_Empty_Type_Body %= Non_Empty_Type_Body + Method, lambda h,s: s[1] + [s[2]], None, None
Non_Empty_Type_Body %= Attribute, lambda h,s: [s[1]], None
Non_Empty_Type_Body %= Method, lambda h,s: [s[1]], None

Attribute %= id_ + Possibly_Empty_Type + eq + Line_Expression, lambda h,s: AttributeNode(s[1], s[4], s[2]), None, None, None, None

Method %= id_ + opar + Possibly_Empty_Params_list + cpar + Possibly_Empty_Type + arrow + Simple_Expression + semi, lambda h,s: MethodNode(s[1], s[3], s[7], s[5]), None, None, None, None, None, None, None, None
Method %= id_ + opar + Possibly_Empty_Params_list + cpar + Possibly_Empty_Type + Expression_Block, lambda h,s: MethodNode(s[1], s[3], s[6], s[5]), None, None, None, None, None, None
Method %= id_ + opar + Possibly_Empty_Params_list + cpar + Possibly_Empty_Type + Expression_Block + semi, lambda h,s: MethodNode(s[1], s[3], s[6], s[5]), None, None, None, None, None, None, None

# Function Declarations
Func_Declaration %= func_ + id_ + opar + Possibly_Empty_Params_list + cpar + Possibly_Empty_Type + arrow + Simple_Expression + semi, lambda h,s: FunctionDeclarationNode(s[2], s[4], s[8], s[6]), None, None, None, None, None, None, None, None, None
Func_Declaration %= func_ + id_ + opar + Possibly_Empty_Params_list + cpar + Possibly_Empty_Type + Expression_Block, lambda h,s: FunctionDeclarationNode(s[2], s[4], s[7], s[6]), None, None, None, None, None, None, None
Func_Declaration %= func_ + id_ + opar + Possibly_Empty_Params_list + cpar + Possibly_Empty_Type + Expression_Block + semi, lambda h,s: FunctionDeclarationNode(s[2], s[4], s[7], s[6]), None, None, None, None, None, None, None, None

# Protocol Declarations
Protocol_Declaration %= protocol_ + id_ + ocurly + Protocol_Methods_Signatures + ccurly, lambda h,s: ProtocolDeclarationNode(s[2], s[4], None), None, None, None, None, None
Protocol_Declaration %= protocol_ + id_ + extends_ + id_ + ocurly + Protocol_Methods_Signatures + ccurly, lambda h,s: ProtocolDeclarationNode(s[2], s[6], s[4]), None, None, None, None, None, None, None

Protocol_Methods_Signatures %= Protocol_Methods_Signatures + id_ + opar + Params_Typed + cpar + colon + Non_Empty_Type + semi, lambda h,s: s[1] + [ProtocolMethodSignatureNode(s[2], s[4], s[7])], None, None, None, None, None, None, None, None
Protocol_Methods_Signatures %= id_ + opar + Params_Typed + cpar + colon + Non_Empty_Type + semi, lambda h,s: [ProtocolMethodSignatureNode(s[1], s[3], s[6])], None, None, None, None, None, None, None

Params_Typed %= G.Epsilon, lambda h,s: []
Params_Typed %= Params_Typed + comma + id_ + colon + Non_Empty_Type, lambda h,s: s[1] + [(s[3], s[5])], None, None, None, None, None
Params_Typed %= id_ + colon + Non_Empty_Type, lambda h,s: [(s[1], s[3])], None, None, None


#----------------------------------------------------End of Productions---------------------------------------------------

print(G)