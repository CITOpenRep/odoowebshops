# -*- coding: utf-8 -*-
"""
    This model is used to create a boolean social sharing options.
"""
import base64
from odoo import fields, models, tools, api
from odoo.modules.module import get_resource_path

class res_config(models.TransientModel):
    _inherit = "res.config.settings"

    is_lazy_load = fields.Boolean(string='Lazyload', related='website_id.is_lazy_load', readonly=False,
                                 help="Lazy load will be enabled.")
    lazy_load_image = fields.Binary(string='Lazyload Image', related='website_id.lazy_load_image', readonly=False,
                                   help="Display this image while lazy load applies.")

    @api.onchange('is_lazy_load')
    def get_value_icon_lazy_load(self):
        if self.is_lazy_load == False:
            img_path = get_resource_path('emipro_theme_lazy_load', 'static/src/img/Lazyload.gif')
            with tools.file_open(img_path, 'rb') as f:
                self.lazy_load_image = base64.b64encode(f.read())

