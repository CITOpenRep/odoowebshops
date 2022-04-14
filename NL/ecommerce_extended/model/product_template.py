# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class ProductTemplate(models.Model):

    _inherit = ['product.template']

    website_sale_description = fields.Text(
        'Website Description', translate=True,
        help="A description of the Product that you want to display as short descrpition to your customers. ")

