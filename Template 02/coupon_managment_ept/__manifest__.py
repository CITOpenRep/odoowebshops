{
   
    # App information
    'name': 'Sale Coupon',
    'version': '12.0',
    'category': 'Sales',
    'summary': 'Allows to use discount coupons in sales orders',
    'description': 'Integrate coupon mechanism in sales orders.',
    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',   
    'website': 'http://www.emiprotechnologies.com/',
    
    # Dependencies
    'depends': ['sale_management', 'website_sale_customisation', 'account'],
    
    'data': [
        'security/ir.model.access.csv',
        'views/sale_coupon_view.xml',
        'views/assets.xml',
        'views/sale_order_view.xml',
        'views/website_coupon_views.xml',
        'report/report_template.xml',
    ],

    # Technical        
    'installable': True,
}
