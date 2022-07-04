# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    @api.model
    def _get_branch(self):
        if self.env.user.branch_id:
            return self.env.user.branch_id.id
        else:
            return self.env['res.branch'].search([], limit=1, order='id').id

    branch_id = fields.Many2one('res.branch', string='Branch', default=_get_branch, required=True,
                                states={'draft': [('readonly', False)]})

    location_ids = fields.Many2many(
        'stock.location', string='Locations',
        readonly=True, check_company=True,
        states={'draft': [('readonly', False)]},
        domain="[('company_id', '=', company_id), ('usage', 'in', ['internal', 'transit']),('branch_id', '=', branch_id)]")
