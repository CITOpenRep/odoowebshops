# -*- coding: utf-8 -*-
from odoo import api, fields, models,_

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    is_low_stock = fields.Boolean(string="Low Stock Notification", related='company_id.is_low_stock', readonly=False)

    low_stock_notification_mail_template = fields.Many2one('mail.template', 'Notification Template',
                                                           domain="[('model', '=', 'res.users')]",
                                                           related='company_id.low_stock_notification_mail_template',
                                                           readonly=False,help="Notification Template",
                                                           default=lambda self: self.env.ref(
                                                               'low_stock_notification.low_stack_notification_email',
                                                               False))

    low_stock_user_ids = fields.Many2many('res.users', string='Notify Recipients',readonly=False,help="Notify Recipients",
                                          related='company_id.low_stock_user_ids',domain="[('share','=',False)]")


