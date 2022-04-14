# -*- coding: utf-8 -*-

from odoo import api, fields, models

class website(models.Model):
    _inherit = 'website'

    is_cookie_notice=fields.Boolean(string="Cookie Notice")   
    message=fields.Text(string="Message",translate=True, default="This website uses cookies")
    btn_text=fields.Char(string="Button Text",translate=True, default="Got It")
    policy_link_text=fields.Char(string="Policy Link Text",translate=True, default="Learn more")
    policy_url=fields.Char(string="Policy URL")
    position=fields.Selection([
        ('bottom','Banner bottom'),
        ('top','Banner Top'),
        ('bottom-left','Floating left'),
        ('bottom-right','Floating right'),
        ('static_top','Banner top (pushdown)'),
        ],string="Position",default='bottom')