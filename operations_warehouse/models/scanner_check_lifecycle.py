from odoo import models, fields, api
import logging

def visible_log(log):
    logging.info("===============================")
    logging.info(log)
    logging.info("===============================")

class DownloadShipmentGuides(models.TransientModel):
    _name = 'download.shipment.guides'
    file = fields.Binary()
    scanner_view = fields.Many2one(
        comodel_name = 'scanner.check.view',
        string = 'Scanner View'
    )

class ShipmentOrders(models.TransientModel):
    _name = 'shipment.orders'
    name = fields.Char(
        string = 'Shipment Order Name',
        readonly = True
    )

class ScannerCheckLifecycle(models.TransientModel):
    _name = 'scanner.check.lifecycle'

    shipment_order_id = fields.Many2one(
        comodel_name = 'shipment.orders'
        )

    internal_barcode = fields.Char(
        string = 'Internal Barcode'
    )

    product_barcode = fields.Char(
        string = 'Product Barcode'
    )

    internal_barcode_exists = fields.Boolean(
        string = "Internal Barcode Exists",
        default = True
    )

    product_name = fields.Char(
        string = "Product Name",
        readonly = True
    )

    product_card = fields.Boolean(
    )

    image = fields.Binary()

    status_of_product = fields.Char(
        string = "Status of Product",
        readonly = True
    )

    order_id = fields.Char(
        string = "Order ID",
        readonly = True
    )

    marketplace = fields.Char(
        string = "Marketplace",
        readonly = True
    )

    delivery_company = fields.Char(
        string = "Delivery Company",
        readonly = True
    )

    documents = fields.One2many(
        comodel_name = "download.shipment.guides",
        inverse_name = "scanner_view",
        readonly = True
    )

    #EXECUTE FUNCTION WHEN OPENING THE MODEL
    @api.model
    def default_get(self, fields):
        #visible_log("Creating a shipment scan")
        #DROP ALL THE RECORDS IN SHIPMENT ORDERS
        for order in self.env["shipment.orders"].search([]):
            #visible_log(f"deleting shipment order {order.name}")
            order.unlink()
            #visible_log("delete")
        #CREATE THEM AGAIN, BASED ON THE ACTUAL MODEL
        shipments = self.env["shipment.orders"]
        for order in self.env["bossa.shipment.orders"].search([]):
            #visible_log(f"creating shipment order {order.order_title}")
            shipments.create({
                "name": order.order_title
            })
            #visible_log("create")
            #visible_log(self.env["shipment.orders"].search([]))

        self.product_card = not(self.product_card)
        return super(ScannerCheckLifecycle, self).default_get(fields)






    def get_sale_lines_ids(self):
        ids = []
        shipment_order= self.env["bossa.shipment.orders"].search(
            [
                ("order_title", "=", self.shipment_order_id.name)
            ]
        )

        sell_orders = shipment_order.sell_orders
        for sell_order in sell_orders:
            for order_line in sell_order.order_line:
                ids.append(order_line.id)

        return ids

    @api.onchange("internal_barcode")
    def _onchange_internal_barcode(self):
        visible_log(f"search internal barcode {self.internal_barcode}")
        #IF THERE'S A BAR CODE TO SEARCH
        if self.internal_barcode:
            #SEARCH THE INTERNAL BARCODE AND GET THE INFO
            sell_line = self.env['sale.order.line'].search(
                [
                    ('internal_barcode', '=', self.internal_barcode),
                    ('id', 'in', self.get_sale_lines_ids())
                ]
            )
            #MUST BE AT LEAST 1
            if len(sell_line) >0 :
                visible_log(f"barcode exists {sell_line}")
                self.internal_barcode_exists = True
                sell_line = sell_line [0]
                #ASSIGN THE DATA TO THE VIEW
                self.product_name = sell_line.name
                self.image = sell_line.product_template_id.image_1920
                self.status_of_product = sell_line.life_cycle
                # .get(self.type)
                self.order_id = sell_line.order_id.name
                self.marketplace = "Marketplace no asignado" if len(sell_line.order_id.tag_ids) == 0  else sell_line.order_id.tag_ids[0].name
                self.delivery_company = "Paqueteria no asignada" if len(sell_line.order_id.x_studio_envio) == 0 else sell_line.order_id.x_studio_envio[0].name
                visible_log(f"""
                {self.internal_barcode_exists}
                {sell_line}
                {self.product_name} 
                {self.image} 
                {self.status_of_product} 
                {self.order_id} 
                {self.marketplace} 
                {self.delivery_company} 
                """)
            else:
                visible_log(f"barcode does not exist")
                self.internal_barcode_exists = False