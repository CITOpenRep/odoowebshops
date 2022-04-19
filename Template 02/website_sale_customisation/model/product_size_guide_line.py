# -*- coding: utf-8 -*-

from odoo import fields, models

class ProductSizeGuideLine(models.Model):
    
    _name = "product.size.guide.line"
    _rec_name = 'size_guide_id'

    product_tmpl_id = fields.Many2one('product.size.guide.template', string='Product Category', ondelete='cascade', required=True, index=True)
    size_guide_id = fields.Many2one('product.size.guide', string='Size Guide', ondelete='restrict', required=True, index=True)
    value_ids = fields.Many2many('product.size.guide.value', string='Size Guide Values',required=True)
    