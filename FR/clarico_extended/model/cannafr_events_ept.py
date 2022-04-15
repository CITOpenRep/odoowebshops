# -*- coding: utf-8 -*-
"""
    This model is used to create a website events field
"""
from odoo import fields, models


class CannaFrEventsEpt(models.Model):

    _name = "cannafr.events"
    _order = "sequence"
    _inherit = ['website.published.multi.mixin']
    _description = "Canna FR Website Events"

    name = fields.Char(string="Title", required=True, translate=True)
    subtitle = fields.Char(string="Sub Title", required=True, translate=True)
    image = fields.Binary(string='Events Banner Image')
    # description = fields.Text(string='Description', translate=True)
    description = fields.Html(string='Description', translate=True, sanitize_style=True)
    sequence = fields.Integer(help="Gives the sequence order of News block.", index=True)
    position = fields.Integer(string='Position', default=1)
    is_active = fields.Boolean(string='Is Active?', default=True)
