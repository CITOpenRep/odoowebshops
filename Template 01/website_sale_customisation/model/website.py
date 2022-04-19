# -*- coding: utf-8 -*-

from odoo import models, fields,api,tools
from odoo.http import request

class Website(models.Model):
    _inherit = 'website'

    is_order_comment_feature = fields.Boolean(string='Do you want to disable order comment feature',default=False)
    
    @tools.cache('self.id')
    def _get_languages(self):
        return [(lg.code, lg.name, lg) for lg in self.language_ids]
    
    @api.multi
    def get_languages(self):
        self.ensure_one()
        return self._get_languages()
    
    @api.multi
    def get_alternate_languages(self, req=None):
        langs = []
        if req is None:
            req = request.httprequest
        default = self.get_current_website().default_lang_code
        shorts = []
        uri = req.path
        if req.query_string:
            uri += u'?' + req.query_string.decode('utf-8')
    
        for code, dummy, l in self.get_languages():
            lg_path = ('/' + code) if code != default else ''
            lg_codes = code.split('_')
            shorts.append(lg_codes[0])
    
            lang = {
                'hreflang': ('-'.join(lg_codes)).lower(),
                'short': lg_codes[0],
                'href': req.url_root[0:-1] + lg_path + uri,
            }
            langs.append(lang)
        for lang in langs:
            if shorts.count(lang['short']) == 1:
                lang['hreflang'] = lang['short']
        return langs
