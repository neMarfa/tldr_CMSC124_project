import string

#################################
# Constants
#################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
SPECIAL = '?'
LETTERS_DIGITS = LETTERS+DIGITS+SPECIAL


#################################
# TOKENS
#################################

arithmetic = ["SUM OF", "DIFF OF", "PRODUKT OF", "MOD OF", "QUOSHUNT OF", "BIGGR OF", "SMALLR OF"]


TK_INT = "NUMBR"
TK_FLOAT = "NUMBAR"
TK_STRING = "YARN"
TK_BOOL = "TROOF"
TK_VOID = "NOOB"
TK_STRING_DELIMITER = "String Delimiter"
TK_LITERAL = "literal"          # might use later
TK_CONCAT = "Concatenation Operator"     # string concatenation operator
TK_DELIMITER = "Operator Delimiter"
TK_EOF = "EOF"

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