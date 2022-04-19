# -*- coding: utf-8 -*-

import logging
import werkzeug
import odoo
from odoo import http, _
from odoo import api, SUPERUSER_ID
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.web.controllers.main import Home, ensure_db, abort_and_redirect
from odoo.exceptions import UserError
from odoo import fields, http, _
from odoo.http import request

_logger = logging.getLogger(__name__)

class AuthSignupHomeValidate(AuthSignupHome):

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                               raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                            password=request.params.get('password')
                        ).send_mail(user_sudo.id, force_send=True)
                return request.render("auth_signup_verification.signup_confirmation")
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    
    # render reset password success message 
    @http.route('/reset_password/success', type='http', auth='public', website=True)
    def reset_password_success(self, **kw):
        return request.render('auth_signup_verification.password_change_success')
    
    # override reset password controller to render success page after reseting password
    @http.route('/web/reset_password', type='http', auth='public', website=True, sitemap=False)
    def web_auth_reset_password(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('reset_password_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                if qcontext.get('token'):
                    self.do_signup(qcontext)
                    request.session.logout(keep_db=True)
                    return request.redirect('/reset_password/success') 
                else:
                    login = qcontext.get('login')
                    assert login, _("No login provided.")
                    _logger.info(
                        "Password reset attempt for <%s> by user <%s> from %s",
                        login, request.env.user.login, request.httprequest.remote_addr)
                    request.env['res.users'].sudo().reset_password(login)
                    qcontext['message'] = _("An email has been sent with credentials to reset your password")
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except SignupError:
                qcontext['error'] = _("Could not reset your password")
                _logger.exception('error when resetting password')
            except Exception as e:
                qcontext['error'] = str(e)

        response = request.render('auth_signup.reset_password', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
    
    # added extra filed for sign up registration process
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password')}
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang
        values.update({'website_id':request.website.id})
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()
    
    # send mail to registered user to confirm there account
    def _signup_with_values(self, token, values):
        db, login, password = request.env['res.users'].sudo().signup(values, token)
        request.env.cr.commit()

        user_sudo = request.env['res.users'].sudo().search([('login', '=', login)])
        if len(user_sudo) > 1:
            user_sudo = user_sudo[len(user_sudo)-1]
        if not token:
            template = request.env.ref('auth_signup_verification.mail_template_user_signup_confirmation', raise_if_not_found=False)
            template.sudo().send_mail(user_sudo.id, force_send=True)


    # Activate User Registration
    @http.route('/web/signup/confirmation', type='http', auth='public', website=True)
    def signup_confirmation(self, access_token=False):
        if access_token:
            user_id = request.env['res.users'].sudo().search([('access_token', '=', access_token)])
            user_id.sudo().write({
                'is_validate': True,
            })
            if user_id.is_validate == True:
                request.env.cr.commit()
                try:
                    if user_id is not False:
                        request.params['login_success'] = True
                        if user_id.redirect_url:
                            return request.redirect(user_id.redirect_url)
                        else:
                            return request.render("auth_signup_verification.user_valid")
                except odoo.exceptions.AccessDenied as e:
                    if e.args == odoo.exceptions.AccessDenied().args:
                        values['error'] = _("Wrong login/password")
                    else:
                        values['error'] = e.args[0]
            else:
                return request.render("auth_signup_verification.signup_not_valid_user")
    
    # seprate login of admin 
    @http.route('/web/admin/login', type='http', auth="public", website=True, sitemap=False)
    def web_admin_login(self, redirect=None, **kw):
        values = request.params.copy()
        if request.httprequest.method == 'POST':
            old_uid = request.uid
            user_sudo = request.env['res.users'].sudo().search([('login', '=', request.params['login'])])
            if user_sudo and not user_sudo.is_authenticate_user:
                request.session.logout(keep_db=True)
                return request.redirect("/web/login")
            else:
                request.env.cr.commit()
                try:
                    uid = request.session.authenticate(request.session.db, request.params['login'],request.params['password'])
                    if uid is not False:
                        request.params['login_success'] = True
                        
                        return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
                except odoo.exceptions.AccessDenied as e:
                    request.uid = old_uid
                    if e.args == odoo.exceptions.AccessDenied().args:
                        values['error'] = _("Wrong login/password")
                    else:
                        values['error'] = e.args[0]
            
        return request.render("auth_signup_verification.auth_admin_login",values)
    
# override login controller 
# login to check the user account is activated or not
class authHome(Home):
    
    @http.route(website=True, auth="public")
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)
        
        if not request.uid:
            request.uid = odoo.SUPERUSER_ID
        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None
        if request.httprequest.method == 'POST':
            old_uid = request.uid
            user_sudo = request.env['res.users'].sudo().search([('login', '=', request.params['login'])])
            if user_sudo and user_sudo.is_authenticate_user:
                values['error'] = _("Wrong login/password")
                #return False
                return request.render('web.login', values)
                request.env.cr.commit()
                try:
                    uid = request.session.authenticate(request.session.db, request.params['login'],request.params['password'])
                    if uid is not False:
                        request.params['login_success'] = True
                        #ADDED
                        user_sudo.partner_id.lang = request.httprequest.cookies.get('frontend_lang')
                        return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
                except odoo.exceptions.AccessDenied as e:
                    request.uid = old_uid
                    if e.args == odoo.exceptions.AccessDenied().args:
                        values['error'] = _("Wrong login/password")
                    else:
                        values['error'] = e.args[0]	
            if user_sudo and user_sudo.id != SUPERUSER_ID: 
                if user_sudo.is_validate == True:
                    request.env.cr.commit()
                    try:
                        uid = request.session.authenticate(request.session.db, request.params['login'],request.params['password'])
                        if uid is not False:
                            request.params['login_success'] = True
                            #ADDED
                            user_sudo.partner_id.lang = request.httprequest.cookies.get('frontend_lang')
                            return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
                    except odoo.exceptions.AccessDenied as e:
                        request.uid = old_uid
                        if e.args == odoo.exceptions.AccessDenied().args:
                            values['error'] = _("Wrong login/password")
                        else:
                            values['error'] = e.args[0]
                else:
                    return request.render("auth_signup_verification.signup_not_valid_user")
            request.uid = old_uid
            values['error'] = _("Wrong login/password")
            
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employee can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        response.qcontext.update(self.get_auth_signup_config())
        return response
