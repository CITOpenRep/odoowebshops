from odoo import api, models, tools
from odoo.addons.base.models.qweb import QWeb

from odoo.addons.theme_clarico.htmlmin.htmlmin import main

class IrQWeb(models.AbstractModel, QWeb):
    _inherit = 'ir.qweb'

    @api.model
    def render(self, id_or_xml_id, values=None, **options):
        """
        @desc: Inherit base method for Minify HTML of all the pages.
        @args: id_or_xml_id: str - name or etree (see get_template)               
               values: dict - template values to be used for rendering.
               options: dict - Used to compile the template (the dict available for the rendering is frozen)            
        @return: Result with encode minify HTML. 
        @author: Pragnadeep - Emipro Technologies on dated 27-February-2020 
        """
        result = super(IrQWeb, self).render(id_or_xml_id, values=values, **options)
        if values.get('request',False) and values.get('request',False).is_frontend:
            if id_or_xml_id and isinstance(id_or_xml_id, int):
                view_id = self.env['ir.ui.view'].browse(id_or_xml_id)
                if view_id and view_id.xml_id in ['website.sitemap_locs', 'website.sitemap_xml', 'website.sitemap_index_xml', 'website.robots', 'biztech_prod_data_feeds.biztech_prod_data_feeds']:
                    return result
            return main.minify(result.decode(), remove_empty_space=True).encode()
        return result
