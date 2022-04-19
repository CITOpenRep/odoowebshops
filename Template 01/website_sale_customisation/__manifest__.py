# Copyright (C) feb,18 2019, Emipro Technologies Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    # About Module
    'name': 'Website Sale Customisation',
    'category': 'Extra Tools',
    'version': '12.0.0.1',
    'license': 'AGPL-3',
    'description': """
    
    """,

    # Dependencies
    'depends': ['website_sale_wishlist'],

    # Views
    'data': [
        'data/mail_template_data.xml',
        'template/assets.xml',
        'template/sale_customize_template.xml',
        'template/font_customize_template.xml',
        'view/res_country_views.xml',
        'view/res_config_settings_views.xml',
        'view/sale_order_views.xml',
        'view/product_public_category_views.xml',
        'view/product_size_guide_views.xml',
        'view/res_flag.xml',
        'security/ir.model.access.csv',
        'report/report_templates.xml',
        'data/report_name.xml',
    ],

    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',

    # Technical
    'installable': True,
}
