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
		console.log("====================")
		console.log(recordId)
		console.log("====================")

         rpc.query({
            model: 'bossa.shipment.orders',
            method: 'create_xlsx',
			 args: [
				 {
					 id: recordId
				 }
			 ]
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
PrintAction.template = "PrintAction"
actionRegistry.add('print_action', PrintAction);

