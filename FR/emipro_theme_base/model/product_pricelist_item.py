# -*- coding: utf-8 -*-

from odoo import api, fields, models
    
class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"
    
    offer_msg = fields.Char(string="Offer Message",translate=True)