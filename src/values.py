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
            return NumOps(self.value + other.value)

    def diff_of(self, other):
        if isinstance(other, NumOps):
            return NumOps(self.value - other.value)

    def produkt_of(self, other):
        if isinstance(other, NumOps):
            return NumOps(self.value * other.value)

    def quoshunt_of(self, other):
        if isinstance(other, NumOps):
            return NumOps(self.value / other.value)

    def mod_of(self, other):
        if isinstance(other, NumOps):
            return NumOps(self.value % other.value)

    def bigger_of(self, other):
        if isinstance(other, NumOps):
            return NumOps(self.value > other.value)

    def smallr_of(self, other):
        if isinstance(other, NumOps):
            return NumOps(self.value < other.value)