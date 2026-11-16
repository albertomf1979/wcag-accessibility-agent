# UX Accesible — Guía de referencia

Fuente: https://www.w3.org/WAI/tips/designing/ | https://www.w3.org/WAI/design-develop/

---

## Principios de UX accesible

La accesibilidad en UX no es una capa adicional: es diseño de interacción que funciona para todos los usuarios, independientemente de sus capacidades sensoriales, motoras o cognitivas. El marco WCAG establece los criterios mínimos; el buen diseño de UX accesible va más allá.

---

## Patrones de navegación accesible

### Skip links (Bypass Blocks — 2.4.1 A)
El primer elemento interactivo debe ser un enlace "Saltar al contenido principal" visible al recibir foco.

```html
<a href="#main-content" class="skip-link">Saltar al contenido principal</a>
```

El skip link puede estar oculto visualmente hasta recibir foco (nunca con `display:none` ni `visibility:hidden` — usar posicionamiento fuera de pantalla).

### Jerarquía de encabezados (1.3.1 A)
- Un único `<h1>` por página, que describe el contenido principal.
- La jerarquía es secuencial: h1 → h2 → h3. Nunca saltar niveles.
- Los encabezados no son decorativos: describen la sección que encabezan.
- Fuente: https://www.w3.org/WAI/tutorials/page-structure/headings/

### Landmarks / Regiones (1.3.1 A)
Usar landmarks HTML5 semánticos para estructurar la página:
- `<header>` → banner
- `<nav>` → navigation (etiquetar si hay múltiples: `aria-label="Principal"`)
- `<main>` → main (solo uno por página)
- `<aside>` → complementary
- `<footer>` → contentinfo
- `<section>` / `<article>` → con `aria-label` o `aria-labelledby` cuando sea necesario

### Navegación consistente (3.2.3 AA)
Los componentes de navegación que se repiten en múltiples páginas deben aparecer en el mismo orden relativo en cada página. El usuario no debe reaprender la estructura.

---

## Formularios accesibles

Fuente: https://www.w3.org/WAI/tutorials/forms/

### Etiquetado de controles (3.3.2 A)
- Cada campo de formulario tiene una etiqueta visible y asociada programáticamente.
- Usar `<label for="id">` como método preferido.
- El placeholder NO es un sustituto del label: desaparece al escribir y no tiene contraste suficiente.

### Instrucciones y contexto (3.3.2 A)
- Las instrucciones de formato (ej: "DD/MM/AAAA") van antes del campo, no solo en el placeholder.
- Los campos obligatorios se indican visualmente Y con `required` en el HTML.
- No depender exclusivamente del asterisco (*) sin explicación textual.

### Gestión de errores (3.3.1 A + 3.3.3 AA)
- Los errores se identifican en texto, no solo con color.
- El mensaje de error describe QUÉ salió mal Y CÓMO corregirlo.
- Los errores se asocian al campo: `aria-describedby="error-id"`.
- En formularios largos: resumen de errores al inicio del formulario con foco gestionado.

### Prevención de errores en datos críticos (3.3.4 AA)
En transacciones legales, financieras o con datos personales:
- El usuario puede revisar, corregir y confirmar antes de enviar.
- O la acción es reversible.
- O hay confirmación explícita.

### Agrupación de controles (1.3.1 A)
- Usar `<fieldset>` + `<legend>` para grupos relacionados (radios, checkboxes).
- La legend describe el grupo, no cada opción individual.

---

## Patrones de interacción

### Foco y contexto (3.2.1 A + 3.2.2 A)
- Recibir foco NO produce cambios de contexto (no abre modales, no envía formularios, no cambia de página).
- Cambiar el valor de un campo NO produce cambios de contexto sin previo aviso.
- Los cambios de contexto son siempre iniciados por el usuario.

### Modales y diálogos (2.1.1 A + 4.1.2 A)
- Al abrir un modal, el foco se mueve al interior del modal.
- El foco queda atrapado dentro del modal mientras está abierto (focus trap).
- Al cerrar el modal, el foco vuelve al elemento que lo abrió.
- El modal tiene `role="dialog"`, `aria-modal="true"`, `aria-labelledby`.
- Cerrar con Escape.
- Fuente de patrón: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/

### SPAs y navegación dinámica (2.4.3 A + 4.1.3 AA)
- Al cambiar de ruta, gestionar el foco (moverlo al `<h1>` de la nueva página o a un elemento anunciador).
- Los mensajes de estado (carga, éxito, error) se anuncian mediante live regions sin mover el foco.
- `aria-live="polite"` para mensajes no urgentes; `aria-live="assertive"` solo para errores críticos.

### Tiempo suficiente (2.2.1 A)
- Si hay límites de tiempo, el usuario puede desactivarlos, ajustarlos o extenderlos.
- Excepciones: tiempo real (subasta), tiempo esencial para la actividad, más de 20 horas.

### Carruseles y contenido en movimiento (2.2.2 A)
- El usuario puede pausar, detener u ocultar cualquier contenido que se mueva automáticamente más de 5 segundos.
- Los carruseles automáticos tienen control de pausa visible.
- Fuente: https://www.w3.org/WAI/tutorials/carousels/

---

## Arquitectura de información accesible

### Títulos de página (2.4.2 A)
- Cada página tiene un `<title>` único y descriptivo.
- Formato recomendado: "Nombre de página — Nombre del sitio".
- En SPAs: actualizar el title dinámicamente en cada cambio de ruta.

### Propósito de los enlaces (2.4.4 A)
- El texto del enlace describe su destino o función en contexto.
- Evitar "Haz clic aquí", "Más información", "Ver" sin contexto adicional.
- Si el texto visible es insuficiente: añadir `aria-label` o `aria-describedby`.

### Múltiples vías de acceso (2.4.5 AA)
- El usuario puede encontrar el mismo contenido por más de un camino: buscador, mapa del sitio, navegación principal, breadcrumbs.

---

## Perfiles de usuario a considerar

| Perfil | Herramienta / Necesidad | Criterios WCAG más relevantes |
|---|---|---|
| Ceguera | Lector de pantalla (NVDA, JAWS, VoiceOver) | 1.1.1, 1.3.1, 2.1.1, 2.4.x, 4.1.2 |
| Baja visión | Ampliador, zoom, contraste alto | 1.4.3, 1.4.4, 1.4.10, 1.4.12 |
| Daltonismo | Sin dependencia del color | 1.4.1, 1.4.3 |
| Motor / Manos | Solo teclado, switches, eye tracking | 2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.5.x |
| Cognitivo | Lenguaje simple, estructura clara, sin distracciones | 2.4.2, 3.1.x, 3.2.x, 3.3.x |
| Auditivo | Subtítulos, transcripciones | 1.2.x |
| Fotosensibilidad | Sin flashes | 2.3.x |
| Edad avanzada | Combinación de varios | Múltiples |

Fuente de historias de usuario reales: https://www.w3.org/WAI/people-use-web/user-stories/
