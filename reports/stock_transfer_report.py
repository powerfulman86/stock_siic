# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockTransferReportView(models.TransientModel):
    _name = "stock.transfer.report.view"
    _description = "Stock Transfer Report View"
    _order = "date"

    date = fields.Date()
    reference = fields.Char()
    location_id = fields.Many2one(comodel_name="stock.location")
    location_dest_id = fields.Many2one(comodel_name="stock.location")
    product_id = fields.Many2one(comodel_name="product.product")
    product_qty = fields.Float()
    product_uom = fields.Many2one(comodel_name="uom.uom")
    state = fields.Char()


class StockTransferReport(models.TransientModel):
    _name = "report.stock.transfer.report"
    _description = "Stock Transfer Report"

    date_from = fields.Date()
    date_to = fields.Date()
    product_ids = fields.Many2many(comodel_name="product.product")
    branch_id = fields.Many2one(comodel_name="res.branch")
    location_id = fields.Many2one(comodel_name="stock.location")
    code = fields.Char(string="Code", required=False, )

    # Data fields, used to browse report data
    results = fields.Many2many(
        comodel_name="stock.transfer.report.view",
        compute="_compute_results",
        help="Use compute fields, so there is nothing store in database",
    )

    def _compute_results(self):
        self.ensure_one()
        date_from = self.date_from or "0001-01-01"
        self.date_to = self.date_to or fields.Date.context_today(self)
        locations = self.env["stock.location"].search([("id", "child_of", [self.location_id.id])])
        self._cr.execute(
            """
            select sml.date,
                sml.reference,
                sml.location_id,
                sml.location_dest_id,
                sml.product_id,
                sml.qty_done as product_qty,
                sml.product_uom_id as product_uom,
                sml.state
            from stock_move_line sml join stock_picking sp on sml.picking_id = sp.id
	            join stock_picking_type spt on spt.id= sp.picking_type_id
	        where (sml.location_id in %s or sml.location_dest_id in %s)
	            and sml.product_id in %s
	            and (CAST(sml.date as date) >= %s and CAST(sml.date as date) <= %s)
	            and spt.code = %s
	        ORDER BY sml.date
                """,
            (
                tuple(locations.ids),
                tuple(locations.ids),
                tuple(self.product_ids.ids),
                self.date_from,
                self.date_to,
                self.code,
            ),
        )

        stock_transfer_results = self._cr.dictfetchall()
        report_line = self.env["stock.transfer.report.view"]
        self.results = [report_line.new(line).id for line in stock_transfer_results]

    def print_report(self, report_type="qweb"):
        self.ensure_one()
        action = (self.env.ref("stock_siic.action_stock_transfer_report_pdf"))
        return action.report_action(self, config=False)

    def _get_html(self):
        result = {}
        rcontext = {}
        report = self.browse(self._context.get("active_id"))
        if report:
            rcontext["o"] = report
            result["html"] = self.env.ref("stock_siic.report_stock_transfer_report_html").render(rcontext)
        return result

    @api.model
    def get_html(self, given_context=None):
        return self.with_context(given_context)._get_html()
