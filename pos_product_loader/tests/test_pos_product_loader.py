from pathlib import Path

from odoo.tests.common import SavepointCase


class TestPosProductLoader(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_path = Path("/tmp/odoo_pos_product_loader_test")
        cls.images_path = cls.temp_path / "images"
        cls.images_path.mkdir(parents=True, exist_ok=True)
        cls.csv_path = cls.temp_path / "products.csv"

        # 1x1 transparent PNG
        png_bytes = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
            b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfe"
            b"A\x0f\x95\x9b\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        (cls.images_path / "test.png").write_bytes(png_bytes)

        cls.csv_path.write_text(
            "default_code,name,list_price,category,pos_category,image_file,barcode\n"
            "POS-TST-01,Test Coffee,2.50,Bebidas/Cafe,Barra/Cafe,test.png,1234567890123\n",
            encoding="utf-8",
        )

        cls.env["ir.config_parameter"].sudo().set_param(
            "pos_product_loader.import_path", str(cls.temp_path)
        )

    def test_import_creates_product(self):
        log = self.env["pos.product.import.log"].run_import()
        self.assertEqual(log.status, "done")
        self.assertEqual(log.imported_count, 1)

        product = self.env["product.template"].search([("default_code", "=", "POS-TST-01")], limit=1)
        self.assertTrue(product)
        self.assertEqual(product.name, "Test Coffee")
        self.assertTrue(product.available_in_pos)
        self.assertEqual(product.list_price, 2.5)
        self.assertTrue(product.image_1920)

