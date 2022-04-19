# Copyright (C) feb,18 2019, Emipro Technologies Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    # About Module
    'name': 'Cookie Alert',
    'category': 'Extra Tools',
    'version': '12.0.0.1',
    'license': 'AGPL-3',
    'description': """
    
    """,

    # Dependencies
    'depends': ['website'],

    # Views
    'data': [
        'templates/assets.xml',
        'views/res_config_settings_views.xml',
        'views/website_views.xml'
    ],
    
    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',

    # Technical
    'application' : True,
    'installable': True,
}
