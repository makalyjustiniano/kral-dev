from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class PurchaseOrderPrice(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('price_unit')
    def onchange_price_unit_pivot(self):
        if self.currency_id:
            usd_currency = self.env.ref('base.USD')
            if self.currency_id == usd_currency:
                self.price_unit_aux2 = self.price_unit * self.currency_id.rate
            else:
                self.price_unit_aux2 = self.price_unit

    @api.depends('currency_id')
    def _compute_is_currency_usd(self):
        for record in self:
            record.is_currency_usd = record.currency_id and record.currency_id.name == 'USD'

    price_unit_aux2 = fields.Float(string='Bs Precio Unitario')

    is_currency_usd = fields.Boolean(
        string="¿Divisa en USD?",
        compute='_compute_is_currency_usd',
        store=True
    )




