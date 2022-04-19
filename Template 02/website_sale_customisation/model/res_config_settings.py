# -*- coding: utf-8 -*-

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_order_comment_feature = fields.Boolean(string="Do you want to disable order comment feature?",related='website_id.is_order_comment_feature',)
