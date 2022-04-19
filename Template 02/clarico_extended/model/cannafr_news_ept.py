from odoo import fields, models

class CannaFrNewsEpt(models.Model):
    # pylint: disable=too-few-public-methods
    """
    This model is provide canna_fr news block fields
    """
    _name = "cannafr.news"
    _order = "sequence"
    _inherit = ['website.published.multi.mixin']
    _description = "Canna FR Website News"

    name = fields.Char(string="Title", required=True, translate=True)
    canna_fr_subtitle = fields.Char(string="Sub Title", required=True, translate=True)
    canna_fr_news_image = fields.Binary(string='News Banner Image')
    canna_fr_description = fields.Text(string='Description', translate=True)
    sequence = fields.Integer(help="Gives the sequence order of News block.", index=True)
    position = fields.Integer(string='Position', default=1)
    is_active = fields.Boolean(string='Is Active?', default=True)
    created_date = fields.Date(string="Created Date", help="created date")
