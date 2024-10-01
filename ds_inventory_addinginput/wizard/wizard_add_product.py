from odoo import models, fields, api

class PurchaseEntryWizard(models.TransientModel):
    _name = 'stock.entry.wizard'
    _description = 'Wizard para cargar masiva de entradas'

    picking_id = fields.Many2one('stock.picking', string='Transferencia')
    additional_notes = fields.Text(string='Notas adicionales')
    product_ids = fields.Many2many('product.product', string='Productos a recibir')
    
    def confirm_wizard_action(self):
        picking = self.picking_id
        if picking:
            picking.message_post(body=f'Se ha confirmado el wizard con notas: {self.additional_notes}')
        return {'type': 'ir.actions.act_window_close'}
