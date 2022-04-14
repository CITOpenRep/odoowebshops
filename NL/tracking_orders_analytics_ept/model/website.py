from odoo import api, fields, models, _

class website(models.Model):
    _inherit = "website"

    matomo_id = fields.Char(string="Matomo id")
    matomo_url = fields.Char(string="Matomo Url")