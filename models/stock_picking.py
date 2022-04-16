# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _


class Picking(models.Model):
    _inherit = "stock.picking"

    date_done = fields.Datetime('Date of Transfer', copy=False, readonly=True,
                                states={'draft': [('readonly', False)], 'waiting': [('readonly', False)]},
                                help="Date at which the transfer has been processed or cancelled.")

    def action_done(self):
        for rec in self:
            date = rec.date_done
            res = super(Picking, rec).action_done()
            rec.date_done = date
            return res
