# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit="res.config.settings"
    
    is_cookie_notice=fields.Boolean(related="website_id.is_cookie_notice",string="Cookie Notice",readonly=False)
    message=fields.Text(related="website_id.message",translate=True, string="Message", readonly=False)
    btn_text=fields.Char(related="website_id.btn_text", translate=True,string="Button Text", readonly=False)
    policy_link_text=fields.Char(related="website_id.policy_link_text", translate=True,string="Policy Link Text", readonly=False)
    policy_url=fields.Char(related="website_id.policy_url", string="Policy URL", readonly=False)
    position=fields.Selection([
        ('bottom','Banner bottom'),
        ('top','Banner Top'),
        ('bottom-left','Floating left'),
        ('bottom-right','Floating right'),
        ('static_top','Banner top (pushdown)'),
        ],string="Position",related="website_id.position", readonly=False)