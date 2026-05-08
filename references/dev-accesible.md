# Desarrollo Técnico Accesible — Guía de referencia

Fuente: https://www.w3.org/WAI/tips/developing/ | https://www.w3.org/WAI/ARIA/apg/

---

## HTML semántico — base de todo

La accesibilidad técnica empieza por el HTML correcto. Antes de ARIA, usar el elemento HTML nativo adecuado. La primera regla de ARIA es: **no usar ARIA si el HTML nativo lo resuelve**.

### Elementos y roles nativos

| Necesidad | HTML nativo (preferido) | ARIA equivalente |
|---|---|---|
| Botón | `<button>` | `role="button"` en `<div>` |
| Enlace | `<a href>` | `role="link"` |
| Checkbox | `<input type="checkbox">` | `role="checkbox"` |
| Encabezado | `<h1>–<h6>` | `role="heading" aria-level="1"` |
| Lista | `<ul>/<ol>/<li>` | `role="list"` |
| Tabla | `<table><th><td>` | Complejo con ARIA |
| Formulario | `<form>` | `role="form"` |

### Estructura de página mínima accesible

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Nombre de página — Nombre del sitio</title>
</head>
<body>
  <a href="#main" class="skip-link">Saltar al contenido principal</a>

  <header>
    <nav aria-label="Principal">...</nav>
  </header>

  <main id="main">
    <h1>Título principal de la página</h1>
    ...
  </main>

  <aside aria-label="Información relacionada">...</aside>

  <footer>...</footer>
</body>
</html>
```

### Idioma (3.1.1 A + 3.1.2 AA)
```html
<!-- Idioma de la página -->
<html lang="es">

<!-- Fragmento en otro idioma -->
<p>El término inglés <span lang="en">accessibility</span> se traduce como accesibilidad.</p>
```

---

## Imágenes (1.1.1 A)

Fuente: https://www.w3.org/WAI/tutorials/images/

```html
<!-- Imagen informativa — describe el contenido -->
<img src="grafico-ventas.png" alt="Gráfico de barras: ventas Q1 2024, 45.000€; Q2 2024, 67.000€">

<!-- Imagen decorativa — alt vacío, no se anuncia -->
<img src="separador.png" alt="">

<!-- Imagen funcional (botón/enlace) — describe la función -->
<button>
  <img src="buscar.svg" alt="Buscar">
</button>

<!-- Imagen compleja — alt breve + descripción larga -->
<figure>
  <img src="mapa-complejo.png" alt="Mapa de distribución regional"
       aria-describedby="mapa-descripcion">
  <figcaption id="mapa-descripcion">
    El mapa muestra... [descripción detallada]
  </figcaption>
</figure>

<!-- SVG decorativo -->
<svg aria-hidden="true" focusable="false">...</svg>

<!-- SVG informativo -->
<svg role="img" aria-label="Icono de advertencia">
  <title>Advertencia</title>
  ...
</svg>
```

---

## Formularios (3.3.x + 1.3.1)

Fuente: https://www.w3.org/WAI/tutorials/forms/

```html
<!-- Label explícita — método preferido -->
<label for="email">Correo electrónico <span aria-hidden="true">*</span>
  <span class="sr-only">(obligatorio)</span>
</label>
<input id="email" type="email" name="email"
       required
       aria-describedby="email-hint email-error"
       autocomplete="email">
<p id="email-hint">Introduce tu dirección de correo profesional.</p>
<p id="email-error" role="alert" aria-live="assertive" hidden>
  Error: introduce un correo válido (ejemplo@dominio.com)
</p>

<!-- Grupo de opciones -->
<fieldset>
  <legend>Método de pago preferido</legend>
  <label><input type="radio" name="pago" value="tarjeta"> Tarjeta de crédito</label>
  <label><input type="radio" name="pago" value="paypal"> PayPal</label>
</fieldset>

<!-- autocomplete para datos personales (1.3.5 AA) -->
<input type="text" autocomplete="given-name">
<input type="text" autocomplete="family-name">
<input type="email" autocomplete="email">
<input type="tel" autocomplete="tel">
```

Valores de autocomplete: https://www.w3.org/TR/WCAG21/#input-purposes

---

## WAI-ARIA — cuándo y cómo usarlo

Fuente: https://www.w3.org/WAI/ARIA/apg/

### Las cinco reglas de ARIA (de más importante a menos)

1. **No uses ARIA si el HTML nativo lo hace** — `<button>` antes que `role="button"`.
2. **No cambies la semántica nativa** — no pongas `role="heading"` en un `<button>`.
3. **Todos los controles ARIA interactivos deben ser operables por teclado**.
4. **No ocultes elementos focusables** — no uses `aria-hidden="true"` en un elemento con foco.
5. **Todos los elementos interactivos deben tener un nombre accesible**.

### Nombre accesible — formas de proporcionarlo

```html
<!-- 1. Contenido textual (botones, enlaces) -->
<button>Enviar formulario</button>

<!-- 2. aria-label — sobreescribe el texto visible -->
<button aria-label="Cerrar diálogo de confirmación">✕</button>

<!-- 3. aria-labelledby — referencia a otro elemento -->
<h2 id="titulo-seccion">Configuración de privacidad</h2>
<section aria-labelledby="titulo-seccion">...</section>

<!-- 4. alt en imágenes -->
<img src="logo.png" alt="Empresa XYZ">

<!-- 5. label asociado -->
<label for="busqueda">Buscar en el sitio</label>
<input id="busqueda" type="search">
```

### ARIA Live Regions (4.1.3 AA)

```html
<!-- Mensajes de estado no urgentes (carga completada, guardado...) -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  <!-- Insertar mensaje dinámicamente con JavaScript -->
</div>

