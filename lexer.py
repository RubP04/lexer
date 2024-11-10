import re
from enum import Enum
from typing import List, Tuple, Dict

TOKEN_PATTERNS = {
    'KEYWORD' : r'\b(int|bool|float|char|if|else|while|true|false|main)\b',
    'IDENTIFIER' : r'[a-zA-Z_][a-zA-Z0-9_]*',
    'INTEGER' : r'\b\d+\b',
    'FLOAT' : r'\b\d+\.\d+\b',
    'CHAR' : r"'(?:\\.|[^'\\])'",
    'OPERATOR' : r'==|!=|<=|>=|\+|-|\*|/|%|=|<|>|!',
    'DELIMITER' : r'[{}();,]',
    'LOGICAL_OP' : r'&&|\|\|',
    'BRACKET' : r'[\[\]]'
}

TOKEN_ORDER = ['KEYWORD', 'LOGICAL_OP', 'OPERATOR', 'FLOAT', 'INTEGER', 'CHAR', 'BRACKET', 'DELIMITER']