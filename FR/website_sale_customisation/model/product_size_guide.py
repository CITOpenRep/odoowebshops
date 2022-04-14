# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductSizeGuide(models.Model):
    _name='product.size.guide'
    
    name = fields.Char('Name',required=True)
    value_ids = fields.One2many('product.size.guide.value', 'value_id', 'Values', copy=True)
