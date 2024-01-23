/**@odoo-module */
const FormController = require('web.FormController');
const { Component, useState } = owl;
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

	constructor() {
		super(...arguments);
		this.state = useState({
			product_name: "",
    		image:"",
    		status_of_product:"",
    		order_id:"",
    		marketplace: "",
    		delivery_company: ""
		});
	}

	start() {
        super.start();
		this.on('scanned_internal', this, this._onCustomEvent);
        return this._render();
    }

	 _onCustomEvent(ev) {
		console.log("It triggers the event")
        // Handle the custom_event and access the data
        const eventData = ev.data;
        console.log('Custom Event Received in Component:', eventData);

    }

	render() {
		console.log("Renders the widget")
		return this.env.qweb.render('operations_warehouse.product_id', {
			widget: this,
			data: this.state,
		});
	}
}

ProductCard.template = 'operations_warehouse.product_id';


