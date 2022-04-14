from odoo import fields, models, api

class stock_move(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def write(self,vals):
        if 'state' in vals and self:
            if self[0].picking_code=='incoming' and vals.get('state')=='done':
                rma=self.env['crm.claim.ept'].search([('return_picking_id','=',self[0].picking_id.id)])
                rma and rma.state == 'approve' and rma.write({'state':'process'})
                if rma and rma.state == 'process':
                    email_template = rma.website_id.rma_validate_mail_template or self.env.ref('rma_ept.rma_validate_mail_template', False)
                    mail_mail = email_template and email_template.send_mail(rma.id) or False
                    mail_mail and self.env['mail.mail'].browse(mail_mail).sudo().send()
        return super(stock_move,self).write(vals)