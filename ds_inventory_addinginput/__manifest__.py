# -*- coding: utf-8 -*-
{
    'name': "KRAL - Ingreso Masivo De Productos",
    'summary': """
        Ingreso masivo de entradas a inventario
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
        'views/stock_picking_view.xml',
        'wizard/wizard_add_product_view.xml'

    ],
    'demo': [

    ],
    'license': 'LGPL-3',
}
