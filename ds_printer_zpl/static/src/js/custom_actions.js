odoo.define("ds_printer_zpl.custom_actions", function (require) {
  "use strict";
  require("web.dom_ready");
  var ajax = require("web.ajax");
  const AbstractAction = require("web.AbstractAction");
  const core = require("web.core");
  const QWeb = core.qweb;
  console.log("ADD JS");
  let device = null;
  let writeCharacteristic = null;

  async function getSaleOrderByName(saleOrderName) {
    try {
      const searchResponse = await ajax.jsonRpc(
        "/web/dataset/call_kw",
        "call",
        {
          model: "sale.order",
          method: "search_read",
          args: [[["name", "=", saleOrderName]]],
          kwargs: {
            fields: [
              "id",
              "name",
              "partner_id",
              "date_order",
              "amount_total",
              "order_line",
            ],
            limit: 1,
          },
        },
      );
      if (searchResponse && searchResponse.length > 0) {
      }

      //console.log("Order_line: " , searchResponse[0].order_line)
      const searchResponseOrderlines = await ajax.jsonRpc(
        "/web/dataset/call_kw",
        "call",
        {
          model: "sale.order.line",
          method: "search_read",
          args: [[["id", "in", searchResponse[0].order_line]]],
          kwargs: {
            fields: [
              "product_id",
              "product_uom_qty",
              "price_unit",
              "price_subtotal",
            ],
          },
        },
      );

      for (var i = 0; i < searchResponseOrderlines.length; i++) {
        //console.log("Product_id: " , searchResponseOrderlines[i].product_id[1]);
      }
      var data_sale = [searchResponse, searchResponseOrderlines];
      return data_sale;
    } catch (error) {
      console.error("Error al obtener datos de la venta:", error);
      return null;
    }
  }
  $(document).on("click", function (event) {
    const $target = $(event.target).closest('button[name="connect_printer"]');
    if ($target.length) {
      var nombreVenta;
      var nombreVentaElement = document.querySelector(
        'span.o_field_char[name="name"]',
      );
      if (nombreVentaElement) {
        nombreVenta = nombreVentaElement.textContent.trim();
      } else {
        console.error("Elemento no encontrado");
      }
      console.log(nombreVentaElement.textContent.trim());
      getSaleOrderByName(nombreVentaElement.textContent.trim()).then((data) => {
        if (data) {
          var data2 = data[0];
          console.log(data2);
          for (var i = 0; i < data2.length; i++) {
            console.log(data2[i].partner_id[1]);
            console.log(data2[i].name);
          }

          var data3 = data[1];
          console.log(data3);
          for (var i = 0; i < data3.length; i++) {
            console.log(data3[i].product_id[1]);
          }
          connectToBluetoothDevice(data);
        }
      });
    }
  });
  async function connectToBluetoothDevice(data) {
    try {
      if (device == null) {
        device = await navigator.bluetooth.requestDevice({
          acceptAllDevices: true,
          //optionalServices: ['38eb4a80-c570-11e3-9507-0002a5d5c51b']
          services: ["38eb4a80-c570-11e3-9507-0002a5d5c51b"],
        });

        const server = await device.gatt.connect();
        const services = await server.getPrimaryService(
          "38eb4a80-c570-11e3-9507-0002a5d5c51b",
        );
        const characteristics = await services.getCharacteristics();

        for (let characteristic of characteristics) {
          if (characteristic.properties.write) {
            writeCharacteristic = characteristic;
            break;
          }
        }

        localStorage.setItem("lastConnectedDeviceName", device.name);
        localStorage.setItem("lastConnectedDeviceId", device.id);
        localStorage.setItem("lastConnectedDeviceAll", device);
      }
      if (writeCharacteristic) {
        const saleOrderId = data[0].id;
        console.log("ID de la venta: ", saleOrderId);
        const amount_total = data[0].amount_total;
        console.log("Amount Total: ", amount_total);
        const partnerName = data[0].partner_id[1];
        const orderLine = data[0].order_line;
        console.log("Nombre Cliente: ", partnerName);

        const zplCommand =
          "FACTURA " +
          saleOrderId +
          " TOTAL: " +
          amount_total +
          " Cliente: " +
          partnerName +
          "Order Line: " +
          orderLine;
        const encodedZPL = new TextEncoder("ascii").encode(zplCommand);
        await writeCharacteristic.writeValue(encodedZPL);

        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i);
          const value = localStorage.getItem(key);
          console.log(`Clave: ${key}, Valor: ${value}`);
        }
      } else {
        alert(
          "No se encontró ninguna característica con permisos de escritura.",
        );
      }
    } catch (error) {
      console.error("Error al conectar al dispositivo Bluetooth:", error);
    }
  }
});
