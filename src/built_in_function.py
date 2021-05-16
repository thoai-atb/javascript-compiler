from .value import *
import math

class BuiltInFunction(Function):
    def __init__(self, name, num_parameters):
        super().__init__(name)
        self.num_parameters = num_parameters
    
    def parameter_count(self):
        return self.num_parameters
    
    def execute(self, args):
        return None

    def copy(self):
        return self.__class__()

class LogFunction(BuiltInFunction):
    def __init__(self):
        super().__init__('log', 1)
    
    def execute(self, args):
        print(args[0])

class AbsoluteFunction(BuiltInFunction):
    def __init__(self):
        super().__init__('abs', 1)
    
    def execute(self, args):
        if not isinstance(args[0], Number):
            raise Exception("cannot find absolute value of a string")
        return Number(abs(args[0].value))

class CosineFunction(BuiltInFunction):
    def __init__(self):
        super().__init__('cos', 1)
    
    def execute(self, args):
        if not isinstance(args[0], Number):
            raise Exception("cannot find cosine value of a string")
        return Number(math.cos(args[0].value))

class SineFunction(BuiltInFunction):
    def __init__(self):
        super().__init__('sin', 1)
    
    def execute(self, args):
        if not isinstance(args[0], Number):
            raise Exception("cannot find sine value of a string")
        return Number(math.sin(args[0].value))

class SquareRootFunction(BuiltInFunction):
    def __init__(self):
        super().__init__('sqrt', 1)
    
    def execute(self, args):
        if not isinstance(args[0], Number):
            raise Exception("cannot find square root value of a string")
        return Number(math.sqrt(args[0].value))