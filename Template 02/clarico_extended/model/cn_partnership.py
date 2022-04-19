from odoo import models, fields


class CNPartnership(models.Model):
    _name = 'cn.partnership'
    _description = 'Partnership Data'

    name = fields.Char()
    email = fields.Char(string="E-mail")
    description = fields.Text()
    is_become_partner = fields.Boolean(string="Become Partner ?", default=False)
    is_organize_event = fields.Boolean(string="Organize Event ?", default=False)
    is_other = fields.Boolean(string="Other ?", default=False)

