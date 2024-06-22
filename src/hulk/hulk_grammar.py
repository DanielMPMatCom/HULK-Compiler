from ..cmp.pycompiler import Grammar

G =  Grammar()


#---------------------------------------------------Non-Terminals---------------------------------------------------------
Program = G.NonTerminal('Program', startSymbol=True)
Declaration_list, Declaration = G.NonTerminals('Declaration_list Declaration')
Expression, Line_Expression, Program_Expression, Simple_Expression, Non_Empty_Expression_list, Comma_Sep_Expr_List, Expression_Block, = G.NonTerminals(
    'Expression Line_Expression Program_Expression Simple_Expression Non_Empty_Expression_list Comma_Sep_Expr_List Expression_Block'
    )
Factor, Atom = G.NonTerminals('Factor Atom')
Arithmetic_Expression_p_m, Arithmetic_Expression_s_d_mod = G.NonTerminal(
    'Arithmetic_Expression_p_m Arithmetic_Expression_s_d_mod'
    )
Destructive_Operation, Or_Operation, And_Operation, Not_Operation = G.NonTerminals(
    'Destructive_Operation Or_Operation And_Operation Not_Operation'
    )
Equality_Operation, Inequality_Operation, Is_As_Operation, Concat_Operation, Plus_Minus_Sign_Operation, Pow_Operation = G.NonTerminals(
    'Equality_Operation Inequality_Operation Is_As_Operation Concat_Operation Plus_Minus_Sign_Operation Pow_Operation'
    )
Obj_Indx_Method_Attr_Call = G.NonTerminals('Obj_Indx_Method_Attr_Call')
Type_Declaration, New_Type_Operation, Type_Params, Type_Body = G.NonTerminals(
    'Type_Declaration New_Type_Operation Type_Params Type_Body'
    )
Protocol_Declaration, Protocol_Body = G.NonTerminal('Protocol_Declaration')
Func_Declaration, Func_Call = G.NonTerminals('Func_Declaration Func_Call')
Params_list, Params_Typed, Attribute, Method = G.NonTerminals('Params_list Params_Typed Attribute Method')
Assignment_list, Type_Var, Possibly_Empty_Type, Non_Empty_Type = G.NonTerminals('Assignment_list Type_Var Non_Empty_Type')
Elif_list = G.NonTerminal('Elif_list')
Vector_Initialization = G.NonTerminal('Vector_Initialization')



#------------------------------------------------------Terminals----------------------------------------------------------
semi, colon, comma, dot, opar, cpar, ocurly, ccurly, obrack, cbrack = G.Terminal('; : , . ( ) { } [ ]')
plus, minus, star, div, power, power_star , concat, dobleconcat, arrow, mod = G.Terminal('+ - * / ^ ** @ @@ => %')
eq, neq, le, leq, gr, greq, eqeq, dest_eq = G.Terminals('= != < <= > >= == :=')
and_, or_, not_ = G.Terminal('& | !') 
num_, str_, bool_, const_, id_, let_, in_, is_, as_, if_, elif_, else_, while_, for_, new, type_id = G.Terminal('num str bool const id let in is as if elif else while for new type_id')
func_, type_, inherits_, protocol_, extends_, base_ = G.Terminal('func type inherits protocol extends base')
bar_bar_ = G.Terminal('||')



#-----------------------------------------------------Productions---------------------------------------------------------

#----------------------------------------------------Expressions----------------------------------------------------------

# A Program is a declaration list followed by an expression
Program %= Declaration_list + Program_Expression

# A declaration list is a list of 0 or more declarations
Declaration_list %= Declaration + Declaration_list
Declaration_list %= G.Epsilon

# A declaration is a type declaration, a function declaration or a protocol declaration
Declaration %= Type_Declaration
Declaration %= Func_Declaration
Declaration %= Protocol_Declaration

# A program expression is the global program expression
Program_Expression %= Simple_Expression
Program_Expression %= Line_Expression

# A line expression is a simple expression followed by a semicolon, an expression block or an expression block followed by a semicolon
Line_Expression %= Expression + semi
Line_Expression %= Expression_Block

