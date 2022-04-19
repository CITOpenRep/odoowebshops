from odoo import api, fields, models, _

class res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    matomo_id = fields.Char(related="website_id.matomo_id", string="Set the Matomo Id to trace the order.",
                                          readonly=False)
    matomo_url = fields.Char(related="website_id.matomo_url", string="Matomo url",
                            readonly=False)

