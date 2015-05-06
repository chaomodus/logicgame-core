from .base import staticvariable
from . import lut


@staticvariable('cnt', 0)
def AND(bits, name=None):
    if not name:
        name = 'AND' + str(AND.cnt)
        AND.cnt += 1

    return lut.LUT(lut.generate_AND(bits), name=name)


@staticvariable('cnt', 0)
def OR(bits, name=None):
    if not name:
        name = 'OR' + str(OR.cnt)
        OR.cnt += 1

    return lut.LUT(lut.generate_OR(bits), name=name)


@staticvariable('cnt', 0)
def NOR(bits, name=None):
    if not name:
        name = 'NOR' + str(NOR.cnt)
        NOR.cnt += 1

    return lut.LUT(lut.generate_NOR(bits), name=name)


@staticvariable('cnt', 0)
def NAND(bits, name=None):
    if not name:
        name = 'NAND' + str(NAND.cnt)
        NAND.cnt += 1

    return lut.LUT(lut.generate_NAND(bits), name=name)


@staticvariable('cnt', 0)
def XOR(bits, name=None):
    if not name:
        name = 'XOR' + str(XOR.cnt)
        XOR.cnt += 1

    return lut.LUT(lut.generate_XOR(bits), name=name)


@staticvariable('cnt', 0)
def XNOR(bits, name=None):
    if not name:
        name = 'XNOR' + str(XNOR.cnt)
        XNOR.cnt += 1

    return lut.LUT(lut.generate_XNOR(bits), name=name)
