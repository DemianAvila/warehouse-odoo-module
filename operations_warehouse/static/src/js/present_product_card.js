/**@odoo-module */
const FormController = require('web.FormController');
const { Component, useState, onMounted } = owl;
const core = require('web.core');

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
	static template = "operations_warehouse.product_id";
	setup(){
		console.log("access the state")
        super.setup();
		this.state = useState({
			product_name: "",
    		image:"",
    		status_of_product:"",
    		order_id:"",
    		marketplace: "",
    		delivery_company: ""
		});
    }




}




