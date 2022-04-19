# Copyright (C) feb,18 2019, Emipro Technologies Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    # Theme information
    'name': 'Emipro Theme Base',
    'category': 'Base',
    'summary': 'Base module containing common libraries for all Emipro eCommerce themes.',
    'version': '12.0.0.13',
    'license': 'OPL-1',	
    'depends': [
        'website_theme_install',
        'website_sale_wishlist',
        'website_sale_comparison',
        'website_blog',        
    ],

    'data': [
		'data/score_cron.xml',
		'security/ir.model.access.csv',
	    'views/website_menu_views.xml',
	    'views/product_label_views.xml',
        'views/slider_views.xml',
        'views/slider_filter_views.xml',
        'views/slider_styles_views.xml',
        'views/product_pricelist_item_views.xml',
        'views/res_company_views.xml',
        'views/product_brand_ept_views.xml',
        'views/product_template_views.xml',
        'views/product_rule_views.xml',
        'views/product_attribute_views.xml',
        'views/website_views.xml',
	    'views/template.xml'
    ],

    #Odoo Store Specific
    'images': [
        'static/description/emipro_theme_base.jpg',
    ],

    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'https://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Technical
    'installable': True,
    'auto_install': False,
    'price': 49.00,
    'currency': 'EUR', 
}
