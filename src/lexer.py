"""
WHY NOT USE REGEX?

one of the benefits of this method is by showing which line the error is. Making it easier for us in the debugging phase
specifically when working towards the logic of the actual language. Regex does not do this although it is a lot easier I suppose?
"""

#################################
# Imports
#################################

import string

#################################
# Constants
#################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
SPECIAL = '?'
LETTERS_DIGITS = LETTERS+DIGITS+SPECIAL


#################################
# ERROR
#################################

# Class handles error printing and tells what specific error there will be WIll add more in the future
# Currently only Illegal characters will be displayed
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln +1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end,'Illegal Character', details)

class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)



#################################
# TOKENS
#################################


TK_INT = "NUMBR"
TK_FLOAT = "NUMBAR"
TK_STRING = "YARN"
TK_BOOL = "TROOF"
TK_VOID = "NOOB"

KEYWORDS = {
    'NUMBR' : "NUMBR Type Literal",
    'NUMBAR' : "NUMBAR Type Literal",
    'YARN' : "YARN Type Literal",
    'TROOF' : "TROOF Type Literal",
    "HAI" : "Start of Program",
    "KTHXBYE" : "End of Program",
    "WAZZUP" : "Variable Declaration Block Start",
    "BUHBYE" : "Variable Declaration Block End",
    "BTW" : "Single-Line Comment Delimiter",
    "OBTW" : "Multi-Line Comment Delimiter",
    "TLDR" : "Multi-Line Comment Delimiter",
    "ITZ" : "Variable Assignment",
    "R" : "Assignment Operation",
    "SUM OF" : "Addition Operator",
    "DIFF OF" : "Subtraction Operator",
    "PRODUKT OF" : "Multiplication Operator",
    "QUOSHUNT OF" : "Quotient Operator",
    "MOD OF" : "Modulo Operator",
    "BIGGR OF" : "Max Operator",
    "SMALLR OF" : "Min Operator",
    "BOTH OF" : "And Operator",
    "EITHER OF" : "Or Operator",
    "WON OF" : "Xor Operator",
    "NOT" : "Boolean Not Operator",
    "ANY OF" : "Infinite Arity Or Operator",
    "ALL OF" : "Infinite Arity And Operator",
    "BOTH SAEM" : "Equal Operator",
    "DIFFRINT" : "Not Equal Operator",
    "SMOOSH" : "Concatenation Keyword",
    "MAEK" : "Typecast Keyword",
    "I HAS A" : "Variable Declaration",
    "IS NOW A" : "Typecast Keyword",
    'A' : "Typecast Keyword",
    "VISIBLE" : "Output Keyword",
    "GIMMEH" : "Input Keyword",
    "O RLY?" : "Start of If-then Delimiter",
    "YA RLY" : "If Keyword",
    "MEBBE" : "Else-if Keyword",
    "NO WAI" : "Else Keyword",
    "OIC" : "End of If-then",
    "WTF?" : "Start of Switch-case",
    "OMG" : "Case Delimiter",
    "OMGWTF" : "Default Case Keyword",
    "IM IN YR" : "Loop Delimiter",
    "UPPIN" : "Increment Keyword",
    "NERFIN" : "Decrement Keyword",
    "YR" : "Loop Operator-Variable Delimiter",
    "TIL" : "Loop Until Keyword",
    "WILE" : "Loop While Keyword",
    "IM OUTTA YR" : "Loop Delimiter",
    'NOOB' : "Type Literal",
    "AN" : "Operator Delimiter",
    "GTFO": "Break Keyword",
    "MKAY": "Operation End",
    "WIN" : "Boolean Literal (True)",
    "FAIL" : "Boolean Literal (False)"
}

# for multi-word keywords
MULTIWORD_PREFIXES = [
    'I', 'I HAS',                                            
    'SUM', 'DIFF', 'PRODUKT', 'QUOSHUNT', 'MOD',         
    'BIGGR', 'SMALLR', 'BOTH', 'EITHER', 'WON', 'ANY', 'ALL',
    'IS', 'IS NOW',                                          
    'O', 'YA', 'NO', 
    'IM', 'IM IN', 'IM OUTTA'                                 
]

# Contains the array of tokens taken from our lexer
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value is not None: return f'{self.type}:{self.value}'
        return f'{self.type}'

#################################
# POSITION
#################################

