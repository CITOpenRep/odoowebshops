# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = 'Sale Order'

    customer_comment = fields.Text('Customer Order Comment',default="No comment")

    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        values = super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        try:
            if self:
                self._check_carrier_quotation()
        except Exception as e:
            return values
        return values

    @api.multi
    def action_quotation_send(self):
        """
        @desc: if order is done and any transaction is also done then only send the mail.
        @args: None
        @return: Base super method.
        """
        if self.state in ['sale', 'done'] and (self.transaction_ids.filtered(lambda r: r.state in ['done']) or (self.coupon_applied and not self.amount_total)):
            return super(SaleOrder, self).action_quotation_send()
        else:
            return False

