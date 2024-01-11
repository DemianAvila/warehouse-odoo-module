from datetime import date, datetime
from odoo import models, fields


class ShipmentOrder(models.Model):
    _name = "bossa.shipment.orders"
    _inherit = "mail.thread"
    _description = """Generates and stores the shipment orders, 
    as well as it manages the state of the orders"""

 
class InverseSell2Shipment(models.Model):
    _inherit = "sale.order"
    
    shipment_order = fields.Many2one(
        string="Shipment order",
        comodel_name="bossa.shipment.orders"
    )


