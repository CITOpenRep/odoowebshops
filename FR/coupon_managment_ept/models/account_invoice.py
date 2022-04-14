from odoo import models, fields, api, _

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def get_sale_order_discount(self):
        """
        Use: search the sale order and return discount amount
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 16/06/2021
        :return: string or boolean
        """
        sale_order = self.env['sale.order'].search([('name', '=', self.origin)], limit=1)
        if sale_order and sale_order.coupon_applied:
            return sale_order.coupon_discount_amount
        return False


    def get_sale_order_record(self):
        """
        Use: search and return the sale order
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 17/06/2021
        :return: object or boolean
        """
        sale_order = self.env['sale.order'].search([('name', '=', self.origin)], limit=1)
        if sale_order:
            return sale_order
        return False