# An expression is a single exrpession or an expression block
Expression %= Simple_Expression
Expression %= Expression_Block

# An expression block is a list of expressions enclosed in curly braces. It can't be empty
Expression_Block %= ocurly + Non_Empty_Expression_list + ccurly

# A non empty expression list is a line expression or a line expression followed by a non empty expression list
Non_Empty_Expression_list %= Line_Expression
Non_Empty_Expression_list %= Line_Expression + Non_Empty_Expression_list

# A list of expressions separated by commas
Comma_Sep_Expr_List %= G.Epsilon
Comma_Sep_Expr_List %= Expression
Comma_Sep_Expr_List %= Expression + comma + Comma_Sep_Expr_List

# A simple expression is a let in expression, an if expression, a while expression, a for expression or a destructive operation
Simple_Expression %= let_ + Assignment_list + in_ + Expression
Simple_Expression %= if_ + opar + Expression + cpar + Expression + Elif_list + else_ + Expression
Simple_Expression %= while_ + opar + Expression + cpar + Expression
Simple_Expression %= for_ + opar + id_ + in_ + Expression + cpar + Expression
Simple_Expression %= Destructive_Operation

# Elif list is a list of 0 or more elif statements
Elif_list %= elif_ + opar + Expression + cpar + Expression + Elif_list
Elif_list %= G.Epsilon

# Let in
Assignment_list %= Assignment_list + comma + Type_Var
Assignment_list %= Type_Var

Type_Var %= id_ + Possibly_Empty_Type + eq + Expression

Possibly_Empty_Type %= G.Epsilon
Possibly_Empty_Type %= Non_Empty_Type

Non_Empty_Type %= colon + id_
Non_Empty_Type %= colon + Type_Var + obrack + cbrack

# Desctructive operation
Destructive_Operation %= Or_Operation + dest_eq + Destructive_Operation
Destructive_Operation %= Or_Operation

Or_Operation %= Or_Operation + or_ + And_Operation
Or_Operation %= And_Operation

And_Operation %= And_Operation + and_ + Equality_Operation
And_Operation %= Equality_Operation

Equality_Operation %= Equality_Operation + eqeq + Inequality_Operation
Equality_Operation %= Equality_Operation + neq + Inequality_Operation
Equality_Operation %= Inequality_Operation

Inequality_Operation %= Inequality_Operation + le + Is_As_Operation
Inequality_Operation %= Inequality_Operation + leq + Is_As_Operation
Inequality_Operation %= Inequality_Operation + gr + Is_As_Operation
Inequality_Operation %= Inequality_Operation + greq + Is_As_Operation
Inequality_Operation %= Is_As_Operation

Is_As_Operation %= Is_As_Operation + is_ + Concat_Operation
Is_As_Operation %= Is_As_Operation + as_ + Concat_Operation
Is_As_Operation %= Concat_Operation

Concat_Operation %= Concat_Operation + concat + Arithmetic_Expression_p_m
Concat_Operation %= Concat_Operation + dobleconcat + Arithmetic_Expression_p_m
Concat_Operation %= Arithmetic_Expression_p_m

Arithmetic_Expression_p_m %= Arithmetic_Expression_p_m + plus + Arithmetic_Expression_s_d_mod
Arithmetic_Expression_p_m %= Arithmetic_Expression_p_m + minus + Arithmetic_Expression_s_d_mod
Arithmetic_Expression_p_m %= Arithmetic_Expression_s_d_mod

Arithmetic_Expression_s_d_mod %= Arithmetic_Expression_s_d_mod + star + Plus_Minus_Sign_Operation
Arithmetic_Expression_s_d_mod %= Arithmetic_Expression_s_d_mod + div + Plus_Minus_Sign_Operation
Arithmetic_Expression_s_d_mod %= Arithmetic_Expression_s_d_mod + mod + Plus_Minus_Sign_Operation
Arithmetic_Expression_s_d_mod %= Plus_Minus_Sign_Operation

