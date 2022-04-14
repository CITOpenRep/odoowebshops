# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductLabel(models.Model):
    _name="product.label" 
    _description = "Product Label"  
    
    name=fields.Char("Name",required=True,translate=True)
    
