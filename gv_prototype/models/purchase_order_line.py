# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2018 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sale_order_line_ids = fields.One2many('sale.order.line', 'purchase_order_line_id', 'Sale lines')
    product_qty_processed = fields.Float('Quantity Processed', compute='_compute_product_qty_processed')
    lot_name = fields.Char('Lot/Serial Number')

    @api.multi
    @api.depends('sale_order_line_ids')
    def _compute_product_qty_processed(self):
        for line in self:
            line.product_qty_processed = sum(line.sale_order_line_ids.mapped('product_uom_qty'))

    @api.multi
    def create_sale_order_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'gfvi_prototype.add_sol_to_pol',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_purchase_order_line_id': self.id,
            },
        }

    @api.multi
    def write(self, values):
        if values.get('lot_name', False):
            self.mapped('move_ids').filtered(
                lambda m: m.state not in ['cancel', 'done']
            ).mapped('move_line_ids').write({
                'lot_name': values['lot_name'],
            })
        return super(PurchaseOrderLine, self).write(values)
