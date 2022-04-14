# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"
    
    is_size_guide = fields.Boolean('Website Published')
    size_guide_template = fields.Many2one('product.size.guide.template', string='Size Guide')