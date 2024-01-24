/**@odoo-module */
const FormController = require('web.FormController');
const { Component, useState} = owl;
import { registry } from "@web/core/registry";

export class ProductCard extends Component {
	static template = "operations_warehouse.ProductCard";
	setup(){
		console.log("access the state")
        super.setup();
		let self = this;
		let recordData = self.props.record.data;
		console.log("==========================")
		console.log(self)
		console.log(recordData)
		console.log("==========================")
		this.state = useState({
			product_name: recordData.product_name,
    		image:recordData.image,
    		status_of_product:recordData.status_of_product,
    		order_id:recordData.order_id,
    		marketplace: recordData.marketplace,
    		delivery_company: recordData.delivery_company
		});
    }
}

registry.category("fields").add("product_card",ProductCard)




