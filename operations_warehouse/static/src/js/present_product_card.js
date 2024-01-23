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
        onMounted(()=>{
            console.log("the widget has been mounted")
        });
    }


	start() {
        super.start();
		console.log("Component.started")
		this.on('scanned_internal', this, this._onCustomEvent);
    }

	 _onCustomEvent(ev) {
		console.log("It triggers the event")
        // Handle the custom_event and access the data
        const eventData = ev.data;
        console.log('Custom Event Received in Component:', eventData);

    }

}




