# -*- coding: utf-8 -*-
{
    # Theme information
    'name': 'Theme Canna',
    'category': 'Theme/eCommerce',
    'summary': 'For Inherit theme_clarico templates',
    'version': '12.0.1.0.0',
    'license': 'OPL-1',    
    'description': """
- This module provide inheritance of theme templates.
  (Because in theme templates can't generate External ID of any view.
  So, It needs to create this theme and inherit that theme_clarico view.)
- For Display product stock status at Different Pages.""",
                   
    'depends': ['theme_clarico','website'],

    'data': [
        'templates/assets.xml',
        'templates/shop_landing.xml',
        'templates/recently_viewed_extended.xml',
        'templates/product_extended.xml',
        'templates/shop.xml',
    ],

    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'https://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Technical
    'installable': True,
    'auto_install': False,    
}
