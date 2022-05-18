# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "SIIC Stock Customization",
    "summary": "SIIC Stock Customization",
    'author': "SIIC",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "category": "Product",
    "depends": ["product", "stock"],
    'data': [
        'views/product_product.xml',
        'views/stock_inventory.xml',
        'views/stock_location.xml',
        'views/stock_move.xml',
        'views/stock_picking.xml',
        'views/stock_warehouse.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
