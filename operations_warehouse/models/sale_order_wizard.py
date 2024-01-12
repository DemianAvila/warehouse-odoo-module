from odoo import models, fields

class SaleOrderWizard(models.TransientModel):
    _name = "sale.order.edit"
    sale_order_id = fields.Many2one(
        comodel_name = "sale.order"
    )
    documents = fields.Many2many(
        comodel_name = "ir.attachment"
    )
    products = fields.Many2many(
        comodel_name = "sale.order.lines"
    )

