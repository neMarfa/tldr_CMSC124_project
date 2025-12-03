from constants import *
from error import *

# Use comparison list from constants (same pattern as arithmetic)
comparison_ops = comparison

#################################
# INDIVIDUAL GRAMMAR ENTRIES FROM OUR DOCUMENT
#################################
"""
THESE CLASSES JUST PRINT OUT THE VALUES TO PRODUCE THE PARSE TREE NEEDED
"""


class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok.type}:{self.tok}'

class BoolNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

# WILL HOLD ALL THE STATEMENTS
class ListNode:
    def __init__(self, statement_nodes):
        self.statement_nodes = statement_nodes

    def __iter__(self):
        return iter(self.statement_nodes)

class KeywordNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end  

    def __repr__(self):
        return f'{self.tok}'

class NegationNode:        
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = op_tok.pos_start
        self.pos_end = node.pos_end
    
    def __repr__(self):
        return f'({self.op_tok, {self.node}})'


class ArithmeticOperationNode:
    def __init__(self,op_tok):
        self.op_tok = op_tok
        self.value = op_tok.value
        self.pos_start = op_tok.pos_start
    
    def __repr__(self):
        return f'{self.op_tok}'

class ArithmeticNode:
    def __init__(self,op_tok, left_node, separator_node, right_node):
        self.op_tok = op_tok 
        self.left_node = left_node
        self.right_node = right_node
        self.separator_node = separator_node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.left_node}, {self.separator_node}, {self.right_node})'

class LoopDeclarationNode:
    def __init__(self, op_tok, label, operation, varident, clause, expression):
        self.op_tok = op_tok
        self.label = label
        self.operation = operation
        self.varident = varident
        self.clause = clause
        self.expression = expression
        self.pos_start = op_tok.pos_start
        self.pos_end = expression.pos_end
    
    def __repr__(self):
        return f'{self.op_tok}, {self.label}, {self.operation}, {self.varident}, {self.expression}'

class LoopEndNode:
    def __init__(self, end_tok, label):
        self.end_tok = end_tok
        self.label = label
        self.pos_start = end_tok.pos_start
        self.pos_end = label.pos_end

    def __repr__(self):
        return f'{self.end_tok}, {self.label}'

class LoopNode:
    def __init__(self, start, statements, end):
        self.start = start
        self.statements = statements
        self.end = end
        self.pos_start = start.pos_start
        self.pos_end = end.pos_end
    
    def __repr__(self):
        return f'{self.start}, {self.statements}, {self.end}'

class BreakNode:
    def __init__(self, tok, pos_start, pos_end):
        self.tok = tok
        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def __repr__(self):
        return f'{self.tok}'

class IdentifierNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    
    def __repr__(self):
        return f'{self.tok}'

class StringNode: 
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    
    def __repr__(self):
        return f'YARN:{self.tok}'
    
class PrintNode: 
    def __init__(self, keyword_tok, expressions, eos=False):
        self.keyword_tok = keyword_tok
        self.expressions = expressions
        self.eos = eos
        
        self.pos_start = keyword_tok.pos_start
        if expressions:
            self.pos_end = expressions[-1].pos_end if hasattr(expressions[-1], 'pos_end') else keyword_tok.pos_end
        else:
            self.pos_end = keyword_tok.pos_end

    def __repr__(self):
        mark = "!" if self.eos else ""
        return f'(VISIBLE, {", ".join(str(expr) for expr in self.expressions)}{mark})'
class VarDeclBlockNode:
    def __init__(self, wazzup_tok, declarations, buhbye_tok):
        self.wazzup_tok = wazzup_tok
        self.declarations = declarations 
        self.buhbye_tok = buhbye_tok
        self.pos_start = wazzup_tok.pos_start
        self.pos_end = buhbye_tok.pos_end
    
    def __repr__(self):
        return f'(WAZZUP, {self.declarations}, BUHBYE)'

class VarDeclNode:
    def __init__(self, keyword_tok, identifier_tok, assignment_tok=None, value_node=None):
        self.keyword_tok = keyword_tok
        self.identifier_tok = identifier_tok
        self.assignment_tok = assignment_tok
        self.value_node = value_node
    
    def __repr__(self):
        if self.assignment_tok and self.value_node:
            return f'(I HAS A, {self.identifier_tok}, {self.assignment_tok}, {self.value_node})'
        return f'(I HAS A, {self.identifier_tok})'

class ConcatNode:
    def __init__(self, keyword, expressions):
        self.keyword = keyword
        self.expressions = expressions
        self.pos_start = keyword.pos_start
        if expressions:
            self.pos_end = expressions[-1].pos_end
        else:
            self.pos_end = keyword.pos_end
    def __repr__(self):
        return f'(SMOOSH, {", ".join(str(expr) for expr in self.expressions)})'

class GimmehNode:
    def __init__(self, keyword, varident, val):
        self.keyword_tok = keyword
        self.varident = varident
        self.pos_start = keyword.pos_start
        self.pos_end = varident.pos_end
    
    def __rzepr__(self):
        return f'({self.keyword_tok}, {self.varident})'


class ComparisonNode:
    def __init__(self, op_tok, left_node, separator_node, right_node):
        self.op_tok = op_tok 
        self.left_node = left_node
        self.right_node = right_node
        self.separator_node = separator_node
        self.pos_start = op_tok.pos_start
        self.pos_end = right_node.pos_end
    
    def __repr__(self):
        return f'({self.op_tok}, {self.left_node}, {self.separator_node}, {self.right_node})'

class TypeCastNode:
    def __init__(self, maek_tok, expr_node, type_tok):
        self.maek_tok = maek_tok
        self.expr_node = expr_node
        self.type_tok = type_tok
        self.pos_start = maek_tok.pos_start
        self.pos_end = type_tok.pos_end
    
    def __repr__(self):
        return f'(MAEK, {self.expr_node}, A, {self.type_tok})'
    
