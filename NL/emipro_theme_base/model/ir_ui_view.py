# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class View(models.Model):
    _inherit = "ir.ui.view"
    
    #Assign correct inherited_id of duplicated view_id for a customize views when customize_show going to swiched
    @api.multi
    def toggle(self):
        super(View,self).toggle()
        
        current_website_id = self._context.get('website_id')
        duplicated_view=self.env['ir.ui.view'].sudo().search([('active','=',True),('website_id','=',self._context.get('website_id')),('key','=',self.key)])
        for view in duplicated_view.inherit_children_ids :
            if view.website_id.id != current_website_id and view.theme_template_id:
                view.write({'inherit_id': self.id})
