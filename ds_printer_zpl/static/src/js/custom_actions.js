odoo.define('ds_printer_zpl.custom_actions', function(require) {
  'use strict';
  require('web.dom_ready');
  var ajax = require('web.ajax');
  const AbstractAction = require('web.AbstractAction');
  const core = require('web.core');
  const QWeb = core.qweb;
  console.log("ADD JS");
  let device = null;
  let writeCharacteristic = null;
  
async function getSaleData(saleOrderName) {
    try {
        const searchResponse = await ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'sale.order',
            method: 'search_read',
            args: [[['name', '=', saleOrderName]]],
            kwargs: {
                fields: ['id','name', 'partner_id', 'date_order', 'amount_total','order_line', 'tax_totals_json'],
                limit: 1
            }
        });
             
        const searchResponseOrderlines = await ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'sale.order.line',
            method: 'search_read',
            args: [[['id', 'in', searchResponse[0].order_line]]],
            kwargs: {
                fields: ['product_id', 'product_uom_qty', 'price_unit', 'price_subtotal']
            }
            
        });

        var id_partner = searchResponse[0].partner_id[0];
       const searchResponsePartner = await ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'res.partner',
            method: 'search_read',
            args: [[['id', '=', id_partner]]],
            kwargs: {
               fields: ['street', 'vat', 'name', 'id']
        }
      });

      const searchResponseCompany = await ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'res.company',
            method: 'search_read',
            args: [[['id', '=', 1]]],
            kwargs: {
                fields: ['name', 'street', 'city', 'phone', 'mobile', 'vat']
        }
      });

       var data_sale = [searchResponse, searchResponseOrderlines, searchResponsePartner, searchResponseCompany]
       return data_sale;
    } catch (error) {
        console.error('Error al obtener datos de la venta:', error);
        alert("Error al obtener datos de la venta: ", error);
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

    getSaleData(nombreVentaElement.textContent.trim()).then(data => {
        if(data){
          var dataSale = data[0];
          console.log(dataSale);
          for (var i = 0; i < dataSale.length; i++) {
            console.log("Cliente Id : ", dataSale[i].partner_id[0]);
            console.log("Cliente Nombre: " , dataSale[i].partner_id[1]);
            console.log("Name Sale: ",dataSale[i].name);
            console.log("Total Venta: ",dataSale[i].amount_total);
            console.log("Total JSON: ",dataSale[i].tax_totals_json);
          }

          var dataOrderLines = data[1];
          console.log(dataOrderLines);
          for (var i = 0; i < dataOrderLines.length; i++) {
            console.log("Producto ", i , " : ", dataOrderLines[i].product_id[1]);
            console.log("Producto ", i , " Precio unitario : ", dataOrderLines[i].price_unit);
            console.log("Producto ", i , " Cantidad : ", dataOrderLines[i].product_uom_qty);
            console.log("Producto ", i , " Subtotal : ", dataOrderLines[i].price_subtotal);
          }
          var dataPartner = data[2];
          console.log(dataPartner);
          for (var i = 0; i < dataPartner.length; i++){
            console.log("Cliente NIT: ", dataPartner[i].vat);
            console.log("Cliente Dirección: ", dataPartner[i].street);
            console.log("Cliente Nombre: ", dataPartner[i].name);
          }
          var dataCompany = data[3];
          console.log(dataCompany);
          for (var i = 0; i < dataCompany.length; i++){
            console.log("Compañía NIT: ", dataCompany[i].vat);
            console.log("Compañía Dirección: ", dataCompany[i].street);
            console.log("Compañía Nombre: ", dataCompany[i].name);
            console.log("Compañía City: ", dataCompany[i].city);
          }

          connectToBluetoothDevice(data);
        }
        else {
          alert("Data no encontrada");
        }
    });
    }
  });
  async function connectToBluetoothDevice(data) {
    try {

      if (device == null){
      device = await navigator.bluetooth.requestDevice({
          acceptAllDevices: true, 
          //optionalServices: ['38eb4a80-c570-11e3-9507-0002a5d5c51b']
          services: ['38eb4a80-c570-11e3-9507-0002a5d5c51b']
      });
      
      
      const server = await device.gatt.connect();
      const services = await server.getPrimaryService('38eb4a80-c570-11e3-9507-0002a5d5c51b');
      const characteristics = await services.getCharacteristics();
      
      for (let characteristic of characteristics) {
        if (characteristic.properties.write) {
          writeCharacteristic = characteristic;
          break;
        }
      }

      localStorage.setItem('lastConnectedDeviceName', device.name);
      localStorage.setItem('lastConnectedDeviceId', device.id);
      localStorage.setItem('lastConnectedDeviceAll', device);
      }
      if (writeCharacteristic) {

        writeZPL(data, writeCharacteristic);
       
        //for (let i = 0; i < localStorage.length; i++) {
        //const key = localStorage.key(i);  
        //const value = localStorage.getItem(key);  
        //console.log(`Clave: ${key}, Valor: ${value}`);
        //}
        
      }
      else
      {
          alert('No se encontró ninguna característica con permisos de escritura.');
      }
    }catch (error) {
      console.error('Error al conectar al dispositivo Bluetooth:', error);
    }
  }
  async function writeZPL(data, writeCharacteristic) {
    try{
    const saleOrderId = data[0].id;
        
        const zplCommand = 'FACTURA ' + saleOrderId + ' TOTAL: ' + amount_total + ' Cliente: ' + partnerName + 'Order Line: ' + orderLine ;                              
        const encodedZPL = new TextEncoder('ascii').encode(zplCommand);
        await writeCharacteristic.writeValue(encodedZPL);
    } catch (error){
      console.error('Error al mandar datos a la impresora');
      alert('No se realizó el envío de los datos a la impresora');
    }
  }
});
