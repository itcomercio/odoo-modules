{
    "name": "Comodoo POS Icon Picker",
    "summary": "Pick POS icons and floor images from bundled style libraries",
    "version": "19.0.1.0.0",
    "category": "Point of Sale",
    "author": "ITC",
    "license": "LGPL-3",
    "depends": ["point_of_sale", "pos_restaurant", "product", "web"],
    "data": [
        "views/product_template_views.xml",
        "views/restaurant_floor_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "pos_icon_picker/static/src/js/pos_icon_picker_action.js",
            "pos_icon_picker/static/src/xml/pos_icon_picker_dialog.xml",
            "pos_icon_picker/static/src/scss/pos_icon_picker.scss",
        ],
    },
    "installable": True,
    "application": False,
}

