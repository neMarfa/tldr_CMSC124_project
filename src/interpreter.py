from parser import *
from values import *
import lexer
from constants import *
import string_with_arrows


class Interpreter:
    def __init__(self, console_writer = None, input_writer = None):
        self.symbol_table = {}
        self.console_writer = console_writer
        self.input_writer = input_writer

    # gagawa ng function based sa type na provided
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node):
        return NumOps(node.tok.value).set_pos(node.pos_start, node.pos_end)

    def visit_BoolNode(self, node):
        # Convert WIN -> True, FAIL -> False
        bool_value = (node.tok.value == "WIN")
        return BoolOps(bool_value).set_pos(node.pos_start, node.pos_end)
    
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

        if isinstance(left.value, str):
            if left.value not in self.symbol_table:
                raise Exception(f"Cannot assign to undeclared variable '{var_name}'")
        

            stored = self.symbol_table[left.value]
            if isinstance(stored.value, int) or isinstance(stored.value, float):
                left = stored
            else:
                error_msg = f"Type Error: Cannot proceed with arithmetic operations on NON-NUMBR/NUMBAR types: {type(left).__name__} and {type(right).__name__}\n{node.pos_start.fn}, line {node.pos_start.ln+1}\n\n{string_with_arrows.string_with_arrows(node.pos_start.ftxt, node.pos_start, node.pos_end)}"
                raise Exception(error_msg)
        
        if isinstance(right.value, str):
            if right.value not in self.symbol_table:
                raise Exception(f"Cannot assign to undeclared variable '{var_name}'")
        
            stored = self.symbol_table[right.value]

            if isinstance(stored.value, int) or isinstance(stored.value, float):
                right = stored
            else:
                error_msg = f"Type Error: Cannot proceed with arithmetic operations on NON-NUMBR/NUMBAR types: {type(left).__name__} and {type(right).__name__}\n{node.pos_start.fn}, line {node.pos_start.ln+1}\n\n{string_with_arrows.string_with_arrows(node.pos_start.ftxt, node.pos_start, node.pos_end)}"
                raise Exception(error_msg)

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
        print(var_name)
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
        # print(f"Declared var: {var_name}\nValue: {value}")  # for checking

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
    
    # for user input
    # TODO:add value node
    def visit_GimmehNode(self, node):
        var_name = node.varident.value


        value = self.input_writer()

        print(type(node.varident.pos_end))

        string_tok = lexer.Token(TK_STRING, value, node.varident.pos_end, node.varident.pos_end)
        string = StringNode(string_tok)
        visited = self.visit_StringNode(string)

        self.symbol_table[var_name] = visited
        
        return value

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
        
        elif target_type == "TROOF":
            # cast to boolean
            if isinstance(value, NumOps):
                # Numbers: 0 = FAIL, non-zero = WIN
                return BoolOps(value.value != 0)
            elif isinstance(value, StringOps):
                # Strings: empty = FAIL, non-empty = WIN
                return BoolOps(len(value.value.strip()) > 0)
            elif isinstance(value, BoolOps):
                return value  # already boolean
            elif isinstance(value, NoobOps):
                return BoolOps(False)  # NOOB = FAIL
            return BoolOps(True)  # default to WIN for unknown types

        elif target_type == "NOOB":
            # cast to null
            return NoobOps()

        return value

    # If the operands are not TROOFs, they should be implicitly typecast
    def to_bool(self, value):
        if isinstance(value, BoolOps):
            return value.value
        elif isinstance(value, NumOps):
            return value.value != 0
        elif isinstance(value, StringOps):
            return len(value.value.strip()) > 0
        elif isinstance(value, NoobOps):
            return False
        return bool(value)  # fallback

    def visit_BooleanNode(self, node):
        op_type = node.op_tok.value

        if op_type == "NOT":
            # NOT operation
            operand = self.visit(node.left_node)
            bool_value = self.to_bool(operand)
            result = BoolOps(not bool_value)
        else:
            # Binary operations
            left = self.visit(node.left_node)
            right = self.visit(node.right_node)

            left_bool = self.to_bool(left)
            right_bool = self.to_bool(right)

            if op_type == "BOTH OF":
                result = BoolOps(left_bool and right_bool)  # AND
            elif op_type == "EITHER OF":
                result = BoolOps(left_bool or right_bool)   # OR
            elif op_type == "WON OF":
                result = BoolOps(left_bool ^ right_bool)    # XOR
            else:
                raise Exception(f"Unknown boolean operation: {op_type}")

        return result.set_pos(node.pos_start, node.pos_end)

    def visit_BooleanInfiniteNode(self, node):
        op_type = node.op_tok.value

        # Evaluate all operands to boolean values
        bool_operands = []
        for operand_node in node.operands:
            operand = self.visit(operand_node)
            bool_operands.append(self.to_bool(operand))

        if op_type == "ALL OF":
            # ALL OF = AND all operands
            result = all(bool_operands)
        elif op_type == "ANY OF":
            # ANY OF = OR all operands
            result = any(bool_operands)
        else:
            raise Exception(f"Unknown infinite boolean operation: {op_type}")

        bool_result = BoolOps(result)
        return bool_result.set_pos(node.pos_start, node.pos_end)

    def visit_ComparisonNode(self, node):
        op_type = node.op_tok.value

        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if op_type == "BOTH SAEM":
            # Equality comparison
            if type(left) != type(right):
                error_msg = f"Type Error: Cannot compare different types in BOTH SAEM: {type(left).__name__} and {type(right).__name__}\n{node.pos_start.fn}, line {node.pos_start.ln+1}\n\n{string_with_arrows.string_with_arrows(node.pos_start.ftxt, node.pos_start, node.pos_end)}"
                raise Exception(error_msg)
            result = self.equality_check(left, right)
            return BoolOps(result).set_pos(node.pos_start, node.pos_end)
        elif op_type == "DIFFRINT":
            # Inequality comparison
            if type(left) != type(right):
                error_msg = f"Type Error: Cannot compare different types in DIFFRINT: {type(left).__name__} and {type(right).__name__}\n{node.pos_start.fn}, line {node.pos_start.ln+1}\n\n{string_with_arrows.string_with_arrows(node.pos_start.ftxt, node.pos_start, node.pos_end)}"
                raise Exception(error_msg)
            result = not self.equality_check(left, right)
            return BoolOps(result).set_pos(node.pos_start, node.pos_end)
        elif op_type == "BIGGR OF":
            # Maximum operation
            return self.max_operation(left, right, node.pos_start, node.pos_end)
        elif op_type == "SMALLR OF":
            # Minimum operation
            return self.min_operation(left, right, node.pos_start, node.pos_end)
        else:
            raise Exception(f"Unknown comparison operation: {op_type}")

    def equality_check(self, left, right):
        if type(left) == type(right):
            return left.value == right.value

        # Different types are not equal
        return False

    def format_detailed_error(self, pos_start, pos_end, error_name, details):
        result = f'{error_name}: {details}'
        result += f'\n{pos_start.fn}, line {pos_start.ln+1}'
        result += '\n\n' + string_with_arrows.string_with_arrows(pos_start.ftxt, pos_start, pos_end)
        return result

    def max_operation(self, left, right, pos_start, pos_end):
        if type(left) != type(right):
            error_msg = f"Type Error: Cannot compare different types in BIGGR OF: {type(left).__name__} and {type(right).__name__}\n{pos_start.fn}, line {pos_start.ln+1}\n\n{string_with_arrows.string_with_arrows(pos_start.ftxt, pos_start, pos_end)}"
            raise Exception(error_msg)

        try:
            # Numbers: standard max
            if isinstance(left, NumOps):
                return NumOps(max(left.value, right.value)).set_pos(pos_start, pos_end)
            # Strings: lexicographic max
            elif isinstance(left, StringOps):
                return StringOps(max(left.value, right.value)).set_pos(pos_start, pos_end)
            # Booleans: True > False
            elif isinstance(left, BoolOps):
                result = BoolOps(True) if left.value else right
                return result.set_pos(pos_start, pos_end)
        except Exception as e:
            error_msg = self.format_detailed_error(pos_start, pos_end, "Runtime Error", f"Error in BIGGR OF operation: {e}")
            raise Exception(error_msg)

    def min_operation(self, left, right, pos_start, pos_end):
        if type(left) != type(right):
            error_msg = f"Type Error: Cannot compare different types in SMALLR OF: {type(left).__name__} and {type(right).__name__}\n{pos_start.fn}, line {pos_start.ln+1}\n\n{string_with_arrows.string_with_arrows(pos_start.ftxt, pos_start, pos_end)}"
            raise Exception(error_msg)

        try:
            # Numbers: standard min
            if isinstance(left, NumOps):
                return NumOps(min(left.value, right.value)).set_pos(pos_start, pos_end)
            # Strings: lexicographic min
            elif isinstance(left, StringOps):
                return StringOps(min(left.value, right.value)).set_pos(pos_start, pos_end)
            # Booleans: False < True
            elif isinstance(left, BoolOps):
                result = BoolOps(False) if not left.value else right
                return result.set_pos(pos_start, pos_end)
        except Exception as e:
            error_msg = self.format_detailed_error(pos_start, pos_end, "Runtime Error", f"Error in SMALLR OF operation: {e}")
