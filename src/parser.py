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
    
    def __repr__(self):
        return f'{self.tok}'

class KeywordNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'

class ArithmeticOperationNode:
    def __init__(self,op_tok):
        self.op_tok = op_tok
    
    def __repr__(self):
        return f'{self.op_tok}'

class ArithmeticNode:
    def __init__(self,op_tok, left_node, separator_node, right_node):
        self.op_tok = op_tok 
        self.left_node = left_node
        self.right_node = right_node
        self.separator_node = separator_node

    def __repr__(self):
        return f'({self.op_tok}, {self.left_node}, {self.separator_node}, {self.right_node})'


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

        # checks if the first character in the list of tokens is the start of program character
        if tok.value != "HAI":
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'HAI' "))
        statements = [KeywordNode(tok)]
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

        # WARN: as of now this only accepts arithmetic values
        while self.current_tok.value != "KTHXBYE":
            if self.current_tok.type == TK_NEWLINE:
                res.register(self.advance())

            if self.current_tok.value in arithmetic:
                arith = self.arithmetic_expr()
                statements.append(arith)

            if self.current_tok not in arithmetic:
                return res.failure(InvalidSyntaxError(final_tok.pos_start, final_tok.pos_end, "VERSION 1 ARITHMETIC ONLY "))

        statements.append(KeywordNode(final_tok))
        return res.success(statements)
    
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

        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected NUMBR or NUMBAR "))

    # SUM OF, MOD OF, ETC
    def arithmetic_ops(self):
        res = ParserResult()
        tok = self.current_tok 
        if tok.value in arithmetic:
            res.register(self.advance())
            return res.success(ArithmeticOperationNode(tok))
        
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected Arithmetic Operation "))

    # WHERE THE ARITHMETIC PARSE TREE BEGINS
    def arithmetic_expr(self):
        res = ParserResult()
        if self.current_tok.type == TK_NEWLINE:
            res.register(self.advance())

        start = res.register(self.arithmetic_ops())
        
        if res.error: return res

        # handles nested operations on the left side
        if self.current_tok.value in arithmetic:
            left = res.register(self.arithmetic_expr())
            if res.error: return res
        else:
            left = res.register(self.arithmetic_values())
            if res.error: return res

        # Checks for the delimiter AN
        delimiter = res.register(self.delimiter_values())
        if res.error: return res
        
        # Handles nested operations on the right side 
        if self.current_tok.value in arithmetic:
            right = res.register(self.arithmetic_expr())
            if res.error: return res
        else:
            right = res.register(self.arithmetic_values())
            if res.error: return res
   
        start = ArithmeticNode(start, left, delimiter, right)
        
        return res.success(start)
