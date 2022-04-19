# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_guest_partner = fields.Boolean("Is a Guest Partner")