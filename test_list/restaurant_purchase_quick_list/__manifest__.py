# -*- coding: utf-8 -*-
{
    'name': "QuikListUpdate2",

    'summary': """""",

    'description': """
        
    """,

    'author': "",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','sale','product'],

    # 'qweb': ['static/src/xml/temp.xml'],
    # always loaded
    'data': [
       'security/ir.model.access.csv',
       'views/quick_list_up.xml',

    ],

    'demo': [
        'demo/demo.xml',
    ],
}
