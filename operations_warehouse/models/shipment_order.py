from datetime import date, datetime
from odoo import models, fields, api
import json
from . import printable_order
import base64
import logging

class ShipmentGuides(models.TransientModel):
    _name = 'sale_order.shipment_guides'

    file = fields.Binary(
        attachment = False,
        string = "Shipment Guide"
    )

    filename = fields.Char()

    sale_guide = fields.Many2one(
        comodel_name="tmp.shipment_guides"
    )

    ext_id = fields.Char()

class TmpGuides(models.TransientModel):
    _name = 'tmp.shipment_guides'

    guides = fields.One2many(
        comodel_name="sale_order.shipment_guides",
        inverse_name="sale_guide"
    )

    @api.model
    def default_get(self, fields):
        logging.info("==========================")
        logging.info(self)
        logging.info(self.env.context)
        logging.info("==========================")
        #WRITE THE DOCUMENTS IN THIS TMP MODEL
        documents = self.env["ir.attachment"].search(
            [
                ("id", "in", self.env.context.get('documents'))
            ]
        )
        logging.info("==========================")
        logging.info(documents)
        logging.info("==========================")
        for document in documents:
            self.create({
                "file": document.datas,
                "filename": document.name,
                "ext_id": document.id
            })
        return super(TmpGuides, self).default_get(fields)

    @api.model
    def write(self, vals):
        non_erased = []
        #OVERRIDE THE DOCUMENTS
        for guide in self.guides:
            #IF DOCUMENT HAS EXTERNAL ID
            if guide.ext_id:
                logging.info("==========================")
                logging.info("overriding doc")
                logging.info("==========================")
                non_erased.append(guide.ext_id)
                document = self.env['ir.attachment'].search(
                    [
                        ('id', '=', guide.ext_id)
                    ]
                )
                document[0].datas = self.file,
                document[0].name = self.filename
                logging.info("==========================")
                logging.info(guide.ext_id)
                logging.info("==========================")
            #IF IT DOESN'T EXIST, CREATE THEM
            else:
                logging.info("creating doc")
                id_write = self.env['ir.attachment'].create(
                    {
                        "datas": self.file,
                        "name": self.filename,
                        "order_line": self.env["sale.order.line"].search(
                            ["id", "=", self.env.context.get('order_line')]
                        )[0]
                    }
                )
                logging.info("==========================")
                logging.info(id_write.id)
                logging.info("==========================")
            #COMPARE THE NON ERASED IDS IF THE MODEL, ERASE THE ONES NOT ON THE LIST
            for file in self.env.context.get("documents"):
                if file not in non_erased:
                    logging.info("==========================")
                    logging.info("deleting file")
                    logging.info(file.id)
                    logging.info("==========================")
                    document = self.env['ir.attachment'].search(
                        [
                            ('id', '=', file)
                        ]
                    )
                    document[0].unlink()

        return super(TmpGuides, self).write(vals)

    @api.model
    def create(self, vals):
        non_erased = []
        # OVERRIDE THE DOCUMENTS
        for guide in self.guides:
            # IF DOCUMENT HAS EXTERNAL ID
            if guide.ext_id:
                logging.info("==========================")
                logging.info("overriding doc")
                logging.info("==========================")
                non_erased.append(guide.ext_id)
                document = self.env['ir.attachment'].search(
                    [
                        ('id', '=', guide.ext_id)
                    ]
                )
                document[0].datas = self.file,
                document[0].name = self.filename
                logging.info("==========================")
                logging.info(guide.ext_id)
                logging.info("==========================")
            # IF IT DOESN'T EXIST, CREATE THEM
            else:
                logging.info("creating doc")
                id_write = self.env['ir.attachment'].create(
                    {
                        "datas": self.file,
                        "name": self.filename,
                        "order_line": self.env["sale.order.line"].search(
                            ["id", "=", self.env.context.get('order_line')]
                        )[0]
                    }
                )
                logging.info("==========================")
                logging.info(id_write.id)
                logging.info("==========================")
            # COMPARE THE NON ERASED IDS IF THE MODEL, ERASE THE ONES NOT ON THE LIST
            for file in self.env.context.get("documents"):
                if file not in non_erased:
                    logging.info("==========================")
                    logging.info("deleting file")
                    logging.info(file.id)
                    logging.info("==========================")
                    document = self.env['ir.attachment'].search(
                        [
                            ('id', '=', file)
                        ]
                    )
                    document[0].unlink()

        return super(TmpGuides, self).create(vals)


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

    correct_scan = fields.Boolean(
        string = "Correct",
        default = False
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
        comodel_name = "ir.attachment",
        inverse_name = "order_line"
    )


    internal_barcode = fields.Char(
        string = "Internal Barcode",
        readonly = True
    )

    life_cycle = fields.Selection(
        selection=[
            ("not_supplied", "Not Supplied"),
            ('supplied', 'Supplied'),
            ('delivered_to_the_package_company', 'Delivered To The Package Company')
        ],
        default = 'not_supplied'
    )

    def check_guides (self):
        logging.info("==========================")
        logging.info(dir(self))
        logging.info(self.id)
        logging.info(self.name)
        logging.info("==========================")
        return {
            'name': "operations_warehouse.upload_shipment_guides_action",
            'res_model': "tmp.shipment_guides",
            'type': 'ir.actions.act_window',
            'view_mode': "form",
            'context': {
                'order_id': self.id,
                'documents': [guide.id for guide in self.shipment_guides]
            },
        }

        #return self.env.ref("operations_warehouse.upload_shipment_guides_action").read()[0]

