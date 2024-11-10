import re
from enum import Enum
from typing import List, Tuple, Dict
import tkinter as tk
from tkinter import filedialog, scrolledtext

TOKEN_PATTERNS = [
    ('KEYWORD', r'\b(int|bool|float|char|if|else|while|true|false|main)\b'),
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

    while position < len(cleaned):
        match = False

        for token, pattern in TOKEN_PATTERNS:
            regex = re.compile(pattern)
            check = regex.match(cleaned, position)

            if check:
                lexeme = check.group(0)
                lexemes.append(f'Token = {token} : Lexeme = {lexeme}')
                position += len(lexeme)
                match = True
                break

        if not match:
            position += 1

    return lexemes

def lexer(filename):
    raw_text = read_file(filename)
    tokens = tokenize(raw_text)
    display_tokens(tokens)

    print(f"Lexemes and Tokens for {filename}:")
    for token in tokens:
        print(token)

def open_file():
    filename = filedialog.askopenfilename(title = "Select a txt file", filetypes=[("Text Files", "*.txt")]) 
    if filename:
        lexer(filename)

def display_tokens(tokens: List[str]):
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