import base
import lut

ANDCNT=0
ORCNT=0
NORCNT=0
NANDCNT=0
XORCNT=0
XNORCNT=0

def AND(bits, name=None):
    global ANDCNT
    if not name:
        name='AND' + str(ANDCNT)
        ANDCNT+=1

    return lut.LUT(lut.generate_AND(bits), name=name)

def OR(bits, name=None):
    global ORCNT
    if not name:
        name='OR' + str(ORCNT)
        ORCNT+=1

    return lut.LUT(lut.generate_OR(bits), name=name)

def NOR(bits, name=None):
    global NORCNT
    if not name:
        name='NOR' + str(NORCNT)
        NORCNT+=1

    return lut.LUT(lut.generate_NOR(bits), name=name)

def NAND(bits, name=None):
    global NANDCNT
    if not name:
        name='NAND' + str(NANDCNT)
        NANDCNT+=1

    return lut.LUT(lut.generate_NAND(bits), name=name)

def XOR(bits, name=None):
    global XORCNT
    if not name:
        name='XOR' + str(XORCNT)
        XORCNT+=1

    return lut.LUT(lut.generate_XOR(bits), name=name)

def XNOR(bits, name=None):
    global XNORCNT
    if not name:
        name='XNOR' + str(XNORCNT)
        XNORCNT+=1

    return lut.LUT(lut.generate_XNOR(bits), name=name)
