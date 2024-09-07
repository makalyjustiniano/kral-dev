# -*- coding: utf-8 -*-
{
    'name': "KRAL - Design Tree",
    'summary': """
         Design Tree
    """,
    'description': """
        -  Design Tree Product_id
    """,
    'author': "Anthony Amutari Justiniano",
    'website': "https://www.kral.com",
    'category': 'Development',
    'version': '0.1',
    'depends': ['purchase','base','web'],
    'data': [
        'views/purchase_design.xml',
        'views/purchase_design.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'static/src/xml/**/*',
        ],
        'web.assets_common': [
            'ds-design-purchase/static/src/js/product_line_custom.js',
        ],
    },
    'demo': [

    ],
    'license': 'LGPL-3',
}
