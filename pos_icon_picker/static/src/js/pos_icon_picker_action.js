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
        targetModel: { type: String },
        targetId: { type: Number },
        targetName: { type: String, optional: true },
        pickerMode: { type: String },
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

    get titleLabel() {
        return this.props.pickerMode === "floor" ? _t("Choose Floor Image") : _t("Choose POS icon");
    }

    get styleLabel() {
        return this.props.pickerMode === "floor" ? _t("Image style") : _t("Icon style");
    }

    get loadingLabel() {
        return this.props.pickerMode === "floor" ? _t("Loading images...") : _t("Loading icons...");
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
            const warningMsg =
                this.props.pickerMode === "floor"
                    ? _t("Select an image before applying.")
                    : _t("Select an icon before applying.");
            this.notification.add(warningMsg, { type: "warning" });
            return;
        }

        const rpcMethod = this.props.pickerMode === "floor" ? "apply_pos_floor_image" : "apply_pos_icon";
        const successMsg =
            this.props.pickerMode === "floor" ? _t("Floor image updated.") : _t("POS icon updated.");
        const errorMsg =
            this.props.pickerMode === "floor"
                ? _t("Could not apply selected image.")
                : _t("Could not apply selected icon.");

        try {
            await this.orm.call(this.props.targetModel, rpcMethod, [
                this.props.targetId,
                this.state.selectedStyle,
                this.state.selectedIcon,
            ]);
            this.notification.add(successMsg, { type: "success" });
            this.props.close();
            this.action.doAction({ type: "ir.actions.client", tag: "reload" });
        } catch (error) {
            this.notification.add(error.message || errorMsg, {
                type: "danger",
            });
        }
    }
}

function openPosIconPicker(env, action) {
    const params = action?.params || {};
    const targetModel = params.target_model || "product.template";
    const targetId = params.target_id || params.product_tmpl_id;
    const pickerMode = params.picker_mode || "product";

    if (!targetId) {
        const missingContextMsg =
            pickerMode === "floor" ? _t("Floor context is missing.") : _t("Product context is missing.");
        env.services.notification.add(missingContextMsg, { type: "danger" });
        return;
    }

    env.services.dialog.add(PosIconPickerDialog, {
        targetModel,
        targetId,
        pickerMode,
        targetName: params.target_name || params.product_name || "",
    });
}

registry.category("actions").add("pos_icon_picker_open", openPosIconPicker);

