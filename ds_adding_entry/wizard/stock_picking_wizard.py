# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import base64
import xlrd
class StockWizard(models.TransientModel):
    _name = 'custom.stock.wizard'
    _description = 'Wizard: Adding Stock'
    

    excel_file = fields.Binary('Cargar Archivo Excel')
    picking_id = fields.Many2one('stock.picking', string="Documento de Entrada")    

  
    def cargar_data(self):
        if not self.excel_file:
            raise UserError("Cargue su archivo excel, por favor.")

        data = base64.b64decode(self.excel_file)
  
        workbook = xlrd.open_workbook(file_contents=data)
        sheet = workbook.sheet_by_index(0)  
   
        for move_line in self.picking_id.move_lines:

            product_id = move_line.product_id
            product_name = move_line.product_id.name
            quantity_demanded = move_line.product_uom_qty  
            description_picking = move_line.description_picking
            contador = 0
            excel_data_serie = []
            excel_data_nombre = []
            for row in range(1, sheet.nrows):
                product_code = str(sheet.cell(row, 0).value).strip()
                serial_number = str(sheet.cell(row, 2).value).strip()
                #peso_bruto = sheet.cell(row, 1).value
                #peso_neto = sheet.cell(row, 3).value


                if not product_code:
                    raise ValidationError(f"El código de producto en la fila {row} está vacío o no es válido.")

                product = self.env['product.product'].search([('name', '=', product_code)], limit=1)
                if not product:
                    raise ValidationError(f"El producto con código '{product_code}' no existe en el sistema.")

                if product.id == product_id.id:
                    if product_code in excel_data_nombre:

                        excel_data_serie.append(serial_number)
                        excel_data_nombre.append(product_name)
                        #raise ValidationError(serial_number)
                    else:
                        excel_data_serie.append(serial_number)
                        excel_data_nombre.append(product_name)

                    #serial_numbers = excel_data[serial_number]
                    
                    contador = contador + 1
                contadorp = 0
            #raise ValidationError(f' serie0: "{excel_data_serie[0]}", serie1:  "{excel_data_serie[1]}"')
                if product.id == product_id.id:
                        
                    for serial_number in excel_data_serie:
                        lot = self.env['stock.production.lot'].search([
                            ('name', '=', serial_number),
                            ('product_id', '=', product_id.id)
                        ], limit=1)
    
                        if not lot:
                            contadorp += 1
    
                            lot = self.env['stock.production.lot'].create({
                                'name': serial_number,  
                                'product_id': product_id.id,
                                'company_id': self.picking_id.company_id.id,
                            })

                        self.env['stock.move.line'].create({
                        'move_id': move_line.id,
                        'product_id': product_id.id,
                        'lot_id': lot.id,
                        'lot_name': lot.name,
                        'qty_done': 1,
                        'location_id': move_line.location_id.id,
                        'location_dest_id': move_line.location_dest_id.id,
                        'picking_id': self.picking_id.id,
                        'product_uom_id': move_line.product_uom.id
                        })
                    excel_data_serie = []
                    excel_data_nombre = []

                     
                #raise ValidationError(contadorp)



            #move_line.quantity_done = contado



