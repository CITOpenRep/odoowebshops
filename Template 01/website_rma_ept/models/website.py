from odoo import fields, models, api
from odoo.http import request

class WebsiteZipcode(models.Model):
    
    _inherit = 'website'
      
    rma_return_days = fields.Integer(string="Order Return days")
    rma_create_mail_template = fields.Many2one('mail.template',default=lambda self: self.env.ref("rma_ept.rma_create_mail_template"), string='Return Order Create Mail Template', domain="[('model', '=', 'crm.claim.ept')]")
    rma_approve_mail_template = fields.Many2one('mail.template',default=lambda self: self.env.ref("rma_ept.rma_approve_mail_template"), string='RMA Approve Mail Template', domain="[('model', '=', 'crm.claim.ept')]")
    rma_close_mail_template = fields.Many2one('mail.template', default=lambda self: self.env.ref("rma_ept.rma_close_mail_template"),string='RMA Close Mail Template', domain="[('model', '=', 'crm.claim.ept')]")
    rma_reject_mail_template = fields.Many2one('mail.template', default=lambda self: self.env.ref("rma_ept.rma_reject_mail_template"),string='Return Order Reject Mail Template', domain="[('model', '=', 'crm.claim.ept')]")
    rma_validate_mail_template = fields.Many2one('mail.template', default=lambda self: self.env.ref("rma_ept.rma_validate_mail_template"),string='Return Order Validate Mail Template', domain="[('model', '=', 'crm.claim.ept')]")
    rma_ack_mail_template = fields.Many2one('mail.template', default=lambda self: self.env.ref("rma_ept.rma_ack_mail_template"),string='Return Order Acknowledgement Mail Template', domain="[('model', '=', 'crm.claim.ept')]")
    rma_ack_group = fields.Many2one('res.groups', string='Return Order Acknowledgement Group')
    rma_responsible_person = fields.Many2one('res.users', string='RMA Responsible Person')