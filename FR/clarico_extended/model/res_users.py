# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    last_name = fields.Char(string='Last name')
    date_of_birth = fields.Date(string='Date of birth')
    telephone = fields.Char(string='Telephone')
