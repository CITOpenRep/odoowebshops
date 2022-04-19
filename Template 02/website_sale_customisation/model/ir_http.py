from odoo import api, models
from odoo.http import request

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'
    
    @classmethod
    def _add_dispatch_parameters(cls, func):
        # only called for is_frontend request
        super(IrHttp, cls)._add_dispatch_parameters(func)
        if request.routing_iteration == 1:
            context = dict(request.context)
            path = request.httprequest.path.split('/')
            langs = [lg.code for lg in cls._get_languages()]
            is_a_bot = cls.is_a_bot()
            cook_lang = request.httprequest.cookies.get('frontend_lang')
            nearest_lang = not func and cls.get_nearest_lang(path[1])
            preferred_lang = ((cook_lang if cook_lang in langs else False)
                              or cls._get_default_lang().code
                              or (not is_a_bot and cls.get_nearest_lang(request.lang)))

            request.lang = context['lang'] = nearest_lang or preferred_lang

            # bind modified context
            request.context = context    
            
    @classmethod
    def get_nearest_lang(cls, lang):
        # Try to find a similar lang. Eg: fr_BE and fr_FR
        short = lang.partition('_')[0]
        short_match = False
        for code, dummy,l in request.website.get_languages():
            if code == lang:
                return lang
            if not short_match and code.startswith(short):
                short_match = code
        return short_match