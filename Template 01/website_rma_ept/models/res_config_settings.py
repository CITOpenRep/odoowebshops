from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    rma_return_days = fields.Integer(related="website_id.rma_return_days",string="Order Return days",readonly=False)
    rma_create_mail_template = fields.Many2one('mail.template', string='Return Order Create', domain="[('model', '=', 'crm.claim.ept')]",related='website_id.rma_create_mail_template', readonly=False)
    rma_approve_mail_template = fields.Many2one('mail.template', string='RMA Action', domain="[('model', '=', 'crm.claim.ept')]",related='website_id.rma_approve_mail_template', readonly=False)
    rma_close_mail_template = fields.Many2one('mail.template', string='RMA Close', domain="[('model', '=', 'crm.claim.ept')]",related='website_id.rma_close_mail_template', readonly=False)
    rma_reject_mail_template = fields.Many2one('mail.template', string='Return Order Reject', domain="[('model', '=', 'crm.claim.ept')]",related='website_id.rma_reject_mail_template', readonly=False)
    rma_validate_mail_template = fields.Many2one('mail.template', string='Return Order Validate', domain="[('model', '=', 'crm.claim.ept')]",related='website_id.rma_validate_mail_template', readonly=False)
    rma_ack_mail_template = fields.Many2one('mail.template', string='Return Order Acknowledgement', domain="[('model', '=', 'crm.claim.ept')]",related='website_id.rma_ack_mail_template', readonly=False)
    rma_ack_group = fields.Many2one('res.groups', string='Return Order Acknowledgement Group',related='website_id.rma_ack_group', readonly=False)
    rma_responsible_person = fields.Many2one('res.users', related="website_id.rma_responsible_person", string='RMA Responsible Person', readonly=False)