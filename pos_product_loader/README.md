# POS Product Loader

Modulo para Odoo 19 que importa productos para POS (restaurante) desde un directorio del filesystem Linux.

## Que hace

- Lee `products.csv` desde una ruta configurable en Ajustes.
- Opcionalmente toma imagenes desde `images/` en esa misma ruta.
- Crea o actualiza productos (`product.template`) para POS.
- Crea categorias de producto y categorias POS si no existen.
- Guarda logs de cada importacion.

## Formato de archivo esperado

Ruta configurada (ejemplo): `/opt/odoo/imports/pos_product_loader`

- `/opt/odoo/imports/pos_product_loader/products.csv`
- `/opt/odoo/imports/pos_product_loader/images/<archivo_imagen>`

Columnas del CSV:

- `default_code` (referencia interna)
- `name` (nombre producto)
- `list_price` (precio venta)
- `category` (categoria de producto, admite jerarquia: `Bebidas/Cafe`)
- `pos_category` (categoria POS, admite jerarquia: `Barra/Cafe`)
- `image_file` (nombre de archivo dentro de `images/`)
- `barcode` (opcional)

## Flujo rapido

1. Instalar el modulo.
2. Ir a **Punto de Venta > Configuracion > Ajustes** y definir la ruta en **POS Product Loader Path**.
3. Ir a **Punto de Venta > Product Loader > Import Logs** y pulsar **Importar ahora**.
4. Revisar el log de resultado.

## Prueba rapida

El modulo incluye datos de demo para pruebas:

- CSV de ejemplo: `pos_product_loader/demo/import/products.csv`
- Imagenes de ejemplo: `pos_product_loader/demo/import/images/`

Puedes copiar ese contenido a la ruta real configurada y lanzar la importacion.

