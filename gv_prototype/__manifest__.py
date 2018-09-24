# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2018 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################

{
    'name': "GFVI Prototype",
    'summary': "GFVI Prototype",
    'description': """GFVI Prototype""",
    'author': "brain-tec",
    'website': "http://www.braintec-group.com/",
    'category': 'Extra Tools',
    'version': '11.0.1.0.0',
    'currency': 'EUR',
    'license': 'OPL-1',
    'images': [],
    'external_dependencies': {
    },
    'depends': [
        'base',
        'purchase',
        'sale',
        'onchange_helper',  # OCA: server-tools -> git clone -b 11.0 git@github.com:OCA/server-tools.git
    ],
    'data': [
        'views/purchase_order_line.xml',
        'wizards/add_sale_order_line_to_purchase_line.xml',
    ],
    'js': [],
}
