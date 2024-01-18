/** @odoo-module */
import {loadBundle} from "@web/core/assets";
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var rpc = require('web.rpc');
var PrintAction = AbstractAction.extend(
	{
		start: function() {
			this._super.apply(this, arguments);
			console.log("BEFORE RPC")
			console.log(this)

			rpc.query(
				{
					model: 'bossa.shipment.orders',
					method: 'create_xlsx',
					args: [this.res_id]
				}
			).then(
				function (result) {
					console.log("================================")
					console.log(result)
					console.log("================================")

					const link = document.createElement("a");
					link.href = result;
					link.download = "ShipmentOrder.xlsx"
					link.click();
				}
			).catch(
				function(error) {
					console.error("Error during RPC call:", error);
				}
			);;
		}
	}
)
	
core.action_registry.add('print_action', PrintAction);
return PrintAction;