class VarTypeCastNode:
    def __init__(self, var_tok, is_now_a_tok, type_tok):
        self.var_tok = var_tok
        self.is_now_a_tok = is_now_a_tok
        self.type_tok = type_tok
        self.pos_start = var_tok.pos_start
        self.pos_end = type_tok.pos_end
    
    def __repr__(self):
        return f'({self.var_tok}, IS NOW A, {self.type_tok})'
    
class AssignmentNode:
    def __init__(self, var_tok, r_tok, value_node):
        self.var_tok = var_tok
        self.r_tok = r_tok
        self.value_node = value_node
        self.pos_start = var_tok.pos_start
        self.pos_end = value_node.pos_end
    
    def __repr__(self):
        return f'({self.var_tok}, R, {self.value_node})'
    
class SwitchCaseNode:
    def __init__(self, start, statements, end):
        self.start = start
        self.statements = statements
        self.end = end
        self.pos_start = start.pos_start
        self.pos_end = end.pos_end
    
    def __repr__(self):
        return f'({self.start}, {self.statements}, {self.end})'

class SwitchOMGNode:
    def __init__(self, start, expression, code):
        self.start = start
        self.expression = expression
        self.code = code
        self.pos_start = start.pos_start

    def __repr__(self):
        return f'({self.start}, {self.expression}, {self.code})'

class SwitchOMGWTFNode:
    def __init__(self, start, code):
        self.start = start
        self.code = code
        self.pos_start = start.pos_start
    def __repr__(self):
        return f'({self.start}, {self.code})'

class BooleanNode:
    def __init__(self, op_tok, left_node, right_node=None):
        self.op_tok = op_tok
        self.left_node = left_node
        self.right_node = right_node  # None for NOT operation
        self.pos_start = op_tok.pos_start
        self.pos_end = (right_node.pos_end if right_node else left_node.pos_end)

    def __repr__(self):
        if self.right_node:
            return f'({self.op_tok}, {self.left_node}, {self.right_node})'
        return f'({self.op_tok}, {self.left_node})'

class BooleanInfiniteNode:
    def __init__(self, op_tok, operands, end_tok):
        self.op_tok = op_tok  # ALL OF or ANY OF
        self.operands = operands  # List of expressions
        self.end_tok = end_tok  # MKAY token
        self.pos_start = op_tok.pos_start
        self.pos_end = end_tok.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.operands})'

class IfNode:
    def __init__(self, if_statements, else_statements, pos_start, pos_end):
        self.if_statements = if_statements
        self.else_statements = else_statements
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'(IF: {self.if_statements}, ELSE: {self.else_statements})'


# TODO: Update pos_end
class FunctionDefinitionNode:
    def __init__(self, op_tok, function_name, parameters):
        self.op_tok = op_tok
        self.function_name = function_name
        self.parameters = parameters

        self.pos_start = op_tok.pos_start
        self.pos_end = function_name.pos_end

class FunctionNode:
    def __init__(self, start, body, end):
        self.start = start
        self.body = body
        self.end = end

        self.pos_start = start.node.pos_start
        self.pos_end = end.pos_end

class CallNode:
    def __init__(self, op_tok, function_name, parameters):
        self.op_tok = op_tok
        self.function_name = function_name
        self.parameters = parameters

        self.pos_start = op_tok.pos_start
        self.pos_end = function_name.pos_end

class ReturnNode:
    def __init__(self, expression, pos_start, pos_end):
        self.expression = expression
        self.pos_start = pos_start
        self.pos_end = pos_end
    
#################################
# RESULT
#################################
class ParserResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register(self, res):
        if isinstance(res, ParserResult):
            if res.error: self.error = res.error
            return res.node
            
        return res
    
    def success(self, node):
        self.node = node
        return self
    
    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

