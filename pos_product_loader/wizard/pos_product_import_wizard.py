from odoo import _, models


class PosProductImportWizard(models.TransientModel):
    _name = "pos.product.import.wizard"
    _description = "POS Product Import Wizard"

    def action_run_import(self):
        log = self.env["pos.product.import.log"].run_import()
        action = self.env.ref("pos_product_loader.action_pos_product_import_log").read()[0]
        action["views"] = [(self.env.ref("pos_product_loader.view_pos_product_import_log_form").id, "form")]
        action["res_id"] = log.id
        action["target"] = "current"
        return action

