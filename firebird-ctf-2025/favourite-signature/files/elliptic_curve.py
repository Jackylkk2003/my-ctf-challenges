# Point is a tuple of (x, y, k). If the point is not a point at infinity, k = 1.
# If the point is a point at infinity, (x, y, k) = (0, 1, 0)


ZERO = (0, 1, 0)


def xy(point):
    x, y, _ = point
    return x, y


class Curve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def is_point(self, point):
        if point == ZERO:
            return True
        x, y = xy(point)
        return (y**2 - x**3 - self.a * x - self.b) % self.p == 0

    def add(self, A, B):
        assert self.is_point(A) and self.is_point(B)
        if A == ZERO:
            return B
        if B == ZERO:
            return A
        x1, y1 = xy(A)
        x2, y2 = xy(B)
        if x1 == x2 and y1 != y2:
            return ZERO
        if A != B:
            m = (y2 - y1) * pow(x2 - x1, -1, self.p) % self.p
        else:
            m = (3 * x1**2 + self.a) * pow(2 * y1, -1, self.p) % self.p
        x3 = (m**2 - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p
        return (x3, y3, 1)

    def mul(self, n, P):
        assert self.is_point(P)
        R = ZERO
        for i in range(n.bit_length()):
            if n & (1 << i):
                R = self.add(R, P)
            P = self.add(P, P)
        return R


secp256k1 = Curve(0, 7, 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1)
G = (
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    1,
)
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
