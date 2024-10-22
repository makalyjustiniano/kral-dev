
# -*- coding: utf-8 -*-

from odoo import http, api, models, fields
from odoo.http import request

import odoo.addons.web.controllers.main
from odoo.exceptions import UserError, ValidationError
from jinja2.environment import Template

from datetime import datetime

import json
import ssl
import requests
import os
import datetime
import pytz


global_url_geneararToken = "autenticacion/v1/generarToken"
global_url_geneararQr = "api/v1/generaQr"
global_url_inhabilitarPago = "api/v1/inhabilitarPago"
global_url_estadoTra = "api/v1/estadoTransaccion"
global_url_confirmPago = "endpoint/conﬁrmaPago"
port: 8443

class QRConection(http.Controller):

    @http.route('/api/get_token', type='json', auth='none', methods=['POST'], csrf=False)
    def get_token(self, **kwargs):

        company_id = 1
        #data_company = request.env['res.company'].browse(company_id)
        url = "https://dev-sip.mc4.com.bo:8443/autenticacion/v1/generarToken"
        
        api_key = kwargs.get('apikey', 'bcb2a3db7b6a0ad75c1238fbc996dcbf97af8b1f6c9fd375')
        username = kwargs.get('username', 'EMISORAMUTARIDESAROLLO')
        password = kwargs.get('password', 'Admin12345.+.')
        
        headers = {
            'apikey': api_key,
            'Content-Type': 'application/json'
        }
        
        body = {
            "username": username,
            "password": password
        } 
        try:
            response = requests.post(url, headers=headers, json=body)
            #response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'Error de conexión: ': str(e)}
  


    @http.route('/qr_pago/', auth='public', website=True, csrf=False)
    def index(self, **kw):
        data2 = http.request.env['res.company'].search_read([], limit=1)
        global global_url
        return "ok"

    @http.route('/qr_pago/', type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def index(self, **kw):
        data_message = json.loads(request.httprequest.data)
        return data_message 

    @http.route('/endpoint/conﬁrmaPago/', type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def index(self, **kw):
        data_message = json.loads(request.httprequest.data)
        return "ok"

    @http.route('/sent_request/', type='json', auth='public', methods=['POST'], cors='*', csrf=False)
    def get_form_values(self, **kw):
        data = json.loads(request.httprequest.data)
        return data