<!-- Mensajes urgentes (errores críticos, alertas de sesión) -->
<div role="alert">
  <!-- El contenido insertado aquí se anuncia inmediatamente -->
</div>

<!-- Región de estado para datos en tiempo real -->
<div role="status" aria-live="polite">
  Mostrando 1-10 de 234 resultados
</div>
```

---

## Patrones ARIA comunes

### Modal / Diálogo
```html
<div role="dialog"
     aria-modal="true"
     aria-labelledby="modal-titulo"
     aria-describedby="modal-descripcion">
  <h2 id="modal-titulo">Confirmar eliminación</h2>
  <p id="modal-descripcion">Esta acción no se puede deshacer.</p>
  <button>Cancelar</button>
  <button>Eliminar</button>
</div>
```

JavaScript requerido:
- Al abrir: mover foco al primer elemento interactivo o al `<h2>`.
- Mantener focus trap dentro del modal (Tab/Shift+Tab circulares).
- Cerrar con Escape; devolver foco al elemento que abrió el modal.

Patrón oficial: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/

### Navegación con pestañas (Tabs)
```html
<div role="tablist" aria-label="Secciones del perfil">
  <button role="tab" aria-selected="true" aria-controls="panel-info" id="tab-info">
    Información
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-config" id="tab-config"
          tabindex="-1">
    Configuración
  </button>
</div>

<div role="tabpanel" id="panel-info" aria-labelledby="tab-info">
  ...
</div>
<div role="tabpanel" id="panel-config" aria-labelledby="tab-config" hidden>
  ...
</div>
```

Teclado: Tab activa el tablist; flechas izquierda/derecha navegan entre tabs; Enter/Space activa.

Patrón oficial: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/

### Menú desplegable (Disclosure / Dropdown)
```html
<button aria-expanded="false" aria-controls="menu-usuario">
  Mi cuenta
</button>
<ul id="menu-usuario" hidden>
  <li><a href="/perfil">Perfil</a></li>
  <li><a href="/configuracion">Configuración</a></li>
  <li><a href="/cerrar-sesion">Cerrar sesión</a></li>
</ul>
```

Al expandir: cambiar `aria-expanded` a `true`, quitar `hidden`, mover foco al primer ítem.
Cerrar con Escape; devolver foco al botón.

---

## Teclado — gestión del foco

### tabindex
- `tabindex="0"` — incluye el elemento en el orden natural de Tab.
- `tabindex="-1"` — excluye del Tab pero permite foco programático (`element.focus()`).
- `tabindex > 0` — **evitar**. Crea un orden de Tab diferente al DOM, genera confusión.

### Orden de foco (2.4.3 A)
El orden de Tab debe seguir el orden lógico del contenido. Si el DOM está desordenado respecto al visual (con CSS absolute/grid/flex), el orden de foco puede no coincidir con el visual — problema de accesibilidad.

### Gestión de foco en SPAs
```javascript
// Al cambiar de ruta en una SPA
router.afterEach(() => {
  nextTick(() => {
    // Opción 1: mover foco al h1 de la nueva página
    document.querySelector('h1')?.focus();

    // Opción 2: anunciar el cambio de página
    const announcer = document.getElementById('route-announcer');
    announcer.textContent = `Página cargada: ${document.title}`;
  });
});
```

---

## Accesibilidad en componentes JavaScript comunes

### Infinite scroll / Carga paginada
- Proporcionar siempre alternativa de paginación tradicional.
- Anunciar nuevos elementos cargados con live region.
- Gestionar el foco correctamente tras la carga.

### Autocompletado / Combobox
Patrón oficial: https://www.w3.org/WAI/ARIA/apg/patterns/combobox/

### Datepicker
- Debe ser operable completamente por teclado.
- El campo de texto permite introducir fecha manualmente.
- Patrón: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/datepicker-dialog/

---

## Testing técnico

### Herramientas automatizadas (detectan ~30-40% de problemas)
```bash
# axe-core (integrable en CI/CD)
npm install axe-core

# axe con Playwright
npm install @axe-core/playwright

# Pa11y (línea de comandos)
npm install -g pa11y
pa11y https://ejemplo.com
```

### Testing manual de teclado — protocolo mínimo
1. Desconectar el ratón.
2. Navegar con Tab — verificar que todos los elementos interactivos son alcanzables.
3. Verificar que el indicador de foco es visible en todo momento.
4. Verificar que no hay trampas de teclado (excepto en modales, donde es correcto).
5. Operar formularios, modales, menús y tabs solo con teclado.
6. Verificar que Escape cierra modales y menús.

### Testing con lector de pantalla — protocolo mínimo
- **NVDA + Firefox** (Windows, gratuito): https://www.nvaccess.org/
- **VoiceOver + Safari** (macOS/iOS): activar con Cmd+F5
- Navegar por encabezados (H), landmarks (D), formularios (F), tablas (T).
- Verificar que todos los controles tienen nombre accesible.
- Verificar que los mensajes de error se anuncian.
- Verificar que el contenido dinámico se anuncia correctamente.

---

## CSS accesible — patrones comunes

### Clase sr-only (contenido solo para lectores de pantalla)
```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Versión visible al recibir foco (skip links) */
.sr-only-focusable:focus {
  position: static;
  width: auto;
  height: auto;
  margin: 0;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

### Focus visible
```css
/* Nunca eliminar el outline sin reemplazarlo */
:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

/* Estilos de foco mejorados para dark mode */
@media (prefers-color-scheme: dark) {
  :focus-visible {
    outline-color: #7fb3f5;
  }
}
```

### Motion reducido
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
