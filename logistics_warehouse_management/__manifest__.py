{
    "name": "Logistics & Warehouse Management",
    "version": "20.0.1.0.0",
    "summary": "Shipment tracking, storage billing, outbound operations and warehouse workflows",
    "category": "Inventory/Logistics",
    "author": "Karim Soliman",
    "license": "LGPL-3",
    "depends": ["base", "contacts", "stock", "account"],
    "data": [
        "security/logistics_security.xml",
        "security/ir.model.access.csv",
        "data/logistics_sequence.xml",
        "views/logistics_shipment_views.xml",
        "views/logistics_menus.xml",
        "reports/logistics_shipment_report.xml"
    ],
    "demo": [
        "demo/logistics_demo.xml"
    ],
    "application": True,
    "installable": True
}
