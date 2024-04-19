import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
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

        if current_char.isalpha():
            return self.word()

        if current_char.isdigit():
            return self.number()
        
        if current_char == "'" or current_char == '"':
            return self.string()

        self.error()

    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.advance()

    def word(self):
        result = ''
        while self.pos < len(self.text) and (self.text[self.pos].isalpha() or self.text[self.pos] in ['"', ' ']):
            result += self.text[self.pos]
            self.advance()
        return Token('WORD', result)

    def number(self):
        result = ''
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            result += self.text[self.pos]
            self.advance()
        return Token('NUMBER', result)

    def string(self):
        result = ''
        character = self.text[self.pos]
        self.advance()
        while self.pos < len(self.text) and self.text[self.pos] != character:
            result += self.text[self.pos]
            self.advance()
        
        return Token('STRING', result)

    def error(self):
        raise Exception('Invalid character')

    def tokenize(self):
        tokens = []
        while (token := self.get_next_token()).type != 'EOF':
            tokens.append(token)
        return tokens
