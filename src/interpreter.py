from parser import *
from values import *


class Interpreter:
    # gagawa ng function based sa type na provided
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node):
        return NumOps(node.tok.value).set_pos(node.pos_start, node.pos_end)
    
    def visit_ListNode(self, node):
        res = ParserResult()
        statements = []
        print("Found program node!")
        for statement in node.statement_nodes:
            statements.append(res.register(self.visit(statement))) 

    def visit_NegationNode(self, node):
        node = self.visit(node.node)
        result = node.negation()

        print(result.value)
        return result.set_pos(node.pos_start, node.pos_end)

    
    # All nodes involving arithmetic operations
    def visit_ArithmeticNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        operand = node.op_tok.value

        if operand == "SUM OF":
            result = left.sum_of(right)
        elif operand == "DIFF OF":
            result = left.diff_of(right)
        elif operand == "PRODUKT OF":
            result = left.produkt_of(right)
        elif operand == "QUOSHUNT OF":
            result = left.quoshunt_of(right)
        elif operand == "MOD OF":
            result = left.mod_of(right)
        
        print(result.value)
        return result.set_pos(node.pos_start, node.pos_end)