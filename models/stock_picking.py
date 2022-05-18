# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    branch_id = fields.Many2one('res.branch', string='Branch')

    @api.model
    def create(self, vals):
        if not vals.get('branch_id'):
            vals.update({'branch_id': self.env['res.branch'].sudo().get_default_branch()})
        picking = super(StockPicking, self).create(vals)
        return picking
