from odoo import fields, models, api

class StockMove(models.Model):
    _inherit = 'stock.move'


    purchase_line_id = fields.Many2one(
        'purchase.order.line',
        string='Purchase Order Line',
    )

    price_unit_aux = fields.Float(
        string='Precio Unitario',
        related='purchase_line_id.price_unit_aux2',
        readonly=True,
        store=True,
    )



