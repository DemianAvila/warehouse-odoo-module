from datetime import date, datetime
from odoo import models, fields


class InverseSell2Shipment(models.Model):
    _inherit = "sale.order"
    
    shipment_order = fields.Many2one(
        string="Shipment order",
        comodel_name="bossa.shipment.orders"
    )

class ShipmentFields(models.Model):
    _inherit = "sale.order.line"
    
    scaner_log = fields.One2many(
        string = "Scanner log",
        comodel_name = "scanner.log",
        inverse_name = "order_line"
    )
    
    shipment_guides = fields.One2many(
        string = "Shipment guides",
        comodel_name = "shipment.guides",
        inverse_name = "order_line"
    )

    has_been_shipped = fields.Boolean(
        string = "Shipped",
        default = False
    )


