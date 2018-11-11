# coding=utf-8
import time
from .curve import Curve
from .error import PointsOnDifferentCurveError


def _mul_inv(a, b):
    a = a % b
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


class Point(object):
    """
    A point on a ellitic curve which can be represented by a
    Weierstrass equation y^2 = x^3 + a * x + b mod p
    """


    def __init__(self, x: int, y: int, curve: Curve = Curve.secp256r1()):
        self._x = x
        self._y = y
        self._curve = curve
        self._order = None
        self._isOnCurve = None


    def _reset(self):
        self._order = None
        self._isOnCurve = None


    @property
    def x(self):
        return self._x


    @x.setter
    def x(self, value):
        self._x = value
        self._reset()


    @property
    def y(self):
        return self._y


    @y.setter
    def y(self, value):
        self._y = value
        self._reset()


    @property
    def curve(self):
        return self._curve


    @curve.setter
    def curve(self, value: Curve):
        self._curve = value
        self._reset()


    @property
    def isOnCurve(self):
        """
        Checks if a point is on the selected curve by evaluating the
        Weierstrass equation of the curve.
        :return: True or False
        :rtype: bool
        """
        if self._isOnCurve:
            return self._isOnCurve

        return ((self.y ** 2) % self.curve.p) == (self.x ** 3 + self.curve.a * self.x + self.curve.b) % self.curve.p


    def calcOrder(self, timeout=10):
        """
        Tries to calculate the order of a point on an elliptic curve in max. `timeout` seconds.
        :param timeout: Max calculation time
        :return: smallest number n that e = n * P mod p, with e as the neutral element of the group
        :rtype: int
        """
        if self._order:
            return self._order

        order = 2
        P = self + self

        maxExecTime = time.time() + timeout
        while not P.isInverseOf(self):
            if time.time() > maxExecTime:
                raise TimeoutError('Calculation of the order took too long.')
            P = P + self
            order += 1

        self._order = order + 1
        return self._order


    def isInverseOf(self, other):
        """
        Checks if *self* is the inverse point of *other*
        :param other: Another Point
        :type other: Point
        :return: True or False
        :rtype: bool
        """
        if not isinstance(other, Point):
            raise ValueError('First argument has to be a Point')
        if self.curve != other.curve:
            raise PointsOnDifferentCurveError()

        return self.x == other.x and self.y == (-other.y % self.curve.p)


    def inverse(self):
        """
        Calculates the inverse point of *self*
        :return: The inverse point of *self*
        :rtype: Point
        """
        return Point(self.x, (-self.y % self.curve.p), self.curve)


    def __str__(self):
        onCurve_s = 'Not on Curve ' + self.curve.name
        if self.isOnCurve:
            onCurve_s = 'On Curve ' + self.curve.name

        return "(\n X: {0},\n Y: {1}\n) {2}".format(self.x, self.y, onCurve_s)


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __add__(self, other):
        """
        Add two points. Uses the equations listed in `Understanding Cryptography` by Christof Paar and Jan Pelzl.
        :param other: A second Point
        :type other: Point
        :return: new_point = self + other
        :rtype: Point
        """
        if self.curve != other.curve:
            raise PointsOnDifferentCurveError()

        if self == other:
            s = ((3 * self.x ** 2 + self.curve.a) * _mul_inv(2 * self.y, self.curve.p)) % self.curve.p
        else:
            s = ((other.y - self.y) * _mul_inv(other.x - self.x, self.curve.p)) % self.curve.p

        x_3 = (s ** 2 - self.x - other.x) % self.curve.p
        y_3 = (s * (self.x - x_3) - self.y) % self.curve.p

        return Point(x_3, y_3, self.curve)


    def __neg__(self):
        return self.inverse()


    def __sub__(self, other):
        return self + -other


    def __mul__(self, scalar: int):
        """
        Multiplies a point with a scalar. Uses the double and add approach to perform the multiplication.
        :param scalar: A factor to multiply the point with.
        :type scalar: int
        :return: new_point = self * scalar
        :rtype: Point
        """

        # lossless conversion to int possible?
        temp_scalar = int(scalar)
        if temp_scalar == scalar:
            scalar = temp_scalar

        if not isinstance(scalar, int):
            raise ValueError('Point multiplication is only supported with a scalar of type int.')

        negative = False
        if scalar < 0:
            negative = True
            scalar *= -1

        Q = self
        index = 1
        n_bin = bin(scalar).replace('0b', '')

        while index < len(n_bin):
            Q = Q + Q

            if n_bin[index] == '1':
                Q = Q + self

            index += 1

        if negative:
            Q = -Q
        return Q


    def __rmul__(self, scalar: int):
        return self.__mul__(scalar)


    def __truediv__(self, other, timeout=10):
        """
        Divides two points.
        :param other: Another point.
        :type other: Point
        :param timeout: Max calculation time
        :type timeout: int
        :return: scalar = self / other, such that self = other * scalar
        :rtype: int
        """
        if not isinstance(other, Point):
            raise ValueError('Point division is only supported with another point.')

        temp = other
        res = 1
        maxCalcTime = time.time() + timeout
        while temp != self:
            if time.time() > maxCalcTime:
                raise TimeoutError('Maximum calculation time exceeded.')
            temp = temp + other
            res += 1

        return res


    def __copy__(self):
        return Point(self.x, self.y, self.curve)


    def __repr__(self):
        return '<ECC.Point, _x = {0}, _y = {1}, _curve = {2}>'.format(self.x, self.y, self.curve.name)
