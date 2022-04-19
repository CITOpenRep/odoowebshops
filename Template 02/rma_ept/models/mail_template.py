# -*- coding: utf-8 -*-
import base64

from odoo.exceptions import UserError
from odoo import _, api, fields, models, tools

class MailTemplate(models.Model):
    _inherit = "mail.template"
    
    @api.multi
    def send_mail(self, res_id, force_send=False, raise_exception=False, email_values=None, notif_layout=False):
        self.ensure_one()
        rma_id = self.env.context.get('rma_id',False)
        rma_id = self.env['crm.claim.ept'].search([('id','=',rma_id)])
        if rma_id and rma_id.state == 'approve':
            report_name = 'RMA Delivery Label - %s'%(rma_id.code)
            report = self.env['ir.actions.report'].search([('report_name', '=', 'rma_ept.report_rma_delivery_label')])
            if report.report_type not in ['qweb-html', 'qweb-pdf']:
                raise UserError(_('Unsupported report type %s found.') % report.report_type)
            result, format = report.render_qweb_pdf([res_id])
            result = base64.b64encode(result)
            if not report_name:
                report_name = 'RMA Delivery Label - %s'%(rma_id.code)
            ext = "." + format
            if not report_name.endswith(ext):
                report_name += ext
            
            attachment_data = {
                'name': report_name,
                'datas_fname': report_name,
                'datas': result,
                'type': 'binary',
                'res_model': 'mail.message',
            }
            Attachment = self.env['ir.attachment']
            attachment_id = Attachment.sudo().create(attachment_data)
            
            email_values = {'attachment_ids': [attachment_id.id]}
            results = super(MailTemplate, self).send_mail(res_id=res_id, force_send=force_send,raise_exception=raise_exception,email_values=email_values,notif_layout=notif_layout)
            return results
        else:
            results = super(MailTemplate, self).send_mail(res_id=res_id, force_send=force_send,raise_exception=raise_exception,email_values=email_values,notif_layout=notif_layout)
            return results
    
    
        
