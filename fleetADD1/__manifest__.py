# -*- coding: utf-8 -*-
{
    'name': "flletADD1",

    'summary': """ """,

    'description': """
        
    """,

    'author': "",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
        #'security/security.xml',

        #'views/contract.xml',
        'views/vehicle.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