# defines the position of the string that is currently being read
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    
    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0
        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


#################################
# LEXER
#################################


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    #  advances towards the next character in the inputted string
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self.current_char in ' \t\n': #skip if contains a space, tab, or newline
                self.advance()
            elif self.current_char == '"': # handles YARN (string) literals
                result = self.make_string()
                if isinstance(result, tuple) and result[1] is not None:  # Error case
                    return [], result[1]
                tokens.append(result)
            elif self.current_char in LETTERS: # If it contains any letters check the format if it is a keyword otherwise it is just a variable
                result = self.make_identifier()
                
                # Check if it's a single-line comment keyword (BTW)
                if isinstance(result, Token) and result.type == "Single-Line Comment Delimiter":
                    self.skip_single_line_comment()
                    continue
                
                tokens.append(result)
            elif self.current_char in DIGITS: # handles NUMBARS AND NUMBRS
                result = self.make_number()
                if isinstance(result, tuple) and result[1] is not None:  # Error case
                    return [], result[1]
                else:
                    tokens.append(result)
                    self.advance()
            else:  # case when an illegal character has been found
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    # reads each line up until it stops reading a number.
    def make_number(self):
        num_str = ''
        dot_count = 0

        #  goes through the numbers and sees if they are valid digits
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        # if the last character is not a space or Nothing then it will throw an error
        if self.current_char != None and self.current_char not in DIGITS+' ':
            pos_start = self.pos.copy()
            char = self.current_char    
            return None, IllegalCharError(pos_start, self.pos, "'" + char + "' ")

        if dot_count == 0:
            return Token(TK_INT, int(num_str))
        else:
            return Token(TK_FLOAT, float(num_str))

    # reads a string literal enclosed in double quotes
    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        self.advance()  # skip opening quote
        
        # Check for empty string
        if self.current_char == '"':
            self.advance()  # skip closing quote
            return Token(TK_STRING, '')
        
        while self.current_char != None and self.current_char != '"':
            # Check for newline in string (unclosed string)
            if self.current_char == '\n':
                pos_end = self.pos.copy()
                return None, ExpectedCharError(pos_start, pos_end, 'Unclosed string')
            
            string += self.current_char
            self.advance()
        
        # Check if string was properly closed
        if self.current_char == None:
            pos_end = self.pos.copy()
            return None, ExpectedCharError(pos_start, pos_end, 'Unclosed string')
        
        # Skip closing quote
        self.advance()
        return Token(TK_STRING, string)

    # TODO: MAKE it work for words that include spaces. currently in progress ==> check changes
    #  reads a line up until it does not read a letter or a digit
    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()
        
        # read the first word
        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()
        
        # check if current str could be part of a multi-word keyword
        while True:
            temp_pos = self.pos.copy()      # copy of current position for backtracking (if needed)
            temp_str = id_str               # copy of current traced str

            # skip spaces
            space_counter = 0
            while self.current_char == ' ':
                space_counter += 1
                self.advance()

            # if space_counter == 0, current str cannot be extended (not a multi-word)
            if space_counter == 0:
                break
            
            # else, try to read next word
            next_word = ''
            while self.current_char != None and self.current_char in LETTERS_DIGITS + '_?':
                next_word += self.current_char
                self.advance()
            
            # if cannot read next word, backtrack and stop
            if not next_word:
                self.pos = temp_pos
                self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
                break

            # check the extended version
            temp_extended = temp_str + ' ' + next_word

            # check if temp_extended is a valid keyword 
            if temp_extended in KEYWORDS.keys() or temp_extended in MULTIWORD_PREFIXES:
                id_str = temp_extended

            else:
                self.pos = temp_pos
                self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
                break

        tok_type = KEYWORDS.get(id_str, "varident")
        
        # Handle boolean literals WIN and FAIL
        if id_str == "WIN":
            return Token(TK_BOOL, True)
        elif id_str == "FAIL":
            return Token(TK_BOOL, False)
        
        return Token(tok_type, id_str if tok_type == "varident" else None)
    
    # skip single-line comment (BTW)
    def skip_single_line_comment(self):
        # Skip everything until end of line or end of file
        while self.current_char != None and self.current_char != '\n':
            self.advance()
        # Don't advance past newline, let whitespace handler take care of it        
        
#################################
# RUN THE LEXER!!!
#################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
