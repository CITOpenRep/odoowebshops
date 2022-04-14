# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductSizeGuide(models.Model):
    _name='product.size.guide.value'
    
    name = fields.Char('Name',required=True)
    value_id = fields.Many2one('product.size.guide', string='Size Guide Value', ondelete='cascade', required=True, index=True)
    

