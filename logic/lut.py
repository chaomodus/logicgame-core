import base

class LUT(base.Base):
    basename='LUT'

    def __init__(self, table, name=None):
        base.Base.__init__(self, name)
        self.table = table

        self._add_pin('OUT', base.PIN_DIRECTION_OUT)
        self.in_pins = list()

        for p in range(len(table.keys()[0])):
            self._add_pin('IN%d' % p, base.PIN_DIRECTION_IN)
            self.in_pins.append('IN%d' % p)

    def execute(self, time):
        key = tuple([self.next_pin_states[p] for p in self.in_pins])

        self.next_pin_states['OUT'] = self.table[key]

def generate_table(inputs, function):
    table = dict()

    for addr in base.addr_range(inputs):
        table[addr] = function(addr)

    return table

def generate_AND(inputs):
    def multi_and(bits):
        return reduce(lambda x, y: x & y, bits)

    return generate_table(inputs, multi_and)

def generate_OR(inputs):
    def multi_or(bits):
        return reduce(lambda x, y: x | y, bits)

    return generate_table(inputs, multi_or)


def generate_XOR(inputs):
    def multi_xor(bits):
        return reduce(lambda x, y: x ^ y, bits)

    return generate_table(inputs, multi_xor)

def generate_NOR(inputs):
    def multi_nor(bits):
        return reduce(lambda x, y: x | y, bits) ^1

    return generate_table(inputs, multi_nor)

def generate_XNOR(inputs):
    def multi_xnor(bits):
        return reduce(lambda x, y: x ^ y, bits) ^ 1

    return generate_table(inputs, multi_xnor)


def generate_NAND(inputs):
    def multi_nand(bits):
        return reduce(lambda x, y: x & y, bits) ^ 1

    return generate_table(inputs, multi_nand)
