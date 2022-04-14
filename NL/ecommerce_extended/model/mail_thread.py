# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class MailThread(models.AbstractModel):

    _inherit = 'mail.thread'

    @api.multi
    def _message_auto_subscribe_notify(self, partner_ids, template):
        """ Notify new followers, using a template to render the content of the
        notification message. Notifications pushed are done using the standard
        notification mechanism in mail.thread. It is either inbox either email
        depending on the partner state: no user (email, customer), share user
        (email, customer) or classic user (notification_type)

        :param partner_ids: IDs of partner to notify;
        :param template: XML ID of template used for the notification;
        """
        if not self or self.env.context.get('mail_auto_subscribe_no_notify'):
            return
        if not self.env.registry.ready:  # Don't send notification during install
            return
        view = self.env['ir.ui.view'].browse(self.env['ir.model.data'].xmlid_to_res_id(template))

        #ADDED
        if self._name == 'crm.lead' and template and template == 'mail.message_user_assigned':
            view = self.env['ir.ui.view'].browse(self.env['ir.model.data'].xmlid_to_res_id('ecommerce_extended.crm_lead_user_assigned'))
        #END

        for record in self:
            model_description = self.env['ir.model']._get(record._name).display_name
            values = {
                'object': record,
                'model_description': model_description,
            }
            assignation_msg = view.render(values, engine='ir.qweb', minimal_qcontext=True)
            assignation_msg = self.env['mail.thread']._replace_local_links(assignation_msg)

            #ADDED
            subject = _('You have been assigned to %s') % record.display_name
            if self._name == 'crm.lead' and template and template == 'mail.message_user_assigned':
                subject = _('Enquiry')
            #END

            record.message_notify(
                subject=subject,
                body=assignation_msg,
                partner_ids=[(4, pid) for pid in partner_ids],
                record_name=record.display_name,
                notif_layout='mail.mail_notification_light',
                model_description=model_description,
            )