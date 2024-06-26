{
    'name': 'Operations - Warehouse',
    'version': '1',
    'author': 'Demian Avila - demian.avila@bossa.com.mx',
    'website': 'bossa.com.mx',
    "summary": 'Modlue to manage and automate the storage department task',
    "depends": ['base', 'sale_management'],
    'data': [
        "views/shipment_order_views.xml",
        "views/sale_order_wizard.xml",
        "views/scan_shipments.xml",
        "views/shipment_guide_inherit.xml"
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    "external_dependencies": {
        "python" : [
            "xlsxwriter",
            "io",
            "python-barcode",
            "opencv-python",
            "numpy"
        ]
    },
    'assets': {
        'web.assets_backend': [
            "operations_warehouse/static/src/xml/empty_template.xml",
            "operations_warehouse/static/src/js/download_shipment_order.js",
            "operations_warehouse/static/src/xml/product_card_template.xml",
            "operations_warehouse/static/src/js/present_product_card.js",
        ],
    },
}
