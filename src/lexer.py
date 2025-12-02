#################################
# Imports
#################################

from error import *
from constants import *
from parser import *
from interpreter import *

# Contains the array of tokens taken from our lexer
class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end    

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
    
    def advance(self, current_char=None):
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
            if self.current_char in ' \t\r': #skip if contains a space, tab, or newline
                self.advance()
            elif self.current_char in '\n':
                tokens.append(Token(TK_NEWLINE, "\\n",self.pos.copy(), self.pos.copy()))
                self.advance()
            elif self.current_char == '"': # handles YARN (string) literals
                result = self.make_string()
                if isinstance(result, tuple) and result[1] is not None:  # Error case
                    return [], result[1]
                tokens.extend(result)
            elif self.current_char == '!':
                tokens.append(Token(TK_EOS, '!', pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char in LETTERS: # If it contains any letters check the format if it is a keyword otherwise it is just a variable
                result = self.make_identifier(tokens)
                
                if isinstance(result, tuple) and result[1] is not None:  # Error case
                    return [], result[1]

                # Check if it's a single-line comment keyword (BTW)
                if isinstance(result, Token) and result.type == "Single-Line Comment Delimiter":
                    self.skip_single_line_comment()
                    continue

                # check if it's a multi-ine comment keyword
                if isinstance(result, Token) and result.type == "Multi-Line Comment Delimiter" and result.value is None:
                    # Skip multi-line comment (OBTW ... TLDR)
                    error = self.skip_multi_line_comment()
                    if error:
                        return [], error
                    continue
                tokens.append(result)
            elif self.current_char in DIGITS: # handles NUMBARS AND NUMBRS
                result = self.make_number()
                if isinstance(result, tuple) and result[1] is not None:  # Error case
                    return [], result[1]
              
                tokens.append(result)
                self.advance()
            elif self.current_char == '+': # String concatenation operator
                tokens.append(Token(TK_CONCAT, '+', pos_start=self.pos, pos_end=self.pos))
                self.advance()
            elif self.current_char == '-': # String concatenation operator
                pos_start = self.pos.copy()
                tokens.append(Token(TK_NEG, '-', pos_start, self.pos))
                self.advance()
                if self.current_char not in DIGITS:
                    return [], IllegalCharError(pos_start, self.pos, "'-' ")
            else:  # case when an illegal character has been found
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "' ")

        tokens.append(Token(TK_EOF,"EOF", pos_start=self.pos))
        return tokens, None

    # reads each line up until it stops reading a number.
    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
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
        if self.current_char != None and self.current_char not in DIGITS+' \t\n':
            pos_start = self.pos.copy()
            char = self.current_char    
            self.advance()
            return None, IllegalCharError(pos_start, self.pos, "'" + char + "' ")

        if dot_count == 0:
            return Token(TK_INT, int(num_str), pos_start, self.pos.copy())
        else:
            return Token(TK_FLOAT, float(num_str), pos_start, self.pos.copy())

    # reads a string literal enclosed in double quotes
    # returns: [String Delimiter, YARN:content, String Delimiter]
    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        
        # Create opening delimiter token
        opening_delimiter = Token(TK_STRING_DELIMITER, '"', pos_start, self.pos.copy())
        self.advance()  # skip opening quote
        
        # Check for empty string
        if self.current_char == '"':
            self.advance()  # skip closing quote
            closing_delimiter = Token(TK_STRING_DELIMITER, '"', pos_start, self.pos.copy())
            return [opening_delimiter, Token(TK_STRING, ''), closing_delimiter]
        
        while self.current_char != None and self.current_char != '"':
            # Check for newline in string (unclosed string)
            if self.current_char == '\n':
                pos_end = self.pos.copy()
                return None, ExpectedCharError(pos_start, pos_end, 'Unclosed string - ')
            
            string += self.current_char
            self.advance()
        
        # Check if string was properly closed
        if self.current_char == None:
            pos_end = self.pos.copy()
            return None, ExpectedCharError(pos_start, pos_end, 'Unclosed string - ')
        
        # Create YARN token with content
        yarn_token = Token(TK_STRING, string, pos_start, self.pos.copy())
        
        # Skip closing quote and create closing delimiter token
        self.advance()
        closing_delimiter = Token(TK_STRING_DELIMITER, '"', pos_start, self.pos)
        
        return [opening_delimiter, yarn_token, closing_delimiter]

    # TODO: MAKE it work for words that include spaces. currently in progress ==> check changes
    #  reads a line up until it does not read a letter or a digit
    def make_identifier(self, tokens):
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

        if id_str == "OBTW":
            return Token(tok_type, None, pos_start, self.pos.copy())
        # Handle boolean literals WIN and FAIL
        # Store the original string as value for display, boolean value can be accessed via token.value
        elif id_str == "WIN":
            return Token(TK_BOOL, "WIN", pos_start, self.pos.copy())
        elif id_str == "FAIL":
            return Token(TK_BOOL, "FAIL", pos_start, self.pos.copy())
        elif id_str in KEYWORDS.keys():
            return Token(tok_type, id_str, pos_start, self.pos.copy())
        
        if ' ' in id_str:
            return None, ExpectedCharError(pos_start, self.pos.copy(), 'Incomplete Keyword Error ')

        # For case in functions
        if len(tokens) != 0 and tokens[-1].value in function_specific:
            tok_type = TK_FUNC_IDENTIFIER

        if len(tokens) != 0 and tokens[-1].value in loop_specific:
            tok_type = "Loop Identifier"

        return Token(tok_type, id_str, pos_start, self.pos.copy())
    
    # skip single-line comment (BTW)
    def skip_single_line_comment(self):
        # Skip everything until end of line or end of file
        while self.current_char != None and self.current_char != '\n':
            self.advance()
        # Don't advance past newline, let whitespace handler take care of it     

    # for OBTW
    # TODO: OBTW must come first before TLDR
    # TODO: OBTW and TLDR must have their own lines
    def skip_multi_line_comment(self):
        pos_start = self.pos.copy()

        # Skip whitespaces and new lines after OBTW (if any)
        while self.current_char != None and self.current_char in ' \t\n':
            self.advance()

        # look for end of comment ==> TLDR
        while self.current_char != None:
            if self.current_char == 'T':
                # save curr position if ever needed (if the next word is not TLDR)
                saved_pos = self.pos.copy()

                # try try to read TLDR
                temp_str = 'T'  # Start with 'T' 
                self.advance()  # Move past 'T'
                
                # Read the rest of the word (LDR) - only letters
                while self.current_char != None and self.current_char in LETTERS:
                    temp_str += self.current_char
                    self.advance()

                # Check if TLDR
                if temp_str == 'TLDR':
                    # end the multi-line comment, skip all na nasa line ng TLDR
                    while self.current_char != None and self.current_char != '\n':
                        self.advance()
                    # Skip the newline after TLDR (if present)
                    if self.current_char == '\n':
                        self.advance()
                    return None  # Successfully skipped comment
                else:
                    # if the curr word na nir-read ay not TLDR
                    self.pos = saved_pos
                    self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
                    self.advance()
            else:
                # Skip any character 
                self.advance()
        
        # If end of file reached without finding TLDR, return error
        pos_end = self.pos.copy()
        return ExpectedCharError(pos_start, pos_end, 'Unclosed multi-line comment - ')


#################################
# RUN THE LEXER!!!
#################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error


    # return tokens, None
    # # for the parser
    parser = Parser(tokens)
    ast = parser.parse()


    # print(ast.error)
    if ast.error: return None, ast.error


    # interprester = Interpreter()
    # interpreter.visit(ast.node)


    return tokens, None
    # return ast.node, ast.error
