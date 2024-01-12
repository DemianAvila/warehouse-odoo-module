from odoo import models, fields

class SaleOrderWizard(models.TransientModel):
    _name = "sale.order.edit"
    product_title = fields.Char()
    documents = fields.Many2many(
        comodel_name = "ir.attachment"
    )
    products = fields.Many2many(
        comodel_name = "sale.order.lines"
    )