#################################
# PARSER/CREATES THE TEE
#################################

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.tok_idx = 0 #index
        self.current_tok = self.tokens[0]
        self.previous_tok = self.tokens[0]
    
    # MOVING TO NEXT INDEX
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
            self.previous_tok = self.tokens[self.tok_idx-1]
        return self.current_tok


    # TODO:make possible not only for arithmetic operations
    def parse(self):
        # print(self.tokens)
        res = self.statements()
        return res  


    # contains all the functions to be parsed, data handling will be considered at a later date
    def statements(self):
        res = ParserResult()
        tok = self.current_tok
        # final_tok = self.tokens[-2]
        # newline_check = self.tokens[-3]
        
        statements = []
        while self.current_tok.value != "HAI":
            if self.current_tok.value == "HOW IZ I":
                func = self.function()
                if func.error: return func
                statements.append(func.node)

            while self.current_tok.type == TK_NEWLINE:
                res.register(self.advance())
            
            if self.current_tok.value not in  ["HAI","HOW IZ I"]:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'HAI' "))


        pos_start = self.current_tok.pos_start.copy()
        
        # checks if the first character in the list of tokens is the start of program character
        if self.current_tok.value != "HAI":
            if self.current_tok.value != "BTW":
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'HAI' "))
        res.register(self.advance())

        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))

        res.register(self.advance())
                
        # skip initial newlines
        while self.current_tok.type == TK_NEWLINE:
            res.register(self.advance())

        # check for var declaration block using both value AND type
        if self.current_tok.value != "WAZZUP" and self.current_tok.type != "Variable Declaration Block Start":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'WAZZUP' after 'HAI' for variable declarations"))

        var_block = self.var_decl_block()
        if var_block.error:
            return var_block
        statements.append(var_block.node)

        # skip newlines after BUHBYE
        while self.current_tok.type == TK_NEWLINE:
            res.register(self.advance())

        KTHXBYE_count = 0
        # parse statements until we hit KTHXBYE
        while self.current_tok.value != "KTHXBYE":
            # print(self.current_tok)

            err = self.statement_section(statements)
            if err != None: return err
            
            if self.current_tok.value == "HAI":
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Unexpected 'HAI' "))

            # skip newlines between statements
            while self.current_tok.type == TK_NEWLINE:
                res.register(self.advance())

            if self.current_tok.type == TK_EOF:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'KTHXBYE' "))
                break
        else:
            if self.previous_tok.type != TK_NEWLINE:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))
            res.register(self.advance())
            KTHXBYE_count += 1
            
        while self.current_tok.type != TK_EOF:
            if self.current_tok.value == "KTHXBYE":
               return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Unexpected 'KTHXBYE' "))

            if self.current_tok.type == TK_EOF:
                break

            if self.current_tok.value == "HOW IZ I":
                func = self.function()
                if func.error: return func
                statements.insert(0, func.node)

            while self.current_tok.type == TK_NEWLINE:
                res.register(self.advance())
                
            if self.current_tok.value not in ["EOF","HOW IZ I"]:
                name = "unexpected '" + str(self.current_tok.value) + "' "
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, name))


        return res.success(ListNode(statements))

    # PLACE ALL THE STATEMENTS HERE, WILL BE REUSED IN FUNCTIONS AND LOOPS
    def statement_section(self, statements):
        res = ParserResult()

        # skip any leading newlines
        while self.current_tok.type == TK_NEWLINE:
            res.register(self.advance())
        
        # check if we've reached the end
        if self.current_tok.value == "KTHXBYE":
            return None
        
        # check for same-line VISIBLE !!!
        if statements and self.current_tok.type == "Output Keyword":
            last_stmt = statements[-1]
            
            # check if last statement was a VISIBLE
            if type(last_stmt).__name__ == 'PrintNode':
                # check if they're on the same line
                if hasattr(last_stmt, 'pos_end') and hasattr(self.current_tok, 'pos_start'):
                    if self.current_tok.pos_start.ln == last_stmt.pos_end.ln:
                        return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Multiple VISIBLE statements on same line not allowed"))

        if self.current_tok.type == "Output Keyword":
            print_stmt = self.print_statement()
            if print_stmt.error: return print_stmt
            statements.append(print_stmt.node)

        elif self.current_tok.value in arithmetic:
            arith = self.arithmetic_expr()
            if arith.error: return arith
            if self.current_tok.type != TK_NEWLINE:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))
            statements.append(arith.node)

        elif self.current_tok.value == "IM IN YR":
            loop = self.loop()
            if loop.error: return loop
            statements.append(loop.node)
        
        elif self.current_tok.value == "MAEK":
            typecast = self.typecast_maek()
            if typecast.error: return typecast
            statements.append(typecast.node)

        elif self.current_tok.value == "GIMMEH":
            gimmeh = self.input()
            if gimmeh.error: return gimmeh
            statements.append(gimmeh.node)

        elif self.current_tok.value == "I IZ":
            call = self.func_call()
            if call.error: return call
            statements.append(call.node)

        elif self.current_tok.value == "FOUND YR":
            ret = self.return_expressions()
            if ret.error: return ret
            if self.current_tok.type != TK_NEWLINE:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))
            statements.append(ret.node)

        elif self.current_tok.value == "HOW IZ I":
            func = self.function()
            if func.error: return func
            statements.append(func.node)
        
        elif self.current_tok.value == "SMOOSH" and self.current_tok.type == "Concatenation Keyword":
            concat = self.concat()
            if concat.error:
                return concat
            if self.current_tok.type != TK_NEWLINE:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))
            statements.append(concat.node)

        elif self.current_tok.type == "varident":
            # try to extend and see if it's assignment (R) or typecast (IS NOW A)
            next_idx = self.tok_idx + 1
            if next_idx < len(self.tokens):
                next_tok = self.tokens[next_idx]
                
                if next_tok.value == "R":
                    # assignment
                    assign = self.assignment()
                    if assign.error: return assign
                    if self.current_tok.type != TK_NEWLINE:
                        return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))                   

                    statements.append(assign.node)
                elif next_tok.value == "IS NOW A":
                    # typecast
                    typecast = self.typecast_is_now_a()
                    if typecast.error: return typecast
                    if self.current_tok.type != TK_NEWLINE:
                        return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))
                    statements.append(typecast.node)
                else:
                    # # just a variable reference (skip for now)
                    # res.register(self.advance())
                    # lone variable reference - treat as expression
                    expr = self.expression()
                    if expr.error: return expr
                    if self.current_tok.type != TK_NEWLINE:
                        return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))
                    statements.append(expr.node)

        elif self.current_tok.value == "WTF?":
            switch = self.switch_case()
            if switch.error: return switch
            if self.current_tok.type != TK_NEWLINE:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))
            statements.append(switch.node)

        elif self.current_tok.value == "GTFO":
            tok = self.current_tok
            res.register(self.advance())
            if self.current_tok.type != TK_NEWLINE:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))
            statements.append(BreakNode(tok, tok.pos_start, tok.pos_end))

        elif self.current_tok.value == "O RLY?":
            if_stmt = self.if_statement()
            if if_stmt.error: return if_stmt
            if self.current_tok.type != TK_NEWLINE:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))
            statements.append(if_stmt.node)

        elif self.current_tok.value == "YA RLY":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "YA RLY must be within O RLY? block - "))

        elif self.current_tok.value == "NO WAI":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "NO WAI must be within O RLY? block - "))

        elif self.current_tok.value == "OIC":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "OIC must be within O RLY? or WTF? block - "))
        
        elif self.current_tok.value == "IM OUTTA YR":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "IM OUTTA YR must close a IM IN YR block - "))

        elif self.current_tok.value == "IF U SAY SO":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "IF U SAY SO must close a HOW IZ I block - "))

        elif self.current_tok.value == "MKAY":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "MKAY must pair with an expression or a function call - "))

        else:
            # Parse expression statement
            expr = self.expression()
            if expr.error: return expr
            if self.current_tok.type != TK_NEWLINE:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))
            statements.append(expr.node)

   
        
    # ========== END OF REPLACED METHODS ==========


    def delimiter_values(self):
        res = ParserResult()
        tok = self.current_tok
        if tok.type == TK_DELIMITER:
            res.register(self.advance())
            return res.success(KeywordNode(tok))
        
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected 'AN' "))
 
    
    # HANDLES ANYTHING INVOLVING NUMBERS
    def arithmetic_values(self):
        res = ParserResult()
        tok = self.current_tok

        if tok.type in (TK_INT, TK_FLOAT, "varident"):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        # case for boolean expressions
        elif tok.type == TK_BOOL:
            if tok.value == "WIN":
                tok.value = 1
            else:
                tok.value = 0
            res.register(self.advance())
            return res.success(NumberNode(tok))

        # case when it is a string but it is a integer
        elif tok.type == TK_STRING_DELIMITER:
            res.register(self.advance())
            num = self.current_tok
            print(num)
            if not checkFloat(num.value):
                return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected Typecastable String Value "))

            elif checkFloat(num.value) == "FLOAT":
                num.value = float(num.value)
            else:
                num.value = int(num.value)

            res.register(self.advance())
            res.register(self.advance())

            print(self.current_tok)
            return res.success(NumberNode(num))


        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected NUMBR or NUMBAR "))

    # SUM OF, MOD OF, ETC
    def arithmetic_ops(self):
        res = ParserResult()
        tok = self.current_tok 
        if tok.value in arithmetic:
            res.register(self.advance())
            return res.success(ArithmeticOperationNode(tok))
        
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected Arithmetic Operation "))

    # handles negative values
    def negation_op(self):
        res = ParserResult()
        neg_tok = self.current_tok
        if neg_tok.type == TK_NEG:
            res.register(self.advance())
            if self.current_tok.type == TK_NEG:
                right = res.register(self.negation_op())
            else:
                right = res.register(self.arithmetic_values())
            if res.error: return right
            return res.success(NegationNode(neg_tok, right))
        
        return res.failure(InvalidSyntaxError(neg_tok.pos_start, neg_tok.pos_end, "Expected '-'"))


    # WHERE THE ARITHMETIC PARSE TREE BEGINS
    def arithmetic_expr(self):
        res = ParserResult()

        start = res.register(self.arithmetic_ops())
        if res.error: return res


        # handles nested operations on the left side
        if self.current_tok.value in arithmetic:
            left = res.register(self.arithmetic_expr())
        elif self.current_tok.type == TK_NEG:
            left = res.register(self.negation_op())
        else:
            left = res.register(self.arithmetic_values())

        if res.error: return res

        # Checks for the delimiter AN
        delimiter = res.register(self.delimiter_values())
        if res.error: return res
        
        # Handles nested operations on the right side 
        if self.current_tok.value in arithmetic:
            right = res.register(self.arithmetic_expr())
        elif self.current_tok.type == TK_NEG:
            right = res.register(self.negation_op())
        else:
            right = res.register(self.arithmetic_values())
        if res.error: return res
   
        start = ArithmeticNode(start, left, delimiter, right)

        return res.success(start)
    
    def comparison_expr(self):
        res = ParserResult()
        
        # Check if it's a comparison operator (BOTH SAEM, DIFFRINT) or comparison operation (BIGGR OF, SMALLR OF)
        if self.current_tok.value not in ("BOTH SAEM", "DIFFRINT"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, 
                self.current_tok.pos_end, 
                "Expected 'BOTH SAEM', 'DIFFRINT', 'BIGGR OF', or 'SMALLR OF'"
            ))
        
        op_tok = self.current_tok
        res.register(self.advance())
        
        # Parse left expression (can be arithmetic, identifier, nested comparisons, etc.)
        left = res.register(self.expression())
        if res.error: return res
        
        # Check for AN delimiter
        delimiter = res.register(self.delimiter_values())
        if res.error: return res
        
        # Parse right expression
        right = res.register(self.expression())
        if res.error: return res
        
        return res.success(ComparisonNode(op_tok, left, delimiter, right))

    def boolean_expr(self):
        res = ParserResult()

        # Handle NOT 
        if self.current_tok.value == "NOT":
            op_tok = self.current_tok
            res.register(self.advance())

            operand = res.register(self.expression())
            if res.error: return res

            return res.success(BooleanNode(op_tok, operand))

        # Handle infinite arity operators (ALL OF, ANY OF)
        if self.current_tok.value in ("ALL OF", "ANY OF"):
            op_tok = self.current_tok
            res.register(self.advance())

            operands = []

            # Parse first operand
            expr = res.register(self.expression())
            if res.error: return res
            operands.append(expr)

            # Parse additional operands separated by AN
            while self.current_tok.type == TK_DELIMITER:
                res.register(self.advance())  # Skip AN
                expr = res.register(self.expression())
                if res.error: return res
                operands.append(expr)

            # Check for MKAY terminator
            if self.current_tok.value != "MKAY":
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'MKAY'"
                ))

            end_tok = self.current_tok
            res.register(self.advance())

            return res.success(BooleanInfiniteNode(op_tok, operands, end_tok))

        # Handle binary boolean operators (BOTH OF, EITHER OF, WON OF)
        if self.current_tok.value in ("BOTH OF", "EITHER OF", "WON OF"):
            op_tok = self.current_tok
            res.register(self.advance())

            # Parse left operand
            left = res.register(self.expression())
            if res.error: return res

            # Check for AN delimiter
            if self.current_tok.type != TK_DELIMITER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected 'AN'"
                ))

            res.register(self.advance())

            # Parse right operand
            right = res.register(self.expression())
            if res.error: return res

            return res.success(BooleanNode(op_tok, left, right))

        return res.failure(InvalidSyntaxError(
            self.current_tok.pos_start,
            self.current_tok.pos_end,
            "Expected boolean operator"
        ))

    def print_statement(self):
        # format: VISIBLE <expression> [AN|+ <expression>]* [!]
        res = ParserResult()
        tok = self.current_tok
        
        if tok.type != "Output Keyword":
            return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected 'VISIBLE'"))
        
        res.register(self.advance())
        
        expressions = []
        
        expr = res.register(self.expression())
        if res.error: return res
        expressions.append(expr)
        
        # after_first_expr = self.current_tok
        
        # parse additional expressions ONLY if separated by AN, +, or SMOOSH
        while self.current_tok and (self.current_tok.type == TK_DELIMITER or self.current_tok.type == TK_CONCAT or self.current_tok.type == "Concatenation Keyword"):   
            res.register(self.advance())
            expr = res.register(self.expression())
            if res.error: return res
            expressions.append(expr)
        
        expression_starters = [
        "varident",           # variables
        TK_STRING_DELIMITER,  # strings
        TK_INT,               # numbers
        TK_FLOAT,             # floats
        TK_BOOL,              # WIN/FAIL
        "Concatenation Keyword",  # SMOOSH
        ]
        
        expression_starter_keywords = [
            "MAEK",           # typecast
            "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF",  # arithmetic
            "BIGGR OF", "SMALLR OF",  # comparison operations
            "BOTH SAEM", "DIFFRINT",  # comparison operators
            "NOT", "BOTH OF", "EITHER OF", "WON OF", "ALL OF", "ANY OF",  # boolean
        ]
        
        if self.current_tok:
            if self.current_tok.type in expression_starters:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Multiple expressions in VISIBLE must be separated by '+' or 'AN'"
                ))
            
            if self.current_tok.value in expression_starter_keywords:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Multiple expressions in VISIBLE must be separated by '+' or 'AN'"
                ))
            
        suppress_newline = False
        if self.current_tok and self.current_tok.type == TK_EOS:
            suppress_newline = True
            res.register(self.advance())
        
        return res.success(PrintNode(tok, expressions, suppress_newline))

    def var_decl_block(self):
        res = ParserResult()
        # check both value and type
        if self.current_tok.value != "WAZZUP" and self.current_tok.type != "Variable Declaration Block Start":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'WAZZUP'"))
        
        # else, continue 
        wazzup_tok = self.current_tok
        res.register(self.advance())

        # checkif there is newline after wazzup 
        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after WAZZUP"))
    
        res.register(self.advance())

        # skip any extra newlines
        while self.current_tok.type == TK_NEWLINE:
            res.register(self.advance())

        declarations = []   # initialize empty list (to be occupied by var declarations)
        while self.current_tok.value != "BUHBYE" and self.current_tok.type != "Variable Declaration Block End":
            while self.current_tok.type == TK_NEWLINE:
                res.register(self.advance())
            
            if self.current_tok.value == "BUHBYE" or self.current_tok.type == "Variable Declaration Block End":
                break

            if self.current_tok.type == "Variable Declaration":
                var_decl = self.var_declaration()
                if var_decl.error:
                    return var_decl
                declarations.append(var_decl.node)
            else: 
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected variable declaration (I HAS A) or BUHBYE"))

        # assume that we're at the end of the wazzup code/ var block
        if self.current_tok.value != "BUHBYE" and self.current_tok.type != "Variable Declaration Block End":
               return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'BUHBYE'"))

        buhbye_tok = self.current_tok
        res.register(self.advance())
        return res.success(VarDeclBlockNode(wazzup_tok, declarations, buhbye_tok))
    
    def var_declaration(self):
        # format: I HAS A <identifier> [ITZ <expression>]
        res = ParserResult()
        tok = self.current_tok
        
        if tok.type != "Variable Declaration":
            return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected 'I HAS A'"))
        
        res.register(self.advance())
        
        if self.current_tok.type != "varident":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))
        
        identifier_tok = self.current_tok
        res.register(self.advance())
        
        if self.current_tok and self.current_tok.type == "Variable Assignment":
            assignment_tok = self.current_tok
            res.register(self.advance())
            
            value = res.register(self.expression())
            if res.error: return res
            
            return res.success(VarDeclNode(tok, identifier_tok, assignment_tok, value))
        
        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))

        return res.success(VarDeclNode(tok, identifier_tok))
    
    def concat(self):
        res = ParserResult()
        tok = self.current_tok

        if tok.type != "Concatenation Keyword":
            return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected 'SMOOSH'"))
        
        res.register(self.advance())
        
        expressions = []
        
        expr = res.register(self.expression())
        if res.error: 
            return res
        expressions.append(expr)
        
        # basically extends as long as there is a delimiter in the current statement
        while self.current_tok and self.current_tok.type == TK_DELIMITER:   
            res.register(self.advance())
            expr = res.register(self.expression())
            if res.error: 
                return res
            expressions.append(expr)
        if self.current_tok.type == "Operation End" or self.current_tok.value == "MKAY":
            res.register(self.advance())
        return res.success(ConcatNode(tok, expressions))

    def typecast_maek(self):
        res = ParserResult()
        maek_tok = self.current_tok

        if maek_tok.value != "MAEK":
            return res.failure(InvalidSyntaxError(maek_tok.pos_start, maek_tok.pos_end, "Expected 'MAEK'"))
    
        res.register(self.advance())
        
        # parse the expression to cast
        expr = res.register(self.expression())
        if res.error: return res
        
        # expect A
        if self.current_tok.value == "A":
            # return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'A'"))
            res.register(self.advance())
        # res.register(self.advance())
        
        # expect type (NUMBR, NUMBAR, YARN, TROOF, NOOB)
        type_tok = self.current_tok
        if type_tok.value not in ("NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"):
            return res.failure(InvalidSyntaxError(type_tok.pos_start, type_tok.pos_end, "Expected type (NUMBR, NUMBAR, YARN, TROOF, NOOB)"))
        
        res.register(self.advance())
        
        return res.success(TypeCastNode(maek_tok, expr, type_tok))

    def typecast_is_now_a(self):
        res = ParserResult()
        var_tok = self.current_tok  

        if var_tok.type != "varident":
            return res.failure(InvalidSyntaxError(var_tok.pos_start, var_tok.pos_end, "Expected variable identifier"))
        
        res.register(self.advance())
        
        # expect IS NOW A
        is_now_a_tok = self.current_tok  
        if is_now_a_tok.value != "IS NOW A":
            return res.failure(InvalidSyntaxError(is_now_a_tok.pos_start, is_now_a_tok.pos_end, "Expected 'IS NOW A'"))
        
        res.register(self.advance())
        
        # expect type
        type_tok = self.current_tok
        if type_tok.value not in ("NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"):
            return res.failure(InvalidSyntaxError(type_tok.pos_start, type_tok.pos_end, "Expected type (NUMBR, NUMBAR, YARN, TROOF, NOOB)"))
        
        res.register(self.advance())
        
        return res.success(VarTypeCastNode(var_tok, is_now_a_tok, type_tok))

    def typecast_r_maek(self):
        res = ParserResult()
        tok = self.current_tok

        if tok.value != "MAEK":
            return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected 'MAEK'"))

        res.register(self.advance())
        expr = res.register(self.expression())
        if res.error:
            return res

        if self.current_tok.value == "A":
            res.register(self.advance())

        type_tok = self.current_tok
        if type_tok.value not in ("NUMBR", "NUMBAR", "YARN", "NOOB", "TROOF"):
            return res.failure(InvalidSyntaxError(type_tok.pos_start, type_tok.pos_end, "Expected 'MAEK'"))
        
        res.register(self.advance())
        return res.success(TypeCastNode(tok, expr, type_tok))


    def assignment(self):
        res = ParserResult()
        tok = self.current_tok

        if tok.type != "varident":
            return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected variable identifier"))
        
        res.register(self.advance())
    
        # expect R
        r_tok = self.current_tok
        if r_tok.value != "R":
            return res.failure(InvalidSyntaxError(r_tok.pos_start, r_tok.pos_end, "Expected 'R'"))
        
        res.register(self.advance())
        
        # check if it's R MAEK
        if self.current_tok.value == "MAEK":
            typecast = res.register(self.typecast_r_maek())
            if res.error:
                return res
            return res.success(AssignmentNode(tok, r_tok, typecast))
        else:
            # regular assignment 
            value = res.register(self.expression())
            if res.error: return res
        
        return res.success(AssignmentNode(tok, r_tok, value))

    
    def input(self):
        res = ParserResult()
        tok = self.current_tok
        res.register(self.advance())
        varident = self.current_tok

        if varident.type != "varident":
            return res.failure(InvalidSyntaxError(varident.pos_start, varident.pos_end, "Expected variable identifier "))
        res.register(self.advance())

        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))

        return res.success(GimmehNode(tok, varident, varident.value))
        

