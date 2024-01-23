/**@odoo-module */
const FormController = require('web.FormController');
const { Component, useState, status } = owl;
import { registry } from "@web/core/registry";

export class InternalCodeListener extends FormController{
	scannedInternalBarcode (value) {
		console.log("The internal barcode value has changed")
		this.trigger_up(
			'scanned_internal',
			{
				value: value
			}
		);
	}
}



export class ProductCard extends Component {
	static template = "operations_warehouse.ProductCard";
	setup(){
		console.log("access the state")
		console.log(status)
        super.setup();
		this.state = useState({
			product_name: "a",
    		image:"",
    		status_of_product:"",
    		order_id:"",
    		marketplace: "",
    		delivery_company: ""
		});
    }
}

registry.category("fields").add("product_card",ProductCard)




