# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_brand_value_consider = fields.Boolean(related="website_id.is_brand_value_consider",string="Brand Value In Product Popularity",readonly=False,
                            help="Consider brand value in product popularity method.")