# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2018 brain-tec AG (http://www.braintec-group.com)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AddSOLtoPOL(models.TransientModel):
    _name = 'gfvi_prototype.add_sol_to_pol'

    purchase_order_line_id = fields.Many2one('purchase.order.line', 'Purchase line')
    max_quantity = fields.Float(compute='_compute_max_quantity', string='Maximum quantity',
                                help='Quantity - Quantity Processed')
    product_id = fields.Many2one(related='purchase_order_line_id.product_id', readonly=True)
    details_ids = fields.One2many('gfvi_prototype.add_sol_to_pol_details', 'add_sol_to_pol_id', 'Details')

    @api.multi
    @api.depends('purchase_order_line_id')
    def _compute_max_quantity(self):
        for w in self:
            w.max_quantity = w.purchase_order_line_id.product_qty - w.purchase_order_line_id.product_qty_processed

    @api.multi
    def create_sol(self):
        self.ensure_one()
        # check quantities of the details
        if self.max_quantity < sum(self.details_ids.mapped('quantity')):
            raise ValidationError(
                'Please check the quantities set:\nYou have an amount of %s products and are setting %s' % (
                    self.max_quantity,
                    sum(self.details_ids.mapped('quantity'))
                )
            )
        sol = self.env['sale.order.line']
        vals_template = {
            'product_id': self.product_id.id,
        }
        vals_template = sol.play_onchanges(vals_template, ['product_id'])
        for detail in self.details_ids:
            vals = vals_template.copy()
            vals.update({
                'order_id': detail.sale_order_id.id,
                'product_uom_qty': detail.quantity,
            })
            sol.create(vals)

        return True


class Details(models.TransientModel):
    _name = 'gfvi_prototype.add_sol_to_pol_details'

    add_sol_to_pol_id = fields.Many2one('gfvi_prototype.add_sol_to_pol', 'Parent')
    sale_order_id = fields.Many2one('sale.order', 'Sale', required=True)
    quantity = fields.Float('Quantity', default=0.0)
