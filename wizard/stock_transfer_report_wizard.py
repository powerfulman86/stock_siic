# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class StockTransferReportWizard(models.TransientModel):
    _name = "stock.transfer.report.wizard"
    _description = "Stock Transfer Report Wizard"

    @api.model
    def _get_branch(self):
        if self.env.user.branch_id:
            return self.env.user.branch_id.id
        else:
            return self.env['res.branch'].search([], limit=1, order='id').id

    date_from = fields.Date(string="Start Date", default=fields.Date.today())
    date_to = fields.Date(string="End Date", default=fields.Date.today())
    product_ids = fields.Many2many(comodel_name="product.product", string="Products", required=True)
    branch_id = fields.Many2one(comodel_name="res.branch", string="Branch", help='This is branch to set',
                                default=_get_branch, required=True, )
    location_id = fields.Many2one(comodel_name="stock.location", string="Location", required=True,
                                  domain="[('usage', '=', 'internal'),'|',('branch_id','=',branch_id),('branch_id','=',False)]", )

    code = fields.Selection([('incoming', 'Receipt'),
                             ('outgoing', 'Delivery'),
                             ('internal', 'Internal Transfer'),
                             ('mrp_operation', 'Manufacturing')],
                            'Type of Operation', required=True)

    def button_export_html(self):
        self.ensure_one()
        action = self.env.ref("stock_siic.action_report_stock_transfer_report_html")
        vals = action.read()[0]
        context = vals.get("context", {})
        if context:
            context = safe_eval(context)
        model = self.env["report.stock.transfer.report"]
        report = model.create(self._prepare_stock_transfer_report())
        context["active_id"] = report.id
        context["active_ids"] = report.ids
        vals["context"] = context
        return vals

    def button_export_pdf(self):
        self.ensure_one()
        report_type = "qweb-pdf"
        return self._export(report_type)

    # def button_export_xlsx(self):
    #     self.ensure_one()
    #     report_type = "xlsx"
    #     return self._export(report_type)

    def _prepare_stock_transfer_report(self):
        self.ensure_one()
        return {
            "date_from": self.date_from,
            "date_to": self.date_to or fields.Date.context_today(self),
            "product_ids": [(6, 0, self.product_ids.ids)],
            "location_id": self.location_id.id,
            "branch_id": self.branch_id.id,
            "code": self.code,
        }

    def _export(self, report_type):
        model = self.env["report.stock.transfer.report"]
        report = model.create(self._prepare_stock_transfer_report())
        return report.print_report(report_type)
