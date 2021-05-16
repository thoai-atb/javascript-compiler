from lib.string_with_arrows import string_with_arrows

class Error:
    def __init__ (self, pos_start, pos_end, name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.name = name
        self.details = details

    def set_pos(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def as_string (self):
        result =  f'{self.name}: {self.details}\n'
        result += f'File {self.pos_start.file_name}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.file_txt, self.pos_start, self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__ (self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class ExpectedCharError(Error):
    def __init__ (self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)

class ExpectedStmtError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Statement', details)

class InvalidSyntaxError(Error):
    def __init__ (self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


class RTError(Error):
    def __init__ (self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_string (self):
        result = self.generate_traceback()
        result +=  f'{self.name}: {self.details}\n'
        result += '\n\n' + string_with_arrows(self.pos_start.file_txt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context
        while ctx:
            result = f' File {pos.file_name}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result 
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        return 'Traceback (last is the most recent call):\n' + result
