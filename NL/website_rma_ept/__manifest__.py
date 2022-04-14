{
   
   # App information
    'name': 'Website RMA (Return Merchandise Authorization)',
    'version': '12.0',
    'category': 'Sales',
    'license': 'OPL-1',
    'summary' : 'Website RMA (Return Merchandise Authorization) provides an easy interface to manage return or replacement order directly from the website portal ',

    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',   
    'website': 'http://www.emiprotechnologies.com/',
   
   # Dependencies
   
    'depends': ['rma_ept','website_sale_stock'],
    
    
    'data': [
        'views/assets.xml',
        'views/sale_portal_template_ept.xml',
        'views/res_config_settings.xml'
    ],
   
   
   # Odoo Store Specific   
    'images': ['static/description/Website-RMA.jpg'],

             
     # Technical        
    
    'installable': True,
    'auto_install': False,
    'application' : True,
    'active': False,
    'live_test_url':'https://www.emiprotechnologies.com/free-trial?app=website-rma-ept&version=12&edition=enterprise',
    'price': 50.00,
    'currency': 'EUR',      
}
