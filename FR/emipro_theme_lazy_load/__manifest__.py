{
    #Module information
    'name': 'Emipro Theme Lazyload Image',
    'category': 'eCommerce',
    'summary': 'Shows images only when the visitor scrolls',
    'version': '1.0.0',
    'license': 'OPL-1',
    'depends':['website_sale'],

    'data': [
        'views/lazy_load.xml',
        'templates/assets.xml',
        'templates/templates.xml',
    ],

    #Odoo Store Specific
    'images': [
	'static/description/emipro_theme_lazy_load.jpg',
    ],

    # Author
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'https://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Technical
    'installable': True,
    'auto_install': False,
}
