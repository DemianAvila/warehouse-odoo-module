from datetime import date, datetime
from odoo import models, fields


class ShipmentGuides(models.Model):
    _name = "shipment.guides"
    _description = """Stores all of the shipment guides for printing"""

    guides = fields.Binary(
        string = "File"
    )

    order_line = fields.Many2one(
        string = "Order line",
        comodel_name = "sale.order.line"
    )


class ScanerLog(models.Model):
    _name = "scanner.log"
    _description = """Store the tries of scan a right product when 
    preparing the shipment order"""
    
    order_line = fields.Many2one(
        string = "Order line",
        comodel_name = "sale.order.line"
    )

    timestamp = fields.Datetime(
        string = "Time Stamp"
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

class ShipmentOrderInherit(models.Model):
    _inherit = "bossa.shipment.orders"

    def null_date(sefl,date):
        if not date:
            return True

    def reset_error(self):
        self.is_error = False
        self.error_code = ""

    def panic_error(self, message):
        self.is_error = True
        self.error_code = message

    def search_sale_orders(self, since, until):
        sale_order_cursor = self.env["sale.order"]
        rec_in_dates = sale_order_cursor.search(
            [
                ("create_date", ">=" since),
                ("create_date", "<=", until)
            ]
        )
        self.shipment_table = rec_in_dates


    def create_shipment(self):
        #AT ANY CLICK, RESTART THE ERROR 
        self.reset_error()
        #CHECK IF NO DATES
        if self.null_date(self.datetime_from):
            self.panic_error("Por favor, introduzca fecha de inicio")
            return 1
        if self.null_date(self.datetime_until):
            self.panic_error("Por favor, introduzca fecha de fin")
            return 1
        #CHECK IF DATE FROM IS LARGER THAN DATE UNTIL
        if self.datetime_from<self.datetime_until:
            self.panic_error("No se puede buscar una fecha con intervalos invertidos")
            return 1
        
        self.search_sale_orders(self.datetime_from, self.datetime_until)

    placement_date = fields.Date(
        string = "Placement date",
        default = date.today()
    )
    
    order_title = fields.Char(
        string = "Order title",
        default = f"Shipment order from {datetime.strftime(date.today(), '%d/%m/%Y')}"
    )

    #sell_orders = fields.One2many(
    #    string = "Sell orders",
    #    comodel = "sale.order",
    #    inverse_name = "shipment_order"
    #)

    datetime_from = fields.Datetime(
        string = "From"
    )
    
    datetime_until =  fields.Datetime(
        string = "Until"
    )

    shipment_table = fields.Text(
    )
    
    is_error = fields.Boolean(
        default = False
    )

    error_code = fields.Char()

