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

class DelimiterNode:
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
    
    def register(self, res):
        if isinstance(res, ParserResult):
            if res.error: self.error = res.error
            return res.node
        
        return res
    
    def success(self, node):
        self.node = node
        return self
    
    def failure(self, error):
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
        res = self.arithmetic_expr()
        if not res.error and self.current_tok.type != TK_EOF:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Code "))
        return res  

    def delimiter_values(self):
        res = ParserResult()
        tok = self.current_tok
        if tok.type == TK_DELIMITER:
            res.register(self.advance())
            return res.success(DelimiterNode(tok))
        
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
        start = res.register(self.arithmetic_ops())
        
        if res.error: return res

        if self.current_tok.value in arithmetic:
            left = res.register(self.arithmetic_expr())
            if res.error: return res
        else:
            left = res.register(self.arithmetic_values())
            if res.error: return res

        delimiter = res.register(self.delimiter_values())
        if res.error: return res
        
        right = res.register(self.arithmetic_values())
        if res.error: return res
        start = ArithmeticNode(start, left, delimiter, right)
        
        return res.success(start)
