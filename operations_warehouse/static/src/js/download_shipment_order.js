/**@odoo-module */
import { registry } from "@web/core/registry";
const { Component, onMounted } = owl;
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
		let recordId = self.props.action.context.active_id

         rpc.query({
            model: 'bossa.shipment.orders',
            method: 'create_xlsx',
			args: [recordId]
        }).then(
			function (result) {
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
PrintAction.template = "PrintAction"
actionRegistry.add('print_action', PrintAction);

