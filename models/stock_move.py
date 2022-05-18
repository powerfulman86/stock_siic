# -*- coding: utf-8 -*-

from odoo import fields, api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    branch_id = fields.Many2one('res.branch', string='Branch')

    @api.model
    def create(self, vals):
        Picking = self.env['stock.picking'].sudo()
        if vals.get('picking_id', None):
            picking = Picking.browse(vals.get('picking_id'))
            if picking.branch_id:
                vals.update({'branch_id': picking.branch_id.id})
        if not vals.get('branch_id'):
            vals.update({'branch_id': self.env['res.branch'].sudo().get_default_branch()})
        return super(StockMove, self).create(vals)


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    branch_id = fields.Many2one('res.branch', string='Branch')

    @api.model
    def create(self, vals):
        if vals.get('picking_id', None):
            picking = self.env['stock.picking'].browse(vals.get('picking_id'))
            if picking.branch_id:
                vals.update({'branch_id': picking.branch_id.id})
        if not vals.get('branch_id'):
            vals.update({'branch_id': self.env['res.branch'].sudo().get_default_branch()})

        return super(StockMoveLine, self).create(vals)


