from abc import ABC
from typing import List, Tuple
from cmp.semantic import Scope
import cmp.visitor as visitor
from hulk.hulk_ast import *


class FormatVisitor:
    def __init__(self):
        self.ans = ""
        self.tabs = 0

    def increase_tabs(self):
        self.tabs += 2

    def decrease_tabs(self):
        self.tabs -= 2

    def add_ans(self, text):
        tb = " " * self.tabs
        self.ans += "\n" + tb + text

    @visitor.on("node")
    def visit(self, node: Node):
        self.ans += f"Node: {node.column} {node.line}"

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.add_ans(
            "<Program Node> col: " + str(node.column) + " line: " + str(node.line)
        )

        self.increase_tabs()
        for d in node.declarations:
            self.visit(d)
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(TypeDeclarationNode)
    def visit(self, node: TypeDeclarationNode):
        self.add_ans(
            "<Type Declaration Node> col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )
        self.increase_tabs()
        for i in node.attributes:
            self.visit(i)
        for i in node.methods:
            self.visit(i)
        self.decrease_tabs()

    @visitor.when(FunctionDeclarationNode)
    def visit(self, node: FunctionDeclarationNode):
        self.add_ans(
            "<Function Declaration Node> col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(ProtocolDeclarationNode)
    def visit(self, node: ProtocolDeclarationNode):
        self.add_ans(
            "<Protocol Declaration Node> col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )
        self.increase_tabs()
        for i in node.signatures:
            self.visit(i)
        self.decrease_tabs()

    @visitor.when(MethodNode)
    def visit(self, node: MethodNode):
        self.add_ans(
            "<Method Node> id "
            + node.identifier
            + " col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )

        self.increase_tabs()
        for i in node.params_ids:
            self.add_ans(f"Param: {i}")
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(AttributeNode)
    def visit(self, node: AttributeNode):
        self.add_ans(
            "<Attribute Node> id "
            + node.identifier
            + " col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(ProtocolMethodSignatureNode)
    def visit(self, node: ProtocolMethodSignatureNode):
        self.add_ans(
            "<Protocol Method Signature Node> id "
            + node.identifier
            + " col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )
        self.increase_tabs()
        for i in node.params_ids:
            self.add_ans(f"Param: {i}")
        self.decrease_tabs()

    @visitor.when(VectorNode)
    def visit(self, node: VectorNode):
        self.add_ans(
            "<Vector Node> col: " + str(node.column) + " line: " + str(node.line)
        )

    @visitor.when(VariableDeclarationNode)
    def visit(self, node: VariableDeclarationNode):
        self.add_ans(
            "<Variable Declaration Node> col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(ExpressionBlockNode)
    def visit(self, node: ExpressionBlockNode):
        self.add_ans(
            "<Expression Block Node> col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )
        self.increase_tabs()
        for i in node.expressions:
            self.visit(i)
        self.decrease_tabs()

    @visitor.when(LetInNode)
    def visit(self, node: LetInNode):
        self.add_ans(
            "<Let In Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        for i in node.assignment_list:
            self.visit(i)
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(IfElseNode)
    def visit(self, node: IfElseNode):
        self.add_ans(
            "<If Else Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        for i in range(len(node.conditions)):
            self.add_ans(f"Condition: {node.conditions[i]}")
            self.visit(node.expressions[i])
        self.visit(node.else_expression)
        self.decrease_tabs()

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode):
        self.add_ans(
            "<While Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(ForNode)
    def visit(self, node: ForNode):
        self.add_ans("<For Node> col: " + str(node.column) + " line: " + str(node.line))
        self.increase_tabs()
        self.visit(node.iterable_expression)
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(DestructiveOperationNode)
    def visit(self, node: DestructiveOperationNode):
        self.add_ans(
            "<Destructive Operation Node> col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(NewTypeNode)
    def visit(self, node: NewTypeNode):
        self.add_ans(
            "<New Type Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        for i in node.args:
            self.visit(i)
        self.decrease_tabs()

    @visitor.when(IsNode)
    def visit(self, node: IsNode):
        self.add_ans("<Is Node> col: " + str(node.column) + " line: " + str(node.line))
        self.increase_tabs()
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(AsNode)
    def visit(self, node: AsNode):
        self.add_ans("<As Node> col: " + str(node.column) + " line: " + str(node.line))
        self.increase_tabs()
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(FunctionCallNode)
    def visit(self, node: FunctionCallNode):
        self.add_ans(
            "<Function Call Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        for i in node.args:
            self.visit(i)
        self.decrease_tabs()

    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode):
        self.add_ans(
            "<Method Call Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        for i in node.args:
            self.visit(i)
        self.decrease_tabs()

    @visitor.when(AttributeCallNode)
    def visit(self, node: AttributeCallNode):
        self.add_ans(
            "<Attribute Call Node> col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.object)
        self.decrease_tabs()

    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode):
        self.add_ans(
            "<Base Call Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        for i in node.args:
            self.visit(i)
        self.decrease_tabs()

    @visitor.when(IndexNode)
    def visit(self, node: IndexNode):
        self.add_ans(
            "<Index Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.object)
        self.visit(node.index)
        self.decrease_tabs()

    @visitor.when(InitializeVectorNode)
    def visit(self, node: InitializeVectorNode):
        self.add_ans(
            "<Initialize Vector Node> col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )
        self.increase_tabs()
        for i in node.elements:
            self.visit(i)
        self.decrease_tabs()

    @visitor.when(InitializeVectorListComprehensionNode)
    def visit(self, node: InitializeVectorListComprehensionNode):
        self.add_ans(
            "<Initialize Vector List Comprehension Node> col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )
        self.visit(node.operation)
        self.add_ans(f"Variable Identifier: {node.variable_identifier}")
        self.increase_tabs()
        self.visit(node.iterable_expression)
        self.decrease_tabs()

    @visitor.when(NumNode)
    def visit(self, node: NumNode):
        self.add_ans("<Num Node> col: " + str(node.column) + " line: " + str(node.line))

    @visitor.when(StringNode)
    def visit(self, node: StringNode):
        self.add_ans(
            "<String Node> value"
            + str(node.lexeme)
            + " col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )

    @visitor.when(BoolNode)
    def visit(self, node: BoolNode):
        self.add_ans(
            "<Bool Node> value"
            + str(node.lexeme)
            + " col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )

    @visitor.when(IDNode)
    def visit(self, node: IDNode):
        self.add_ans(
            "<ID Node> id"
            + node.lexeme
            + " col: "
            + str(node.column)
            + " line: "
            + str(node.line)
        )

    @visitor.when(OrNode)
    def visit(self, node: OrNode):
        self.add_ans("<Or Node> col: " + str(node.column) + " line: " + str(node.line))
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(AndNode)
    def visit(self, node: AndNode):
        self.add_ans("<And Node> col: " + str(node.column) + " line: " + str(node.line))
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        self.add_ans(
            "<Equal Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(NonEqualNode)
    def visit(self, node: NonEqualNode):
        self.add_ans(
            "<Non Equal Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode):
        self.add_ans(
            "<Less Than Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(LessEqualNode)
    def visit(self, node: LessEqualNode):
        self.add_ans(
            "<Less Equal Node> col: " + str(node.column) + " line: " + str(node.line)
        )

        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode):
        self.add_ans(
            "<Greater Than Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(GreaterEqualNode)
    def visit(self, node: GreaterEqualNode):
        self.add_ans(
            "<Greater Equal Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode):
        self.add_ans(
            "<Concat Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(SpacedConcatNode)
    def visit(self, node: SpacedConcatNode):
        self.add_ans(
            "<Spaced Concat Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        self.add_ans(
            "<Plus Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        self.add_ans(
            "<Minus Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(StarNode)
    def visit(self, node: StarNode):
        self.add_ans(
            "<Star Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(DivNode)
    def visit(self, node: DivNode):
        self.add_ans("<Div Node> col: " + str(node.column) + " line: " + str(node.line))
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(ModNode)
    def visit(self, node: ModNode):
        self.add_ans("<Mod Node> col: " + str(node.column) + " line: " + str(node.line))
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(PowNode)
    def visit(self, node: PowNode):
        self.add_ans("<Pow Node> col: " + str(node.column) + " line: " + str(node.line))
        self.increase_tabs()
        self.visit(node.left_expression)
        self.visit(node.right_expression)
        self.decrease_tabs()

    @visitor.when(SignUnaryOpNode)
    def visit(self, node: SignUnaryOpNode):
        self.add_ans(
            "<Minus Node> col: " + str(node.column) + " line: " + str(node.line)
        )
        self.increase_tabs()
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(NotNode)
    def visit(self, node: NotNode):
        self.add_ans("<Not Node> col: " + str(node.column) + " line: " + str(node.line))
        self.increase_tabs()
        self.visit(node.expression)
        self.decrease_tabs()

    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode):
        self.add_ans("<ConstantNumNode> " + node.lexeme + " " + str(node.value))
