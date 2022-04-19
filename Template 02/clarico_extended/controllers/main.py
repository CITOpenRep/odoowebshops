# -*- coding: utf-8 -*-
"""
    This file is used for create and inherit the core controllers
"""
import datetime
from datetime import timedelta
from odoo.http import request, Controller, route
from odoo import _, http
import logging
from odoo.exceptions import UserError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.mass_mailing.controllers.main import MassMailController

_logger = logging.getLogger(__name__)


class ClaricoExtended(http.Controller):

    @http.route(['/get_best_seller_data'], type='json', auth="public", website=True)
    def get_best_seller_data(self, **kwargs):
        website_id = request.website.id
        request.env.cr.execute("""SELECT PT.id, SUM(SO.product_uom_qty),PT.website_id
                                          FROM sale_order S
                                          JOIN sale_order_line SO ON (S.id = SO.order_id)
                                          JOIN product_product P ON (SO.product_id = P.id)
                                          JOIN product_template pt ON (P.product_tmpl_id = PT.id)
                                          WHERE S.state in ('sale','done')
                                          AND (S.date_order >= %s AND S.date_order <= %s)
                                          AND (PT.website_id IS NULL OR PT.website_id = %s)
                                          AND PT.active='t'
                                          AND PT.is_published='t'
                                          GROUP BY PT.id
                                          ORDER BY SUM(SO.product_uom_qty)
                                          DESC LIMIT %s
                                       """,
                               [datetime.datetime.today() - timedelta(30), datetime.datetime.today(), website_id, 12])
        table = request.env.cr.fetchall()
        products = []
        for record in table:
            if record[0]:
                pro_obj = request.env['product.template'].sudo().browse(record[0])
                if pro_obj.sale_ok == True and pro_obj.is_published == True:
                    products.append(pro_obj)
        if products:
            values = {
                'filter_data': products,
                'is_default': False,
            }
            response = http.Response(template="clarico_extended.common_dynamic_ept", qcontext=values)
            return response.render()

    @http.route(['/get_limited_edition_data'], type='json', auth="public", website=True)
    def get_limited_edition_data(self, **kwargs):
        products = request.env['product.template'].sudo().search(
            [('website_published', '=', True), ('sale_ok', '=', True), ('is_published', '=', True),
             ('is_limited_edition', '=', True)], order='id desc',
            limit=12)
        if products:
            values = {
                'filter_data': products,
                'is_default': False,
                'limited_edition': True if request.env.user._is_public() else False,
            }
            response = http.Response(template="clarico_extended.common_dynamic_ept", qcontext=values)
            return response.render()

    @http.route(['/news_item'], type='json', auth="public", website=True)
    def get_news_item(self, news_id=None):
        """
        This controller return the template for news
        :param news_id:
        :return: cannafr_news_popup_view template html
        """
        if news_id:
            news = request.env['cannafr.news'].search([['id', '=', news_id]])
            values = {
                'news': news,
            }
            response = http.Response(template="clarico_extended.cannafr_news_popup_view", qcontext=values)
            return response.render()

    @http.route(['/event_item'], type='json', auth="public", website=True)
    def get_event_item(self, event_id=None):
        """
        This controller return the template for events
        :param event_id:
        :return: cannafr_event_popup template html
        """
        if event_id:
            event = request.env['cannafr.events'].search([['id', '=', int(event_id)]])
            values = {
                'event': event,
            }
            response = http.Response(template="clarico_extended.cannafr_event_popup", qcontext=values)
            return response.render()

    @http.route(['/get_department_team'], type='json', auth="public", website=True)
    def get_department_team(self, department_id=None):
        """
        This controller return the template for teams
        :param department_id:
        :return: cannafr_team_popup_ept template html
        """
        if department_id:
            # is_video_data = request.env['cannafr.department'].search([['id', '=', int(department_id)]]).is_video_display
            dept_teams = request.env['cannafr.department'].search(
                [['id', '=', int(department_id)]]).team_line_ids.mapped('team_id').filtered('website_published')
            values = {
                'dept_teams': dept_teams
            }
            response = http.Response(template="clarico_extended.cannafr_team_popup_ept", qcontext=values)
            return response.render()

    @http.route(['/get_department_team_data'], type='json', auth="public", website=True)
    def get_department_team_data(self, team_id=None):
        """
        This controller return the template for Team details
        :param team_id:
        :return: cannafr_team_detail_popup_ept template html
        """
        if team_id:
            team = request.env['cannafr.team'].search([['id', '=', int(team_id)]])
            values = {
                'team': team,
            }
            response = http.Response(template="clarico_extended.cannafr_team_detail_popup_ept", qcontext=values)
            return response.render()


class UserCustomFields(AuthSignupHome):

    def do_signup(self, qcontext):
        """ Override the do_signup() from the auth_signup base model for adding lastname, date_of_birth, telephone field
            :param qcontext : represent all key values of signup response.
            :returns: object of super method of auth_signup model's base class.
        """
        values = {key: qcontext.get(key) for key in
                  ('login', 'name', 'last_name', 'date_of_birth', 'telephone', 'password')}
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        if values.get('name') == '':
            raise UserError(_("Name is necessary."))
        if values.get('last_name') == '':
            raise UserError(_("Last name is necessary."))
        if values.get('date_of_birth') == '':
            raise UserError(_("Date of Birth is necessary."))
        if values.get('login') == '':
            raise UserError(_("Email is necessary."))

        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]

        if request.lang in supported_langs:
            values['lang'] = request.lang

        Contacts = request.env['mail.mass_mailing.contact'].sudo()
        name, email = Contacts.get_name_email(values.get('login'))

        website_list_id = request.env['mail.mass_mailing.list'].sudo().search([('is_website_mailing', '=', True)], limit=1)
        if website_list_id:
            list_id = website_list_id
        else:
            list_id = request.env['mail.mass_mailing.list'].sudo().search([('name', '!=', '')],limit=1)

        contact_ids = Contacts.search([
            ('list_ids', 'in', [int(list_id)]),
            ('email', '=', email),
        ], limit=1)
        if not contact_ids:
            # inline add_to_list as we've already called half of it
            Contacts.create({'name': name, 'email': email, 'list_ids': [(6, 0, [int(list_id)])]})
        elif contact_ids.opt_out:
            contact_ids.opt_out = False
        # add email to session
        request.session['mass_mailing_email'] = email

        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()


class CannaPartnership(http.Controller):

    @http.route(['/create_partnership_data'], type='json', auth="public", website=True, csrf=False)
    def create_partnership_data(self, **kwargs):
        """
            @desc: This method takes data from form and creates record in cn.partnership model.
            @args: **kwargs
            @return: returns to Home Page after form is submitted.
        """
        request.env['cn.partnership'].sudo().create({
            'name': kwargs.get('name', ''),
            'email': kwargs.get('email', ''),
            'description': kwargs.get('description', ''),
            'is_become_partner': kwargs.get('is_become_partner', ),
            'is_organize_event': kwargs.get('is_organize_event', ),
            'is_other': kwargs.get('is_other', )
        })

        return request.redirect("/")

# class CannaNewslaterSubscribe(MassMailController):
