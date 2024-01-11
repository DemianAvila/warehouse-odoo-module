from datetime import date, datetime
from odoo import models, fields


class ShipmentOrder(models.Model):
    _name = "bossa.shipment.orders"
    _inherit = "mail.thread"
    _description = """Generates and stores the shipment orders, 
    as well as it manages the state of the orders"""

    placement_date = fields.Date(
        string = "Placement date",
        default = date.today()
    )
    
    order_title = fields.Char(
        string = "Order title",
        default = f"Shipment order from {datetime.strftime(date.today(), '%d/%m/%Y')}"
    )

    datetime_from = fields.Datetime(
        string = "From"
    )
    
    datetime_until =  fields.Datetime(
        string = "Until"
    )



class InverseSell2Shipment(models.Model):
    _inherit = "sale.order"

    document_shipment_guides = fields.One2many(
        string = "Document shipment Guides",
        comodel_name = "ir.attachment",
        inverse_name = "guide_from_sell_order"
    )

    shipment_order = fields.Many2one(
        string="Shipment order",
        comodel_name="bossa.shipment.orders"
    )

