# -*- coding: utf-8 -*-
{
    'name': "KRAL - Printer ZPL Zebra",
    'summary': """
        Printer ZPL Zebra
    """,
    'description': """
        - Printer ZPL Zebra
    """,
    'author': "Anthony Amutari Justiniano",
    'website': "https://www.kral.com",
    'category': 'Development',
    'version': '0.1',
    'depends': ['sale','web'],
    'data': [
        'views/printer_zpl_views.xml',
        'views/sale_printer_zpl_view.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'ds_printer_zpl/static/src/js/custom_actions.js',
            'ds_printer_zpl/static/src/scss/custom_styles.scss',

        ],
    
    },
  
    'demo': [

    ],
    'license': 'LGPL-3',
}
