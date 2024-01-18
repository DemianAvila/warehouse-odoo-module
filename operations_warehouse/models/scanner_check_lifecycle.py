from odoo import models, fields, api

class DownloadShipmentGuides(models.TransientModel):
    _name = 'download.shipment.guides'
    file = fields.Binary()
    scanner_view = fields.Many2one(
        comodel_name = 'scanner.check.view',
        string = 'Scanner View'
    )
class ScannerCheckLifecycle(models.TransientModel):
    _name = 'scanner.check.lifecycle'

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

    @api.onchange("internal_barcode")
    def _onchange_internal_barcode(self):
        #IF THERE'S A BAR CODE TO SEARCH
        if self.internal_barcode:
            #SEARCH THE INTERNAL BARCODE AND GET THE INFO
            sell_line = self.env['sale.order.line'].search(
                [
                    ('internal_barcode', '=', self.internal_barcode)
                ]
            )
            #MUST BE AT LEAST 1
            if len(sell_line) >0 :
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

            else:
                self.internal_barcode_exists = False