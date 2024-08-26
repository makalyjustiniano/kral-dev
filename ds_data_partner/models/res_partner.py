from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_aux = fields.Boolean(string='Partner Aux')
