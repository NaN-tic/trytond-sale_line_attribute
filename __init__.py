# This file is part of the sale_line_attribute module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .sale import *

def register():
    Pool.register(
        SaleLine,
        module='sale_line_attribute', type_='model')
