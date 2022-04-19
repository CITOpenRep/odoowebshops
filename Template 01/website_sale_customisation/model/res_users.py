# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    # If check the registered user email is used in res.partner with is_guest_partner is true
    # then not create new partner and assign this parter to new register user 
    # to check guest checkout process transaction
    @api.model
    def signup(self,values=None,token=None):
        email = values.get('login', False)
        partner = self.env['res.partner'].sudo().search([('email','=',email),('is_guest_partner', '=', True)])
        if partner and not token:
            values.update({'partner_id' : partner.id})
            self._signup_create_user(values)
            return (self.env.cr.dbname, values.get('login'), values.get('password'))
        else:
            return super(ResUsers, self).signup(values=values, token=token)