# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.translate import html_translate

class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"
     
    content = fields.Html('Content', translate=html_translate)
    website_published = fields.Boolean("Website Published",default=True)