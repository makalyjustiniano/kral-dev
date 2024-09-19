from odoo import fields, models, api

class Resusers(models.Model):
    _inherit = 'res.users'

    from odoo import models, api

    class ResUsers(models.Model):
        _inherit = 'res.users'

        @api.constrains('category_preventista', 'category_auto_venta', 'category_jefe_venta')
        def _onchange_sales_permission(self):
            preventista_group = self.env.ref('ds_accounts_users.group_custom_sales_restricted')
            autoventa_group = self.env.ref('ds_accounts_users.group_custom_sales_restricted_auto_venta')
            jefeventa_group = self.env.ref('ds_accounts_users.group_custom_sales_restricted_jefe_venta')
            if self.category_preventista:
                self.groups_id = preventista_group
            if self.category_auto_venta == True and self.category_jefe_venta == False:
                self.groups_id = preventista_group
                self.groups_id += autoventa_group
            if self.category_jefe_venta == True and self.category_preventista == True:
                self.groups_id = preventista_group
                self.groups_id += jefeventa_group


    category_preventista = fields.Boolean(string='Preventista', default=False, computed="_onchange_sales_permission")
    category_auto_venta = fields.Boolean(string='Auto Venta', default=False, computed="_onchange_sales_permission")
    category_jefe_venta = fields.Boolean(string='Jefe de Ventas', default=False, computed="_onchange_sales_permission")
    category_jefe_contable = fields.Boolean(string='Jefe contable', default=False)
    category_cobrador = fields.Boolean(string='Cobrador', default=False)
    category_distribuidor = fields.Boolean(string='Distribuidor', default=False)
