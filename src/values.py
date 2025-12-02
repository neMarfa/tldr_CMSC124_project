from constants import *

# DITO ilalagay lahat ng operations
# Operations related to numbers
class NumOps:
    def __init__(self, value):
        self.value = value
        self.set_pos()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def negation(self):
        return NumOps(self.value * -1)

    def sum_of(self, other):
        if isinstance(other, NumOps):
            if checkFloat(str(other.value)) == "INT" and checkFloat(str(self.value)) == "INT":
                return NumOps(int(self.value + other.value))
            else:
                return NumOps(float(self.value + other.value))
    def diff_of(self, other):
        if isinstance(other, NumOps):
            if checkFloat(str(other.value)) == "INT" and checkFloat(str(self.value)) == "INT":
                return NumOps(int(self.value - other.value))
            else:
                return NumOps(float(self.value - other.value))

    def produkt_of(self, other):
        if isinstance(other, NumOps):
            if checkFloat(str(other.value)) == "INT" and checkFloat(str(self.value)) == "INT":
                return NumOps(int(self.value * other.value))
            else:
                return NumOps(float(self.value * other.value))

    def quoshunt_of(self, other):
        if isinstance(other, NumOps):
            if checkFloat(str(other.value)) == "INT" and checkFloat(str(self.value)) == "INT":
                return NumOps(int(self.value / other.value))
            else:
                return NumOps(float(self.value / other.value))

    def mod_of(self, other):
        if isinstance(other, NumOps):
            if checkFloat(str(other.value)) == "INT" and checkFloat(str(self.value)) == "INT":
                return NumOps(int(self.value % other.value))
            else:
                return NumOps(float(self.value % other.value))

    def bigger_of(self, other):
        if isinstance(other, NumOps):
            return NumOps(self.value > other.value)

    def smallr_of(self, other):
        if isinstance(other, NumOps):
            return NumOps(self.value < other.value)

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)

class StringOps:
    def __init__(self, value):
        self.value = str(value)
        self.pos_start = None
        self.pos_end = None

    def set_pos(self, pos_start = None, pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

class NoobOps:
    def __init__(self):
        self.value = None
        self.pos_start = None
        self.pos_end = None

    def set_pos(self, pos_start = None, pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def __str__(self):
        return "NOOB"

    def __repr__(self):
        return "NOOB"

class BoolOps:
    def __init__(self, value):
        # Convert to boolean: True for WIN/True, False for FAIL/False
        self.value = bool(value) if isinstance(value, bool) else (value == "WIN")
        self.pos_start = None
        self.pos_end = None

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def __str__(self):
        return "WIN" if self.value else "FAIL"

    def __repr__(self):
        return f"WIN" if self.value else f"FAIL"

# This is just a function class that will be used for traversal
class Function():
    def __init__(self, name, body, parameters):
        self.name = name
        self.body = body
        self.parameters = parameters

    def __repr__(self):
        return f"<function {self.name}>"