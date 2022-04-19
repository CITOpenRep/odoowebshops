# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from ast import literal_eval

class ResCompany(models.Model):

    _inherit = 'res.company'

    is_low_stock = fields.Boolean(string="Low Stock Notification")
    low_stock_notification_mail_template = fields.Many2one('mail.template', string='Low stock notification Email',
                           domain="[('model', '=', 'res.users')]",help="Low Stock Notification Email Template")
    low_stock_user_ids = fields.Many2many('res.users', string='Notified Users',domain="[('share','=',False)]")


