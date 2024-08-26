from odoo import fields, models, api

from odoo.exceptions import UserError, ValidationError

class StockMove(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('partner_id', 'company_id')
    def onchange_partner_id(self):
        self = self.with_company(self.company_id)
        default_currency = self._context.get("default_currency_id")
        if not self.partner_id:
            self.fiscal_position_id = False
            #bob_currency = self.env.ref('base.BOB')
            self.currency_id = default_currency
        else:
            self.fiscal_position_id = self.env['account.fiscal.position']._get_fiscal_position(self.partner_id)
            self.payment_term_id = self.partner_id.property_supplier_payment_term_id.id
            if self.partner_id.partner_aux:
                usd_currency = self.env.ref('base.USD')
                if usd_currency:
                    self.currency_id = usd_currency
            else:
                bob_currency = self.env.ref('base.BOB')
                if bob_currency:
                    self.currency_id = bob_currency
        return {}



    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id, readonly=True)

