# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.exceptions import Forbidden, NotFound
from odoo import fields, http, tools, _


_logger = logging.getLogger(__name__)

class websiteSaleOrder(WebsiteSale):
    # added order note
    @http.route(['/order_comment'], type='json', auth="public", methods=['POST'], website=True)
    def order_comment(self, **post):
        if post.get('comment'):
            order = request.website.sale_get_order()
            redirection = self.checkout_redirection(order)
            if redirection:
                return redirection

            if order and order.id:
                order.write({'customer_comment': post.get('comment')})

        return True

    @http.route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        res = super(websiteSaleOrder,self).cart(access_token=access_token, revive=revive, **post)
        order = request.website.sale_get_order()
        if order and order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order()
        if order and order.order_line and order.state == 'draft':
            order._check_carrier_quotation()
        return res
    
    # list attribute value of loaded product
    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>''',
        '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        try:
            if not post.get('filter_id',False):
                res = super(websiteSaleOrder, self).shop(page=page, category=category, search=search, ppg=ppg,**post)
                products = res.qcontext.get('products',False)
                if products :
                    attrib_val_ids = []
                    for product in products:
                        for attribute_line_id in product.attribute_line_ids:
                            for value_id in attribute_line_id.value_ids:
                                if value_id.id not in attrib_val_ids:
                                    attrib_val_ids.append(value_id.id)
                    res.qcontext['attrib_val_ids'] = attrib_val_ids
                return res
        except Exception as e:
            return request.redirect('/shop')
    
#     @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True)
#     def address(self, **kw):
#         Partner = request.env['res.partner'].with_context(show_address=1).sudo()
#         order = request.website.sale_get_order()
# 
#         redirection = self.checkout_redirection(order)
#         if redirection:
#             return redirection
# 
#         mode = (False, False)
#         can_edit_vat = False
#         def_country_id = order.partner_id.country_id
#         values, errors = {}, {}
# 
#         partner_id = int(kw.get('partner_id', -1))
#         # IF PUBLIC ORDER
#         if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
#             mode = ('new', 'billing')
#             can_edit_vat = True
#             country_code = request.session['geoip'].get('country_code')
#             if country_code:
#                 def_country_id = request.env['res.country'].search([('code', '=', country_code)], limit=1)
#             else:
#                 def_country_id = request.website.user_id.sudo().country_id
#         # IF ORDER LINKED TO A PARTNER
#         else:
#             if partner_id > 0:
#                 if partner_id == order.partner_id.id:
#                     mode = ('edit', 'billing')
#                     can_edit_vat = order.partner_id.can_edit_vat()
#                 else:
#                     shippings = Partner.search([('id', 'child_of', order.partner_id.commercial_partner_id.ids)])
#                     if partner_id in shippings.mapped('id'):
#                         mode = ('edit', 'shipping')
#                     else:
#                         return Forbidden()
#                 if mode:
#                     values = Partner.browse(partner_id)
#             elif partner_id == -1:
#                 mode = ('new', 'shipping')
#             else: # no mode - refresh without post?
#                 return request.redirect('/shop/checkout')
# 
#         # IF POSTED
#         if 'submitted' in kw:
#             pre_values = self.values_preprocess(order, mode, kw)
#             errors, error_msg = self.checkout_form_validate(mode, kw, pre_values)
#             post, errors, error_msg = self.values_postprocess(order, mode, pre_values, errors, error_msg)
# 
#             if errors:
#                 errors['error_message'] = error_msg
#                 values = kw
#             else:
#                 if request.website.is_public_user():
#                     email_add = pre_values.get('email',None)
#                     res_user = request.env['res.users'].sudo().search([('login', '=', email_add),('website_id', '=', request.website.id)],limit=1)
#                     if res_user:
#                         #res_user.sudo().partner_id.sudo().write(post)
#                         partner_id = res_user.sudo().partner_id.id
#                     else:
#                         partner_obj = request.env['res.partner'].sudo().search([('email', '=', email_add),('is_guest_partner', '=', True),('website_id', '=', request.website.id)],limit=1)
#                         if partner_obj:
#                             #partner_obj.sudo().write(post)
#                             partner_id = partner_obj.sudo().id
#                         else:
#                             partner_id = self._checkout_form_save(mode, post, kw)
#                             
#                     # When guest user checkout set is_guest_partner True 
#                     # In future this email was used to sign up then it will mapped the order transaction
#                     partner_obj = request.env['res.partner'].browse(int(partner_id))
#                     partner_obj.sudo().is_guest_partner = True
#                 else:
#                     partner_id = self._checkout_form_save(mode, post, kw)
#                 
#                 if mode[1] == 'billing':
#                     order.partner_id = partner_id
#                     order.onchange_partner_id()
#                     if not kw.get('use_same'):
#                         kw['callback'] = kw.get('callback') or \
#                             (not order.only_services and (mode[0] == 'edit' and '/shop/checkout' or '/shop/address'))
#                 elif mode[1] == 'shipping':
#                     order.partner_shipping_id = partner_id
# 
#                 order.message_partner_ids = [(4, partner_id), (3, request.website.partner_id.id)]
#                 if not errors:
#                     return request.redirect(kw.get('callback') or '/shop/confirm_order')
# 
#         country = 'country_id' in values and values['country_id'] != '' and request.env['res.country'].browse(int(values['country_id']))
#         country = country and country.exists() or def_country_id
#         render_values = {
#             'website_sale_order': order,
#             'partner_id': partner_id,
#             'mode': mode,
#             'checkout': values,
#             'can_edit_vat': can_edit_vat,
#             'country': country,
#             'countries': country.get_website_sale_countries(mode=mode[1]),
#             "states": country.get_website_sale_states(mode=mode[1]),
#             'error': errors,
#             'callback': kw.get('callback'),
#             'only_services': order and order.only_services,
#         }
#         return request.render("website_sale.address", render_values)
    
    @http.route(['/shop/pricelist'], type='http', auth="public", website=True, sitemap=False)
    def pricelist(self, promo, **post):
        redirect = post.get('r', '/shop/cart')
        # empty promo code is used to reset/remove pricelist (see `sale_get_order()`)
        _logger.info("=========================== Emirpo pricelist ==================")
        _logger.info("promo")
        if promo:
            is_valid = True
            pricelist = request.env['product.pricelist'].sudo().search([('code', '=', promo)], limit=1)
            promo_id = request.env['ir.config_parameter'].sudo().get_param('promotion_pricelist_id')
            order = request.website.sale_get_order()
            if promo_id:
                promo_id = request.env['product.pricelist'].sudo().search([('id', '=', int(promo_id))], limit=1)
            _logger.info(promo_id)
            if pricelist and promo_id and pricelist == promo_id  and order:
                if request.env.user.partner_id.id and not request.env.user._is_public():
                    user_sale_order = request.env['sale.order'].sudo().search(
                        [ ('id','!=',order.id),('state', 'in', ['sale','draft','sent','done']), ('partner_id', '=', request.env.user.partner_id.id)])
                    _logger.info(user_sale_order)
                    if user_sale_order:
                        is_valid = False
                else:
                    is_valid = False
            if not is_valid or (
                    not pricelist or (pricelist and not request.website.is_pricelist_available(pricelist.id))):
                return request.redirect("%s?code_not_available=1" % redirect)

        request.website.sale_get_order(code=promo)
        return request.redirect(redirect)
                
                
class websiteSaleCustomisation(http.Controller):  
    # fatch product while changing the product variant
    # @http.route(['/product/variant/change'], type='json', auth="public", website=True, csrf=False)
    # def product_varaint_change(self,product_id=False,**kw):
    #     if product_id:
    #         product_id = request.env['product.product'].sudo().search([('id', '=', product_id)])
    #         attr_val_ids = product_id.attribute_value_ids.ids
    #         value ={
    #             'attribute_value_ids': attr_val_ids,
    #             'product_id' : product_id.id
    #         }
    #         return value
    #     else:
    #         return False
        
    # Clear all the product from cart 
    @http.route(['/shop/clear_cart'], type='json', auth="public", methods=['POST'], website=True)
    def clear_cart(self, **kw):
        order = request.website.sale_get_order(force_create=1)
        if order :
            order.unlink()
            
    @http.route(['/shop/product/size_guide_json'], type='json', auth="public", website=True)
    def product_size_guide(  self , categ_id, **post):
        tmp_object = request.env['product.public.category'].browse(int(categ_id))
        if tmp_object    :
                values ={'categ_id': tmp_object.with_context()}
                response = http.Response(template="website_sale_customisation.product_size_guide_model",qcontext=values)
                return response.render()
        return False
    
    @http.route( ['/shop/cart/popover'], type='json', auth="public", website=True )
    def shop_cart_popover(self , **post):
        order = request.website.sale_get_order()
        values = {}
        if order and order.order_line and order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order()
        if order and order.order_line and order.state == 'draft':
            order._check_carrier_quotation()
            from_currency = order.company_id.currency_id
            to_currency = order.pricelist_id.currency_id
            compute_currency = lambda price: from_currency._convert(
                price, to_currency, request.env.user.company_id, fields.Date.today())
        else:
            compute_currency = lambda price: price

        values.update({
            'website_sale_order': order,
            'compute_currency': compute_currency,
            'date': fields.Date.today(),
        })
        return request.env.ref("website_sale.cart_popover").render(values)

    
    