from .error import *

class Value:
    def __init__ (self, value=None):
        self.value = value
        self.set_pos()
        self.set_context()
    
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError(
            self.pos_start, other.pos_end,
            'Illegal Operation',
            self.context
        )

class Function(Value):
    def __init__(self, name, body_node, arg_names):
        super().__init__()
        self.name = name or '<anonymous>'
        self.body_node = body_node
        self.arg_names = arg_names
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__ (self):
            return f"<function {self.name}>"
        
class Number(Value):
    def __init__ (self, value):
        super().__init__(value)

    def copy(self):
        return Number(self.value).set_context(self.context).set_pos(self.pos_start, self.pos_start)

    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None # error
    
    def sub(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
    
    def mult(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
    
    def div(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end, "Division by zero", self.context
                )
            return Number(self.value / other.value).set_context(self.context), None
    
    def pow(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None

    def compare_ee(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None

    def compare_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
    
    def compare_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
    
    def compare_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
    
    def compare_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None

    def compare_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None

    def bool_and(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
    
    def bool_or(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
    
    def bool_not(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    #################

    def is_true(self):
        return self.value != 0

    def __repr__ (self):
        return str(self.value)