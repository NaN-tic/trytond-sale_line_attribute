# This file is part of the sale_line_attribute module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta

from trytond.model import fields
from trytond.pyson import Bool, Eval, Not


__all__ = ['SaleLine']
__metaclass__ = PoolMeta


class SaleLine:
    __name__ = 'sale.line'
    attributes = fields.Dict('product.attribute', 'Attributes',
        domain=[
            ('sets', '=', Eval('attribute_set')),
            ],
        depends=['attribute_set'])
    attribute_set = fields.Many2One('product.attribute.set', 'Attribute Set')

    @fields.depends('attribute_set', 'product')
    def on_change_product(self):
        super(SaleLine, self).on_change_product()
        if (not self.attribute_set and self.product
                and getattr(self.product, 'attribute_set', None)):
            self.attribute_set = self.product.attribute_set.id

    @classmethod
    def view_attributes(cls):
        return super(SaleLine, cls).view_attributes() + [
            ('//page[@id="attributes"]', 'states', {
                    'invisible': Not(Bool(Eval('attribute_set', 0))),
                    })]
