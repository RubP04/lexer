import re
import tkinter as tk
from tkinter import filedialog, scrolledtext

TOKEN_PATTERNS = [
    ('KEYWORD', r'\b(int|bool|float|char|void|if|else|while|true|false|main)\b'),
    ('LOGICAL_OP', r'&&|\|\|'),
    ('OPERATOR', r'==|!=|<=|>=|\+|-|\*|/|%|=|<|>|!'),
    ('FLOAT', r'\b\d+\.\d+\b'),
    ('INTEGER', r'\b\d+\b'),
    ('CHAR', r"'(?:\\.|[^'\\])'"),
    ('BRACKET', r'[\[\]]'),
    ('DELIMITER', r'[{}();,]'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')
]

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def clean_code(input):
    code = re.sub(r'//.*', '', input)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    code = code.strip()
    return code

def tokenize(input):
    cleaned = clean_code(input)
    lexemes = []
    position = 0
    line = 1
    scope_stack = ['Global']
    symbol_table = {}
    current_type = None  # Tracks type keywords (e.g., int, float, char)
    last_token = None
    last_lexeme = None

    def get_current_scope():
        return '_'.join(scope_stack)

    while position < len(cleaned):
        if cleaned[position] == '\n':
            line += 1
            position += 1
            continue
        if cleaned[position].isspace():
            position += 1
            continue

        match = False

        for token, pattern in TOKEN_PATTERNS:
            regex = re.compile(pattern)
            check = regex.match(cleaned, position)

            if check:
                lexeme = check.group(0)
                
                # Track type declarations
                if token == 'KEYWORD' and lexeme in ['int', 'bool', 'float', 'char', 'void']:
                    current_type = lexeme
                
                # Add all identifiers to the symbol table
                if token == 'IDENTIFIER':
                    # Add identifier to symbol table if not already present
                    if lexeme not in symbol_table:
                        symbol_table[lexeme] = {
                            'scope': get_current_scope(),
                            'declaration_line': line,
                            'type': current_type,  # Use current_type if available, otherwise None
                            'references': set([line])
                        }
                    else:
                        # Update references for an existing identifier
                        symbol_table[lexeme]['references'].add(line)
                
                # Handle entering and exiting braces for scope tracking
                elif lexeme == '{':
                    if last_token == 'KEYWORD' and last_lexeme in ['if', 'while']:
                        # Append control structure to scope
                        scope_stack.append(last_lexeme)
                    else:
                        # Generic block within the current scope
                        scope_stack.append(f'block{line}')
                elif lexeme == '}':
                    # Exit the current scope
                    if len(scope_stack) > 1:
                        scope_stack.pop()
                
                # Reset type after a statement ends
                elif lexeme == ';':
                    current_type = None

                # Track last token for scope-based decisions
                last_token = token
                last_lexeme = lexeme

                # Append lexeme and scope information
                lexemes.append(f'Token -> {token:<10}  Lexeme -> {lexeme}  Scope -> {get_current_scope()}')
                position += len(lexeme)
                match = True
                break

        if not match:
            position += 1

    return lexemes, symbol_table





def lexer(filename):
    raw_text = read_file(filename)
    tokens, symbol_table = tokenize(raw_text)
    #display_tokens(tokens)

    print(f"Lexemes and Tokens for {filename}:")
    for index, token in enumerate(tokens, start=1):
        print(f'{index}. {token}')
    print('-' * 80)
    print("Symbol Table:")
    for key, value in symbol_table.items():
        print(f'{key} -> {value}')

def open_file():
    filename = filedialog.askopenfilename(title = "Select a txt file", filetypes=[("Text Files", "*.txt")]) 
    if filename:
        lexer(filename)

def display_tokens(tokens):
    output_text.delete(1.0, tk.END)
    for token in tokens:
        output_text.insert(tk.END, token + '\n')  # Insert each token on a new line

if __name__ == "__main__":
    #lexer("text.txt")
    root = tk.Tk()
    root.title("Lexer")
    root.geometry("500x500")

    open_button = tk.Button(root, text = "Open File", command = open_file)
    open_button.pack(pady = 10)

    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
    output_text.pack(pady=10)


    root.mainloop()