class ShipmentOrderInherit(models.Model):
    _inherit = "bossa.shipment.orders"

    sell_orders = fields.One2many(
        string="Sell orders",
        comodel_name="sale.order",
        inverse_name="shipment_order"
    )

    shipment_table = fields.Text(
        readonly=True
    )

    shipment_data = fields.Char()

    is_error = fields.Boolean(
        default=False
    )

    error_code = fields.Char()

    def null_date(sefl,date):
        if not date:
            return True

    def reset_error(self):
        self.is_error = False
        self.error_code = ""

    def panic_error(self, message):
        self.is_error = True
        self.error_code = message

    def link_sale_order(self, id_):
        self.write({
            "sell_orders": [
                (4, id_)
            ]
        })

    
    def search_sale_orders(self, since, until):
        sale_order_cursor = self.env["sale.order"]
        rec_in_dates = sale_order_cursor.search(
            [
                ("create_date", ">=", since),
                ("create_date", "<=", until),
                ("state", "!=", "cancel")
            ]
        )
        #STABLISH AN ONLY ID BY THE EPOCH
        epoch_ids = []
        #STORE PRODUCT BY ORDER CODE, AND ITSELF BY DELIVERY
        order_with_delivery_service = {}
        #FOR EACH ONE OF THE ORDERS
        for r in rec_in_dates:
            #LINK THE SALE ORDER TO THE MODEL 
            self.link_sale_order(r.id)
            #GET NAME OF THE DELIVERY SERVICE
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
                    #IF THERE IS ALREADY INTERNAL BARCODE, DO NOT REASSIGN
                    if not line.internal_barcode:
                        product["internal_barcode"] = order_barcode
                        line.internal_barcode = order_barcode
                    else:
                        product["internal_barcode"] = line.internal_barcode 
                    order["products"].append(product)
            order_with_delivery_service[delivery_service]["order_ids"].append(order)
                        
                
        return order_with_delivery_service 

    def delivery_header(self, delivery):
        return f""" 
        <div class="w-100 p-3  bg-info text-white row font-weight-bold">
            {delivery}
        </div>
        """
        
    def order_id_header(self, order, marketplace):
        return f""" 
        <div class="w-100 p-3 bg-info text-white row font-weight-bold">
            <div class="w-50 col">
                {order}
            </div>
            <div class="w-50 col">
                {marketplace}
            </div>
        </div>
        """

    def product_id(self, product):
        return f"""
        <div class="w-100 p-3 bg-light text-dark row">
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
        <div class="w-100 container">
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
        self.shipment_data = str(json.dumps(order))


    @api.model
    def create_xlsx(self, rec_id):
        rec = self.env["bossa.shipment.orders"].search([("id", "=", rec_id)])[0]
        excel_data = base64.b64encode(
            printable_order.printable_order(rec.shipment_data, rec.order_title)
        ).decode('utf-8')

        excel_mediatype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return f"data:{excel_mediatype};base64,{excel_data}"

    def process_xlsx(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'print_action',
        }





