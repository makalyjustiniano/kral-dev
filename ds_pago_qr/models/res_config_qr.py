from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
class ResConfigQR(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.constrains('apikey_config', 'username', 'password', 'verify_config')
    def _get_save(self):
        for record in self:
            data = self.env['res.company'].search([('method_qr', '=', True)], limit=1)
            if data:
                if record.verify_config:
                    if record.username != False and record.password != False and record.apikey_config != False:
                   
                        valores = {
                            'username': record.username,
                            'password': record.password,
                            'apikey_config': record.apikey_config, 
                            'text_conection': record.url_conection
                            
                        }
                        
                        data.write(valores)


    verify_config = fields.Boolean(string="Verificar Configuración", related="company_id.method_qr")
    username = fields.Char(string="Username")
    password = fields.Char(string="password")
    apikey_config = fields.Text(string="ApiKey")
    url_conection = fields.Char( string="URL")
