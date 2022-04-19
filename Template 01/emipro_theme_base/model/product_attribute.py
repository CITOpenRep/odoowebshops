# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductAttribute(models.Model):
    _inherit = ['product.attribute']
    
    is_quick_filter = fields.Boolean(string='Quick Filter')