# -*- coding: utf-8 -*-

{
    'name': 'Mollie Payments',
    'version': '12.0.1.6',
    'category': 'eCommerce',
    'license': 'LGPL-3',
    'author': 'Mollie',
    'maintainer': 'Applix',
    'website': 'https://www.mollie.com/',

    'summary': 'Accept online payments with mollie. Start growing your business with effortless payments.',
    'description': """
        Accept online payments with mollie. Start growing your business with effortless payments.',
    """,

    'depends': [
        'payment'
    ],
    'external_dependencies': {
        'python': ['mollie']
    },
    'data': [
        'security/ir.model.access.csv',
        'views/payment_views.xml',
        'views/payment_mollie_templates.xml',
        'views/account_move_view.xml',
        'views/product_views.xml',
        'data/payment_acquirer_data.xml',
        'data/update_hook.xml',
        'views/account_payment.xml',
    ],

    'images': [
        'static/description/cover.png',
    ],
}
