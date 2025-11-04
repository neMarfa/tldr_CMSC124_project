import lexer

while True:
    text = input('LOL > ')
    result, error = lexer.run("test.lol", text)

    if error: print(error.as_string())
    else: print(result)