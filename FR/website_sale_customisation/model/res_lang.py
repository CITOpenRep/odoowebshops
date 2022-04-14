from odoo import models,api,fields,_

# Add Language Flag
class res_lang(models.Model):
    _name="res.lang"
    _inherit="res.lang"
    _description="Idiomas"

    flag_image = fields.Binary('Flag Image')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
