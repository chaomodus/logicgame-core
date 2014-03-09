import base
import lut

ANDCNT=0
ORCNT=0
NORCNT=0
NANDCNT=0
XORCNT=0
XNORCNT=0

def AND(bits, name=None):
    if not name:
        name='AND' + str(ANDCNT)
        ANDCNT+=1

    return lut.LUT(lut.generate_AND(bits), name=name)

def OR(bits, name=None):
    if not name:
        name='OR' + str(ORCNT)
        ORCNT+=1

    return lut.LUT(lut.generate_OR(bits), name=name)

def NOR(bits, name=None):
    if not name:
        name='NOR' + str(NORCNT)
        NORCNT+=1

    return lut.LUT(lut.generate_NOR(bits), name=name)

def NAND(bits, name=None):
    if not name:
        name='NAND' + str(NANDCNT)
        NANDCNT+=1

    return lut.LUT(lut.generate_NAND(bits), name=name)
