# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductPublicCategory(models.Model):
    _name = "product.size.guide.template"
    
    name = fields.Char(string='Name',required=True,translate=True)
    size_guide_image = fields.Binary(string='Size guide image',required=True)
    size_guide_description = fields.Text(string='Description',required=True,translate=True)
    size_guide_id = fields.Many2one('product.size.guide', string='Size Guide')
    size_guide_line_ids = fields.One2many('product.size.guide.line', 'product_tmpl_id', 'Product Size Guide')
    
