# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import base64
import xlrd
class WhatsappWizard(models.TransientModel):
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
            for row in range(1, sheet.nrows):
                product_code = str(sheet.cell(row, 0).value).strip()
                numero_serie =str(sheet.cell(row, 1).value).strip()
                #quantity = sheet.cell(row, 1).value
                #price_unit = sheet.cell(row, 2).value


                if not product_code:
                    raise ValidationError(f"El código de producto en la fila {row} está vacío o no es válido.")

                product = self.env['product.product'].search([('name', '=', product_code)], limit=1)
                if not product:
                    raise ValidationError(f"El producto con código '{product_code}' no existe en el sistema.")

             
                if product.id == product_id.id:
                    contador = contador + 1
                
            move_line.quantity_done = contador



