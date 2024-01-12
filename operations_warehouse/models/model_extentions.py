from datetime import date, datetime
from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class Guides (models.Model):
    _inherit = "ir.attachment"

    order_line = fields.Many2one(
        string = "Order line",
        comodel_name = "sale.order.line"
    )

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

    def see_product_info(self):
        _logger.debug("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        return self.env.ref("operations_warehouse.sale_order_edit_action").read()[0]

    document_shipment_guides = fields.One2many(
        string = "Document shipment Guides",
        comodel_name = "ir.attachment",
        inverse_name = "order_line"
    )

    shipment_order = fields.Many2one(
        string="Shipment order",
        comodel_name="bossa.shipment.orders"
    )

