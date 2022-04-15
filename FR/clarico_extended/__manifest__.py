# Copyright (C) Apr,17 2020, Emipro Technologies Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    # About Module
    'name': 'Clarico Extended',
    'category': 'Extra Tools',
    'version': '12.0.0.1',
    'license': 'AGPL-3',
    'description': """

    """,

    # Dependencies
    'depends': ['theme_clarico', 'website_crm','website_mass_mailing'],

    # Views
    'data': [
        'views/product_template.xml',
        'views/cannafr_news_ept.xml',
        'views/product_label.xml',
        'views/cannafr_events_ept.xml',
        'views/cannafr_department.xml',
        'views/cannafr_team.xml',
        'security/ir.model.access.csv',
        'template/templates.xml',
        'template/assets.xml',
        'template/customize_extended.xml',
        'template/canna_header.xml',
        'template/homepage_news_block.xml',
        'template/snippet_extended.xml',
        'template/canna_footer.xml',
        'template/world_canna.xml',
        'template/auth_signup_login_templates.xml',
        'views/cn_partnership_views.xml',
        'views/mass_mailing.xml',
    ],

    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',

    # Technical
    'installable': True,
}
