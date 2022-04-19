from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    reward_line = fields.Boolean('Reward Line', default=0, help='Identify if the line is reward line or not')