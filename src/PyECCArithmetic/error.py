# coding=utf-8


class ECCError(Exception):
    def __init__(self, message):
        self.message = message


class PointsOnDifferentCurveError(ECCError):
    def __init__(self):
        super().__init__('The two points are on a different curve!')
