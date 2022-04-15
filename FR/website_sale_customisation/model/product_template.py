from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    size_guide_template_product = fields.Many2one('product.size.guide.template', string='Size Guide')