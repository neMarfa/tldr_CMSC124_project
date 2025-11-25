from parser import *
from values import *


class Interpreter:
    def __init__(self, console_writer = None):
        self.symbol_table = {}
        self.console_writer = console_writer

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
    
    def visit_StringNode(self, node):
        return StringOps(node.tok.value).set_pos(node.pos_start, node.pos_end)
    
    def visit_IdentifierNode(self, node):
        var_name = node.tok.value
        if var_name not in self.symbol_table:
            raise Exception(f"Variable '{var_name}' is not defined.")
        return self.symbol_table[var_name]
    
    def visit_VarDeclBlockNode(self, node):
        # visit each declaration in the block
        for decl in node.declarations:
            self.visit(decl)
        
        # return None or a special value
        return NoobOps()

    def visit_VarDeclNode(self, node):
        var_name = node.identifier_tok.value
        if node.value_node:
            value = self.visit(node.value_node)
        else:
            value = NoobOps()     # basically null siya
            print("Uninitialized")
        self.symbol_table[var_name] = value
        print(f"Declared var: {var_name}\nValue: {value}")  # for checking

        return value

    def visit_AssignmentNode(self, node):
        var_name = node.var_tok.value
        if var_name not in self.symbol_table:
            raise Exception(f"Cannot assign to undeclared variable '{var_name}'")
        
        value = self.visit(node.value_node)
        self.symbol_table[var_name] = value
        return value
    
    # handles typecast for MAEK
    def visit_TypeCastNode(self, node):
         value = self.visit(node.expr_node)
         desired_type = node.type_tok.value

         result = self.cast_value(value, desired_type)
         return result
    
    # handles typecast IS NOW A
    def visit_VarTypeCastNode(self, node):
        var_name = node.var_tok.value
        if var_name not in self.symbol_table:
            raise Exception(f"Cannot cast undeclared variable '{var_name}'")
        
        value = self.symbol_table[var_name]
        desired_type = node.type_tok.value

        result = self.cast_value(value, desired_type)
        self.symbol_table[var_name] = result
        
        return result
    
    def visit_PrintNode(self, node):
        output = []
        
        # eval each expression
        for expr in node.expressions:
            value = self.visit(expr)
            output.append(str(value.value))
        
        # print spaces bet
        result = " ".join(output)
        
        if self.console_writer:
            self.console_writer(result + "\n")  # gui console
        else:
            print(result)  
        
        return StringOps(result)

    def cast_value(self, value, target_type):
        if target_type == "NUMBR":
            # cast to integer
            if isinstance(value, NumOps):
                return NumOps(int(value.value))
            elif isinstance(value, StringOps):
                try:
                    return NumOps(int(value.value))
                except ValueError:
                    return NumOps(0)  # Default to 0 if conversion fails
            elif isinstance(value, NoobOps):
                return NumOps(0)
        
        elif target_type == "NUMBAR":
            # cast to float
            if isinstance(value, NumOps):
                return NumOps(float(value.value))
            elif isinstance(value, StringOps):
                try:
                    return NumOps(float(value.value))
                except ValueError:
                    return NumOps(0.0)
            elif isinstance(value, NoobOps):
                return NumOps(0.0)
        
        elif target_type == "YARN":
            # cast to string
            return StringOps(str(value.value))
        
        # TODO: for boolean
        # elif target_type == "TROOF":
        #     # cast to boolean
        
        elif target_type == "NOOB":
            # cast to null
            return NoobOps()
        
        return value
