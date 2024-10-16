from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class PaymentQR(models.Model):
    _inherit = 'sale.order'

    method_qr = fields.Boolean(related='company_id.method_qr', string="QR Method", readonly=True)
    image_qr = fields.Image(related='company_id.image_qr_saved', string="QR IMAGE", readonly=True)

    def action_open_wizard_qr(self):
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'custom.qr.wizard',
            'name': 'Pago por QR',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_id': self.id,
                'default_image_qr': self.image_qr,        # Usando default_

            }
            
        
        }
    