Plus_Minus_Sign_Operation %= plus + Pow_Operation
Plus_Minus_Sign_Operation %= minus + Pow_Operation
Plus_Minus_Sign_Operation %= Pow_Operation

Pow_Operation %= New_Type_Operation + power + Pow_Operation
Pow_Operation %= New_Type_Operation + power_star + Pow_Operation
Pow_Operation %= New_Type_Operation

New_Type_Operation %= new + id_ + opar + Comma_Sep_Expr_List + cpar
New_Type_Operation %= Not_Operation

Not_Operation %= not_ + Obj_Indx_Method_Attr_Call
Not_Operation %= Obj_Indx_Method_Attr_Call

Obj_Indx_Method_Attr_Call %= Obj_Indx_Method_Attr_Call + dot + id_ + opar + Obj_Indx_Method_Attr_Call + cpar
Obj_Indx_Method_Attr_Call %= Obj_Indx_Method_Attr_Call + dot + id_
Obj_Indx_Method_Attr_Call %= Obj_Indx_Method_Attr_Call + obrack + Expression + cbrack
Obj_Indx_Method_Attr_Call %= Factor

Func_Call %= id_ + opar + Comma_Sep_Expr_List + cpar

Vector_Initialization %= obrack + Comma_Sep_Expr_List + cbrack
Vector_Initialization %= obrack + Expression + bar_bar_ + id_ + in_ + Expression + cbrack

Factor %= opar + Expression + cpar
Factor %= Atom

Atom %= num_
Atom %= str_
Atom %= bool_
Atom %= id_
Atom %= Func_Call
Atom %= base_ + opar + Comma_Sep_Expr_List + cpar
Atom %= Vector_Initialization

#----------------------------------------------Declarations---------------------------------------------------------#

# Type Declarations
Type_Declaration %= type_ + id_ + Type_Params + ocurly + Type_Body + ccurly
Type_Declaration %= type_ + id_ + Type_Params + inherits_ + id_ + ocurly + Type_Body + ccurly
Type_Declaration %= type_ + id_ + Type_Params + inherits_ + id_ + opar + Comma_Sep_Expr_List + cpar + ocurly + Type_Body + ccurly

Type_Params %= G.Epsilon
Type_Params %= opar + Params_list + cpar

Params_list %= G.Epsilon
Params_list %= id_ + Possibly_Empty_Type
Params_list %= Params_list + comma + id_ + Possibly_Empty_Type

Type_Body %= G.Epsilon
Type_Body %= Type_Body + Attribute
Type_Body %= Type_Body + Method
Type_Body %= Attribute
Type_Body %= Method

Attribute %= id_ + Possibly_Empty_Type + eq + Line_Expression

Method %= id_ + opar + Params_list + cpar + Possibly_Empty_Type + arrow + Simple_Expression + semi
Method %= id_ + opar + Params_list + cpar + Possibly_Empty_Type + Expression_Block
Method %= id_ + opar + Params_list + cpar + Possibly_Empty_Type + Expression_Block + semi

# Function Declarations
Func_Declaration %= func_ + id_ + opar + Params_list + cpar + Possibly_Empty_Type + arrow + Simple_Expression + semi
Destructive_Operation %= func_ + id_ + opar + Params_list + cpar + Possibly_Empty_Type + Expression_Block
Destructive_Operation %= func_ + id_ + opar + Params_list + cpar + Possibly_Empty_Type + Expression_Block + semi

# Protocol Declarations
Protocol_Declaration %= protocol_ + id_ + ocurly + Protocol_Body + ccurly
Protocol_Declaration %= protocol_ + id_ + extends_ + id_ + ocurly + Protocol_Body + ccurly

Protocol_Body %= Protocol_Body + id_ + opar + Params_Typed + cpar + colon + Non_Empty_Type + semi
Protocol_Body %= id_ + opar + Params_Typed + cpar + colon + Non_Empty_Type + semi

Params_Typed %= G.Epsilon
Params_Typed %= Params_Typed + comma + id_ + colon + Non_Empty_Type
Params_Typed %= id_ + colon + Non_Empty_Type


#----------------------------------------------------End of Productions---------------------------------------------------

print(G)