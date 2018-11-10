# PyECCArithmetic

This package provides basic arithmethic point operations on elliptic curves. The following operations for points are available:
* addition
* subtraction
* multiplication
* division
* order of point (for fair points)
* inversion

The following curves are already implemented:
* secp224r1
* secp256r1
* secp384r1
* secp521r1
* brainpoolP160r1
* brainpoolP192r1
* brainpoolP224r1
* brainpoolP256r1
* brainpoolP320r1
* brainpoolP384r1
* brainpoolP512r1

It is also possible to define your own curve.

## Installation
```
pip install PyECCArithmetic
```

## Addition
```python
from PyECCArithmetic import Point
from PyECCArithmetic import Curve

p = Point(x_1, y_1, curve=Curve.secp256r1())
q = Point(x_2, y_2, curve=Curve.secp256r1())

z = p + q # z is a new point
```

## Subtraction
```python
from PyECCArithmetic import Point

p = Point(x_1, y_1) # curve defaults to Curve.secp256r1()
q = Point(x_2, y_2)

z = p - q # z = p + (-q), z is a point
```

## Multiplication
Multiplication is realised with the double and add algorithm.
```python
from PyECCArithmetic import Point

p = Point(x_1, y_1) # curve defaults to Curve.secp256r1()

z = p * 3 # z is a new point
```

## Division
```python
from PyECCArithmetic import Point

p = Point(x_1, y_1) # curve defaults to Curve.secp256r1()
q = Point(x_2, y_2)

z = p / q # z is int, such that z * q == p
```

## Order calculation
```python
from PyECCArithmetic import Point

p = Point(x_1, y_1) # curve defaults to Curve.secp256r1()
order = p.order(timeout=5) # tries to calculate the order for maximal timeout seconds 
```

## Custom curve definition
```python
from PyECCArithmetic import Curve

# Only curves defined as Weierstrass equation are supported
# y^2 = x^3 + a * x + b mod p
c = Curve(a, b, p, name='optional')
```



