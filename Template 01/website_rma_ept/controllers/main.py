# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo import _
import base64
from odoo import api, fields, models, _,SUPERUSER_ID


class portal_rma_ept(CustomerPortal):

    ## Prepare values for RMA Form and Render.
    @http.route(['/rma/form/<int:order>'], type='http', auth="public", website=True)
    def rma_form(self, order=None, **kwargs):
        delivery_order = request.env['stock.picking'].sudo().browse(order)
        warehouse_return_partner_id = delivery_order.picking_type_id and delivery_order.picking_type_id.warehouse_id and delivery_order.picking_type_id.warehouse_id.return_partner_id and delivery_order.picking_type_id.warehouse_id.return_partner_id.contact_address or delivery_order.picking_type_id.warehouse_id.partner_id.contact_address
        ReturnReason = request.env['rma.reason.ept'].sudo().search([])
        values = {
            # 'sale_order': delivery_order.sale_id and delivery_order.sale_id.id or '',
            'sale_order': delivery_order.sale_id or '',
            'delivery_order': delivery_order,
            'return_address': warehouse_return_partner_id,
            'return_reason': ReturnReason,
            'current_datetime': datetime.now().strftime(DATETIME_FORMAT),
        }

        return request.render("website_rma_ept.rma_form_ept", values)

    @http.route(['/rma/form/confirm'], type='http', method='post', auth="public", website=True)
    def rma_form_confirm(self,**kwargs):
        my_rma_orders = request.session.get('my_rma_order',False)
        rma_success=request.env['crm.claim.ept']
        if my_rma_orders:
            success=False
            for my_rma_order in my_rma_orders:
                data = my_rma_order.split("-")
                if data[0]== "success":
                    rma = request.env['crm.claim.ept'].sudo().search([('id','=',data[1])])
                    rma_success = rma_success+rma
                    order = request.env['stock.picking'].sudo().search([('id','=',data[2])])
                    success =True
            values = {'success': success, 'rma_success':rma_success,'order': order} 
            request.session['my_rma_order']=False
            return request.render("website_rma_ept.rma_record_ept", values)
        else:
            return request.redirect("/my/rma/orders")
            
    ## Create RMA Record when Click On RMA Template Submit Button
    @http.route(['/rma/form/submit'], type='http', methods=['POST'], auth="public", website=True)
    def rma_form_submit(self, **kwargs):
        request.session['my_rma_order'] =[]
        delivery_order_obj = request.env['stock.picking'].sudo()
        crm_claim_ept_obj = request.env['crm.claim.ept'].sudo()
        claim_line_obj = request.env['claim.line.ept'].sudo()
        delivery_order = delivery_order_obj.browse(int(kwargs.get('current_order')))
        image=None
        if kwargs.get('rma_image'):
            image=base64.encodestring(kwargs.get('rma_image').read()) 
        rma_reason=[]    
        for move in delivery_order.move_lines:
            if kwargs.get('%s_line_return_reason' % (move.id)):
                reason_id = int(kwargs.get('%s_line_return_reason' % (move.id)))
                if reason_id not in rma_reason:
                    rma_reason.append(reason_id) 
        for reason in rma_reason: 
            
            vals = {
                'name': 'RMA for {}'.format(delivery_order.origin),
                'picking_id': delivery_order.id,
                'date': kwargs.get('rma_date', datetime.now().strftime(DATETIME_FORMAT)),
                'description': kwargs.get('return_note', ''),
                'rma_image':image,
                'website_id':request.website.id,
                'rma_reason_id': reason,
            }
            responsible_person = request.website.rma_responsible_person
            vals.update({'user_id': responsible_person if responsible_person else request.env.user.id})
            tmp_rec = crm_claim_ept_obj.new(vals)
            tmp_rec.onchange_picking_id()
            claim_vals = crm_claim_ept_obj._convert_to_write({name: tmp_rec[name] for name in tmp_rec._cache})
            res = crm_claim_ept_obj.create(claim_vals)
            res.claim_line_ids.sudo().unlink()
            if res and res.picking_id:
                for move in res.picking_id.move_lines :
                    tick_val = '%s_tick_line' % (move.id)
                    if kwargs.get(tick_val, False) and int(kwargs.get('%s_line_return_reason' % (move.id))) == reason:
                        claim_line_obj.create({
                            'claim_id': res.id,
                            'product_id': move.product_id.id,
                            'quantity': kwargs.get('%s_line_qty_return' % (move.id)),
                            'move_id': move.id,
                            'rma_reason_id': int(kwargs.get('%s_line_return_reason' % (move.id))),
                        })
                if res.claim_line_ids:
                    grp = request.website.rma_ack_group
                    if grp:
                        for recipient in grp.sudo().users:
                            template=request.website.sudo().rma_ack_mail_template 
                            values = template.sudo().generate_email(res.id)
                            values['email_to'] = recipient.partner_id.email
                            mail_mail_obj = request.env['mail.mail'].sudo()
                            msg_id = mail_mail_obj.create(values)
                            if msg_id:
                                msg_id.sudo().send()
                    request.session['my_rma_order'].append("success-%s-%s"%(res.id or '',delivery_order.id))
                    template=request.website.rma_create_mail_template
                    if template:
                        template.sudo().send_mail(res.id,force_send=True,raise_exception=True) 
                else:
                    res.unlink()
                    request.session['my_rma_order'] = "fail-%s"%(delivery_order.id)

        return request.redirect("/rma/form/confirm")

    #####################################################################
    # Prepare RMA Record Count for RMA Portal Menu
    def _prepare_portal_layout_values(self):
        values = super(portal_rma_ept, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        RmaOrder = request.env['crm.claim.ept']
        rma_record_count = RmaOrder.search_count([
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
        ])

        values.update({
            'rma_record_count': rma_record_count,
        })
        return values

    ## Render RMA Records Form
    @http.route(['/my/rma/orders','/my/rma/orders/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_rma(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        RmaOrder = request.env['crm.claim.ept']

        domain = [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
        ]

        searchbar_sortings = {
            'date': {'label': _('Order Date'), 'order': 'date desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('crm.claim.ept', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        rma_count = RmaOrder.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/rma/orders",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=rma_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        Rma = RmaOrder.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_rma_history'] = Rma.ids[:100]

        values.update({
            'date': date_begin,
            'rma_orders': Rma.sudo(),
            'page_name': 'rma',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/rma/orders',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("website_rma_ept.rma_orders_form_ept", values)

    ## RMA Form
    @http.route(['/my/rma/orders/<int:order>'], type='http', auth="public", website=True)
    def portal_rma_order_page(self, order=None, **kwargs):
        RmaOrder = request.env['crm.claim.ept'].sudo().browse(order)
        warehouse_return_partner_id = RmaOrder.picking_id and RmaOrder.picking_id.picking_type_id and RmaOrder.picking_id.picking_type_id.warehouse_id and RmaOrder.picking_id.picking_type_id.warehouse_id.return_partner_id and RmaOrder.picking_id.picking_type_id.warehouse_id.return_partner_id.contact_address or RmaOrder.picking_id.picking_type_id.warehouse_id.partner_id.contact_address

        values = {
            'order': RmaOrder,
            'return_address': warehouse_return_partner_id,
        }

        if kwargs.get('error'):
            values['error'] = kwargs['error']
        if kwargs.get('warning'):
            values['warning'] = kwargs['warning']
        if kwargs.get('success'):

        ## this is for add pagination on RMA Form
            values['success'] = kwargs['success']
        history = request.session.get('my_rma_history', [])
        if RmaOrder.id in history:
            attr_name = 'portal_url' if hasattr(RmaOrder, 'portal_url') else ''
            if attr_name:
                idx = history.index(RmaOrder.id)
                values.update({
                    'prev_record': idx != 0 and getattr(RmaOrder.browse(history[idx - 1]), attr_name),
                    'next_record': idx < len(history) - 1 and getattr(RmaOrder.browse(history[idx + 1]), attr_name),
                })

        return request.render("website_rma_ept.portal_rma_order_page", values)

    ## Print RMA Record from portal
    @http.route(['/my/rma/orders/pdf/<int:order_id>'], type='http', auth="public", website=True)
    def portal_rma_order_report(self, order_id, **kw):
        if order_id:
            pdf = request.env.ref('rma_ept.action_report_rma').sudo().render_qweb_pdf([int(order_id)])[0]
            pdfhttpheaders = [
		    ('Content-Type', 'application/pdf'),
		    ('Content-Length', len(pdf)),
            ]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return False
