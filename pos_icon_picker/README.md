# Comodoo POS Icon Picker

Odoo 19 addon for Point of Sale product icon selection.

## What it does

- Adds a **Point of Sale > Icon Picker > POS Products** submenu.
- Adds a **Change POS Icon** button in the product form.
- Opens a JavaScript modal with:
  - style selector (`style-1`, `style-2`, `style-3`)
  - icon gallery loaded from `pos_icon_picker/icons`
- Applies the selected icon directly to `product.template.image_1920`.

## Installation

1. Add this repository to your addons path.
2. Update apps list.
3. Install `Comodoo POS Icon Picker`.

## Usage

1. Open **Point of Sale > Icon Picker > POS Products**.
2. Open a POS product.
3. Click **Change POS Icon**.
4. Select style + icon and click **Apply Icon**.

## Technical notes

- Icon files are read from the addon folder at runtime.
- Allowed users: POS Managers (`point_of_sale.group_pos_manager`).

