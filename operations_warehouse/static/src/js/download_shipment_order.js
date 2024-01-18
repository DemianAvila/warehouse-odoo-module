/*var AbstractAction = require('web.AbstractAction');
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
					args: [{}]
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
return PrintAction; */

/**@odoo-module */
const { Component, onMounted } = owl;
import { registry } from "@web/core/registry";
const actionRegistry = registry.category("actions");
const rpc = require('web.rpc');
export class PrintAction extends Component {
    setup(){
        super.setup(...arguments);
        onMounted(()=>{
            this.loadData();
        })
    }
    loadData(){
        let self = this;
         rpc.query({
            model: 'bossa.shipment.orders',
            method: 'create_xlsx',
        }).then(
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
		);
	};
}

actionRegistry.add('print_action', PrintAction);

