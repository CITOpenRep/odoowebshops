# -*- coding: utf-8 -*-
import logging
import pytz
utc = pytz.utc

from dateutil import parser
from werkzeug import urls

from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.addons.payment_kassacompleet_ept.controllers.main import KassaCompleetController
from odoo.tools.float_utils import float_compare
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class PaymentAcquirerKassaCompleet(models.Model):
    _inherit = 'payment.acquirer'
    
    provider = fields.Selection(selection_add=[('kassacompleet',  'KassaCompleet')])
    kassacompleet_api_key = fields.Char('API Key', required_if_provider='kassacompleet', groups='base.group_user')
    kassacompleet_description = fields.Text('Description', default='Sort Description' ,help='A free text description which will be shown with the order in KassaCompleet Control. If the customers bank supports it this description will also be shown on the customers bank statement.')
    
    @api.model
    def _get_kassacompleet_urls(self, environment):
        """ KassaCompleet API URLs"""
        return {'kassacompleet_form_url': 'https://api.kassacompleet.nl/v1'}
     
    @api.multi
    def kassacompleet_form_generate_values(self, values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.website.url')
        values = dict(values,
                                kassacompleet_api_key=self.kassacompleet_api_key,
                                description= self.kassacompleet_description,
                                surl=urls.url_join(base_url, KassaCompleetController._return_url),
                                nurl=urls.url_join(base_url, KassaCompleetController._notification_url),
                                curl=urls.url_join(base_url, KassaCompleetController._cancel_url),
                                )
        return values

    @api.multi
    def kassacompleet_get_form_action_url(self):
        self.ensure_one()
        return "/payment/kassacompleet/feedback"
    
class PaymentTransactionKassaCompleet(models.Model):
    _inherit = 'payment.transaction'
    
    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------
    
    @api.model
    def _kassacompleet_form_get_tx_from_data(self, data):
        """ 
        * @desc Given a data dict coming from KassaCompleet, verify it and find the related transaction record. 
        * @param data - dict coming from KassaCompleet
        * @returns id- relatd transaction
        * @author - Dharmesh Lathiya
        * @date - 23th July 2019
        """
        reference = data['merchant_order_id']
        pay_id = data['id']
        if not reference or not pay_id:
            raise ValidationError(_('KassaCompleet: received data with missing reference (%s) or pay_id (%s)') % (reference, pay_id))

        transaction = self.search([('reference', '=', reference)])

        if not transaction:
            error_msg = (_('KassaCompleet: received data for reference %s; no order found') % (reference))
            raise ValidationError(error_msg)
        elif len(transaction) > 1:
            error_msg = (_('KassaCompleet: received data for reference %s; multiple orders found') % (reference))
            raise ValidationError(error_msg)
        return transaction
    
    @api.multi
    def _kassacompleet_form_get_invalid_parameters(self, data):
        """ 
        * @desc Given a data dict coming from KassaCompleet, verify Transaction Id and price if any one is wrong then return the invalid_parameters list. 
        * @param data - dict coming from KassaCompleet
        * @returns list - invalid parameters list 
        * @author - Dharmesh Lathiya
        * @date - 23th July 2019
        """
        
        invalid_parameters = []

        if self.acquirer_reference and data['id'] != self.acquirer_reference:
            invalid_parameters.append(
                ('Transaction Id', data['id'], self.acquirer_reference))
        #check what is buyed
        if data['status'] == 'completed':
            if float_compare(float(data['amount'] / 100), self.amount, 2) != 0:
                invalid_parameters.append(
                    ('Amount', data.get('amount'), '%.2f' % self.amount))

        return invalid_parameters

    @api.multi
    def _kassacompleet_form_validate(self, data):
        """ 
        * @desc set transaction state according to KassaCompleet transaction statsus. 
        * @param data - dict coming from KassaCompleet
        * @returns boolean - Trus or False
        * @author -Dharmesh Lathiya
        * @date - 23th July 2019
        """
        status = data['status']
        if data.get('completed',False):
            completed_date=data.get('completed',False)
            date_validate=parser.parse(completed_date).astimezone(utc).strftime('%Y-%m-%d %H:%M:%S')
        else:        
            date_validate=fields.datetime.now()
            
        if status == 'completed':
            self.write({
                'state': 'done',
                'acquirer_reference': data['id'],
                'date': date_validate,
                'state_message': 'Payment has been successfully completed.'
            })
            return True
        elif status == 'processing':
            self.write({
                'state': 'pending',
                'acquirer_reference': data['id'],
                'date': date_validate,
                'state_message': 'Payment is on processing.., You have to process this transaction manually according to Kassa Compleet transaction status'
            })
            return True
        elif status in ['canceled']:
            self.write({
                'state': 'cancel',
                'acquirer_reference': data['id'],
                'date': date_validate,
                'state_message': 'Canceled by the merchant (only applies to the status Initialised or Uncleared).'
            })
            return True
        elif status in ['declined', 'expired', 'void']:
            if status == 'decline':
                state_message = 'Rejected by the credit card company.'
            elif status == 'expired':
                state_message = 'Depending on the payment method unfinished transactions automatically expire after a predefined period.' 
            else:
                state_message = 'Failed payment.'
            self.write({
                'state': 'error',
                'acquirer_reference': data['id'],
                'date': date_validate,
                'state_message': state_message
            })
            return True
        elif status in ['uncleared']:
            self.write({
                'state': 'authorized',
                'acquirer_reference': data['id'],
                'date': date_validate,
                'state_message': 'Waiting for manual permission of the merchant to approve/disapprove the payment.'
            })
            return True
        elif status in ['initialized']:
            self.write({
                'state': 'pending',
                'acquirer_reference': data['id'],
                'date': date_validate,
                'state_message': 'A payment link has been generated, but no payment has been received yet.'
            })

            return True
        elif status in ['refunded', 'rartial_refunded']:
            self.write({
                'state': 'refunded',
                'acquirer_reference': data['id'],
                'date': date_validate,
                'state_message': 'Payment has been partially or full refunded or to the customer.'
            })
            return True
        elif status in ['reserved']:
            self.write({
                'state': 'refunding',
                'acquirer_reference': data['id'],
                'date': date_validate,
                'state_message': 'Payout/refund has been temporary put on reserved, a temporary status, till the e-wallet has been checked on sufficient balance.'
            })
            return True
        else:
            error = _('KassaCompleet: feedback error')
            _logger.info(error)
            self.write({
                'state': 'error',
                'state_message': error,
                'acquirer_reference': data['id'],
            })
            return False
