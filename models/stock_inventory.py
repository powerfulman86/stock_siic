# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockInventory(models.Model):
    _name = "stock.inventory"
    _inherit = ["stock.inventory", "mail.thread"]

    @api.model
    def _get_branch(self):
        if self.env.user.branch_id:
            return self.env.user.branch_id.id
        else:
            return self.env['res.branch'].search([], limit=1, order='id').id

    branch_id = fields.Many2one('res.branch', string='Branch', default=_get_branch, required=True, readonly=True,
                                states={'draft': [('readonly', False)]})

    location_ids = fields.Many2many(
        'stock.location', string='Locations',
        readonly=True, check_company=True,
        states={'draft': [('readonly', False)]},
        domain="[('company_id', '=', company_id), ('usage', 'in', ['internal', 'transit']),('branch_id', '=', branch_id)]")

    state = fields.Selection(tracking=True)

    def _track_subtype(self, init_values):
        self.ensure_one()
        if "state" in init_values and self.state == "confirm":
            return self.env.ref("stock_siic.mt_inventory_confirmed")
        elif "state" in init_values and self.state == "done":
            return self.env.ref("stock_siic.mt_inventory_done")
        return super(StockInventory, self)._track_subtype(init_values)
