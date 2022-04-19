from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    coupon_applied = fields.Boolean('Coupon Applied', default=0, help='add a boolean field for coupon applied or not')
    applied_coupon_id = fields.Many2one('website.coupon', string='Applied Coupon Code')
    coupon_discount_amount = fields.Float(help="Applied coupon code discount")

    def unlink(self):
        self.remove_coupon(self.order_line.filtered(lambda line: line.reward_line))
        super(SaleOrder, self).unlink()

    @api.one
    def _compute_website_order_line(self):
        super(SaleOrder, self)._compute_website_order_line()
        self.website_order_line = self.website_order_line.filtered(lambda l: not l.reward_line)

    def _get_coupon_reward_line_values(self, coupon, order):
        """
        Use: prepare order line for sale order
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 09/06/2021
        :return: order line -dict
        """
        return [{
                'name': _("Discount: ") + coupon.name,
                'product_id': coupon.discount_line_product.id,
                'price_unit': - self._get_reward_values_discount_fixed_amount(coupon, order),
                'product_uom_qty': 1.0,
                'product_uom': coupon.discount_line_product.uom_id.id,
                'reward_line': True,
                'tax_id': [(4, tax.id, False) for tax in coupon.discount_line_product.taxes_id],
            }]

    def _get_reward_values_discount_fixed_amount(self, coupon, order):
        """
        Use: calculate and returns the total discount on current sale order.
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 09/06/2021
        :return: discount amount - int
        """
        if float(order.coupon_discount_amount) > 0:
            total_amount = (order.amount_total - order.amount_delivery) + float(order.coupon_discount_amount)
            coupon_balance = coupon.coupon_balance + float(order.coupon_discount_amount)
        else:
            total_amount = (order.amount_total - order.amount_delivery)
            coupon_balance = coupon.coupon_balance
        if total_amount < coupon_balance:
            coupon.write({'coupon_balance': coupon_balance - total_amount})
            self.coupon_discount_amount = total_amount
            return total_amount
        else:
            coupon.write({'coupon_balance': 0})
            self.coupon_discount_amount = coupon_balance
            return coupon_balance


    def _update_existing_coupon_lines(self):
        """
        Use: Update values for already applied coupons at checkout page
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 14/06/2021
        :return: Super Call
        """

        def update_line(order, lines, values):
            ''' Update the line '''
            if values['product_uom_qty'] and values['price_unit']:
                order.write({'order_line': [(1, line.id, values) for line in lines]})


        self.ensure_one()
        order = self

        '''Remove the coupon discount line if no all other line get remove from order'''
        if not order.order_line.filtered(lambda line: not line.reward_line):
            self.remove_coupon(order.order_line.filtered(lambda line: line.reward_line))
            order.order_line.filtered(lambda line: line.unlink())

        if order.applied_coupon_id:
            values = order._get_coupon_reward_line_values(order.applied_coupon_id, order)
            lines = order.order_line.filtered(lambda line: line.reward_line == True)
            update_line(order, lines, values[0])

    @api.multi
    def action_cancel(self):
        """
        Use: Update sale order coupon line to remove discounted amount
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 15/06/2021
        :return: Super Call
        """
        coupon_line = self.order_line.filtered(lambda line: line.reward_line == True)
        if coupon_line:
            self.remove_coupon(coupon_line)
        return super(SaleOrder, self).action_cancel()


    def remove_coupon(self, line):
        """
        Use: Update sale order fields related to coupon and apply discount amount to applied coupon
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 15/06/2021
        :return: True
        """
        if line and self.applied_coupon_id:
            self.applied_coupon_id.coupon_balance += abs(line.price_unit)
            self.coupon_applied = 0
            self.applied_coupon_id = 0
            self.coupon_discount_amount = 0
            line.unlink()


    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        """
        Use: Update amount of coupon discount lines while cart gets update
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 15/06/2021
        :return: Super Call
        """
        res = super(SaleOrder, self)._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)
        self._update_existing_coupon_lines()
        return res