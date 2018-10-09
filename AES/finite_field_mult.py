### copy from python fiddle
### http://pythonfiddle.com/binary-finite-field-multiplication/

from functools import reduce

# constants used in the multGF2 function
mask1 = mask2 = polyred = None
class finite_field_mult:
    def __init__(self, degree, irPoly):
        """Define parameters of binary finite field GF(2^m)/g(x)
           - degree: extension degree of binary field
           - irPoly: coefficients of irreducible polynomial g(x)
        """
        self.degree = degree
        self.irPoly = irPoly

        def i2P(sInt):
            """Convert an integer into a polynomial"""
            return [(sInt >> i) & 1
                    for i in reversed(range(sInt.bit_length()))]

        global mask1, mask2, polyred
        mask1 = mask2 = 1 << degree
        mask2 -= 1
        polyred = reduce(lambda x, y: (x << 1) + y, i2P(irPoly)[1:])

    def multGF2(p1, p2):
        """Multiply two polynomials in GF(2^m)/g(x)"""
        p = 0
        while p2:
            if p2 & 1:
                p ^= p1
            p1 <<= 1
            if p1 & mask1:
                p1 ^= polyred
            p2 >>= 1
        return p & mask2


'''
    if __name__ == "__main__":
        # Define binary field GF(2^3)/x^3 + x + 1
        setGF2(3, 0b1011)

        # Evaluate the product (x^2 + x + 1)(x^2 + 1)
        print(multGF2(0b111, 0b101))

        # Define binary field GF(2^8)/x^8 + x^4 + x^3 + x + 1
        # (used in the Advanced Encryption Standard-AES)
        setGF2(8, 0b100011011)

        # Evaluate the product (x^7)(x^7 + x + 1)
        print((multGF2(0b10000000, 0b10000011)))
'''