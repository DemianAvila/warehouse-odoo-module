/** @odoo-module */
import {loadBundle} from "@web/core/assets";
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var rpc = require('web.rpc');
var PrintAction = AbstractAction.extend(
	{
		start: function() {
			this._super.apply(this, arguments);
			rpc.query(
				{
					model: 'bossa.shipment.orders',
					method: 'create_xlsx',
				}
			).then(
				function (result) {
					const link = document.createElement("a");
					link.href = result;
					link.download = "ShipmentOrder.xlsx"
					link.click();
				}
			);
		}
	}
)
	
core.action_registry.add('print_action', PrintAction);
return PrintAction;