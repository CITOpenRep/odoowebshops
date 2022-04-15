from odoo import api, fields, models


class MassMailing(models.Model):
    _inherit = 'mail.mass_mailing.list'

    is_website_mailing = fields.Boolean(string="Is website mailing")
