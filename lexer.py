import re
from enum import Enum
from typing import List, Tuple, Dict

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

    print(f"Lexemes and Tokens for {filename}:")
    for token in tokens:
        print(token)

if __name__ == "__main__":
    lexer("text.txt")

