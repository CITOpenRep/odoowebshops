# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResPartner(models.Model):

    _inherit = 'res.partner'

    @api.multi
    def get_base_url(self):
        """Get the base URL for the current partner from custom param"""
        self.ensure_one()
        return self.env['ir.config_parameter'].sudo().get_param('web.base.website.url') or self.env['ir.config_parameter'].sudo().get_param('web.base.url')