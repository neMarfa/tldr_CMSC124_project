# THIS FILE IS CREATED FOR THE PURPOSE OF AVOIDING MERGE CONFLICTS
# FOR MAKING STRINGS need to add elif statement to the lexer

def make_string(self):
    string = ''
    pos_start = self.pos.copy()
    
    while self.current_char != None and self.current_char != '"':
        string += self.current_char
        self.advance()
    
    self.advance()
    return Token(TK_STRING, string, pos_start, self.pos)