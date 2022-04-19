# Copyright (C) feb,18 2019, Emipro Technologies Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    # About Module
    'name': 'Signup Verification with Link',
    'category': 'Extra Tools',
    'version': '12.0.0.1',
    'license': 'AGPL-3',
    'description': """
    This module Send a link for verification email which is register.
    After verification user is active to login to webshop 
    """,

    # Dependencies
    'depends': ['website'],

    # Views
    'data': [
        'data/signup_confirmation_data.xml',
        'template/assets.xml',
        'template/signup_confirmation_template.xml',
    ],

    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',

    # Technical
    'installable': True,
}
