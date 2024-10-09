#from odoo import http
#from odoo.http import request
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

class BluetoothPrinterController(http.Controller):
    
    @http.route('/print_bluetooth/', auth='user', website=True)
    def history(self, **kw):
        return request.render('ds_printer_zpl.chathome_website', {})
