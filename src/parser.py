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
    def __init__(self, statement_nodes, pos_start, pos_end):
        self.statement_nodes = statement_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end    

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
    def __init__(self, keyword_tok, expressions):
        self.keyword_tok = keyword_tok
        self.expressions = expressions
    
    def __repr__(self):
        return f'(VISIBLE, {", ".join(str(expr) for expr in self.expressions)})'
    
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

class GimmehNode:
    def __init__(self, keyword, varident):
        self.keyword_tok = keyword
        self.varident = varident
        self.pos_start = keyword.pos_start
        self.pos_end = varident.pos_end
    
    def __repr__(self):
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
        print(self.tokens)
        res = self.statements()
        return res  


    # contains all the functions to be parsed, data handling will be considered at a later date
    def statements(self):
        res = ParserResult()
        tok = self.current_tok
        final_tok = self.tokens[-1]
        pos_start = self.current_tok.pos_start.copy()
        statements = []
        # checks if the first character in the list of tokens is the start of program character
        if tok.value != "HAI":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'HAI' "))
        res.register(self.advance())

        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))

        res.register(self.advance())

        # checks immediately if the last character is the end of program
        if final_tok.value != "KTHXBYE":
            return res.failure(InvalidSyntaxError(final_tok.pos_start, final_tok.pos_end, "Expected 'KTHXBYE' "))
        
        # skip initial newlines
        while self.current_tok.type == TK_NEWLINE:
            res.register(self.advance())

        # parse statements until we hit KTHXBYE
        while self.current_tok.value != "KTHXBYE":
            err = self.statement_section(statements)
            if err != None: return err
            
            if self.current_tok.value == "KTHXBYE":
                if self.previous_tok.type != TK_NEWLINE:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))
                break
            
            # skip newlines between statements
            while self.current_tok.type == TK_NEWLINE:
                res.register(self.advance())
                if self.current_tok.value == "KTHXBYE":
                    break
            res.register(self.advance())

        return res.success(statements)

    # PLACE ALL THE STATEMENTS HERE, WILL BE REUSED IN FUNCTIONS AND LOOPS
    def statement_section(self, statements):
        res = ParserResult()

        # skip any leading newlines
        while self.current_tok.type == TK_NEWLINE:
            res.register(self.advance())
        
        # check if we've reached the end
        if self.current_tok.value == "KTHXBYE":
            return None

        if self.current_tok.type == "Output Keyword":
            print_stmt = self.print_statement()
            if print_stmt.error: return print_stmt
            statements.append(print_stmt.node)

        elif self.current_tok.type == "Variable Declaration":
            var_decl = self.var_declaration()
            if var_decl.error: return var_decl
            statements.append(var_decl.node)

        elif self.current_tok.value in arithmetic:
            arith = self.arithmetic_expr()
            if arith.error: return arith
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

        elif self.current_tok.type == "varident":
            # try to extend and see if it's assignment (R) or typecast (IS NOW A)
            next_idx = self.tok_idx + 1
            if next_idx < len(self.tokens):
                next_tok = self.tokens[next_idx]
                
                if next_tok.value == "R":
                    # assignment
                    assign = self.assignment()
                    if assign.error: return assign
                    statements.append(assign.node)
                elif next_tok.value == "IS NOW A":
                    # typecast
                    typecast = self.typecast_is_now_a()
                    if typecast.error: return typecast
                    statements.append(typecast.node)
                else:
                    # just a variable reference (skip for now)
                    res.register(self.advance())

        elif self.current_tok.value == "WTF?":
            switch = self.switch_case()
            if switch.error: return switch
            statements.append(switch.node)
            

        return None
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

        if tok.type in (TK_INT, TK_FLOAT):
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
            if not num.value.isdigit():
                return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected Typecastable String Value "))
            
            num.value = int(num.value)
            res.register(self.advance())
            res.register(self.advance())

            print(self.current_tok)
            return res.success(NumberNode(num))

        elif tok.type == "varident":
            pass
                
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
        if self.current_tok.value not in ("BOTH SAEM", "DIFFRINT") and self.current_tok.value not in comparison_ops:
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
      
        # format: VISIBLE <expression> [AN <expression>]*
        res = ParserResult()
        tok = self.current_tok
        
        if tok.type != "Output Keyword":
            return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected 'VISIBLE'"))
        
        res.register(self.advance())
        
        expressions = []
        
        expr = res.register(self.expression())
        if res.error: return res
        expressions.append(expr)
        
        # basically extends as long as there is a delimiter in the current statement
        while self.current_tok and self.current_tok.type == TK_DELIMITER:   
            res.register(self.advance())
            expr = res.register(self.expression())
            if res.error: return res
            expressions.append(expr)
        
        return res.success(PrintNode(tok, expressions))

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
        
        return res.success(VarDeclNode(tok, identifier_tok))
    
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
        if self.current_tok.value != "A":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'A'"))
        
        res.register(self.advance())
        
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
        
        # parse value expression
        value = res.register(self.expression())
        if res.error: return res
        
        return res.success(AssignmentNode(tok, r_tok, value))

    
    def input(self):
        res = ParserResult()
        tok = self.current_tok
        res.register(self.advance())
        var = self.current_tok

        if var.type != "varident":
            return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected variable identifier "))
        res.register(self.advance())

        return res.success(GimmehNode(tok, var))
        

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

        print(self.tokens)


        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))

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
            if err != None: return err

            if self.current_tok.value == "IM OUTTA YR":
                if self.previous_tok.type != TK_NEWLINE:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))
                break

            if self.current_tok.value == "KTHXBYE":
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Loop Delimiter 'IM OUTTA YR' " ))
        
            res.register(self.advance())

        end = self.loop_end()
        
        return res.success(LoopNode(start.node, statements, end.node))


    def expression(self):
        """
        Parses any expression (literals, identifiers, arithmetic, comparisons, booleans, etc.)
        """
        res = ParserResult()
        tok = self.current_tok

        if tok.type == TK_STRING_DELIMITER:
            res.register(self.advance())
            tok = self.current_tok

        if tok.value == "MAEK":
            return self.typecast_maek()

        # Check for boolean operators first (highest precedence)
        if tok.value in ("NOT", "ALL OF", "ANY OF", "BOTH OF", "EITHER OF", "WON OF"):
            return self.boolean_expr()

        # Check for comparison operators and operations
        if tok.value in ("BOTH SAEM", "DIFFRINT") or tok.value in comparison_ops:
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
        start = self.current_tok
        res.register(self.advance())

        if self.current_tok.type != TK_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))

        statements = []
        res.register(self.advance())

        while self.current_tok.value != "OIC":
            err = self.switch_keywords(statements)
            if err != None: return err

            if self.current_tok.value == "OIC":
                if self.previous_tok.type != TK_NEWLINE:
                    return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '\\n' "))
                break

            if self.current_tok.value == "KTHXBYE":
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected WTF? Delimiter 'OIC' " ))
        
        end = self.current_tok

        return res.success(SwitchCaseNode(start, statements, end))
