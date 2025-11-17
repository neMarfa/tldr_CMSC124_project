"""
WE DID NOT CREATE THIS FUNCTION
THIS IS A FUNCTION TAKEN FROM THIS GITHUB LINK
https://github.com/davidcallanan/py-myopl-code/blob/master/ep2/strings_with_arrows.py

IN THIS YOUTUBE SERIES:
https://www.youtube.com/watch?v=RriZ4q4z9gU&list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD&index=2

THE BASE ON HOW THE LEXER INTERPRETER AND OTHERS ARE BUILT
USING THIS TUTORIAL, HOWEVER THE IMPLEMENTATION TOWARDS THIS IN
LOLCODE WAS ALL THROUGH THE EFFORTS OF EACH OF THE MEMBERS
"""
def string_with_arrows(text, pos_start, pos_end):
    result = ''

    # Calculate indices
    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: idx_end = len(text)
    
    # Generate each line
    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)

    return result.replace('\t', '')