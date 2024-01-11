{
    'name': 'Operations - Warehouse',
    'version': '1',
    'author': 'Demian Avila - demian.avila@bossa.com.mx',
    'website': 'bossa.com.mx',
    "summary": 'Modlue to manage and automate the storage department task',
    "depends": ['base', 'sale_management'],
    'data': [
        "views/shipment_order_views.xml",
        "views/sale_order_wizard.xml"
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,

}
