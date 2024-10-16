# -*- coding: utf-8 -*-
{
    'name': "KRAL - Pago QR Bisa Bolivia",
    'summary': """
        Pago por QR Bolivia Banco Bisa
    """,
    'description': """
        - Pago por QR Bolivia Banco Bisa
    """,
    'author': "Anthony Amutari Justiniano",
    'website': "https://www.kral.com",
    'category': 'Development',
    'version': '0.1',
    'depends': ['sale','web'],
    'data': [  
        'security/wizard_security.xml',
        'security/ir.model.access.csv',
        'views/action_payment_qr_views.xml',
        'views/res_company_views.xml',
        'wizard/action_wizard_qr_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            #'ds_pago_qr/static/src/js/custom_qr.scss'
            #'ds_printer_zpl/static/src/scss/custom_styles.scss',

        ],
    
    },
  
    'demo': [

    ],
    'license': 'LGPL-3',
}
