from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPosIconPicker(TransactionCase):
    def test_catalog_contains_styles(self):
        catalog = self.env["product.template"].get_pos_icon_catalog()
        self.assertIn("styles", catalog)
        self.assertTrue(catalog["styles"])

    def test_apply_icon_sets_image(self):
        product = self.env["product.template"].create(
            {
                "name": "POS Icon Picker Test Product",
                "available_in_pos": True,
                "list_price": 1.0,
            }
        )
        catalog = self.env["product.template"].get_pos_icon_catalog()
        style = catalog["styles"][0]
        icon = style["icons"][0]

        self.env["product.template"].apply_pos_icon(product.id, style["key"], icon["filename"])
        self.assertTrue(product.image_1920)

    def test_apply_floor_image_sets_background(self):
        floor = self.env["restaurant.floor"].create(
            {
                "name": "POS Icon Picker Floor",
            }
        )
        catalog = self.env["product.template"].get_pos_icon_catalog()
        style = catalog["styles"][0]
        icon = style["icons"][0]

        self.env["restaurant.floor"].apply_pos_floor_image(floor.id, style["key"], icon["filename"])
        self.assertTrue(floor.floor_background_image)

