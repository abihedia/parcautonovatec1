# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'helpdesk_inherit',
    'version': '1.6',
    'category': 'After-Sales',
    'sequence': 15,
    'summary': 'Update assistance',
    'description': "",
    'website': 'https://www.company.com',
    'depends': ["mail", "portal"],
    'data': [
        'view/inherit_view_helpdesk.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_qweb': [

        ],
        'web.assets_backend': [

        ],
        'web.assets_tests': [

        ],
        'web.qunit_suite_tests': [

        ],
    },
    'license': 'LGPL-3',
}
