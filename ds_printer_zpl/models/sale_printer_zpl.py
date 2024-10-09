import serial
from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
class StockPicking(models.Model):
    _inherit = 'sale.order'

    def action_open_controller(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/print_bluetooth',
            'target': 'new',
        }

    def action_print_bluetooth_label(self):
        # ZPL command to print a label
        zpl_command = f"""
        ^XA
        ^FO50,50^A0N,50,50^FDStock Picking: {self.name}^FS
        ^FO50,150^BCN,100,Y,N,N^FD{self.name}^FS
        ^XZ
        """
        # Connect to the Bluetooth printer using serial
        #bt_serial = serial.Serial('/dev/rfcomm0', baudrate=9600, timeout=1)
        #bt_serial.write(zpl_command.encode())
        #bt_serial.close()
        
        # Crear el archivo .zpl y guardarlo temporalmente en memoria
        zpl_filename = f"label_{self.name}.zpl"
        zpl_file_content = zpl_command.encode("utf-8")
        
        # Guardar el archivo como adjunto en Odoo para descargarlo
        attachment = self.env['ir.attachment'].create({
            'name': zpl_filename,
            'datas': base64.b64encode(zpl_file_content),
            'type': 'binary',
            'res_model': 'sale.order',
            'res_id': self.id,
            'mimetype': 'application/x-zpl',
        })



        # Retornar acción para descargar el archivo
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }        
        
