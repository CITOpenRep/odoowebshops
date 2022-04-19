# -*- coding: utf-8 -*-

from odoo import http, models, fields, _
from odoo.http import request

from odoo.addons.website.controllers.main import Website


class Website(Website):

    @http.route('/website/lang/<lang>', type='http', auth="public", website=True, multilang=False)
    def change_lang(self, lang, r='/', **kwargs):
        redirects = super(Website,self).change_lang(lang=lang, r=r, **kwargs)
        order = request.website.sale_get_order()
        try:
            lg = request.website.language_ids.filtered(lambda r: r.code == lang)
            if not request.env.user._is_public() and request.env.user and request.env.user.partner_id:
                lg = request.website.language_ids.filtered(lambda r:r.code == lang)
                request.env.user.partner_id.lang = lg and lg.code
            if order and request.env.user._is_public() and request.env.user.partner_id != order.partner_id:
                order.partner_id.lang = lg and lg.code
        except Exception as e:
            return redirects
        return redirects
