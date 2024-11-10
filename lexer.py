import re
from enum import Enum
from typing import List, Tuple, Dict

TOKEN_PATTERS = [
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