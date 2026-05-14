/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class PosIconPickerDialog extends Component {
    static template = "pos_icon_picker.PosIconPickerDialog";
    static components = { Dialog };
    static props = {
        close: { type: Function },
        productId: { type: Number },
        productName: { type: String, optional: true },
    };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");

        this.state = useState({
            loading: true,
            styles: [],
            selectedStyle: "",
            selectedIcon: "",
            error: "",
        });

        onWillStart(async () => {
            try {
                const catalog = await this.orm.call("product.template", "get_pos_icon_catalog", []);
                this.state.styles = catalog.styles || [];
                if (this.state.styles.length) {
                    this.state.selectedStyle = this.state.styles[0].key;
                }
            } catch (error) {
                this.state.error = error.message || _t("Could not load icon styles.");
            } finally {
                this.state.loading = false;
            }
        });
    }

    get currentIcons() {
        const currentStyle = this.state.styles.find((style) => style.key === this.state.selectedStyle);
        return currentStyle ? currentStyle.icons : [];
    }

    onStyleChange(ev) {
        this.state.selectedStyle = ev.target.value;
        this.state.selectedIcon = "";
    }

    onIconClick(ev) {
        this.state.selectedIcon = ev.currentTarget.dataset.icon;
    }

    async onApply() {
        if (!this.state.selectedStyle || !this.state.selectedIcon) {
            this.notification.add(_t("Select an icon before applying."), { type: "warning" });
            return;
        }
        try {
            await this.orm.call("product.template", "apply_pos_icon", [
                this.props.productId,
                this.state.selectedStyle,
                this.state.selectedIcon,
            ]);
            this.notification.add(_t("POS icon updated."), { type: "success" });
            this.props.close();
            this.action.doAction({ type: "ir.actions.client", tag: "reload" });
        } catch (error) {
            this.notification.add(error.message || _t("Could not apply selected icon."), {
                type: "danger",
            });
        }
    }
}

function openPosIconPicker(env, action) {
    const productId = action?.params?.product_tmpl_id;
    if (!productId) {
        env.services.notification.add(_t("Product context is missing."), { type: "danger" });
        return;
    }
    env.services.dialog.add(PosIconPickerDialog, {
        productId,
        productName: action.params.product_name || "",
    });
}

registry.category("actions").add("pos_icon_picker_open", openPosIconPicker);

