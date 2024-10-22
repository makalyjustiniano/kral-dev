from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import base64
from io import BytesIO
from PIL import Image
import qrcode
import requests
class PaymentQR(models.Model):
    _inherit = 'res.company'


    username = fields.Char(  string="Username", readonly=True)
    password = fields.Char( string="password", readonly=True)
    apikey_config = fields.Text( string="ApiKey", readonly=True)


    method_qr = fields.Boolean( string="Aceptar Pago QR")
    image_qr = fields.Char(string="Cargar Imagen qr", max_width=1024, max_height=1024)
    image_qr_saved = fields.Image(string="Imagen cargada",max_width=1024, max_height=1024)
    text_qr = fields.Char(string="Texto qr")
    text_conection = fields.Char(string="Conection", readonly=True)

    

    def generate_qr_image(self):
        if not self.text_qr:
            raise ValidationError("El campo 'Texto QR' no puede estar vacío.")

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.text_qr)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_byte_arr = buffered.getvalue()
        image_base64 = base64.b64encode(img_byte_arr).decode('utf-8')

        self.image_qr_saved = image_base64


    def resquest_qr_text(self):

        url = 'https://9be1-190-104-16-140.ngrok-free.app/api/get_token'

        payload = {}

        try:
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                result = response.json()
                raise ValidationError(f"Datos enviados estado: {response.status_code} Response: {result}")
            else:
                raise ValidationError("No exitoso")
        except Exception as e:
            raise ValidationError(f"Error: {e}")

