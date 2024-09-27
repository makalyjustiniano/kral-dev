from odoo import fields, models, api
import json

class SaleOrderTotals(models.Model):
    _inherit = 'sale.order'


    
    base_imponible = fields.Monetary(string='Base Imponible', compute='_extract_totales_from_json')
    total_general = fields.Monetary(string='Total General', compute='_extract_totales_from_json')

    @api.depends('tax_totals_json')
    def _extract_totales_from_json(self):
        for order in self:
            if order.tax_totals_json:
                
                tax_totals = json.loads(order.tax_totals_json)
                order.base_imponible = tax_totals.get('amount_untaxed', 0.0)
                order.total_general = tax_totals.get('amount_total', 0.0)



