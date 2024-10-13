odoo.define('ds_printer_zpl.custom_actions', function(require) {
    'use strict';
    require('web.dom_ready'); 
    var ajax = require('web.ajax');
    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');
    const QWeb = core.qweb;
   console.log("ADD JS");
   $(document).on('click', function(event) {
        const $target = $(event.target).closest('button[name="connect_printer"]');
        if ($target.length) { 
            console.log('Botón de impresora presionado:');
            console.log('ID:', $target.attr('id'));
            console.log('Name:', $target.attr('name')); 
             connectToBluetoothDevice();
        }
    });
        async function connectToBluetoothDevice() {
        try {
            console.log('Intentando conectar a un dispositivo Bluetooth...');

            const device = await navigator.bluetooth.requestDevice({
                acceptAllDevices: true, // Puedes filtrar por nombre o servicios específicos si lo deseas
                optionalServices: ['38eb4a80-c570-11e3-9507-0002a5d5c51b']
            });

            
            const server = await device.gatt.connect();
            const services = await server.getPrimaryService('38eb4a80-c570-11e3-9507-0002a5d5c51b');
            console.log("Servicios disponibles:", services);
            const characteristics = await services.getCharacteristics();
            console.log("Características del servicio:", characteristics);

            let writeCharacteristic = null;
            for (let characteristic of characteristics) {
              if (characteristic.properties.write) {
                writeCharacteristic = characteristic;
                break;
              }
            }
            if (writeCharacteristic) {
              const zplCommand = 'IMPRESIÓN DE COTIZACIÓN ODOO V15 INDUSTRIAS KRAL!';                              
              await writeCharacteristic.writeValue(new TextEncoder().encode(zplCommand));
              //alert('Comando ZPL enviado a la impresora.');
            } else {
                alert('No se encontró ninguna característica con permisos de escritura.');
            }
        } catch (error) {
            console.error('Error al conectar al dispositivo Bluetooth:', error);
        }
    }
});
