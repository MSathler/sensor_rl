'''
from pyrep.robots.mobiles.mobile_base import MobileBase


class Espeleo(MobileBase):
    def __init__(self, count: int = 0):
        super().__init__(count, 4, 'Espeleo')
'''
from pyrep.robots.mobiles.nonholonomic_base import NonHolonomicBase


class Espeleo(NonHolonomicBase):
    def __init__(self, count: int = 0):
        super().__init__(count, 2, 'Espeleo')
