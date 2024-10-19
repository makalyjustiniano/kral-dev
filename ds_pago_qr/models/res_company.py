from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import base64
from io import BytesIO
from PIL import Image
class PaymentQR(models.Model):
    _inherit = 'res.company'


    username = fields.Char(  string="Username", readonly=True)
    password = fields.Char( string="password", readonly=True)
    apikey_config = fields.Text( string="ApiKey", readonly=True)
    url = fields.Char( string="URL", readonly=True)

    method_qr = fields.Boolean( string="Aceptar Pago QR")
    image_qr = fields.Image(string="Cargar Imagen qr", max_width=1024, max_height=1024)
    image_qr_saved = fields.Image(string="Imagen cargada",max_width=1024, max_height=1024)
    text_qr = fields.Char(string="Texto qr")


    def generate_qr_image(self):
        decoded_data = base64.b64decode(self.text_qr)
        
        image = Image.open(BytesIO(decoded_data))
        buffered = BytesIO()
        image.save(buffered, format="PNG")                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        image_base64 = base64.b64encode(buffered.getvalue())

       

        #self.text_qr = base64_code  
        self.image_qr_saved = image_base64

    def resquest_qr_text(self):
        pass


