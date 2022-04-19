# -*- coding: utf-8 -*-
from odoo import fields, models

class Website(models.Model):
    _inherit = "website"

    is_lazy_load = fields.Boolean(string='Lazyload', help="Lazy load will be enabled", readonly=False)
    lazy_load_image = fields.Binary('Lazyload Image', help="Display this image while lazy load applies.",
                                    readonly=False)