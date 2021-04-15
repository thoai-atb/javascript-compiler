from .error import *

class Number:
    def __init__ (self, value):
        self.value = value
        self.set_pos()
        self.set_context()
    
    def set_pos(self, start_pos=None, end_pos=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def copy(self):
        return Number(self.value).set_context(self.context).set_pos(self.start_pos, self.end_pos)

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
                    other.start_pos, other.end_pos, "Division by zero", self.context
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

    def __repr__ (self):
        return str(self.value)