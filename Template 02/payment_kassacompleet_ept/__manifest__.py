# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    # App information
   
    'name': 'KassaCompleet Payment Acquirer',
    'version': '12.0.1',
    'category': 'Website',
    'summary': 'Integrate KassaCompleet payment gateway with ODOO for accepting payments from customers.',
    
    
    # Dependencies
    
    'depends': ['payment', 'website_sale'],
    
    # Views
    
    'data': [
        'views/payment_view.xml',
        'views/payment_kassacompleet_ept.xml',
        'templates/templates.xml',
        'data/payment_acquirer_data.xml',
    ],  
    
    # Author

    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',
       
       
    # Technical 
   
    'installable': True,
    'auto_install': False,
    'application' : True,
}