# used for the loop_declaration part
# TODO: ADD CONDITIONAL OPERATORS
    def loop_declaration(self):
        res = ParserResult()
        declaration = self.current_tok 

        if declaration.value != "IM IN YR":
            return res.failure(InvalidSyntaxError(declaration.pos_start, declaration.pos_end, "Expected Function Declaration 'IM IN YR'"))
        
        res.register(self.advance())

        label = self.current_tok

        if label.type != "Loop Identifier":
            return res.failure(InvalidSyntaxError(label.pos_start, label.pos_end, "Expected Loop Label"))

        res.register(self.advance())

        operation = self.current_tok

        if operation.value not in ("UPPIN", "NERFIN"):
            return res.failure(InvalidSyntaxError(operation.pos_start, operation.pos_end, "Expected Operation Value 'UPPIN' or 'NERFIN'"))
        
        res.register(self.advance())

        # Checks for the delimiter YR
        delimiter = self.current_tok

        if delimiter.value != 'YR':
            return res.failure(InvalidSyntaxError(delimiter.pos_start, delimiter.pos_end, "Expected 'YR' "))
        
        res.register(self.advance())

        varident = self.current_tok

        if varident.type != "varident":
            return res.failure(InvalidSyntaxError(varident.pos_start, varident.pos_end, "Expected Varident "))

        res.register(self.advance())

        clause = self.current_tok

        # TODO: ADD CONDITIONAL OPERATORS
        if clause.value not in ("TIL", "WILE"):
            return res.failure(InvalidSyntaxError(clause.pos_start, clause.pos_end, "Expected clause 'TIL' or 'WILE' "))

        res.register(self.advance())
    
        expression = self.current_tok

        print(expression.value not in ("BOTH SAEM", "DIFFRINT"))

        if expression.value not in ("BOTH SAEM", "DIFFRINT") and expression.value not in comparison_ops:
            return res.failure(InvalidSyntaxError(expression.pos_start, expression.pos_end, "Expected 'BOTH SAEM', 'DIFFRINT', 'BIGGR OF', or 'SMALLR OF' "))

        expression = self.comparison_expr()
        if expression.error: return expression

        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))

        return res.success(LoopDeclarationNode(declaration, label, operation, varident, clause, expression.node))

    # for the loop delimiter
    def loop_end(self):
        res = ParserResult()
        declaration = self.current_tok 

        if declaration.value != "IM OUTTA YR":
            return res.failure(InvalidSyntaxError(declaration.pos_start, declaration.pos_end, "Expected Function Declaration 'IM IN YR' "))
        
        res.register(self.advance())

        label = self.current_tok

        if label.type != "Loop Identifier":
            return res.failure(InvalidSyntaxError(label.pos_start, label.pos_end, "Expected Loop Label " ))
        
        res.register(self.advance())

        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))

        return res.success(LoopEndNode(declaration, label))

    # responsible for the loop
    def loop(self):
        res = ParserResult()
        start = self.loop_declaration()

        if start.error: return start
        print(self.current_tok)

        statements = []

        while self.current_tok.value != "IM OUTTA YR":
            
            err = self.statement_section(statements)
            if err != None: 
                if err.error.details == "IM OUTTA YR must close a IM IN YR block - ":
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Statements Before Closing Loop "))
                return err

            if self.current_tok.type == TK_EOF:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Function Delimiter 'IM OUTTA YR' " ))

            if self.current_tok.value == "IM OUTTA YR":
                if self.previous_tok.type != TK_NEWLINE:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))
                break

            res.register(self.advance())

            while self.current_tok.type == TK_NEWLINE:
                res.register(self.advance())

            if self.current_tok.value == "IM OUTTA YR":
                if self.previous_tok.type != TK_NEWLINE:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))
                break
        

        end = self.loop_end()
        if end.error: return end

        if end.node.label.value != start.node.label.value:
            return res.failure(InvalidSyntaxError(end.node.pos_start, end.node.pos_end, "Expected Similar Start and End Label "))

        listed = ListNode(statements)

        return res.success(LoopNode(start.node, listed, end.node))


    def return_expressions(self):
        res = ParserResult()
        tok = self.current_tok
        pos_start = self.current_tok.pos_start.copy()

        if tok.value == "FOUND YR":
            res.register(self.advance())
            expr = self.expression()
            if expr.error: return expr

            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

        expr = res.register(self.expression())
        if expr.error: return expr


    def expression(self):
        res = ParserResult()
        tok = self.current_tok

        if tok.type == TK_STRING_DELIMITER:
            res.register(self.advance())
            tok = self.current_tok

        if tok.value == "MAEK":
            return self.typecast_maek()
        
        if tok.type == "Concatenation Keyword":  
            return self.concat()

        # Check for boolean operators first (highest precedence)
        if tok.value in ("NOT", "ALL OF", "ANY OF", "BOTH OF", "EITHER OF", "WON OF"):
            return self.boolean_expr()

        # Check for comparison operators and operations
        if tok.value in ("BOTH SAEM", "DIFFRINT"):
            return self.comparison_expr()
        
        # Check for arithmetic operations
        if tok.value in arithmetic:
            return self.arithmetic_expr()
        
        if tok.type in (TK_INT, TK_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        if tok.type == TK_STRING:
            res.register(self.advance())
            if self.current_tok and self.current_tok.type == TK_STRING_DELIMITER:
                res.register(self.advance())
            return res.success(StringNode(tok))

        if tok.type == TK_BOOL:
            res.register(self.advance())
            return res.success(BoolNode(tok))  # WIN -> true, FAIL -> false

        if tok.type == "varident":
            res.register(self.advance())
            return res.success(IdentifierNode(tok))
        
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected expression"))


# Handles the cases for the switch statement
    def switch_keywords(self, statements):
        res = ParserResult()
        inner_code = []

        while self.current_tok.type == TK_NEWLINE:
            print("pasok")
            res.register(self.advance())


        if self.current_tok.value == "OMG":
            start = self.current_tok
            res.register(self.advance())

            expression = self.current_tok

            if expression.type not in [TK_BOOL, TK_FLOAT, TK_INT, TK_STRING]:
                return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected 'NUMBR', 'NUMBAR', 'YARN', or 'TROOF'"))
            print(self.current_tok.type)
            res.register(self.advance())
            print(self.current_tok.type)

            while self.current_tok.value != "OMG" or self.current_tok.value != "OMGWTF" or self.current_tok.value != "OIC":
                res.register(self.advance())

                err = self.statement_section(inner_code)
                if err != None: return err

                if self.current_tok.value == "OMG":
                    break
                if self.current_tok.value == "OMGWTF":
                    break
                if self.current_tok.value == "OIC":
                    break  
                if self.current_tok.value == "KTHXBYE":
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected WTF? Delimiter 'OIC' " ))  

            statements.append(SwitchOMGNode(start, expression, inner_code.copy())) 
            return None

        if self.current_tok.value == "OMGWTF":
            start = self.current_tok
            res.register(self.advance())
            
            if self.current_tok.type != TK_NEWLINE:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))
            

            while self.current_tok.value != "OIC":
                res.register(self.advance())

                err = self.statement_section(inner_code)
                if err != None: return err
                
                if self.current_tok.value == "OMG":
                    return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected 'OIC' "))
                if self.current_tok.value == "OMGWTF":
                    return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected 'OIC' "))
                if self.current_tok.value == "OIC":
                    break  
                if self.current_tok.value == "KTHXBYE":
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected WTF? Delimiter 'OIC' " ))  

            statements.append(SwitchOMGWTFNode(start, inner_code.copy())) 
            return None

        
        return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'OMG' " ))

