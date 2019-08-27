# coding=utf-8

import unittest
from PyECCArithmetic import *


class TestECC_SmallCurve(unittest.TestCase):

    def setUp(self):
        x_coords = [5, 6, 10, 3,  9, 16, 0, 13, 7,  7, 13,  0, 16, 9,  3, 10,  6,  5]
        y_coords = [1, 3,  6, 1, 16, 13, 6,  7, 6, 11, 10, 11,  4, 1, 16, 11, 14, 16]
        self.curve = Curve(2, 2, 17, "test")
        self.results = [Point(x, y, self.curve) for x, y in zip(x_coords, y_coords)]
        self.pointOrder = 19


    def test_add(self):
        P = self.results[0]
        temp = P

        for i in range(1, len(self.results)):
            temp = temp + P
            self.assertEqual(self.results[i], temp)


    def test_infinity(self):
        P = self.results[0]
        o = Point(None, None, self.curve)

        # o is the infinity point, P is not
        self.assertFalse(P.isInfinityPoint)
        self.assertTrue(o.isInfinityPoint)
        self.assertEqual(o, Point.infinity())
        self.assertTrue(o.isOnCurve)
        self.assertEqual(o, P - P)
        self.assertEqual(P, P + o)
        self.assertEqual(P, o + P)
        self.assertEqual(o, o.inverse())
        self.assertTrue(o.isInverseOf(o))
        self.assertFalse(o.isInverseOf(P))

        # Changing o should not affect the staticmethod Point.infinity()
        o.x = 42
        self.assertFalse(o.isInfinityPoint)
        self.assertNotEqual(o, Point.infinity())


    def test_infinityCalculation(self):
        P = self.results[0]
        
        self.assertEqual(P * self.pointOrder, Point.infinity())
        self.assertEqual(P * (self.pointOrder + 1), P)
        self.assertEqual(P * (self.pointOrder - 1), -P)


    def test_mul(self):
        P = self.results[0]

        for i in range(1, 2 * len(self.results)):
            if i % self.pointOrder == 0:
                continue

            temp = P * i
            self.assertEqual(self.results[(i - 1) % self.pointOrder], temp)


    def test_mul_neg(self):
        P = self.results[0]

        for i in range(1, 2 * len(self.results)):
            if i % self.pointOrder == 0:
                continue

            temp = P * -i
            self.assertEqual(-self.results[(i - 1) % self.pointOrder], temp)


    def test_order(self):
        P = self.results[0]
        self.assertEqual(self.pointOrder, P.calcOrder())


    def test_inverse(self):
        P = self.results[0]
        self.assertTrue(P.inverse().isInverseOf(P))
        self.assertTrue(P.isInverseOf(P.inverse()))


    def test_div(self):
        for i in range(1, len(self.results)):
            self.assertEqual(i + 1, self.results[i] / self.results[0])


    def test_neg(self):
        P = self.results[0]
        self.assertEqual(P.inverse(), -P)


    def test_sub(self):
        P = self.results[0]

        for i in range(2, len(self.results)):
            self.assertEqual(self.results[i - 1], self.results[i] - P)


class TestECC_secp256r1(TestECC_SmallCurve):

    def setUp(self):
        x_coords = [
            13468892314898525371610240502770272266198042546749343338295390121507516526697,
            44933197154424625414396420674687404537285215820543916478213542852252462680301,
            87292861620245941763729224116377105674049842524084350006092076506713177451999,
            19902534246131648885444051015555008248385969626843434670088771094078517207343,
            55297356144447711988562605973105674083355310838692901373664323015904438999936,
            55297356144447711988562605973105674083355310838692901373664323015904438999936,
            19902534246131648885444051015555008248385969626843434670088771094078517207343,
            87292861620245941763729224116377105674049842524084350006092076506713177451999,
            44933197154424625414396420674687404537285215820543916478213542852252462680301,
            13468892314898525371610240502770272266198042546749343338295390121507516526697
        ]

        y_coords = [
            36799441595734733996700652843872575060981397705837134061659802762143144431184,
            100961064024776030781588915896083152763221482166455775822127486804206065032758,
            92699602807030384482000073880669081583972081757725905966300882919869713216044,
            50437526861842523234944141349987683196667410625883078348524629523061718453195,
            53334826727094344316582174118222090970470814428122392368453287820466827148700,
            62457262483261904446115272831185482559615328987167921827080343488400270705251,
            65354562348513725527753305599419890333418732789407235847009001785805379400756,
            23092486403325864280697373068738491946114061657564408229232748388997384637907,
            14831025185580217981108531053324420766864661248834538373406144504661032821193,
            78992647614621514765996794105534998469104745709453180133873828546723953422767
        ]

        self.assertEqual(len(x_coords), len(y_coords))

        self.curve = Curve.secp256r1()
        self.results = [Point(x, y, self.curve) for x, y in zip(x_coords, y_coords)]
        self.pointOrder = 11


class TestECC_General(unittest.TestCase):

    def setUp(self):
        self.curve1 = Curve.secp256r1()
        self.curve2 = Curve(2, 2, 17)

        self.P1 = Point(13468892314898525371610240502770272266198042546749343338295390121507516526697,
                        36799441595734733996700652843872575060981397705837134061659802762143144431184, self.curve1)
        self.P2 = Point(5, 1, self.curve2)


    def test_addPointsOnDifferentCurve(self):
        with self.assertRaises(PointsOnDifferentCurveError):
            P3 = self.P1 + self.P2


    def test_propertyResets_x(self):
        self.assertEqual(19, self.P2.calcOrder())
        self.P2.x = 6
        self.assertNotEqual(19, self.P2.calcOrder())


    def test_propertyResets_y(self):
        self.assertEqual(19, self.P2.calcOrder())
        self.P2.y = 9
        self.assertNotEqual(19, self.P2.calcOrder())


    def test_propertyResets_curve(self):
        self.assertEqual(19, self.P2.calcOrder())
        self.P2.curve = self.curve1

        with self.assertRaises(TimeoutError):
            self.P2.calcOrder(timeout=0.1)
