from odoo import fields, models

class Resusers(models.Model):
    _inherit = 'res.users'
    

    #category_user = fields.Boolean(string="Preventista", default=False)
    category_preventista = fields.Boolean(string='Preventista', default=False)
    category_auto_venta = fields.Boolean(string='Auto Venta', default=False)
    category_jefe_venta = fields.Boolean(string='Jefe de Ventas', default=False)
    category_jefe_contable = fields.Boolean(string='Jefe contable', default=False)
    category_cobrador = fields.Boolean(string='Cobrador', default=False)
    category_distribuidor = fields.Boolean(string='Distribuidor', default=False)