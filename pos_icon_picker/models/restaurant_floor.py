import base64
import re
from pathlib import Path

from odoo import _, api, models
from odoo.exceptions import AccessError, UserError


SAFE_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


class RestaurantFloor(models.Model):
    _inherit = "restaurant.floor"

    def action_open_pos_floor_image_picker(self):
        self.ensure_one()
        return {
            "type": "ir.actions.client",
            "tag": "pos_icon_picker_open",
            "params": {
                "target_model": "restaurant.floor",
                "target_id": self.id,
                "target_name": self.display_name,
                "picker_mode": "floor",
            },
        }

    @api.model
    def apply_pos_floor_image(self, floor_id, style, filename):
        if not self.env.user.has_group("point_of_sale.group_pos_manager"):
            raise AccessError(_("You do not have permission to update floor images."))

        if not floor_id:
            raise UserError(_("A floor is required."))
        if not style or not filename:
            raise UserError(_("Please select an image style and image file."))
        if not SAFE_NAME_RE.match(style) or not SAFE_NAME_RE.match(filename):
            raise UserError(_("Invalid style or file name."))

        floor = self.browse(int(floor_id)).exists()
        if not floor:
            raise UserError(_("Floor not found."))

        floor.check_access("write")

        icon_file = Path(__file__).resolve().parents[1] / "icons" / style / filename
        if not icon_file.exists() or not icon_file.is_file() or icon_file.suffix.lower() != ".png":
            raise UserError(_("Image file not found: %s") % icon_file.name)

        with icon_file.open("rb") as icon_stream:
            floor.write({"floor_background_image": base64.b64encode(icon_stream.read())})

        return True

