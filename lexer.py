import re
from enum import Enum
from typing import List, Tuple, Dict

# Define token types as an enumeration for better consistency
class TokenType(Enum):
    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    CHAR = 'CHAR'
    OPERATOR = 'OPERATOR'
    DELIMITER = 'DELIMITER'
    LOGICAL_OP = 'LOGICAL_OP'
    BRACKET = 'BRACKET'
    ERROR = 'ERROR'

class Token:
    def __init__(self, type: TokenType, lexeme: str, line: int, position: int):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.position = position

    def __str__(self):
        return f"Token(type={self.type.value}, lexeme='{self.lexeme}', line={self.line}, pos={self.position})"

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.tokens: List[Token] = []
        self.symbol_table: Dict[str, Dict] = {}
        self.current_line = 1
        self.current_position = 0
        self.errors: List[str] = []
        
        # Define token patterns with more comprehensive coverage
        self.token_patterns = [
            # Keywords from the Clite grammar
            (TokenType.KEYWORD, r'\b(int|bool|float|char|if|else|while|true|false|main)\b'),
            
            # Logical operators (higher priority than regular operators)
            (TokenType.LOGICAL_OP, r'&&|\|\|'),
            
            # Operators (expanded to include all from grammar)
            (TokenType.OPERATOR, r'==|!=|<=|>=|\+|-|\*|/|%|=|<|>|!'),
            
            # Numbers (float must come before integer)
            (TokenType.FLOAT, r'\b\d+\.\d+\b'),
            (TokenType.INTEGER, r'\b\d+\b'),
            
            # Character literals with proper escape handling
            (TokenType.CHAR, r"'(?:\\.|[^'\\])'"),
            
            # Brackets and delimiters
            (TokenType.BRACKET, r'[\[\]]'),
            (TokenType.DELIMITER, r'[{}();,]'),
            
            # Identifiers must come last to avoid matching keywords
            (TokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ]

    def remove_comments_and_whitespace(self) -> str:
        # Remove single-line comments
        code = re.sub(r'//.*?(?:\n|$)', '\n', self.code)
        
        # Remove multi-line comments while preserving line numbers
        code = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group().count('\n'), code, flags=re.DOTALL)
        
        return code

    def add_to_symbol_table(self, lexeme: str, token_type: TokenType, line: int) -> None:
        if lexeme not in self.symbol_table:
            self.symbol_table[lexeme] = {
                'type': token_type.value,
                'first_occurrence_line': line,
                'occurrences': 1
            }
        else:
            self.symbol_table[lexeme]['occurrences'] += 1

    def tokenize(self) -> List[Token]:
        # Pre-process the code
        processed_code = self.remove_comments_and_whitespace()
        
        # Split code into lines for better error reporting
        lines = processed_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            position = 0
            while position < len(line):
                # Skip whitespace
                if line[position].isspace():
                    position += 1
                    continue
                
                match_found = False
                for token_type, pattern in self.token_patterns:
                    regex = re.compile(pattern)
                    match = regex.match(line, position)
                    
                    if match:
                        lexeme = match.group(0)
                        token = Token(token_type, lexeme, line_num, position + 1)
                        self.tokens.append(token)
                        
                        # Add identifiers and keywords to symbol table
                        if token_type in [TokenType.IDENTIFIER, TokenType.KEYWORD]:
                            self.add_to_symbol_table(lexeme, token_type, line_num)
                        
                        position += len(lexeme)
                        match_found = True
                        break
                
                if not match_found:
                    # Handle invalid characters
                    error_msg = f"Invalid character '{line[position]}' at line {line_num}, position {position + 1}"
                    self.errors.append(error_msg)
                    token = Token(TokenType.ERROR, line[position], line_num, position + 1)
                    self.tokens.append(token)
                    position += 1

        return self.tokens

    def print_analysis(self) -> None:
        print("\n=== Lexical Analysis Results ===")
        print("\nTokens:")
        for token in self.tokens:
            print(token)
        
        print("\nSymbol Table:")
        for lexeme, info in self.symbol_table.items():
            print(f"{lexeme}: {info}")
        
        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"- {error}")

def test_lexer():
    # Test code that exercises all features of the grammar
    test_code = """
    int main() {
        // Variable declarations
        int x[10];
        float y = 3.14;
        char c = 'a';
        bool flag = true;
        
        /* Multi-line
           comment test */
        
        if (x[0] >= 5 && y != 0.0) {
            x[0] = x[0] + y - 2 * 3 / 6 % 2;
            flag = !flag || (c == 'b');
        } else {
            while (x[0] <= 10) {
                x[0] = x[0] + 1;
            }
        }
    }
    """
    
    lexer = Lexer(test_code)
    lexer.tokenize()
    lexer.print_analysis()

if __name__ == "__main__":
    test_lexer()