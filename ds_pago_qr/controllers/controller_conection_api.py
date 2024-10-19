
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


#url = "https://graph.facebook.com/v16.0/114177218269798/messages"
var_chat = 0
global_url = "https://graph.facebook.com/v17.0/114177218269798/messages"

class Chatroom(http.Controller):

 
    @http.route('/webhook3', auth='public', website=True, csrf=False)
    def index(self, **kw):
        data2 = http.request.env['res.config.settings'].search_read([], limit=1)
        data3 = http.request.env['details_modify.details_modify'].search_read([('verify_config', '=', True),('url', '!=', False)], order='id', limit=1)
        token_config = data3[0]['token_config']
        global global_url
        global_url = data2[0]['url_config']
        data_verify = request.httprequest.args.get('hub.verify_token')
        data_challenge = request.httprequest.args.get('hub.challenge')
        if str(data_verify) == token_config:
            return data_challenge
        else:
            return "ERROR DE AUTENTICACIÓN"

        return "ok"

    @http.route('/webhook3', type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def index(self, **kw):
        data_message = json.loads(request.httprequest.data)
        data3 = http.request.env['details_modify.details_modify'].search_read([('verify_config', '=', True)], order='id', limit=1)
        url = ""
        message_bot = ""
        if data3:
            url = data3[0]['url']
            message_bot = data3[0]['message_bot']
        data = str(data_message)
        data_name = ""
        status_message = ""
        # New Cliente
        automatic_response_saludo_name = "Hola bienvenido a Supercars, un gusto saludarte antes de responder tu solicitud me brindarías tu nombre completo, seguido de tu solicitud. Gracias."
        automatic_response_servicio = "Muchas gracias ahora te responderá un asesor, cuál era su consulta?"
        # Cliente ya registrado
        automatic_response_saludo = "Hola bienvenido a Supercars, un gusto saludarte Mariela, cuál era su consulta"

        try:
            message = data_message['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        except KeyError:
            message = ""
        try:
            id_whatsapp = data_message['entry'][0]['id']
        except KeyError:
            id_whatsapp = ""
        try:
            display_phone_number = data_message['entry'][0]['changes'][0]['value']['metadata']['display_phone_number']
        except KeyError:
            display_phone_number = ""
        try:
            phone_number_id = data_message['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
        except KeyError:
            phone_number_id = ""
        try:
            profile_name = data_message['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
        except KeyError:
            profile_name = ""
        try:
            wa_id = data_message['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
        except KeyError:
            wa_id = ""
        try:
            msg_from = data_message['entry'][0]['changes'][0]['value']['messages'][0]['from']
        except KeyError:
            msg_from = ""
        try:
            timestamp = data_message['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
            utc_time = datetime.datetime.utcfromtimestamp(int(timestamp)).replace(tzinfo=pytz.utc)
            bolivia_tz = pytz.timezone('America/La_Paz')
            local_time = utc_time.astimezone(bolivia_tz)
            local_format2 = str(local_time)
            local_format = ""
            contador = 0
            for letra in local_format2:
                if contador < len(local_format2) - 7:
                    local_format = local_format + letra
                contador = contador + 1
        except KeyError:
            local_format = ""
        try:
            message_type = data_message['entry'][0]['changes'][0]['value']['messages'][0]['type']
        except KeyError:
            message_type = ""
        try:
            field = data_message['entry'][0]['changes'][0]['field']
        except KeyError:
            field = ""
        try:
            message_id = data_message['entry'][0]['changes'][0]['value']['messages'][0]['id']
        except KeyError:
            message_id = ""

        # Recibidos
        try:
            statuses = data_message['entry'][0]['changes'][0]['value']['statuses'][0]['id']
        except KeyError:
            statuses = None

        try:
            status = data_message['entry'][0]['changes'][0]['value']['statuses'][0]['status']
            if len(status) > 0:
                status_message = "API"
            else:
                status_message = "Recibido"
        except KeyError:
            # Maneja la excepción si alguno de los valores no existe en el diccionario
            status = None
            if status == None:
                status_message = "Recibido"
        try:
            conversation_id = data_message['entry'][0]['changes'][0]['value']['messages'][0]['conversation']['id']
            # conversation_id = data_message['entry'][0]['changes'][0]['value']['statuses'][0]['conversation']['id']
        except KeyError:
            conversation_id = None

        try:
            expiration_timestamp = data_message['entry'][0]['changes'][0]['value']['statuses'][0]['conversation'][
                'expiration_timestamp']
            utc_time2 = datetime.datetime.utcfromtimestamp(int(expiration_timestamp)).replace(tzinfo=pytz.utc)
            bolivia_tz2 = pytz.timezone('America/La_Paz')
            local_time2 = utc_time2.astimezone(bolivia_tz2)
        except KeyError:
            expiration_timestamp = None

        try:
            origin_type = data_message['entry'][0]['changes'][0]['value']['statuses'][0]['conversation']['origin'][
                'type']
        except KeyError:
            origin_type = None

        try:
            pricing_model = data_message['entry'][0]['changes'][0]['value']['statuses'][0]['pricing']['pricing_model']
        except KeyError:
            pricing_model = None

        try:
            billable = data_message['entry'][0]['changes'][0]['value']['statuses'][0]['pricing']['billable']
        except KeyError:
            billable = ""

        try:
            recipient_id = data_message['entry'][0]['changes'][0]['value']['statuses'][0]['recipient_id']
        except KeyError:
            recipient_id = ""

        record = http.request.env['details_modify.details_modify'].search_read(
            [('message_from', '=', msg_from), ('nombre', '!=', 'Desconocido'), ], limit=1)
        # record2 = http.request.env['details_modify.details_modify'].search_read([('message_from', '=', msg_from), ('name', '!=', False), ('name', '!=', ''),], limit=1)
        if record:
            for rec in record:
                data_name = rec['nombre']
        else:
            data_name = "Desconocido"

        MyModel = http.request.env['details_modify.details_modify']
        vals = {
            'text_body': message,
            'status_message': status_message,
            'nombre': data_name,
            'id_whatsapp': id_whatsapp,
            'display_phone_number': display_phone_number,
            'phone_number_id': phone_number_id,
            'profile_name': profile_name,
            'wa_id': wa_id,
            'message_from': msg_from,
            'timestamp': str(local_format),
            'type': message_type,
            'field': field,
            'message_id': message_id,
            'statuses_id': statuses,
            'status': status,
            'conversation_id': conversation_id,
            'expiration_timestamp': '',
            'origin_type': origin_type,
            'pricing_model': pricing_model,
            'pricing_billable': billable,
            'recipient_id': recipient_id

        }
        MyModel.create(vals)

        #### Mini Bot ####
        if message == "Hola" or message == "hola" or message == "Información" or message == "información":

            payload2 = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": msg_from,
                "type": "text",
                "text": {
                    "preview_url": True,
                    "body": str(message_bot)
                }
            })
            headers2 = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer EAADPhNb9m9IBACkl7cF0BURQVHxaNnZCcIRoZBszTe98WLZAlbARTvCZCiHjHhwDmt85r2eEXxycedXRszrxtUn8U0KeUnUQD6u2vEFWGKRIP5cp6krnEheCqV1GQkgBto3BTeF8ZC1FZCJXmlGwswI8VrFZAW2pd5wvmmIGdcWL6EzhYe4SaWy'
            }
            global global_url
            response = requests.request("POST", url, headers=headers2, data=payload2)
            MyModel2 = http.request.env['details_modify.details_modify']
            vals2 = {
                'text_body': str(message_bot),
                'status_message': 'Enviado',
                'nombre': data_name,
                'timestamp': str(local_format),
                'wa_id': wa_id,
                'recipient_id': recipient_id,
                'message_from': msg_from,
                'profile_name': profile_name
            }
            MyModel2.create(vals2)

        return "OK"

    @http.route('/chatroom/', auth='user', website=True)
    def history(self, **kw):
        return request.render('chatroom.chathome_website', {})

    @http.route('/sentMessage/', type='json', auth='public', methods=['POST'], cors='*', csrf=False)
    def get_form_values(self, **kw):
        data = json.loads(request.httprequest.data)
        data3 = http.request.env['details_modify.details_modify'].search_read([('verify_config', '=', True)], order='id desc', limit=1)
        url = ""
        message_bot = ""
        if data3:
            url = data3[0]['url']
            message_bot = data3[0]['message_bot']

        result = {}
        result_message = ""
        result_code = ""
        result_number = ""
        result_contact = ""
        result_fecha = ""
        for key, value in data.items():
            if key == 'params':
                result = value
        for key, value in result.items():
            if key == 'message':
                result_message = value
            if key == 'code':
                result_code = value
            if key == 'number':
                result_number = value
            if key == 'fecha':
                result_fecha = value
            if key == 'contact':
                result_contact = value

        result_number = result_code + result_number
        # full_num = '59169188122'
        payload = json.dumps({
            "token": "r57ytpv4xr53u0w4",
            "to": result_number,
            "body": str(result_message)
        })
        payload2 = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": result_number,
            "type": "text",
            "text": {
                "preview_url": True,
                "body": str(result_message)
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }
        headers2 = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer EAADPhNb9m9IBACkl7cF0BURQVHxaNnZCcIRoZBszTe98WLZAlbARTvCZCiHjHhwDmt85r2eEXxycedXRszrxtUn8U0KeUnUQD6u2vEFWGKRIP5cp6krnEheCqV1GQkgBto3BTeF8ZC1FZCJXmlGwswI8VrFZAW2pd5wvmmIGdcWL6EzhYe4SaWy'
        }
        global global_url
        response = requests.request("POST", url, headers=headers2, data=payload2)
        MyModel = http.request.env['details_modify.details_modify']
        vals = {
            'text_body': result_message,
            'status_message': 'Enviado',
            'nombre': result_contact,
            'timestamp': result_fecha,
            'wa_id': result_number,
            'recipient_id': result_number,
            'my_status': True,
            'my_chatLive': True,
            'message_from': result_number,
            'profile_name': ''
        }
        MyModel.create(vals)

        return response
