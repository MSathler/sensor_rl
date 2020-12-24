'''
from pyrep.robots.mobiles.mobile_base import MobileBase


class P3dx(MobileBase):
    def __init__(self, count: int = 0):
        super().__init__(count, 2, 'p3dx')

'''
from pyrep.robots.mobiles.nonholonomic_base import NonHolonomicBase


class P3dx(NonHolonomicBase):
    def __init__(self, count: int = 0):
        super().__init__(count, 2, 'p3dx')
