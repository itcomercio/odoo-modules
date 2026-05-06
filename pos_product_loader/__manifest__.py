{
    "name": "Comodoo POS Product Loader",
    "summary": "Import POS products from a Linux filesystem path",
    "version": "19.0.1.0.0",
    "category": "Point of Sale",
    "author": "ITC",
    "license": "LGPL-3",
    "depends": ["base", "product", "point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/pos_product_import_views.xml",
        "data/ir_cron_data.xml",
    ],
    "demo": [
        "demo/demo_data.xml",
    ],
    "installable": True,
    "application": False,
}

