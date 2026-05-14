import base64
import re
from pathlib import Path

from odoo import _, api, models
from odoo.exceptions import AccessError, UserError


SAFE_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_open_pos_icon_picker(self):
        self.ensure_one()
        return {
            "type": "ir.actions.client",
            "tag": "pos_icon_picker_open",
            "params": {
                "product_tmpl_id": self.id,
                "product_name": self.display_name,
            },
        }

    @api.model
    def get_pos_icon_catalog(self):
        if not self.env.user.has_group("point_of_sale.group_pos_manager"):
            raise AccessError(_("You do not have permission to use the POS icon picker."))

        icons_root = Path(__file__).resolve().parents[1] / "icons"
        if not icons_root.exists() or not icons_root.is_dir():
            return {"styles": []}

        styles = []
        for style_dir in sorted(path for path in icons_root.iterdir() if path.is_dir()):
            style_icons = []
            for icon_file in sorted(style_dir.glob("*.png")):
                with icon_file.open("rb") as icon_stream:
                    encoded = base64.b64encode(icon_stream.read()).decode("ascii")
                style_icons.append(
                    {
                        "filename": icon_file.name,
                        "name": icon_file.stem.replace("-", " ").title(),
                        "image": encoded,
                    }
                )

            if style_icons:
                styles.append(
                    {
                        "key": style_dir.name,
                        "label": style_dir.name.replace("-", " ").title(),
                        "icons": style_icons,
                    }
                )

        return {"styles": styles}

    @api.model
    def apply_pos_icon(self, product_tmpl_id, style, filename):
        if not self.env.user.has_group("point_of_sale.group_pos_manager"):
            raise AccessError(_("You do not have permission to update POS icons."))

        if not product_tmpl_id:
            raise UserError(_("A product is required."))
        if not style or not filename:
            raise UserError(_("Please select an icon style and icon file."))
        if not SAFE_NAME_RE.match(style) or not SAFE_NAME_RE.match(filename):
            raise UserError(_("Invalid style or file name."))

        product = self.browse(int(product_tmpl_id)).exists()
        if not product:
            raise UserError(_("Product not found."))

        product.check_access("write")

        icon_file = Path(__file__).resolve().parents[1] / "icons" / style / filename
        if not icon_file.exists() or not icon_file.is_file() or icon_file.suffix.lower() != ".png":
            raise UserError(_("Icon file not found: %s") % icon_file.name)

        with icon_file.open("rb") as icon_stream:
            product.write({"image_1920": base64.b64encode(icon_stream.read())})

        return True


