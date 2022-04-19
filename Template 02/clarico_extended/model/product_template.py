# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, timedelta
    
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    is_limited_edition = fields.Boolean(string="Is Limited Edition")
    label_line_ids = fields.One2many('product.label.line', 'product_tmpl_id', 'Product Labels',help="Set the number of product labels")
