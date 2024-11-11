import re
import tkinter as tk
from tkinter import filedialog, scrolledtext

TOKEN_PATTERNS = [
    ('KEYWORD', r'\b(int|bool|float|char|void|if|else|while|true|false|main|void|return)\b'),
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
                
                if token == 'IDENTIFIER':
                    if lexeme not in symbol_table:
                        symbol_table[lexeme] = {
                            'scope': get_current_scope(),
                            'declaration_line': line,
                            'type': token,
                            'references': set([line])
                        }
                    else:
                        symbol_table[lexeme]['references'].add(line)
                elif lexeme == '{':
                    if last_token == 'KEYWORD' and last_lexeme in ['if', 'while']:
                        scope_stack.append(last_lexeme)
                    else:
                        scope_stack.append(f'block{line}')
                elif lexeme == '}':
                    if len(scope_stack) > 1:
                        scope_stack.pop()

                last_token = token
                last_lexeme = lexeme

                lexemes.append((token, lexeme))
                position += len(lexeme)
                match = True
                break

        if not match:
            position += 1

    return lexemes, symbol_table

def lexer(filename):
    raw_text = read_file(filename)
    tokens, symbol_table = tokenize(raw_text)
    display_tokens(tokens)
    display_symbol_table(symbol_table)


    print(f"Lexemes and Tokens for {filename}:")
    print('-' * 160)
    title1, title2 = 'Token', 'Lexeme'
    print(f'{title1:<30}{title2:<30}')
    print('-' * 160)
    for token in tokens:
        print(f'{token[0]:<30}{token[1]}')

    print('-' * 160)
    print('\n')
    print("Symbol Table:")
    print('-' * 160)
    title1, title2, title3, title4, title5 = 'Name', 'Type', 'Scope', 'Declaration Line', 'References'
    print(f'{title1:<30}{title2:<30}{title3:<30}{title4:<30}{title5}')
    print('-' * 160)

    for symbol, info in symbol_table.items():
        print(f'{symbol:<30}{info["type"]:<30}{info["scope"]:<30}{info["declaration_line"]:<30}{info["references"]}')


    symbol_table_filename = filename.split('.')[0] + "_symbol_table.txt"
    with open(symbol_table_filename, 'w') as f:
        f.write("Symbol Table:\n")
        f.write('-' * 160)
        f.write('\n')
        f.write(f'{title1:<30}{title2:<30}{title3:<30}{title4:<30}{title5}\n')
        f.write('-' * 160)
        f.write('\n')
        for symbol, info in symbol_table.items():
            f.write(f'{symbol:<30}{info["type"]:<30}{info["scope"]:<30}{info["declaration_line"]:<30}{info["references"]}\n')

    print(f"\nSymbol table has been written to {symbol_table_filename}")

def open_file():
    filename = filedialog.askopenfilename(title = "Select a txt file", filetypes=[("Text Files", "*.txt")]) 
    if filename:
        lexer(filename)

def display_tokens(tokens):
    output_text.delete(1.0, tk.END)
    title1, title2 = 'Token', 'Lexeme'

    output_text.insert(tk.END, "Lexer:\n")
    output_text.insert(tk.END, '-' * 160 + '\n')
    output_text.insert(tk.END, f'{title1:<30}{title2:<30}\n')
    output_text.insert(tk.END, '-' * 160 + '\n')

    for token in tokens:
        output_text.insert(tk.END, f'{token[0]:<30}{token[1]}\n')

def display_symbol_table(symbol_table):
    symbol_table_text.delete(1.0, tk.END)
    title1, title2, title3, title4, title5 = 'Name', 'Type', 'Scope', 'Declaration Line', 'References'
    
    symbol_table_text.insert(tk.END, "Symbol Table:\n")
    symbol_table_text.insert(tk.END, '-' * 160 + '\n')
    symbol_table_text.insert(tk.END, f'{title1:<30}{title2:<30}{title3:<30}{title4:<30}{title5}\n')
    symbol_table_text.insert(tk.END, '-' * 160 + '\n')
    
    for symbol, info in symbol_table.items():
        symbol_table_text.insert(
            tk.END, 
            f'{symbol:<30}{info["type"]:<30}{info["scope"]:<30}{info["declaration_line"]:<30}{info["references"]}\n'
        )



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Lexer")
    root.geometry("500x500")

    open_button = tk.Button(root, text = "Open File", command = open_file)
    open_button.pack(pady = 10)

    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=180, height=20)
    output_text.pack(pady=10)

    symbol_table_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=180, height=15)
    symbol_table_text.pack(pady=10)

    root.mainloop()