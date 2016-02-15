# This file is part of the sale_line_attribute module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class SaleLineAttributeTestCase(ModuleTestCase):
    'Test Sale Line Attribute module'
    module = 'sale_line_attribute'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SaleLineAttributeTestCase))
    return suite
