from constants import *
from error import *

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
    def __init__(self, op_tok, label, operation, varident, expression):
        self.op_tok = op_tok
        self.label = label
        self.operation = operation
        self.varident = varident
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
        return f'{self.tok}'
    
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

class ComparisonNode:
    def __init__(self, op_tok, left_node, right_node):
        self.op_tok = op_tok  # BOTH SAEM or DIFFRINT
        self.left_node = left_node
        self.right_node = right_node
        self.pos_start = op_tok.pos_start
        self.pos_end = right_node.pos_end
    
    def __repr__(self):
        return f'({self.op_tok}, {self.left_node}, {self.right_node})'

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
    
    # MOVING TO NEXT INDEX
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok


    # TODO:make possible not only for arithmetic operations
    def parse(self):
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
        # TODO: will change this in the future so that NEWLINES will be taken into account
        if final_tok.value != "KTHXBYE":
            return res.failure(InvalidSyntaxError(final_tok.pos_start, final_tok.pos_end, "Expected 'KTHXBYE' "))
        
        # Checks if there is a newline between HAI and KTHXBYE
        while self.current_tok.type == TK_NEWLINE:
            res.register(self.advance())

        # WARN: as of now this only accepts arithmetic values ==> added for printing & var dec
        while self.current_tok.value != "KTHXBYE":
            
            err = self.statement_section(statements)
            if err != None: return err
            
            if self.current_tok.value == "KTHXBYE":
                break
            
            res.register(self.advance())

        # for testing interpreter
        # return res.success(ListNode(statements, pos_start, self.current_tok.pos_start.copy()))

        # for testing syntax tree
        return res.success(statements)

    # PLACE ALL THE STATEMENTS HERE, WILL BE REUSED IN FUNCTIONS AND LOOPS
    def statement_section(self, statements):
        res = ParserResult()

        if self.current_tok.type == TK_NEWLINE:
            res.register(self.advance())

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
            ret = arith

        elif self.current_tok.value == "IM IN YR":
            loop = self.loop()
            if loop.error: return loop
            statements.append(loop.node)
        
        return None


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
        print(tok.type)
        if tok.type in (TK_INT, TK_FLOAT, "varident"):
            res.register(self.advance())
            return res.success(NumberNode(tok))

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
        
        # Check if it's a comparison operator
        if self.current_tok.value not in ("BOTH SAEM", "DIFFRINT"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, 
                self.current_tok.pos_end, 
                "Expected 'BOTH SAEM' or 'DIFFRINT'"
            ))
        
        op_tok = self.current_tok
        res.register(self.advance())
        
        # Parse left expression (can be arithmetic, identifier, etc.)
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
        
        # Parse right expression
        right = res.register(self.expression())
        if res.error: return res
        
        return res.success(ComparisonNode(op_tok, left, right))
    
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

        expression = self.current_tok

        # TODO: ADD CONDITIONAL OPERATORS
        if expression.value not in ("TIL", "WILE"):
            return res.failure(InvalidSyntaxError(expression.pos_start, expression.pos_end, "Expected Expression 'TIL' or 'WILE' "))

        res.register(self.advance())

        return res.success(LoopDeclarationNode(declaration, label, operation, varident, expression))

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
        print(start.node)
        if start.error: return start

        statements = []

        while self.current_tok.value != "IM OUTTA YR":

            err = self.statement_section(statements)
            if err != None: return err

            if self.current_tok.value == "IM OUTTA YR":
                break
        
            res.register(self.advance())

        end = self.loop_end()
        
        return res.success(LoopNode(start.node, statements, end.node))


    def expression(self):
        """
        Parses any expression (literals, identifiers, arithmetic, comparisons, etc.)
        """
        res = ParserResult()
        tok = self.current_tok
        
        if tok.type == TK_STRING_DELIMITER:
            res.register(self.advance())
            tok = self.current_tok
        
        # Check for comparison operators first (before arithmetic)
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
        
        if tok.type == "varident":
            res.register(self.advance())
            return res.success(IdentifierNode(tok))
        
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected expression"))