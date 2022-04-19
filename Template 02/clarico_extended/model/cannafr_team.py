# -*- coding: utf-8 -*-
"""
    This model is used to create a website events field
"""
from odoo import fields, models


class CannaFrTeam(models.Model):

    _name = "cannafr.team"
    _description = "Canna FR Website Team"
    _inherit = ['website.published.multi.mixin']

    name = fields.Char(string="Name", required=True, translate=True)
    title = fields.Char(string="Title", required=True, translate=True)
    icon = fields.Binary(string="Team Icon")
    image = fields.Binary(string="Team Image")
    is_video = fields.Boolean(string='Is Video?', default=False)
    video_url = fields.Char(string="Video url")
    department_id = fields.Many2one("cannafr.department", string="Department")
    description = fields.Html("description", translate=True)
