from parser import *
from values import *
import lexer
from constants import *
import string_with_arrows


class Interpreter:
    def __init__(self, console_writer = None, input_writer = None, param_name = None, param_value = None, isFunction = False):
        self.symbol_table = {}
        self.console_writer = console_writer
        self.input_writer = input_writer
        self.IT = NoobOps()  # implicit variable for statements
        
        self.ret = NoobOps()
        self.isFunction = isFunction
        if param_name is not None:
            for i in range(len(param_name)): 
                self.symbol_table[param_name[i]] =  param_value[i]
            


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
        for statement in node.statement_nodes:
            statements.append(res.register(self.visit(statement))) 

    def visit_NegationNode(self, node):
        node = self.visit(node.node)
        result = node.negation()

        print(result.value)
        return result.set_pos(node.pos_start, node.pos_end)

    def determine_type(self,data):
        if not checkFloat(data):
            var = data
            
        elif checkFloat(data) == "FLOAT": 
            var = NumOps(float(data))
        else:
            var = NumOps(int(data))  
        
        return var
    
    def implicit_cast(self, var):
        if var.value not in self.symbol_table:
            raise Exception(f"Cannot assign to undeclared variable '{var.value}'")
    
        stored = self.symbol_table[var.value]

        if isinstance(stored, NumOps):
            stored = self.symbol_table[var.value]
            var = stored


        if isinstance(stored, BoolOps):
            if stored.value == "WIN": 
                var = NumOps(1)
            else:
                var = NumOps(0)


        if isinstance(stored, StringOps):
            print(stored.value)
            var = self.determine_type(stored.value)
        
        return var

    # All nodes involving arithmetic operations
    def visit_ArithmeticNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        operand = node.op_tok.value
        

        if isinstance(left.value, str):
            left = self.implicit_cast(left)
        if isinstance(right.value, str):
            right = self.implicit_cast(right)

        if type(left) != type(right):
            error_msg = f"Type Error: Cannot proceed with arithmetic operations on NON-NUMBR/NUMBAR types: {type(left).__name__} and {type(right).__name__}\n{node.pos_start.fn}, line {node.pos_start.ln+1}\n\n{string_with_arrows.string_with_arrows(node.pos_start.ftxt, node.pos_start, node.pos_end)}"
            raise Exception(error_msg)     
         
        if isinstance(left.value, str):
            if operand == "BIGGR OF":
            # Maximum operation
                result = self.max_operation(left, right, node.pos_start, node.pos_end)
            elif operand == "SMALLR OF":
            # Minimum operation
                result = self.min_operation(left, right, node.pos_start, node.pos_end)
            else: 
                error_msg = f"Type Error: Cannot proceed with arithmetic operations on NON-NUMBR/NUMBAR types: {type(left).__name__} and {type(right).__name__}\n{node.pos_start.fn}, line {node.pos_start.ln+1}\n\n{string_with_arrows.string_with_arrows(node.pos_start.ftxt, node.pos_start, node.pos_end)}"
                raise Exception(error_msg)     
            print(result.value)
            self.IT = result  # set IT to the result
            return result.set_pos(node.pos_start, node.pos_end)
    
        if operand == "SUM OF":
            result = left.sum_of(right)
        elif operand == "DIFF OF":
            result = left.diff_of(right)
        elif operand == "PRODUKT OF":
            result = left.produkt_of(right)
        elif operand == "QUOSHUNT OF":
            if left.value == 0 and right.value == 0:
                error_msg = f"RUNTIME ERROR: DIVISION BY ZERO: {type(left).__name__} and {type(right).__name__}\n{node.pos_start.fn}, line {node.pos_start.ln+1}\n\n{string_with_arrows.string_with_arrows(node.pos_start.ftxt, node.pos_start, node.pos_end)}"
                raise Exception(error_msg)
            result = left.quoshunt_of(right)
        elif operand == "MOD OF":
            result = left.mod_of(right)
        elif operand == "BIGGR OF":
            # Maximum operation
            result = self.max_operation(left, right, node.pos_start, node.pos_end)
        elif operand == "SMALLR OF":
            # Minimum operation
            result = self.min_operation(left, right, node.pos_start, node.pos_end)
        
        print(result.value)
        self.IT = result  # set IT to the result
        return result.set_pos(node.pos_start, node.pos_end)
    
    def visit_StringNode(self, node):
        return StringOps(node.tok.value).set_pos(node.pos_start, node.pos_end)
    
    def visit_IdentifierNode(self, node):
        var_name = node.tok.value
        print(var_name)

        if var_name == "IT":
            return self.IT
        elif var_name not in self.symbol_table:
            raise Exception(f"Variable '{var_name}' is not defined.")
        
        self.IT = self.symbol_table[var_name]
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
    
    def visit_ConcatNode(self, node):
        result = []
        for expr in node.expressions:
            value = self.visit(expr)
            
            if isinstance(value, NumOps):
                result.append(str(value.value))
            elif isinstance(value, StringOps):
                result.append(value.value)
            elif isinstance(value, BoolOps):
                result.append("WIN" if value.value else "FAIL")
            elif isinstance(value, NoobOps):
                result.append("")
            else:
                result.append(str(value.value))
    
        joined = "".join(result)
        
        return StringOps(joined).set_pos(node.pos_start, node.pos_end)
    
    # for user input
    # TODO:add value node
    def visit_GimmehNode(self, node):
        var_name = node.varident.value


        value = self.input_writer()
        if len(value) == 0:
            visited = NoobOps()
            return visited

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
        
        if isinstance(value, BoolOps):
            # convert boolean to WIN/FAIL
            display_value = "WIN" if value.value else "FAIL"
        else:
            # for all other types, use their value
            display_value = str(value.value)
        
        output.append(display_value)
        
        # print spaces bet
        result = " ".join(output)
        
        if self.console_writer:
            if node.eos:
                self.console_writer(result)  # gui console
            else:
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
                    return NumOps(0)
            elif isinstance(value, BoolOps):
                if value.value == True:
                    return NumOps(1)
                else:
                    return NumOps(0)
            elif isinstance(value, NoobOps):
                return NumOps(0)
            else:
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
            elif isinstance(value, BoolOps):
                if value.value == True:
                    return NumOps(1.0)
                else:
                    return NumOps(0.0)
            elif isinstance(value, NoobOps):
                return NumOps(0.0)
            else:
                return NumOps(0.0)
        elif target_type == "YARN":
            if isinstance(value, BoolOps):
                if value.value == True:
                    return StringOps("WIN")
                else:
                    return StringOps("FAIL")
            else:
                return StringOps(str(value.value))
        elif target_type == "TROOF":
            if isinstance(value, NumOps):
                if value.value == 0:
                    return BoolOps(False)
                else:
                    return BoolOps(True)
            elif isinstance(value, StringOps):
                if value.value == "":
                    return BoolOps(False)
                else:
                    return BoolOps(True)
            elif isinstance(value, BoolOps):
                return value
            
            elif isinstance(value, NoobOps):
                return BoolOps(False)
            else:
                return BoolOps(True)
        elif target_type == "NOOB":
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

        self.IT = result  # set IT
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
        self.IT = bool_result  # set IT
        return bool_result.set_pos(node.pos_start, node.pos_end)

    def visit_ComparisonNode(self, node):
        op_type = node.op_tok.value

        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if isinstance(left.value, str):
            left = self.determine_type(left.value)
        if isinstance(right.value, str):
            right = self.determine_type(right.value)

        if op_type == "BOTH SAEM":
            # Equality comparison
            if type(left) != type(right):
                error_msg = f"Type Error: Cannot compare different types in BOTH SAEM: {type(left).__name__} and {type(right).__name__}\n{node.pos_start.fn}, line {node.pos_start.ln+1}\n\n{string_with_arrows.string_with_arrows(node.pos_start.ftxt, node.pos_start, node.pos_end)}"
                raise Exception(error_msg)
            result = self.equality_check(left, right)
            bool_result = BoolOps(result)
            self.IT = bool_result
            return bool_result.set_pos(node.pos_start, node.pos_end)
        elif op_type == "DIFFRINT":
            # Inequality comparison
            if type(left) != type(right):
                error_msg = f"Type Error: Cannot compare different types in DIFFRINT: {type(left).__name__} and {type(right).__name__}\n{node.pos_start.fn}, line {node.pos_start.ln+1}\n\n{string_with_arrows.string_with_arrows(node.pos_start.ftxt, node.pos_start, node.pos_end)}"
                raise Exception(error_msg)
            result = not self.equality_check(left, right)
            bool_result = BoolOps(result)
            self.IT = bool_result
            return bool_result.set_pos(node.pos_start, node.pos_end)

        else:
            raise Exception(f"Unknown comparison operation: {op_type}")

        self.IT = result  # set IT
        return result

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

    def visit_IfNode(self, node):
        if self.to_bool(self.IT):
            for stmt in node.if_statements:
                self.visit(stmt)
        else:
            for stmt in node.else_statements:
                self.visit(stmt)

    def visit_SwitchCaseNode(self, node):
        matched = False
        for case in node.statements:
            if isinstance(case, SwitchOMGNode):
                expected_value = self.visit(case.expression)
                if self.equality_check(self.IT, expected_value):
                    matched = True
                    for stmt in case.code:
                        self.visit(stmt)
                    break
            elif isinstance(case, SwitchOMGWTFNode):
                if not matched:
                    for stmt in case.code:
                        self.visit(stmt)
                    break

    def visit_BreakNode(self, node):
        return "stop"
        

    # Responsible for function declaration and assignment to the symbol table
    def visit_FunctionNode(self, node):
        function_name = node.start.node.function_name.value
        body = node.body
        parameters = [param_name.value for param_name in node.start.node.parameters]
        func_value = Function(function_name, body, parameters)
        self.symbol_table[function_name] = func_value
        return func_value
    """
    creates another interpreter which contains the symbols provided and are not able to access values
    from outside its scope.
    """
    def visit_Function(self, node, parameters):
        function_value = self.symbol_table[node.name]
        parameter_names = function_value.parameters
        if len(parameters) > len(parameter_names):
            error_msg = f"RUNTIME ERROR: too many arguments provided "
            raise Exception(error_msg) 

        if len(parameters) < len(parameter_names):
            error_msg = f"RUNTIME ERROR: too few arguments provided "
            raise Exception(error_msg) 

        parameter_values = parameters

        # For cases where expressions will be used so that they would be calculated
        for i in range(len(parameter_values)):
            parameter_values[i] = self.visit(parameter_values[i])

        func_inter = Interpreter(console_writer = self.console_writer, input_writer = self.input_writer, param_name = parameter_names, param_value = parameter_values, isFunction = True)

        # calculating each function
        for statement in node.body:
            res = func_inter.visit(statement)
            if res == "stop":
                break

        self.IT = func_inter.ret

        return parameter_values

    # Handles function calls
    def visit_CallNode(self, node):
        parameters = node.parameters

        if node.function_name.value not in self.symbol_table:
            raise Exception(f"Cannot call to undeclared function '{node.function_name.value}'")

        called = self.visit_Function(self.symbol_table[node.function_name.value], parameters)
        # called = called.copy()

    def visit_ReturnNode(self, node):
        print("helo")
        if not self.isFunction:
            error = RuntimeError(node.pos_start, node.pos_end, "Unable to return a value to a non-function ")
            raise Exception(error.as_string())

        self.ret = self.visit(node.expression.node)

        return "stop"

    def visit_LoopNode(self, node):
        variable = node.start.varident
        operation = node.start.operation.value
        clause = node.start.clause.value

        if variable.value not in self.symbol_table:
            raise Exception(f"Cannot proceed with undeclared variable '{variable.value}'")
        
        if not isinstance(self.symbol_table[variable.value], NumOps):
            error_msg = f"Type Error: Cannot proceed with loop on NON-NUMBR/NUMBAR types: line {variable.pos_start.ln+1}\n\n{string_with_arrows.string_with_arrows(variable.pos_start.ftxt, variable.pos_start, variable.pos_end)}"
            raise Exception(error_msg)
        count = 0
        while True:
            condition = self.visit(node.start.expression)
            print(condition.value)
            if condition.value == True and clause == "TIL": break
            if condition.value == False and clause == "WILE": break

            statements = self.visit(node.statements)
            if statements == "stop":
                break
            if operation == "UPPIN":
                self.symbol_table[variable.value].value += 1
            else:
                self.symbol_table[variable.value].value -= 1

            # case when infinite loops occur
            if count == 9999:
                error_msg = f"Infinite Loop on loop {node.start.label}"
                raise Exception(error_msg)
            print(self.symbol_table[variable.value].value)
            count += 1
        return None
