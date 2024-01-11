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
                ("create_date", ">=", since),
                ("create_date", "<=", until)
            ]
        )
        #STABLISH AN ONLY ID BY THE EPOCH
        epoch_ids = []
        #STORE PRODUCT BY ORDER CODE, AND ITSELF BY DELIVERY
        order_with_delivery_service = {}
        #FOR EACH ONE OF THE ORDERS
        for r in rec_in_dates:
            delivery_service = r.x_studio_envio[0].name if len(r.x_studio_envio)>0 else "Paqueteria no asignada"
            #IF DELIVERY SERVICE NOT IN DICT
            if delivery_service not in order_with_delivery_service.keys():
                order_with_delivery_service[delivery_service] = {}
                #STORE THE ORDER ID IN LIST OF DICTS
                order_with_delivery_service[delivery_service]["order_ids"] = []
            #CREATE DICT FOR THIS ORDER ID
            order = {
                "id": r.name,
                "marketplace": r.tag_ids[0].name if len(r.tag_ids)>0 else "Marketplace no asignado",
                "products": [] 
            }
            #FOR EACH ONE OF THE PRODUCTS
            for line in r.order_line:
                #EACH ONE OF THE PRODUCTS MUST BE SCANNED ONCE
                for qty in range(int(line.product_uom_qty)):
                    #INTERNAL BARCODE THAT WILL BE NOT REPEATED
                    order_barcode = datetime.now().strftime('%s')
                    while order_barcode in epoch_ids:
                        order_barcode = datetime.now().strftime('%s')
                    epoch_ids.append(order_barcode)
                    product = {}
                    product["id"] = line.name
                    product["barcode"] = line.product_template_id[0].barcode if len(line.product_template_id)>0 else "Sin codigo de barras asignado"
                    product["internal_barcode"] = order_barcode
                    order["products"].append(product)
            order_with_delivery_service[delivery_service]["order_ids"].append(order)
                        
                
        return order_with_delivery_service 

    def delivery_header(self, delivery):
        return f""" 
        <div class="w-100 p-3 mb-2 bg-primary text-white ">
            {delivery_service}
        </div>
        """
        
    def order_id_header(self, order, marketplace):
        return f""" 
        <div class="w-100 p-3 mb-2 bg-info text-white ">
            <div class="w-50">
                {order}
            </div>
            <div class="w-50">
                {marketplace}
            </div>
        </div>
        """

    def product_id(self, product):
        return f"""
        <div class="w-100 p-3 mb-2 bg-light text-dark">
            {product}
        </div>
    """

    def format_datatable(self, data):
        html_agregate = ""
        for delivery in data.keys():
            html_agregate+=self.delivery_header(delivery)
            for order in data[delivery]["order_ids"]:
                html_agregate+=self.order_id_header(order["id"], order["marketplace"])
                for product in order["products"]:
                    html_agregate+=self.product_id(product["id"])

        return f"""
        <div class="w-100">
            {html_agregate}
        </div>    
        """

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
        if self.datetime_from>self.datetime_until:
            self.panic_error("No se puede buscar una fecha con intervalos invertidos")
            return 1
        
        order = self.search_sale_orders(self.datetime_from, self.datetime_until)
        self.shipment_table = self.format_datatable(order)
    


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

