from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_product_loader_path = fields.Char(
        string="POS Product Loader Path",
        config_parameter="pos_product_loader.import_path",
        help="Absolute Linux path containing products.csv and optional images/.",
    )

