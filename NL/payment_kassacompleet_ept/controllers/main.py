# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug
import requests
import json

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class KassaCompleetController(http.Controller):
    _return_url = '/payment/kassacompleet/return'
    _cancel_url = '/payment/kassacompleet/cancel'
    _notification_url = '/payment/kassacompleet/notification'
    
    @http.route(['/payment/kassacompleet/feedback'], type='http', auth='public', csrf=False)
    def kassacompleet_feedback(self, **post):
        """ 
        * @desc prepare required data and call the kassacompleet API 
        * @param post - dict coming from kassacompleet template input values
        * @returns redirect-  if redirect url get from kassacompleet api response then redirect to kassacompleet payment page otherwise homepage or Payment. 
        * @author - Dharmesh Lathiya
        * @date - 25th July 2019
        """
        _logger.info('KassaCompleet: entering form_feedback with post data %s', pprint.pformat(post))
        return_url = post.get('return_url', '/')
        headers = {'Content-Type': 'application/json'}
        data = {
              "currency": str(post['currency']),
              "amount": int(float(post['amount']) * 100),
              "description": str(post['description']),
              "return_url": post['surl'],
              "merchant_order_id": str(post['order_id']),
        }
        reference = post.get('txnid', False)
        if reference:
            transaction_id = request.env['payment.transaction'].sudo().search([('reference', '=', reference)])
        else:
            transaction_id = request.session.get('__website_sale_last_tx_id', False)
        
        if not transaction_id:
            return werkzeug.utils.redirect(return_url)
        
        Acquirer = request.env['payment.acquirer'].sudo()
        acquirer_id =  transaction_id.acquirer_id
        kassacompleet_url = Acquirer._get_kassacompleet_urls(acquirer_id.environment)['kassacompleet_form_url']
        response = requests.post(kassacompleet_url + '/orders', headers=headers, data=json.dumps(data), auth=(post['kassacompleet_api_key'], ''))
        _logger.info('KassaCompleet: redirect ur response %s', response.json())
        response = response.json()
        
        if response['order_url']:
            transaction_id.write({
                'acquirer_reference': response['id'] 
                })
            return_url= response['order_url']
        return werkzeug.utils.redirect(return_url)
    
    @http.route([_notification_url, _cancel_url ,_return_url], type='http', auth='public', csrf=False, website=True)
    def kassacompleet_return(self, **post):
        """ 
        _cancel_url
        * @desc When you click across kassacompleet payment page cancel button you will be redirect to the shopper website payment page.
        * @param transactionid - kassacompleet transaction id(unique)  
        * @param post - dict blank {}
        * @returns redirect- '/shop/payment' or '/'
        * @author - Dharmesh Lathiya
        * @date - 24th July 2019
        
        _return_url, _notification_url
        * @desc after complete payment set transaction and order state according to kassacompleet transaction status
        * @param transactionid - kassacompleet transaction id(unique)  
        * @param post - dict blank {}
        * @returns redirect- '/shop/payment/validate' or '/'
        * @author - Dharmesh Lathiya
        * @date - 24th July 2019
        """
        _logger.info('After Payment kassacompleet form_feedback with post data %s', pprint.pformat(post))  # debug
        return_url = '/'
        transaction_id = request.env['payment.transaction'].sudo().search([('acquirer_reference', '=', post.get('order_id'))])
        if transaction_id.acquirer_id and transaction_id.acquirer_id.kassacompleet_api_key:
            kassacompleet_url = request.env['payment.acquirer'].sudo()._get_kassacompleet_urls(transaction_id.acquirer_id.environment)['kassacompleet_form_url']
            response = requests.get(kassacompleet_url+'/orders/%s/'%post.get('order_id'), auth=(transaction_id.acquirer_id.kassacompleet_api_key, ''))
            _logger.info(response.json())
            response = response.json()
            if not response.get('status',False):
                return_url = '/shop/payment'
            elif response.get('status',False) == 'new':
                return_url = '/shop/payment'
            elif response.get('status',False) in ['error','declined']:
                if response.get('transactions', False):
                    return request.render('payment_kassacompleet_ept.kassacompleet_error', {'error_msg': response['transactions'][0]['reason']})
                return_url = '/shop/payment'
            else:
                request.env['payment.transaction'].sudo().form_feedback(response, 'kassacompleet')
                return_url = '/payment/process' 
        return request.redirect(return_url)
    
    
    
