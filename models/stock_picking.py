# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    branch_id = fields.Many2one('res.branch', related='picking_type_id.branch_id', store=True, readonly=1)

