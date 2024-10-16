# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import base64
import xlrd
class StockWizard(models.TransientModel):
    _name = 'custom.qr.wizard'
    _description = 'Wizard: Payment QR'
   

    image_qr = fields.Image(string="QR IMAGE")

    
    def confirm_payment(self):
        pass

