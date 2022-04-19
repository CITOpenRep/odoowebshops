# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class productTemplate(models.Model):

    _inherit = 'product.template'

    low_stock_count = fields.Integer("Low stock quantity", default=0,
                                        help='Set the low stock quantity based on this provide notification to configured user')

class productProduct(models.Model):

    _inherit = 'product.product'

    low_stock_count = fields.Integer("Low stock quantity", default=0,
                                        help='Set the low stock quantity based on this provide notification to configured user')


