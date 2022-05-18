# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    branch_id = fields.Many2one('res.branch', string='Branch', )

    @api.model
    def create(self, vals):
        if not vals.get('branch_id'):
            vals.update({'branch_id': self.env['res.branch'].sudo().get_default_branch()})
        warehouse = super(StockWarehouse, self).create(vals)
        return warehouse


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    branch_id = fields.Many2one('res.branch', related='warehouse_id.branch_id', store=True, readonly=1)
