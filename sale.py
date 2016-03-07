# This file is part of the sale_line_attribute module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from collections import OrderedDict
from trytond.model import fields
from trytond.pyson import Bool, Eval, Not

from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


try:
    import simplejson as json
except ImportError:
    import json


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
    all_attributes = fields.Function(fields.Text('Attributes'),
        'get_all_attributes')

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

    @classmethod
    def get_all_attributes(cls, lines, name):
        ProductAttribute = Pool().get('product.attribute')
        res = {l.id: '' for l in lines}
        for line in lines:
            party = line.sale and line.sale.party or line.party
            party_lang = None
            if party:
                party_lang = party.lang and party.lang.code
            if not party or not party_lang:
                party_lang = 'en_US'
            with Transaction().set_context({'language': party_lang}):
                attributes = ProductAttribute.search([])
                attributes = {p.name: p for p in attributes}
                translated_line = cls(line.id)
                if translated_line.attributes:
                    for attr in translated_line.attributes:
                        attribute = attributes.get(attr)
                        if attribute:
                            label = attribute.string
                            value = line.attributes[attr]
                            if attribute.type_ != 'boolean' and not value:
                                continue
                            if attribute.type_ == 'selection':
                                value = dict(json.loads(
                                        attribute.selection_json))[value]
                            res[line.id] += ('%s: %s\n' % (label, value))
        return res
