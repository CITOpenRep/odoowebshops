from odoo import fields,models,api
import re
import uuid

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def _get_computed_reference(self):
        self.ensure_one()
        if self.company_id.invoice_reference_type == 'invoice_number':
            seq_suffix = self.journal_id.sequence_id.suffix or ''
            regex_number = '.*?([0-9]+)%s$' % seq_suffix
            exact_match = re.match(regex_number, self.number)
            if exact_match:
                identification_number = int(exact_match.group(1))
            else:
                ran_num = str(uuid.uuid4().int)
                identification_number = int(ran_num[:5] + ran_num[-5:])
            prefix = self.number
        else:
            #self.company_id.invoice_reference_type == 'partner'
            identification_number = self.partner_id.id
            prefix = 'CUST'
        return '%s' % (prefix)