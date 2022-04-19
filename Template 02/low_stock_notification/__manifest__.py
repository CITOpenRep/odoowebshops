# -*- coding: utf-8 -*-
{
    # App information
    'name': 'Low Stock Notification',
    'category': 'Extra Tools',
    'summary': 'This Module notify the specific user automatically based on low stock configuration.',
    'version': '1.0.0',
    'depends': [
        'stock',
    ],

    'data': [
        'view/res_config_setting.xml',
        'view/product_product.xml',
        'data/mail_template.xml',
        'data/ir_cron.xml'
    ],

    'images': [
        'static/description/icon.png',
    ],

    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'https://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Technical
    'installable': True,
    'auto_install': False,
    'application' : True,
}
