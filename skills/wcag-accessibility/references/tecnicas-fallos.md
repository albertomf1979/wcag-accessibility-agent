# Técnicas de fallo WCAG 2.1 — F-series (más frecuentes)

Fuente oficial: https://www.w3.org/WAI/WCAG21/Techniques/#failures

Usar estas referencias al documentar hallazgos en auditorías formales. Solo se listan las más frecuentes en productos digitales. Para la lista completa: https://www.w3.org/WAI/WCAG21/Techniques/failures/

---

## Fallos en Perceivable

| ID | Criterio | Descripción |
|---|---|---|
| F3 | 1.1.1 | Uso de CSS para incluir imágenes informativas con `background-image` |
| F13 | 1.1.1 | El texto alternativo no identifica correctamente la función de una imagen de control |
| F20 | 1.1.1 | El texto alternativo no incluye información que está en el texto presentado como imagen |
| F30 | 1.1.1 | Uso de texto alternativo de relleno ("imagen", "foto", "bullet") |
| F38 | 1.1.1 | `alt` que incluye la extensión del archivo |
| F39 | 1.1.1 | `alt` no vacío en imágenes decorativas |
| F65 | 1.1.1 | Omisión del atributo `alt` en imágenes que no son decorativas |
| F67 | 1.1.1 | `alt=""` en imágenes que transmiten contenido |
| F2 | 1.3.1 | Uso de cambios en la presentación para transmitir información sin usar marcado semántico |
| F33 | 1.3.1 | Uso de espacios en blanco para crear columnas en texto plano |
| F34 | 1.3.1 | Uso de caracteres de espacio en blanco para formatear tablas en texto plano |
| F43 | 1.3.1 | Uso de marcado estructural de forma que no representa relaciones en el contenido |
| F46 | 1.3.1 | Uso de elementos `th`, `caption` o `summary` de forma incorrecta en tablas de layout |
| F48 | 1.3.1 | Uso de elementos `pre` para marcar estructura tabular |
| F87 | 1.3.1 | Uso de `:before` y `:after` para insertar contenido no decorativo |
| F1 | 1.3.2 | Cambio del significado visual del contenido a través de CSS |
| F73 | 1.3.3 | Instrucciones que dependen solo de la forma o ubicación visual |
| F8 | 1.4.1 | El color es el único medio de distinguir los enlaces del texto circundante |
| F13 | 1.4.1 | Identificación de elementos solo por color (errores de formulario, campos obligatorios) |
| F24 | 1.4.3 | Especificación de colores de primer plano sin especificar colores de fondo, o viceversa |
| F83 | 1.4.3 | Uso de imágenes de fondo que no proporcionan contraste suficiente |
| F94 | 1.4.4 | Uso de unidades absolutas (px) en medios de pantalla cuando hay ajuste de texto |

---

## Fallos en Operable

| ID | Criterio | Descripción |
|---|---|---|
| F54 | 2.1.1 | Uso de manejadores de eventos solo de dispositivo apuntador (sin teclado) |
| F55 | 2.1.1 | Uso de scripts para eliminar el foco cuando el foco es recibido |
| F42 | 2.1.1 | Uso de redirect o meta refresh para simular frames (impide teclado) |
| F10 | 2.1.2 | Combinación de atributos `multiple` en `<select>` que crea trampa de teclado |
| F79 | 2.4.7 | El indicador de foco no es visible por CSS que elimina el outline en `:focus` |
| F85 | 2.4.7 | Uso de `display:none` o `visibility:hidden` en el elemento con foco |

---

## Fallos en Understandable

| ID | Criterio | Descripción |
|---|---|---|
| F32 | 3.1.1 | Uso del atributo `lang` con código de idioma equivocado |
| F25 | 3.2.1 | Apertura de una nueva ventana o pestaña al recibir foco |
| F52 | 3.2.1 | Apertura de una nueva ventana al cargar la página |
| F36 | 3.2.2 | Envío automático de formulario al seleccionar una opción |
| F37 | 3.2.2 | Lanzamiento de nueva ventana sin previo aviso al seleccionar opción |
| F68 | 3.3.2 | El atributo `for` del label no coincide con el `id` del control |
| F82 | 3.3.2 | El placeholder es el único indicador del propósito del campo |
| F84 | 3.3.2 | El control `required` no está etiquetado de forma visible |

---

## Fallos en Robust

| ID | Criterio | Descripción |
|---|---|---|
| F59 | 4.1.2 | Uso de scripts para hacer elementos `div` o `span` no semánticos interactivos sin rol ARIA |
| F15 | 4.1.2 | Implementación incorrecta de un plugin o applet accesible |
| F68 | 4.1.2 | El nombre de un campo de usuario no está determinado programáticamente |
| F77 | 4.1.2 | Reuse de `id`s en el mismo documento |
| F89 | 4.1.2 | Elemento interactivo no tiene nombre accesible |
| F103 | 4.1.3 | Los mensajes de estado no se determinan programáticamente |

---

## Cómo referenciar fallos en informes

Formato estándar en un hallazgo de auditoría:

```
**Técnica de fallo**: F79 — Failure of Success Criterion 2.4.7 due to CSS that removes the focus 
indicator when users click into form fields.
**Referencia**: https://www.w3.org/WAI/WCAG21/Techniques/failures/F79
```
