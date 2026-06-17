# Guía para Agentes de IA - odoo-modules

Este documento proporciona información contextual y directrices para agentes de IA que trabajen en este repositorio.

## Restricciones Críticas para Agentes
- **PROHIBIDO** ejecutar comandos de Git que modifiquen la copia de trabajo o el historial (`git add`, `git commit`, `git checkout`, `git reset`, `git push`, etc.).
- El agente solo debe crear o modificar archivos. La gestión del control de versiones (staging y commit) es responsabilidad exclusiva del usuario.

## Descripción del Proyecto
Este repositorio es un conjunto de módulos personalizados para **Odoo 19.0**, diseñados para extender las capacidades del Punto de Venta (POS) y la carga de datos.

## Módulos en el Repositorio

### 1. `pos_icon_picker`
- **Propósito**: Proporciona una interfaz visual para que los usuarios elijan iconos de productos y fondos de mapas de mesas en el restaurante POS.
- **Componentes clave**:
  - `pos_icon_picker_action.js`: Lógica OWL para el diálogo de selección.
  - `product_template.py` / `restaurant_floor.py`: Extensiones de modelos para manejar la aplicación de imágenes.
  - `icons/`: Biblioteca de imágenes organizada por estilos.

### 2. `pos_product_loader`
- **Propósito**: Automatiza la importación de productos desde rutas locales del servidor.
- **Componentes clave**:
  - `pos_product_import.py`: Lógica de importación y procesamiento de CSV/imágenes.
  - `ir_cron_data.xml`: Tarea programada para la carga automática.

### 3. `pos_screen_saver`
- **Propósito**: Cambia el logo del salvapantallas (screensaver) del POS.
- **Componentes clave**:
  - `pos_screen_saver.scss`: Sobrescribe el estilo `.pos-logo` dentro de `.login-overlay`.
  - `comodoo-logo.svg`: Logo personalizado de Comodoo.

## Tecnologías Principales
- **Lenguaje**: Python 3.12+
- **Framework**: Odoo 19.0 (incluye OWL para el frontend).
- **Frontend**: JavaScript, XML (QWeb), SCSS.
- **Datos**: XML para vistas y configuración, CSV para datos de demostración.

## Estándares y Convenciones

### Python
- Seguir **PEP 8**.
- Los nombres de los métodos deben ser descriptivos (ej. `_compute_display_name`).
- Usar decoradores de Odoo (`@api.model`, `@api.depends`, etc.) de forma apropiada.

### Odoo XML
- Usar IDs externos claros (ej. `view_product_template_form_inherit_pos_icon`).
- Preferir `xpath` con expresiones precisas para heredar vistas.

### JavaScript (OWL)
- Seguir el patrón de componentes de OWL.
- Asegurar que los parches (`patch`) a componentes base de Odoo se limpien correctamente si es necesario.

## Pruebas (Testing)
Las pruebas se encuentran en el directorio `tests/` de cada módulo.
- **Ejecución**:
  ```bash
  ./odoo-bin -i <nombre_modulo> --test-enable --stop-after-init
  ```
- **Requisito**: Toda nueva funcionalidad debe incluir al menos un caso de prueba en `TransactionCase`.

## Flujo de Trabajo para Agentes
1. **Investigación**: Antes de proponer cambios, revisa el `__manifest__.py` para entender las dependencias.
2. **Implementación**: Mantén los cambios dentro del módulo correspondiente.
3. **Localización**: Si añades textos nuevos, usa `_("")` en Python o `_t("")` en JS y actualiza los archivos `.po` en `i18n/`.
4. **Verificación**: Ejecuta los tests existentes para asegurar que no hay regresiones.

## Estructura del Repositorio
```text
.
├── pos_icon_picker/          # Módulo de selección de iconos
│   ├── models/               # Lógica de servidor
│   ├── static/src/           # JS/XML/SCSS del POS
│   └── tests/                # Pruebas unitarias
├── pos_product_loader/       # Módulo de carga masiva
│   ├── data/                 # Cron y datos base
│   └── wizard/               # Asistentes de importación
└── AGENTS.md                 # Esta guía
```
