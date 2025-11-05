# import lexer

# while True:
#     text = input('LOL > ')
#     result, error = lexer.run("test.lol", text)

#     if error: print(error.as_string())
#     else: print(result)

from lexer import run

# Test 1
print("Test 1: I HAS A x ITZ 5")
tokens, error = run('test', 'I HAS A x ITZ 5')
print(tokens if not error else error.as_string())
print()

# Test 2
print("Test 2: BTW comment")
tokens, error = run('test', 'HAI\nBTW comment here\nI HAS A x ITZ 5\nKTHXBYE')
print(tokens if not error else error.as_string())
print()

# Test 3
print("Test 3: OBTW...TLDR comment")
tokens, error = run('test', 'HAI\nOBTW\ncomment\nTLDR\nI HAS A x ITZ 5\nKTHXBYE')
print(tokens if not error else error.as_string())
print()

# Test 4
print('Test 4: String "hello"')
tokens, error = run('test', 'I HAS A name ITZ "hello"')
print(tokens if not error else error.as_string())
print()

# Test 5
print("Test 5: Boolean WIN")
tokens, error = run('test', 'I HAS A flag ITZ WIN')
print(tokens if not error else error.as_string())
print()

print("Done!")