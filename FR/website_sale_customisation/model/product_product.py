# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    _inherit = "product.product"
    
    default_code = fields.Char('Internal Reference', index=True,required=True)
    
    _sql_constraints = [
        ('uniq_default_code', 'UNIQUE(default_code)', 'Internal Reference must be unique!'),
    ]
    
    # set internal reference
    @api.model
    def create(self, vals):
        res = super(ProductProduct, self).create(vals)
        res.default_code= "%s%s"%(res.product_tmpl_id.default_code,res.id) if res.product_tmpl_id.default_code else "%s"%(res.id)
        return res
    
    #can not allow to set the same Internal Reference
    @api.multi
    def write(self, vals):
        main = super(ProductProduct, self).write(vals)
        for rec in self:
            res = self.env['product.product'].sudo().search(['&',('default_code', '=',rec.default_code),('default_code', '!=',False)])
            if len(res) > 1:
                raise UserError(_("Internal Reference must be unique!"))
        return main
    