#  Handles the entire switch statement
    def switch_case(self):
        res = ParserResult()
        wtf_tok = self.current_tok
        res.register(self.advance())  # skip WTF?

        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after WTF?"))

        res.register(self.advance())  # skip newline

        # parse cases until OIC
        cases = []

        while self.current_tok.value != "OIC":
            if self.current_tok.value == "OMG":
                # parse OMG
                omg_tok = self.current_tok
                res.register(self.advance())
                
                value_node = res.register(self.expression())
                if res.error: return res

                if self.current_tok.type != TK_NEWLINE:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after OMG"))

                if self.current_tok.type == TK_NEWLINE:
                   res.register(self.advance())

                inner_statements = []
                while self.current_tok.value not in ("OMG", "OMGWTF", "OIC"):
                    err = self.statement_section(inner_statements)
                    if err != None: return err

                    while self.current_tok.type == TK_NEWLINE:
                        res.register(self.advance())

                cases.append(SwitchOMGNode(omg_tok, value_node, inner_statements))

            elif self.current_tok.value == "OMGWTF":
                # parse OMGWTF
                omgwtf_tok = self.current_tok
                res.register(self.advance())

                if self.current_tok.type != TK_NEWLINE:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after OMGWTF - "))

                res.register(self.advance())

                inner_statements = []
                while self.current_tok.value != "OIC":
                    err = self.statement_section(inner_statements)
                    if err != None: return err

                    while self.current_tok.type == TK_NEWLINE:
                        res.register(self.advance())

                cases.append(SwitchOMGWTFNode(omgwtf_tok, inner_statements))

                # expect OIC after default
                if self.current_tok.value == "OIC":
                    oic_tok = self.current_tok
                    res.register(self.advance())
                    return res.success(SwitchCaseNode(wtf_tok, cases, oic_tok))
                else:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected OIC after OMGWTF - "))

            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected OMG, OMGWTF, or OIC in switch-case - "))

        # if end without OMGWTF
        oic_tok = self.current_tok
        res.register(self.advance())
        return res.success(SwitchCaseNode(wtf_tok, cases, oic_tok))

