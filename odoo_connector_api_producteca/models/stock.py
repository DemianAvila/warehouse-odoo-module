# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, osv, models, api
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

import pdb

import requests

class stock_location(models.Model):

    _inherit = "stock.location"

    producteca_logistic_type = fields.Char(string="Logistic Type Asociado (Producteca)",index=True)

class stock_warehouse(models.Model):

    _inherit = "stock.warehouse"

    producteca_logistic_type = fields.Char(string="Logistic Type Asociado (Producteca)",index=True)

class stock_picking(models.Model):

    _inherit = "stock.picking"

    producteca_shippingLink_attachment = fields.Many2one(
            'ir.attachment',
            string='Guia Pdf Adjunta',
            copy=False
        )

    producteca_shippingLink_attachment_ok = fields.Boolean(string="Ok",default=False)

    def producteca_clean_print( self, max=None, date=None ):
        _logger.info("stock.picking_type producteca_clean_print START")
        sps = self.env["stock.picking"].search([
                    ('producteca_shippingLink_attachment','!=',None),
                    ('producteca_shippingLink_attachment_ok','=',False)])

        cMmax = max or 100
        if sps:
            _logger.info("stock.picking_type producteca_clean_print sps:"+str(len(sps))+" max:"+str(cMmax))
        cn = 0
        cM = 0

        for sp in sps:
            cn+=1
            cM+=1
            pris = self.env['ir.attachment'].search([('res_id','=',sp.id),
                                ('res_model','=','stock.picking'),
                                ('mimetype','=','application/pdf')])
            if pris and len(pris)>1:
                for pri in pris:
                    if sp.producteca_shippingLink_attachment!=pri:
                        _logger.info("stock.picking_type producteca_clean_print date:"+str(pri.name)+" "+str(pri.create_date))
                        pri.unlink()
                sp.producteca_shippingLink_attachment_ok = True
            else:
                sp.producteca_shippingLink_attachment_ok = True
            if cn>10:
                _logger.info("stock.picking_type producteca_clean_print commit")
                self.env.cr.commit()
                cn = 0
            if cM>cMmax:
                break;

        sos = self.env["sale.order"].search([
                    ('producteca_shippingLink_attachment','!=',None),
                    ('producteca_shippingLink_attachment_ok','=',False)])

        if sos:
            _logger.info("sale.order producteca_clean_print sos:"+str(len(sos))+" max:"+str(cMmax))
        cn = 0
        cM = 0

        for so in sos:
            cn+=1
            cM+=1
            pris = self.env['ir.attachment'].search([('res_id','=',so.id),
                                ('res_model','=','sale.order'),
                                ('mimetype','=','application/pdf')])
            if pris and len(pris)>1:
                for pri in pris:
                    if so.producteca_shippingLink_attachment!=pri:
                        _logger.info("sale.order producteca_clean_print date:"+str(pri.name)+" "+str(pri.create_date))
                        pri.unlink()
                so.producteca_shippingLink_attachment_ok = True
            else:
                so.producteca_shippingLink_attachment_ok = True
            if cn>10:
                _logger.info("sale.order producteca_clean_print commit")
                self.env.cr.commit()
                cn = 0
            if cM>cMmax:
                break;

        _logger.info("stock.picking_type producteca_clean_print END")

    def producteca_clean_old_print( self, max=None, date=None ):
        _logger.info("stock.picking_type producteca_clean_old_print START date:"+str(date))
        if date:
            cMmax = max or 100
            pris = None
            prisSP = self.env['ir.attachment'].search([('name','ilike','Shipment_PR%'),
                ('res_model','=','stock.picking'),
                ('mimetype','=','application/pdf'),
                ('create_date','<',date)],limit=cMmax/2)
            prisSO = self.env['ir.attachment'].search([('name','ilike','Shipment_PR%'),
                ('res_model','=','sale.order'),
                ('mimetype','=','application/pdf'),
                ('create_date','<',date)],limit=cMmax/2)
            _logger.info("stock.picking_type producteca_clean_old_print prisSP:"+str(len(prisSP)))
            _logger.info("stock.picking_type producteca_clean_old_print prisSO:"+str(len(prisSO)))
            pris = prisSP+prisSO
            #sqls = "select id, name, create_date, store_fname from ir_attachment where res_model = 'stock.picking' and mimetype = 'application/pdf' and create_date < '"+str(date)+"' and name ilike 'Shipment_PR%'"
            #_logger.info("sqls:"+str(sqls))
            #respb = self._cr.execute(sqls)
            #_logger.info("respb:"+str(respb))
            if pris:
                cn = 0
                cM = 0
                _logger.info("stock.picking_type producteca_clean_old_print pris:"+str(len(pris)))
                for pri in pris:
                    _logger.info("stock.picking_type producteca_clean_old_print date:"+str(pri.name)+" "+str(pri.create_date))
                    cn+=1
                    cM+=1
                    pri.unlink()
                    if cn>10:
                        _logger.info("stock.picking_type producteca_clean_old_print commit")
                        self.env.cr.commit()
                        cn = 0
                    if cM>cMmax:
                        break;

        _logger.info("stock.picking_type producteca_clean_old_print END date:"+str(date))

    def producteca_print(self):
        _logger.info("stock.picking_type producteca_print")
        sale_order = self.sale_id
        pso = sale_order and sale_order.producteca_binding
        #self.producteca_clean_print()
        if pso and not self.producteca_shippingLink_attachment:
            ret = pso.shippingLinkPrint()
            if ret and 'name' in ret:
                _logger.error(ret)
                return ret

            ATTACHMENT_NAME = "Shipment_"+sale_order.name
            b64_pdf = pso.shippingLink_pdf_file
            attachment = self.env['ir.attachment'].create({
                'name': ATTACHMENT_NAME,
                'type': 'binary',
                'datas': b64_pdf,
                #'datas_fname': ATTACHMENT_NAME + '.pdf',
                #'store_fname': ATTACHMENT_NAME,
                'res_model': "stock.picking",
                'res_id': self.id,
                'mimetype': 'application/pdf'
            })
            if attachment:
                self.producteca_shippingLink_attachment = attachment.id
    
