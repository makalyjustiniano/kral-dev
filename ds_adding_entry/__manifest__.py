# -*- coding: utf-8 -*-
{
    'name': "KRAL - Ingresos A Stock Carga Masiva",
    'summary': """
        Ingreso masivo de entradas de productos por excel
    """,
    'description': """
        - En formato excel cargar datos de ingreso al invetario.
    """,
    'author': "Anthony Amutari Justiniano",
    'website': "https://www.kral.com",
    'category': 'Development',
    'version': '0.1',
    'depends': ['purchase', 'stock'],
    'data': [
        'security/wizard_security.xml',
        'security/ir.model.access.csv',
        'views/stock_picking_view.xml',
        'wizard/stock_picking_wizard_view.xml'

    ],
    'demo': [

    ],
    'license': 'LGPL-3',
}
