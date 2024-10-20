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
          var client_id;
          var client_name;
          var sale_name;
          var amount_total;
          var amount_totals_json_tax;

          var client_vat;
          var client_address;
          var client_street;
          var client_name2;

          var company_vat;
          var company_street;
          var company_name;
          var company_city;

          //console.log(dataSale);
          var dataSale = data[0];
          for (var i = 0; i < dataSale.length; i++) {
            client_id =  dataSale[i].partner_id[0];
            client_name =  dataSale[i].partner_id[1];
            sale_name = dataSale[i].name;
            amount_total = dataSale[i].amount_total;
            amount_totals_json_tax = dataSale[i].tax_totals_json;
          }

          var dataOrderLines = data[1];
          console.log(dataOrderLines);
          var orderDetails = "";
          for (var i = 0; i < dataOrderLines.length; i++) {
           // console.log("Producto ", i , " : ", dataOrderLines[i].product_id[1]);
           // console.log("Producto ", i , " Precio unitario : ", dataOrderLines[i].price_unit);
           // console.log("Producto ", i , " Cantidad : ", dataOrderLines[i].product_uom_qty);
           // console.log("Producto ", i , " Subtotal : ", dataOrderLines[i].price_subtotal);
            orderDetails += "Producto " + (i + 1) + ": " + dataOrderLines[i].product_id[1] + "\n";
            orderDetails += "Precio unitario: " + dataOrderLines[i].price_unit + "\n";
            orderDetails += "Cantidad: " + dataOrderLines[i].product_uom_qty + "\n";
            orderDetails += "Subtotal: " + dataOrderLines[i].price_subtotal + "\n";
            orderDetails += "--------------------\n"; // Línea separadora
          }
          var dataPartner = data[2];
          //console.log(dataPartner);
          for (var i = 0; i < dataPartner.length; i++){
            client_vat =  dataPartner[i].vat;
            client_street =  dataPartner[i].street;
            client_name2 =  dataPartner[i].name;
          }
          var dataCompany = data[3];
          //console.log(dataCompany);
          for (var i = 0; i < dataCompany.length; i++){
            company_vat =  dataCompany[i].vat;
            company_street = dataCompany[i].street;
            company_name =  dataCompany[i].name;
            company_city = dataCompany[i].city;
          }

          connectToBluetoothDevice(
            client_id,
            client_name,
            sale_name,
            amount_total,
            amount_totals_json_tax,
            client_vat,
            client_address,
            company_vat,
            company_street,
            company_name,
            company_city,
            orderDetails
          );
        }
        else {
          alert("Data no encontrada");
        }
    });
    }
  });
  async function connectToBluetoothDevice(
            client_id,
            client_name,
            sale_name,
            amount_total,
            amount_totals_json_tax,
            client_vat,
            client_address,
            company_vat,
            company_street,
            company_name,
            company_city,
            orderDetails
  )
 {
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

        writeZPL( 
            client_id,
            client_name,
            sale_name,
            amount_total,
            amount_totals_json_tax,
            client_vat,
            client_address,
            company_vat,
            company_street,
            company_name,
            company_city,
            orderDetails,
            writeCharacteristic
        );
       
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
  async function writeZPL(
            client_id,
            client_name,
            sale_name,
            amount_total,
            amount_totals_json_tax,
            client_vat,
            client_address,
            company_vat,
            company_street,
            company_name,
            company_city,
            orderDetails,
            writeCharacteristic
  )
{ 
    try{
          const zplCommand = ' Client Id:  ' + client_id  + ' Client Name: ' + client_name + ' Sale Name: ' + sale_name + ' Amount total: ' + amount_total + ' Detalles Línea Productos: ' + orderDetails;                              
          const encodedZPL = new TextEncoder('ascii').encode(zplCommand);
          await writeCharacteristic.writeValue(encodedZPL);

    } catch (error){
      console.error('Error al mandar datos a la impresora');
      alert('No se realizó el envío de los datos a la impresora');
    }
  }
});
