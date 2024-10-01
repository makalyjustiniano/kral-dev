# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_open_wizard(self):
        wizard = self.env['stock.entry.wizard'].create({
            'picking_id': self.id,
        })
        return {
            'name': 'Gestión de Entrada de Productos',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.entry.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('ds_inventory_addinput.view_stock_purchase_wizard_form').id,
            'target': 'new',
            'res_id': wizard.id,
        }
