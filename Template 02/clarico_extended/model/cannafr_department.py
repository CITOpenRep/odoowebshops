# -*- coding: utf-8 -*-
"""
    This model is used to create a website events field
"""
from odoo import fields, models


class CannaFrDepartment(models.Model):

    _name = "cannafr.department"
    _description = "Canna FR Department"
    _inherit = ['website.published.multi.mixin']

    name = fields.Char(string="Name", required=True, translate=True)
    image = fields.Binary(string='Department Image')
    team_line_ids = fields.One2many('cannafr.department.team.line', 'department_id', 'Lines')

class CannaFrDepartmentTeamLine(models.Model):

    _name = "cannafr.department.team.line"
    _description = "Canna FR Depaerment Team Lines"

    department_id = fields.Many2one('cannafr.department', string='Canna Department', ondelete='cascade', index=True)
    team_id = fields.Many2one('cannafr.team', string='Team', ondelete='restrict', required=True, index=True)
