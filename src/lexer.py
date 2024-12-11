import re

class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def advance(self):
        self.pos += 1

    def get_next_token(self):
        text = self.text

        if self.pos >= len(text):
            return Token('EOF', None)

        current_char = text[self.pos]

        if current_char.isspace():
            self.skip_whitespace()
            return self.get_next_token()

        if current_char.isalnum():
            return self.word()

        # if current_char.isdigit():
        #     return self.number()
        
        if current_char == "'" or current_char == '"':
            return self.string()
        
        if current_char in ['+', '-', '*', '/']:
            return self.operator()

        self.error()

    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.advance()

    def word(self):
        result = ''
        while self.pos < len(self.text) and (self.text[self.pos].isalnum()):
            result += self.text[self.pos]
            self.advance()
        if all([c.isdigit() or c == '.' for c in result]) and result.count('.') < 2:
            return Token('NUMBER', result)
        
        
        return Token('WORD', result)

    # def number(self):
    #     result = ''
    #     char = self.text[self.pos]
    #     while self.pos < len(self.text) and (char.isdigit() or (char == '.' and not '.' in result)):
    #         result += self.text[self.pos]
    #         self.advance()
    #     if self.pos < len(self.text) and 
    #     return Token('NUMBER', result)

    def string(self):
        result = ''
        result += self.text[self.pos]
        self.advance()
        while self.pos < len(self.text) and self.text[self.pos] != result[0]:
            result += self.text[self.pos]
            self.advance()
        
        result += self.text[self.pos]
        self.advance()
        return Token('STRING', result)
    
    def operator(self):
        self.advance()
        return Token('OPERATOR', self.text[self.pos - 1])

    def error(self):
        raise Exception('Invalid character')

    def tokenize(self):
        tokens = []
        while (token := self.get_next_token()).type != 'EOF':
            tokens.append(token)
        return tokens
