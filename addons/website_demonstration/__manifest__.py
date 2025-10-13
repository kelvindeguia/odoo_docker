# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Form Demo',
    'version': '1.0',
    'sequence': -1,
    'category': 'Website/Website Demo',
    'summary': 'Module for website form demonstration',
    'description': """
Module for website form demonstration.
    """,
    'depends': [
        'base',
        'web',
        'website',
        
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/web_form_views.xml',
        'views/menuitems.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
    },
    'license': 'LGPL-3',
}
