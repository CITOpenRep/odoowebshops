# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import base64
import csv
import time
from odoo import api, SUPERUSER_ID

class resUsers(models.Model):

    _inherit = 'res.users'

    # Cron method for sending the low inventory email notification
    def low_stock_notification(self):
        # Fetching the low stock product and product variants
        products = self.env['product.product'].sudo().search([('website_published','=',True)]).filtered(lambda r: (r.low_stock_count > 0 and r.qty_available <= r.low_stock_count) or (r.product_variant_count == 1 and r.product_tmpl_id.low_stock_count > 0 and r.product_tmpl_id.qty_available <= r.product_tmpl_id.low_stock_count))
        if products:
            try:
                super_user_id = self.env['res.users'].sudo().browse(SUPERUSER_ID)
                if super_user_id and super_user_id.company_id.is_low_stock:
                    template = super_user_id.company_id.low_stock_notification_mail_template
                    # Created the csv file
                    filename = "low_stock_report_" + time.strftime("%Y_%m_%d") + '.csv'
                    filepath = '/tmp/' + filename
                    with open(filepath, 'w') as csvfile:
                        filewriter = csv.writer(csvfile, delimiter=',')
                        filewriter.writerow(['Internal Reference', 'Name','On Hand Qty','Low Stock Qty'])
                        for product in products:
                            filewriter.writerow([product.default_code or '',product.name,product.qty_available,product.low_stock_count or product.product_tmpl_id.low_stock_count])
                    attached_file = open('%s' % filepath, 'r')
                    data_file = attached_file.read()
                    data_file = base64.b64encode(data_file.encode('utf-8'))
                    # Created the attachment
                    attachment = self.env['ir.attachment'].create({
                        'name': filename,
                        'datas_fname': filename,
                        'datas': data_file,
                        'res_model': 'res.users',
                        'type': 'binary'
                    })

                    if template and attachment:
                        for user in super_user_id.company_id.low_stock_user_ids:
                            email_values = {'attachment_ids': [attachment.id]}
                            # Send the email to the configured user
                            template.send_mail(user.id,email_values=email_values,force_send=True, raise_exception=True)
            except:
                return False

