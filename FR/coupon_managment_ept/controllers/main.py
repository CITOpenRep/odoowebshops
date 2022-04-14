# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.website_sale_customisation.controller.main import websiteSaleOrder
from odoo.http import request


class WebsiteSaleCoupon(websiteSaleOrder):

    @http.route('/shop/payment/validate', type='http', auth="public", website=True, sitemap=False)
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        res = super(websiteSaleOrder, self).payment_validate(transaction_id=transaction_id,sale_order_id=sale_order_id,**post)
        order=False
        if sale_order_id is None:
            order = request.website.sale_get_order()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')

        if order and not order.amount_total and order.coupon_applied:
            order.action_confirm()
            order.force_quotation_send()
            invoices = order.action_invoice_create()
            if invoices:
                invoices = request.env['account.invoice'].sudo().browse(invoices)
                invoices.action_invoice_open()
                for inv in invoices:
                    inv.action_invoice_sent()
                request.session['sale_order_id'] = None
                return request.redirect('/shop/confirmation')
            else:
                return request.redirect('/shop')
        return res

    @http.route(['/shop/pricelist'])
    def pricelist(self, promo, **post):
        """
        Use: Apply the coupon code to sale order and updates the sale order.
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 09/06/2021
        :return: Super Call
        """
        order = request.website.sale_get_order()
        if order and promo:
            coupon_status = request.env['website.coupon'].sudo().apply_coupon(order, promo)
            if coupon_status.get('not_found'):
                return super(WebsiteSaleCoupon, self).pricelist(promo, **post)
            elif coupon_status.get('error'):
                request.session['error_promo_code'] = coupon_status['error']
                return request.redirect("/shop/cart?code_not_available=1")
        if order and not promo:
            coupon_status = request.env['website.coupon'].sudo().unset_coupon(order)
        return request.redirect(post.get('r', '/shop/cart'))

    @http.route(['/shop/payment'], type='http', auth="public", website=True)
    def payment(self, **post):
        """
        Use: Update amount of coupon discount lines while cart gets update
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 15/06/2021
        :return: Super Call
        """
        order = request.website.sale_get_order()
        if order:
            order._update_existing_coupon_lines()
        return super(WebsiteSaleCoupon, self).payment(**post)

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, **post):
        """
        Use: Update amount of coupon discount lines while cart gets update
        Task: 174863 - Coupon management module development.
        Added by: Preet Bhatti @Emipro Technologies
        Added on: 14/06/2021
        :return: Super Call
        """
        order = request.website.sale_get_order()
        res = super(WebsiteSaleCoupon, self).cart(**post)
        if order:
            order._update_existing_coupon_lines()
        request.httprequest.url = request.httprequest.url.split('?')[0]
        return res
