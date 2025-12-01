# LOLcode Interpreter - TL?DR CMSC 124 Project

## Overview

This project is a LOLcode interpreter developed by Canape, Caoile, and Marfa as part of CMSC 124 (Programming Languages). It includes lexical analysis, syntax analysis (parsing), and a GUI for an interactive programming experience.

## Features

- **Lexical Analysis**: Tokenizes LOLcode source code
- **Syntax Analysis**: Parses tokens into Abstract Syntax Trees (AST)
- **GUI Interface**: User-friendly text editor with dark theme (VS Code Inspired theme)
- **File Support**: Open and edit `.lol` files
- **Real-time Feedback**: View lexemes and symbol table
- **Console Output**: See program execution results

## Project Structure

```
lolcode-interpreter/
├── constants.py      # Token definitions and keywords
├── error.py          # Error handling classes
├── lexer.py          # Lexical analyzer
├── parser.py         # Syntax analyzer
├── gui.py            # Graphical user interface
└── README.md         # This file
```

## Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually comes with Python)

### Setup
1. Clone or download this repository
2. Ensure all files are in the same directory
3. Run the GUI:
```bash
python gui.py
```

## Usage

### Running the Interpreter

1. **Launch the GUI**:
   ```bash
   python gui.py
   ```

2. **Write or Load Code**:
   - Type LOLcode directly in the text editor, or
   - Click "Open File" to load a `.lol` file

3. **Execute**:
   - Click the "EXECUTE" button
   - View results in the console
   - Check lexemes and symbol table in the right panel

### GUI Components

- **File Explorer**: Open `.lol` files
- **Text Editor**: Write and edit LOLcode
- **Lexemes Table**: View tokenized output
- **Symbol Table**: Track variables and their values
- **Console**: See program output and errors

## 📝 Supported LOLcode Features

### Currently Implemented

#### 1. Variable Declaration
```lolcode
I HAS A variable_name
I HAS A variable_name ITZ value
```

#### 2. Print Statement (VISIBLE)
```lolcode
VISIBLE expression
VISIBLE expression AN expression
VISIBLE expression!          BTW suppress newline with !
```

#### 3. Arithmetic Operations
```lolcode
SUM OF x AN y               BTW Addition
DIFF OF x AN y              BTW Subtraction
PRODUKT OF x AN y           BTW Multiplication
QUOSHUNT OF x AN y          BTW Division
MOD OF x AN y               BTW Modulo
BIGGR OF x AN y             BTW Maximum
SMALLR OF x AN y            BTW Minimum
```

#### 4. Data Types
- `NUMBR` - Integer
- `NUMBAR` - Float
- `YARN` - String
- `TROOF` - Boolean (WIN/FAIL)
- `NOOB` - Uninitialized/Null

## Example Codes

### Example 1: Variable Declaration and Print
```lolcode
HAI
WAZZUP
    I HAS A x ITZ 5
    I HAS A name ITZ "Alice"
    I HAS A pi ITZ 3.14
BUHBYE

VISIBLE x
VISIBLE name
VISIBLE pi
KTHXBYE
```

### Example 2: Arithmetic Operations
```lolcode
HAI
WAZZUP
    I HAS A num1 ITZ 10
    I HAS A num2 ITZ 5
BUHBYE

VISIBLE SUM OF num1 AN num2
VISIBLE DIFF OF num1 AN num2
VISIBLE PRODUKT OF num1 AN num2
KTHXBYE
```

### Example 3: Multiple Print Values
```lolcode
HAI
VISIBLE "Hello" AN "World" AN "!"
KTHXBYE
```

### Example 4: Suppress Newline
```lolcode
HAI
VISIBLE "Hello"!
VISIBLE " World"
KTHXBYE
```
Output: `Hello World`

## Components

### constants.py
Defines all token types and LOLcode keywords:
- Token type constants (TK_INT, TK_FLOAT, TK_STRING, etc.)
- Keyword mappings
- Multi-word keyword prefixes
- Special characters and delimiters

### lexer.py
Handles lexical analysis:
- Tokenizes input source code
- Recognizes keywords, literals, identifiers
- Handles comments (BTW, OBTW...TLDR)
- Reports lexical errors with position information

### parser.py
Performs syntax analysis:
- **Node Classes**: Represent parse tree elements
  - `NumberNode`, `StringNode`, `IdentifierNode`
  - `PrintNode`, `VarDeclNode`
  - `ArithmeticNode`, `ArithmeticOperationNode`
- **Parser Methods**:
  - `print_statement()` - Parses VISIBLE statements
  - `var_declaration()` - Parses I HAS A statements
  - `arithmetic_expr()` - Parses arithmetic operations
  - `expression()` - General expression parser

### error.py
Error handling framework:
- Position tracking
- Error formatting
- User-friendly error messages

### gui.py
Graphical user interface:
- VSCode-inspired dark theme
- Syntax highlighting-ready text editor
- Interactive lexeme and symbol table views
- Real-time console output
- File management

## Team

**Course**: CMSC 124 - Programming Languages

**Project Members**:
- Daphne Canape
- Ralph 
- Thad

## LOLcode Language Reference

For complete LOLcode language specifications, visit:
- [LOLcode Official Specification](https://github.com/justinmeza/lolcode-spec/blob/master/v1.2/lolcode-spec-v1.2.md)

