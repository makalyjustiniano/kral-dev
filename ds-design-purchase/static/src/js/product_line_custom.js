odoo.define('ds-design-purchase.inherit', function (require) {
    "use strict";

    console.log("JS Custom From Init");

    var ListView = require('web.ListView');
    var ListController = require('web.ListController');
    var FormController = require('web.FormController');

    var CustomListController = ListController.include({
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
            console.log('JS From ListController');
        }
    });

    var CustomListView = ListView.include({
        init: function (viewInfo, params) {
            this._super.apply(this, arguments);
            console.log('JS Custom ListView');
        }
    });

    var CustomFormController = FormController.include({
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
            this._adjustColumnWidth();
            console.log('JS From FormController');
        },

        _adjustColumnWidth: function () {
            var self = this;
            setTimeout(function () {
                console.log("Adjusting Width for product_id");
                  var formSheet = self.$el.find('.o_form_sheet');

                if (formSheet.length) {
                    formSheet.css('max-width', '95%');
                    console.log("Max-width adjusted for o_form_sheet");
                } else {
                    console.log("o_form_sheet not found");
                }
                var columnHeader = self.$el.find('th[data-name="product_id"]');
                if (columnHeader.length) {
                    columnHeader.css('width', '400px');
                    console.log("Width Product_id Adjusted");
                } else {
                    console.log("product_id not found");
                }
            }, 500);
        }

    });
});