# Handles function definition
    def function_definition(self):
        res = ParserResult()
        
        start = self.current_tok

        if start.value != "HOW IZ I":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'HOW IZ I' "))
        
        res.register(self.advance())

        func_name = self.current_tok

        if func_name.type != TK_FUNC_IDENTIFIER:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Function Identifier "))

        res.register(self.advance())

        params = []


        if self.current_tok.value == "YR":
            res.register(self.advance())

            if self.current_tok.type != "varident":
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Parameter "))
            
            params.append(self.current_tok)
            res.register(self.advance())


            # loops through all the paramters will stope once YR is no longer seen
            while self.current_tok.value == "AN":
                res.register(self.advance())

                # case for multi parameters
                
                if self.current_tok.value != "YR":
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'YR' "))
                
                res.register(self.advance())

                if self.current_tok.type != "varident":
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Parameter "))
                
                params.append(self.current_tok)

                res.register(self.advance())
                print(self.current_tok)
              
        if self.current_tok.type != TK_NEWLINE:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))
        
        print(params)
        return res.success(FunctionDefinitionNode(start, func_name, params))

    # The function itself
    def function(self):
        res = ParserResult()

        start = self.function_definition()
        if start.error: return start
        statements = []
        # while delimeter has not been seen
        while self.current_tok.value != "IF U SAY SO":

            err = self.statement_section(statements)
            if err != None: 
                if err.error.details == "IF U SAY SO must close a HOW IZ I block - ":
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Statements Before Closing Function "))
                return err

            if self.current_tok.type == TK_EOF:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Function Delimiter 'IF U SAY SO' " ))

            if self.current_tok.value == "IF U SAY SO":
                print(self.current_tok)
                end = self.current_tok

                if self.previous_tok.type != TK_NEWLINE:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))
                break

            res.register(self.advance())

            while self.current_tok.type == TK_NEWLINE:
                res.register(self.advance())
        
            if self.current_tok.value == "IF U SAY SO":
                print(self.current_tok)
                end = self.current_tok

                if self.previous_tok.type != TK_NEWLINE:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))
                break


        end = self.current_tok
        res.register(self.advance())

        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after statement"))

        return res.success(FunctionNode(start, statements, end))
    

    def func_call(self):
        res = ParserResult()

        op_tok = self.current_tok

        if op_tok.value != "I IZ":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'I IZ' "))
         
        res.register(self.advance())

        func_name = self.current_tok

        if func_name.type != TK_FUNC_IDENTIFIER:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Function Identifier "))

        res.register(self.advance())

        params = []

        if self.current_tok.value == "YR":
            res.register(self.advance())

            expr = res.register(self.expression())
            if res.error: return res
            
            params.append(expr)


            # loops through all the paramters will stope once YR is no longer seen
            while self.current_tok.value == "AN":
                res.register(self.advance())

                # case for multi parameters
                
                if self.current_tok.value != "YR":
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'YR' "))
                
                res.register(self.advance())

                expr = res.register(self.expression())
                if res.error: return res
                
                params.append(expr)

                print(self.current_tok)
                
        print(params)
        if self.current_tok.value != "MKAY":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'MKAY' " ))

        res.register(self.advance())


        return res.success(CallNode(op_tok, func_name, params))

    def if_statement(self):
        res = ParserResult()

        orly_tok = self.current_tok  # "O RLY?"

        res.register(self.advance())  # skip O RLY?

        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after O RLY? - "))

        res.register(self.advance())  # skip newline

        # parse if block
        if_statements = []

        # expect YA RLY
        if self.current_tok.value != "YA RLY":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected YA RLY - "))

        res.register(self.advance())  # skip YA RLY

        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after YA RLY - "))

        res.register(self.advance())  # skip newline

        # ends when NO WAI or OIC keyword encountered
        while self.current_tok.value not in ("NO WAI", "OIC"):
            err = self.statement_section(if_statements)
            if err != None: return err

            while self.current_tok.type == TK_NEWLINE:
                res.register(self.advance())

        # check if NO WAI or OIC
        if self.current_tok.value == "NO WAI":
            nowai_tok = self.current_tok
            res.register(self.advance())  # skip NO WAI

            if self.current_tok.type != TK_NEWLINE:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected newline after NO WAI - "))

            res.register(self.advance())  # skip newline

            # parse else statements until OIC
            else_statements = []

            while self.current_tok.value != "OIC":
                if self.current_tok.value == "O RLY?":
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Missing OIC to close if-else block - "))

                err = self.statement_section(else_statements)
                if err != None: return err

                while self.current_tok.type == TK_NEWLINE:
                    res.register(self.advance())

            if self.current_tok.value == "OIC":
                oic_tok = self.current_tok
                res.register(self.advance())  # skip OIC

                return res.success(IfNode(if_statements, else_statements, orly_tok.pos_start, oic_tok.pos_end))
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected OIC - "))

        elif self.current_tok.value == "OIC":
            oic_tok = self.current_tok
            res.register(self.advance())  # skip OIC

            return res.success(IfNode(if_statements, [], orly_tok.pos_start, oic_tok.pos_end))
        else:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected NO WAI or OIC - "))
