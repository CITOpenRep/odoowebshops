from odoo import fields, models, api, _
from odoo.tools.translate import _
from odoo.exceptions import UserError
from odoo.exceptions import Warning
from odoo.tools import html2plaintext
from odoo.exceptions import Warning, AccessError
from odoo.http import request
import datetime
from datetime import datetime


class websiteCoupon(models.Model):
    _name = "website.coupon"

    name = fields.Char('Coupon Name', required=True)

    coupon_code = fields.Char(string='Coupon Code', copy=False, required=True)
    # start_date = fields.Datetime('Start Date', default=fields.Datetime.now, copy=False)
    # end_date = fields.Datetime('End Date', default=fields.Datetime.now, copy=False)
    start_date = fields.Date('Start Date', default=fields.Date.today, copy=False)
    end_date = fields.Date('End Date', default=fields.Date.today, copy=False)
    discount_line_product = fields.Many2one('product.product',
                                            help='Product used in the sales order to apply the discount.')
    state = fields.Selection(
        [('new', 'New'), ('in use', 'Available to Use'), ('used', 'Used'), ('expire', 'Expire')],
        default='new')
    active = fields.Boolean('Active', default=1)
    coupon_amount = fields.Float('Coupon Amount', help='Total coupon amount')
    coupon_balance = fields.Float('Coupon Balance', help='Available coupon balance')

    available_for_multi_order = fields.Boolean('Available for Multiple Orders', default=1, help='If it is checked then it will allow using the remaining coupon balance in the next order')
    sale_order_ids = fields.One2many('sale.order', 'applied_coupon_id',
                                     string='Applied on Sale Orders',
                                     help='Orders in which coupon is used')

    order_count = fields.Integer(compute='_compute_order_count')

    coupon_type = fields.Selection([('fixed', 'Fixed'), ('percentage', 'Percentage')],
                                   string='Coupon Value')
    coupon_applicable = fields.Selection(
        [('registered customer', 'Registered Customer'), ('all customer', 'All Customer')],
        string='Applicable Customer')
    limit_to_use = fields.Selection([('unlimited', 'Unlimited'), ('limited', 'Limited')],
                                    string='Limit to Use')
    limited_coupon_use = fields.Integer()
    minimum_cart_amount = fields.Float(string='Min cart amount')
    coupon_used_partner_ids = fields.Many2many('res.partner', 'partner_used_coupon_rel',
                                               'partner_id', 'id')
    welcome_coupon = fields.Boolean(string='First Order')
    specific_customer_ids = fields.Many2many('res.partner', 'specific_partner_coupon_rel',
                                             'partner_id', 'id')
    specific_customer = fields.Boolean(string='Specific Customer')
    reference = fields.Char('Reference')

    _sql_constraints = [
        ('code_coupon_uniq', 'unique (coupon_code)',
         _('Coupon code value must be unique !'))
    ]

    @api.model
    def create(self, vals):
        """
        Use: check if fields are valid to generate coupon code, prepare new product for discount product line, update
                coupon balance
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 09/06/2021
        :return: Super call
        """
        start_date = vals.get('start_date')
        end_date = vals.get('end_date')

        # '''Coupon code validation '''
        # if len(vals.get('coupon_code')) < 12 or len(vals.get('coupon_code')) > 16:
        #     raise Warning(_('The length of coupon code must be in between 12 to 16 characters.'))

        # '''Coupon Date validation '''
        # # if end_date < datetime.now().strftime("%Y-%m-%d %I:%M:%S"):
        # #     raise Warning(_('Incorrect End date'))
        # # elif start_date > end_date:
        # #     raise Warning(_('Incorrect Starte date'))

        # '''Coupon amount validation '''
        # if vals.get('coupon_amount', False) and vals.get('coupon_amount') <= 0:
        #     raise Warning(_('insufficient coupon amount.'))

        # vals['coupon_balance'] = vals.get('coupon_amount')
        self.coupon_record_validation(vals)
        coupon = super(websiteCoupon, self).create(vals)
        coupon.state = 'in use'

        '''Prepare a new product for coupon discount line'''
        if not vals.get('discount_line_product_id', False):
            discount_line_product = self.env['product.product'].create({
                'name': 'Coupon Code Discount',
                'type': 'service',
                'taxes_id': False,
                'supplier_taxes_id': False,
                'sale_ok': False,
                'purchase_ok': False,
                'invoice_policy': 'order',
                'lst_price': 0,
            })
            coupon.write({'discount_line_product': discount_line_product.id})
        return coupon

    @api.multi
    def write(self, vals):
        """
        Use: update coupon balance
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 14/06/2021
        :return: Super call
        """
        # if vals.get('coupon_amount'):
        #     vals['coupon_balance'] = vals.get('coupon_amount')
        # '''Coupon amount validation '''
        # if vals.get('coupon_amount') and vals.get('coupon_amount') <= 0:
        #     raise Warning(_('insufficient coupon amount.'))
        self.coupon_record_validation(vals)
        res = super(websiteCoupon, self).write(vals)
        return res

    def coupon_record_validation(self, vals):
        start_date = vals.get('start_date')
        end_date = vals.get('end_date')
        coupon_amount = vals.get('coupon_amount', False)

        '''Coupon code validation '''
        if vals.get('coupon_code', False):
            if len(vals.get('coupon_code')) < 5:
                raise Warning(_('The length of coupon code must have minimum 5 characters.'))

        '''Coupon Date validation '''
        if end_date and datetime.strptime(end_date, '%Y-%m-%d').strftime(
                "%Y-%m-%d") < datetime.today().strftime("%Y-%m-%d"):
            raise Warning(_('Incorrect End date'))

        if start_date and end_date and start_date > end_date:
            raise Warning(_('Incorrect start date'))

        '''Coupon amount validation '''
        if type(coupon_amount) == int and coupon_amount <= 0:
            raise Warning(_('insufficient coupon amount.'))

        '''Set coupon balance based on coupon amount'''
        # if vals.get('coupon_amount'):
        #     vals['coupon_balance'] = vals.get('coupon_amount')

        '''Minimum cart amount validation'''
        if vals.get('minimum_cart_amount') and vals.get('minimum_cart_amount') < 0:
            raise Warning(_('Minimum cart amount can not be negative'))

    def apply_coupon(self, order, coupon_code):
        """
        Use: apply coupon to current order and add coupon discount line to order
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 09/06/2021
        :return: Super call
        """
        error_status = {'not_found': _('The code %s is expired') % (coupon_code)}
        domain = [('coupon_code', '=', coupon_code), ('active', '=', 'True'),
                  ('state', '=', 'in use'),
                  ('end_date', '>=', datetime.today().strftime("%Y-%m-%d"))]
        coupon_id = request.env['website.coupon'].sudo().search(domain, limit=1)
        if coupon_id:
            error_status = coupon_id._check_coupon_code(order)
            if not error_status:
                order.write({
                    'order_line':
                        [(0, False, value) for value in
                         order._get_coupon_reward_line_values(coupon_id, order)]})
                # coupon_id.write({'state': 'used'})
                order.applied_coupon_id += coupon_id
                order.coupon_applied = 1
        return error_status

    def _check_coupon_code(self, order):
        """
        Use: check if applied coupon code is valid for this order or not
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 09/06/2021
        Modified by: Dhaval Bhut @Emipro Technologies
        Modified on: 31/01/2021
        Task: 183280 - Promo code Process
        :return: message -Dict
        """
        message = {}
        if self.state in ('expire') or \
                (self.end_date.strftime("%Y-%m-%d") < datetime.today().strftime(
                    "%Y-%m-%d") or self.start_date.strftime("%Y-%m-%d") > datetime.today().strftime(
                    "%Y-%m-%d")):
            message = {
                'error': _('This coupon %s has been used or is expired.') % (self.coupon_code)}
            return message
        if not self.active:
            message = {'error': _('The coupon %s is in closed state.') % (self.coupon_code)}
            return message
        # elif not self.coupon_balance:
        #     message = {'not_found': _('The coupon %s has not enought balance') % (self.coupon_code)}
        if self.minimum_cart_amount and self.minimum_cart_amount >= order.amount_total - order.amount_delivery:
            message = {
                'error': _('You not have enough amount to use %s promo code') % (self.coupon_code)}
            return message
        if self.specific_customer and order.partner_id not in self.specific_customer_ids:
            message = {'error': _('You are not eligible %s promo code.') % (self.coupon_code)}
            return message
        if self.welcome_coupon and self.limit_to_use == 'limited':
            confirmed_order = order.search(
                [('partner_id', '=', order.partner_id.id), ('state', 'in', ['sale', 'done'])])
            if confirmed_order:
                message = {
                    'error': _('%s promo code is for welcome coupon , '
                               'It can be used for only first order.') % (
                                 self.coupon_code)}
            else:
                self.coupon_used_partner_ids = [(4, order.partner_id.id)]
            return message
        if self.limit_to_use == 'limited':
            use_coupon_count = self.env['sale.order'].search_count(
                [('partner_id', '=', order.partner_id.id), ('state', 'in', ['sale', 'done']),
                 ('applied_coupon_id', '=', self.id)])
            if not use_coupon_count <= self.limited_coupon_use:
                message = {'error': _('Coupon %s is expired beacause you used it %s times') % (
                    self.coupon_code, self.limited_coupon_use)}
            else:
                self.coupon_used_partner_ids = [(4, order.partner_id.id)]
            return message
        return message

    def unset_coupon(self, order):
        """
        Use: apply coupon to current order and add coupon discount line to order
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 09/06/2021
        :return: Super call
        """
        order_line = order.order_line.filtered(lambda line: line.reward_line == True)
        if order_line:
            order.remove_coupon(order_line)
        return True

    @api.depends('sale_order_ids')
    def _compute_order_count(self):
        """
        Use: set count of sale order where coupon is applied
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 09/06/2021
        :return: Super call
        """
        product_data = self.env['sale.order.line'].read_group(
            [('product_id', 'in', self.mapped('discount_line_product').ids)], ['product_id'],
            ['product_id'])
        mapped_data = dict([(m['product_id'][0], m['product_id_count']) for m in product_data])
        for coupon in self:
            coupon.order_count = mapped_data.get(coupon.discount_line_product.id, 0)

    def action_view_sales_orders(self):
        """
        Use: action for sale order where selected coupon is applied
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 09/06/2021
        :return: Super call
        """
        self.ensure_one()
        orders = self.env['sale.order.line'].search(
            [('product_id', '=', self.discount_line_product.id)]).mapped('order_id')
        return {
            'name': _('Sales Orders'),
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', orders.ids)]
        }

    @api.multi
    def unlink(self):
        for record in self:
            if record.state != 'new':
                raise Warning(_("Coupon cannot be delete once it Processed.\n"
                                "You can Archive the coupon if You want."))
        return super(websiteCoupon, self).unlink()

    @api.onchange('welcome_coupon')
    def onchange_coupon_fields(self):
        """
        Add value of limit to use and and limited
        @return:
        """
        if self.welcome_coupon:
            self.limit_to_use = 'limited'
            self.limited_coupon_use = 1
        else:
            self.limit_to_use = None
            self.limited_coupon_use = None

    @api.onchange('limit_to_use')
    def _onchange_limit_to_use(self):
        if self.limit_to_use == 'limited':
            self.limited_coupon_use = 1
        elif self.limit_to_use == 'unlimited':
            self.limited_coupon_use = None
