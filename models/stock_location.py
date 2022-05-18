# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockLocation(models.Model):
    _inherit = "stock.location"

    allow_negative_stock = fields.Boolean(string="Allow Negative Stock",
                                          help="Allow negative stock levels for the stockable products "
                                               "attached to this location.", )
    branch_id = fields.Many2one('res.branch', string='Branch')
    location_address_id = fields.Many2one('res.partner', string='Location Address')

    @api.onchange('location_id')
    def change_parent(self):
        if self.location_id and self.location_id.branch_id:
            self.branch_id = self.location_id.branch_id
