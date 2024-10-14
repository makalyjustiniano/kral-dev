odoo.define('ds_printer_zpl.custom_actions', function(require) {
  'use strict';
  require('web.dom_ready');
  var ajax = require('web.ajax');
  const AbstractAction = require('web.AbstractAction');
  const core = require('web.core');
  const QWeb = core.qweb;
  console.log("ADD JS");

async function getSaleOrderByName(saleOrderName) {
    try {
        const searchResponse = await ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'sale.order',
            method: 'search_read',
            args: [[['name', '=', saleOrderName]]],
            kwargs: {
                fields: ['id','name', 'partner_id', 'date_order', 'amount_total'],
                limit: 1
            }
        });
        if (searchResponse && searchResponse.length > 0) {
        }
        return searchResponse;
    } catch (error) {
        console.error('Error al obtener datos de la venta:', error);
        return null;
    }
}
  $(document).on('click', function(event) {
    const $target = $(event.target).closest('button[name="connect_printer"]');
    if ($target.length) { 
    var nombreVenta;
    var nombreVentaElement = document.querySelector('span.o_field_char[name="name"]');
    if (nombreVentaElement) {
      nombreVenta = nombreVentaElement.textContent.trim();
    } else {
      console.error("Elemento no encontrado");
    }
    console.log(nombreVentaElement.textContent.trim());
    getSaleOrderByName(nombreVentaElement.textContent.trim()).then(data => {
        if(data){
            const saleOrderId = data[0].id;
            console.log('ID de la venta: ', saleOrderId);
            const amount_total = data[0].amount_total;
            console.log('Amount Total: ', amount_total);
            const partnerName = data[0].partner_id[1];
            console.log('Nombre Cliente: ', partnerName);
         connectToBluetoothDevice(data);

        }
    });
    }
  });
  async function connectToBluetoothDevice(data) {
    try {

      const device = await navigator.bluetooth.requestDevice({
          acceptAllDevices: true, 
          optionalServices: ['38eb4a80-c570-11e3-9507-0002a5d5c51b']
      });
      
      
      const server = await device.gatt.connect();
      const services = await server.getPrimaryService('38eb4a80-c570-11e3-9507-0002a5d5c51b');
      const characteristics = await services.getCharacteristics();
      
      let writeCharacteristic = null;
      for (let characteristic of characteristics) {
        if (characteristic.properties.write) {
          writeCharacteristic = characteristic;
          break;
        }
      }
      if (writeCharacteristic) {
        const saleOrderId = data[0].id;
        console.log('ID de la venta: ', saleOrderId);
        const amount_total = data[0].amount_total;
        console.log('Amount Total: ', amount_total);
        const partnerName = data[0].partner_id[1];
        console.log('Nombre Cliente: ', partnerName);

        const zplCommand = 'FACTURA ' + saleOrderId + ' TOTAL: ' + amount_total + ' Cliente: ' + partnerName ;                              
        const encodedZPL = new TextEncoder('ascii').encode(zplCommand);
        await writeCharacteristic.writeValue(encodedZPL);      
      }
      else
      {
          alert('No se encontró ninguna característica con permisos de escritura.');
      }
    }catch (error) {
      console.error('Error al conectar al dispositivo Bluetooth:', error);
    }
  }
});
