from constants import *

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
        return res  
    
    # HANDLES ANYTHING INVOLVING NUMBERS
    def arithmetic_values(self):
        tok = self.current_tok
        if tok.type in (TK_INT, TK_FLOAT):
            self.advance()
            return NumberNode(tok)

    # SUM OF, MOD OF, ETC
    def arithmetic_ops(self):
        tok = self.current_tok 
        if tok.value in arithmetic:
            self.advance()
            return ArithmeticOperationNode(tok)

    # WHERE THE ARITHMETIC PARSE TREE BEGINS
    # TODO: ALLOW NESTING OF OPERATIONS
    def arithmetic_expr(self):
        start = self.arithmetic_ops()
        left = self.arithmetic_values()

        while self.current_tok.type == TK_DELIMITER:
            delimiter = self.current_tok
            self.advance()
            right = self.arithmetic_values()
            start = ArithmeticNode(start, left, delimiter, right)
        
        return start
