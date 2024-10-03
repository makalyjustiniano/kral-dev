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
        serial_numbers_set = set()
        serial_numbers_set = set()

        for row in range(1, sheet.nrows):
            product_code_pivot = str(sheet.cell(row, 0).value).strip()
            serial_number_pivot = str(sheet.cell(row, 1).value).strip()

            if not product_code_pivot:
                raise ValidationError(f"El código de producto en la fila {row} está vacío o no es válido.")

            product = self.env['product.product'].search([('name', '=', product_code_pivot)], limit=1)
            if not product:
                raise ValidationError(f"El producto con código '{product_code_pivot}' no existe en el sistema.")

            if product.tracking == 'serial':
                if serial_number_pivot in serial_numbers_set:
                    raise ValidationError(f"Se encontró un número de serie duplicado para el producto '{product.name}' en la fila {row + 1}: '{serial_number_pivot}'. Verifique el archivo Excel.")

                serial_numbers_set.add(serial_number_pivot) 

        for move_line in self.picking_id.move_lines:

            product_id = move_line.product_id
            product_name = move_line.product_id.name
            quantity_demanded = move_line.product_uom_qty  
            description_picking = move_line.description_picking
            excel_data_serie = []
            excel_data_nombre = []
            excel_data_peso_brut = []
            excel_data_peso_neto = []
            for row in range(1, sheet.nrows):
                product_code = str(sheet.cell(row, 0).value).strip()
                serial_number = str(sheet.cell(row, 1).value).strip()
                peso_bruto = sheet.cell(row, 2).value
                peso_neto = sheet.cell(row, 3).value


                if not product_code:
                    raise ValidationError(f"El código de producto en la fila {row} está vacío o no es válido.")

                product = self.env['product.product'].search([('name', '=', product_code)], limit=1)
                if not product:
                    raise ValidationError(f"El producto con código '{product_code}' no existe en el sistema.")

                if product.id == product_id.id:
                    excel_data_serie.append(serial_number)
                    excel_data_nombre.append(product_name)
                    excel_data_peso_brut.append(peso_bruto)
                    excel_data_peso_neto.append(peso_neto)
                   
                    for index,serial_number in enumerate(excel_data_serie):
                        lot = self.env['stock.production.lot'].search([
                            ('name', '=', serial_number),
                            ('product_id', '=', product_id.id)
                        ], limit=1)
    
                        if not lot:
     
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
                        #'btc_peso_brut': excel_data_peso_brut[index],
                        'location_id': move_line.location_id.id,
                        'location_dest_id': move_line.location_dest_id.id,
                        'picking_id': self.picking_id.id,
                        'product_uom_id': move_line.product_uom.id
                        })
                    excel_data_serie = []
                    excel_data_nombre = []
                    excel_data_peso_brut = []
                    excel_data_peso_neto = []

                     






