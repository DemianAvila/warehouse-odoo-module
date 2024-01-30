from odoo import models, fields, api
import logging

def visible_log(log):
    logging.info("===============================")
    logging.info(log)
    logging.info("===============================")

class DownloadShipmentGuides(models.TransientModel):
    _name = 'download.shipment.guides'
    file = fields.Binary()
    filename = fields.Char()
    scanner_view = fields.Many2one(
        comodel_name = 'scanner.check.lifecycle',
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

    compare_barcode = fields.Char(
        string = 'Compare Barcode',
        readonly=True
    )

    prod_barcode_equal = fields.Boolean(
        default = False,
        readonly = True
    )

    is_error_prod_equal = fields.Boolean(
        default = False,
        readonly = True
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
        default=False,
        force_save=True
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

    order_id_int = fields.Char(
        readonly=True
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
    )

    internal_barcode_readonly = fields.Boolean(
        default=False
    )

    #EXECUTE FUNCTION WHEN OPENING THE MODEL
    @api.model
    def default_get(self, fields):
        self.internal_barcode_readonly = False
        #visible_log("Creating a shipment scan")
        #DROP ALL THE RECORDS IN SHIPMENT ORDERS
        #CREATE THEM AGAIN, BASED ON THE ACTUAL MODEL
        shipments = self.env["shipment.orders"]
        writen_shipments = [s.name for s in shipments.search([])]
        orders_in_model = self.env["bossa.shipment.orders"].search([
            ("order_title", "not in", writen_shipments)
        ])
        for order in orders_in_model:
            #visible_log(f"creating shipment order {order.order_title}")
            shipments.create({
                "name": order.order_title
            })
            #visible_log("create")
            #visible_log(self.env["shipment.orders"].search([]))
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

    @api.onchange("internal_barcode", "product_barcode")
    def _onchange_internal_barcode(self):
        self.product_card = False
        self.internal_barcode_readonly = True
        visible_log(f"search internal barcode {self.internal_barcode} {self.product_card}")
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
                sell_line = sell_line [0]
                #ASSIGN THE DATA TO THE VIEW
                self.product_name = sell_line.name
                self.image = sell_line.product_template_id.image_1920
                self.status_of_product = sell_line.life_cycle
                # .get(self.type)
                self.order_id = sell_line.order_id.name
                self.order_id_int = sell_line.id
                self.marketplace = "Marketplace no asignado" if len(sell_line.order_id.tag_ids) == 0  else sell_line.order_id.tag_ids[0].name
                self.delivery_company = "Paqueteria no asignada" if len(sell_line.order_id.x_studio_envio) == 0 else sell_line.order_id.x_studio_envio[0].name
                self.compare_barcode = sell_line.product_template_id.barcode
                visible_log(f"""
                {self.internal_barcode_exists}
                {sell_line}
                {self.product_name} 
                {self.image} 
                {self.status_of_product} 
                {self.order_id} 
                {self.marketplace} 
                {self.delivery_company} 
                {self.order_id_int}
                {self.compare_barcode}
                """)
                self.internal_barcode_exists = True
                self.product_card = True
                visible_log(f"card visible {self.product_card}")
            else:
                visible_log(f"barcode does not exist")
                self.internal_barcode_exists = False
                self.product_card = False
        else:
            self.product_card = False
            self.internal_barcode_exists = True

    @api.onchange("product_barcode")
    def _onchange_product_barcode(self):
        visible_log(f"""The product bar code has been scanned
         {self.product_barcode}
         {self.compare_barcode}
         {self.order_id_int}
         """)

        if self.product_barcode == self.compare_barcode:
            visible_log(f"the barcode scanned is equal")
            self.prod_barcode_equal = True
            self.is_error_prod_equal = False
            #GET ALL DOCUMENTS OF A ORDER
            documents = self.env['ir.attachment'].search(
                [
                    ("order_line", "=", int(self.order_id_int)),
                    ("order_line", "!=", False)
                ]
            )
            visible_log(f"GET THE DOCUMENTS {documents}")
            write_documents = []
            for document in documents:
                write_documents.append(
                    (0,0,{
                        "file": document.datas,
                        "filename": document.name
                    })
                )
            visible_log(f"update the documents in this notebook {write_documents}")
            if len(write_documents) > 0:
                visible_log(f"try to upgrade the doc list")
                self.update({"documents":write_documents})
        else:
            visible_log(f"the barcode scanned is different")
            self.prod_barcode_equal = False
            self.is_error_prod_equal = True




    def reset_internal_barcode(self):
        self.internal_barcode = False
        self.internal_barcode_readonly = False
        self.product_card = False
