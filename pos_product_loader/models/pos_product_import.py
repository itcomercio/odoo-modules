import base64
import csv
from pathlib import Path

from odoo import _, api, fields, models


class PosProductImportLog(models.Model):
    _name = "pos.product.import.log"
    _description = "POS Product Import Log"
    _order = "create_date desc"

    name = fields.Char(string="Name", required=True, default=lambda self: _("POS Product Import"))
    status = fields.Selection(
        [
            ("done", "Done"),
            ("error", "Error"),
        ],
        string="Status",
        required=True,
    )
    import_path = fields.Char(string="Import Path", readonly=True)
    imported_count = fields.Integer(string="Imported", readonly=True)
    updated_count = fields.Integer(string="Updated", readonly=True)
    skipped_count = fields.Integer(string="Skipped", readonly=True)
    error_count = fields.Integer(string="Errors", readonly=True)
    notes = fields.Text(string="Notes", readonly=True)

    @api.model
    def cron_import_products(self):
        self.run_import()

    @api.model
    def run_import(self):
        config = self.env["ir.config_parameter"].sudo()
        import_path_value = (config.get_param("pos_product_loader.import_path") or "").strip()

        if not import_path_value:
            return self.create({
                "name": _("POS Product Import %s") % fields.Datetime.now(),
                "status": "error",
                "import_path": import_path_value,
                "error_count": 1,
                "notes": _("No import path configured. Set it in Point of Sale settings."),
            })

        import_path = Path(import_path_value)
        csv_path = import_path / "products.csv"
        images_path = import_path / "images"

        if not csv_path.exists():
            return self.create({
                "name": _("POS Product Import %s") % fields.Datetime.now(),
                "status": "error",
                "import_path": import_path_value,
                "error_count": 1,
                "notes": _("File not found: %s") % csv_path,
            })

        counters = {"imported": 0, "updated": 0, "skipped": 0, "errors": 0}
        messages = []

        with csv_path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for line_number, row in enumerate(reader, start=2):
                try:
                    self._process_row(row, images_path, counters)
                except Exception as err:  # noqa: BLE001
                    counters["errors"] += 1
                    messages.append(
                        _("Line %(line)s: %(error)s")
                        % {"line": line_number, "error": str(err)}
                    )

        status = "done" if counters["errors"] == 0 else "error"
        notes = "\n".join(messages) if messages else _("Import finished without errors.")

        return self.create({
            "name": _("POS Product Import %s") % fields.Datetime.now(),
            "status": status,
            "import_path": import_path_value,
            "imported_count": counters["imported"],
            "updated_count": counters["updated"],
            "skipped_count": counters["skipped"],
            "error_count": counters["errors"],
            "notes": notes,
        })

    def _process_row(self, row, images_path, counters):
        name = (row.get("name") or "").strip()
        default_code = (row.get("default_code") or "").strip()

        if not name:
            raise ValueError(_("Missing required field 'name'."))

        product = self._find_product(default_code, name)
        is_new = not bool(product)

        values = {
            "name": name,
            "default_code": default_code or False,
            "list_price": float((row.get("list_price") or "0").strip() or 0.0),
            "available_in_pos": True,
            "sale_ok": True,
            "purchase_ok": False,
            "type": "consu",
        }

        barcode = (row.get("barcode") or "").strip()
        if barcode:
            values["barcode"] = barcode

        category = self._get_or_create_product_category((row.get("category") or "").strip())
        if category:
            values["categ_id"] = category.id

        pos_category = self._get_or_create_pos_category(
            (row.get("pos_category") or "").strip()
        )
        if pos_category:
            values["pos_categ_ids"] = [(6, 0, [pos_category.id])]

        image_file = (row.get("image_file") or "").strip()
        if image_file:
            image_full_path = images_path / image_file
            if image_full_path.exists() and image_full_path.is_file():
                values["image_1920"] = base64.b64encode(image_full_path.read_bytes())

        if is_new:
            self.env["product.template"].create(values)
            counters["imported"] += 1
        else:
            product.write(values)
            counters["updated"] += 1

    def _find_product(self, default_code, name):
        Product = self.env["product.template"].sudo()
        if default_code:
            product = Product.search([("default_code", "=", default_code)], limit=1)
            if product:
                return product
        return Product.search([("name", "=", name)], limit=1)

    def _get_or_create_product_category(self, path_text):
        if not path_text:
            return False

        Category = self.env["product.category"].sudo()
        parent = False
        for part in [p.strip() for p in path_text.split("/") if p.strip()]:
            domain = [("name", "=", part)]
            if parent:
                domain.append(("parent_id", "=", parent.id))
            else:
                domain.append(("parent_id", "=", False))
            category = Category.search(domain, limit=1)
            if not category:
                category = Category.create({"name": part, "parent_id": parent.id if parent else False})
            parent = category
        return parent

    def _get_or_create_pos_category(self, path_text):
        if not path_text:
            return False

        PosCategory = self.env["pos.category"].sudo()
        parent = False
        for part in [p.strip() for p in path_text.split("/") if p.strip()]:
            domain = [("name", "=", part)]
            if parent:
                domain.append(("parent_id", "=", parent.id))
            else:
                domain.append(("parent_id", "=", False))
            category = PosCategory.search(domain, limit=1)
            if not category:
                category = PosCategory.create({"name": part, "parent_id": parent.id if parent else False})
            parent = category
        return parent

