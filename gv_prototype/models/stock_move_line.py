# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2018 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model
    def create(self, values):
        if not values.get('lot_name', False) and values.get('move_id', False):
            move = self.env['stock.move'].browse(int(values['move_id']))
            purchase_line_id = move.purchase_line_id
            if purchase_line_id:
                values['lot_name'] = purchase_line_id.lot_name
        return super(StockMoveLine, self).create(values)
