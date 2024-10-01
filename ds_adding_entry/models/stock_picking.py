# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class DetailsSale(models.Model):
    _inherit = 'stock.picking'
    
 
    ############## WIZARD STOCK PICKING ##############
        
    def action_open_wizard(self):
        return{
            'type': 'ir.actions.act_window',
            'res_model': 'custom.stock.wizard',
            'name': 'Carga De Datos',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_picking_id': self.id,  
            }
            
        
        }
    
