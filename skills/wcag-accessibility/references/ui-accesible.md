# UI Accesible — Guía de referencia

Fuente: https://www.w3.org/WAI/tips/designing/ | https://www.w3.org/WAI/WCAG21/Understanding/

---

## Contraste de color

Fuente: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum

### Ratios requeridos

| Tipo de elemento | Nivel AA | Nivel AAA |
|---|---|---|
| Texto normal (< 18pt / < 14pt bold) | 4.5:1 | 7:1 |
| Texto grande (≥ 18pt / ≥ 14pt bold) | 3:1 | 4.5:1 |
| Componentes UI (borders, iconos funcionales) | 3:1 | — |
| Gráficos / infografías informativas | 3:1 | — |
| Texto en imágenes | 4.5:1 | 7:1 |
| Logotipos y texto decorativo | Exento | Exento |
| Texto inactivo/deshabilitado | Exento | Exento |

### Texto grande — definición WCAG
- 18pt (24px) o mayor en peso normal.
- 14pt (aproximadamente 18.67px) o mayor en negrita (bold).

### Herramientas de verificación
- Colour Contrast Analyser: https://www.tpgi.com/color-contrast-checker/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Figma: plugins "Contrast" o "A11y - Color Contrast Checker"

### Errores comunes de contraste
- Texto gris claro sobre fondo blanco (muy frecuente en texto secundario / placeholders).
- Iconos en gris medio sin texto alternativo.
- Estados hover/focus con color que pierde contraste.
- Texto sobre imágenes o gradientes sin overlay de contraste garantizado.
- Bordes de inputs insuficientes respecto al fondo de la página.

---

## Color como único medio de información (1.4.1 A)

El color NUNCA es el único medio para transmitir información. Siempre añadir un segundo canal:

| Situación | Solo color ❌ | Correcto ✅ |
|---|---|---|
| Campos obligatorios | Borde rojo | Borde rojo + icono + texto "Obligatorio" |
| Error en formulario | Campo rojo | Campo rojo + icono error + mensaje de texto |
| Enlace en párrafo | Texto azul | Texto azul + subrayado |
| Gráfico de datos | Líneas de colores | Colores + patrones/texturas + leyenda |
| Estado de semáforo | Verde/Rojo | Color + icono + etiqueta textual |

---

## Tipografía accesible

### Tamaño y escalado (1.4.4 AA)
- El texto del cuerpo no debe ser menor de 16px en diseño base.
- El contenido debe ser funcional al 200% de zoom sin pérdida de funcionalidad o contenido.
- Evitar tamaños fijos en px para el texto cuando sea posible; preferir rem/em.

### Espaciado (1.4.12 AA)
El contenido no debe perder funcionalidad si el usuario ajusta:
- Alto de línea (line-height) a 1.5× el tamaño de fuente.
- Espaciado entre párrafos a 2× el tamaño de fuente.
- Espaciado entre letras (letter-spacing) a 0.12× el tamaño de fuente.
- Espaciado entre palabras (word-spacing) a 0.16× el tamaño de fuente.

No usar `overflow: hidden` en contenedores de texto de altura fija sin alternativa.

### Legibilidad
- Evitar texto justificado (crea "ríos" de espacios que dificultan la lectura dislexia).
- Longitud de línea recomendada: 45-75 caracteres.
- Evitar texto en mayúsculas para bloques (dificulta la lectura; los lectores de pantalla pueden anunciarlo letra a letra).
- Contraste mínimo para texto sobre imágenes: garantizar con overlay semitransparente.

---

## Imágenes de texto (1.4.5 AA)

No usar imágenes de texto cuando se puede lograr el mismo efecto visual con CSS.

Excepciones aceptadas:
- Logotipos (texto que forma parte de la identidad visual).
- Casos donde la presentación específica es esencial (caligrafía personalizada).

---

## Diseño responsivo y reflow (1.4.10 AA)

El contenido debe presentarse sin scroll horizontal cuando el viewport es de 320px de ancho CSS (equivalente a zoom 400% en 1280px).

Excepciones: contenido que requiere dos dimensiones por naturaleza (mapas, tablas de datos complejos, editores de código, presentaciones).

**Diseño para pantallas pequeñas**:
- Una columna en móvil.
- Los menús colapsados tienen alternativa accesible.
- Las tablas de datos tienen scroll horizontal contenido con indicador visual.

---

## Componentes UI — especificaciones de accesibilidad

### Botones
- Área táctil: 44×44 CSS px para AAA en WCAG 2.1 (2.5.5). WCAG 2.2 añade un mínimo de 24×24 CSS px en AA (2.5.8 [WCAG 2.2]); no es exigible en una auditoría WCAG 2.1, pero es una buena práctica.
- Texto del botón descriptivo de la acción.
- Estado deshabilitado: `disabled` en HTML (no solo estilos CSS).
- Estado hover y focus con contraste suficiente.
- Diferenciación visual clara entre botón primario, secundario y destructivo.

### Inputs / Campos de formulario
- Border del input: ratio 3:1 respecto al fondo de la página.
- Estado de foco: outline visible, ratio 3:1 mínimo.
- Placeholder: NO sustituye al label. Contraste mínimo 4.5:1 recomendado (aunque es texto "inactive", la excepción es discutible).
- Mensajes de error: en rojo + icono + texto (nunca solo color).

### Iconos
- Iconos puramente decorativos: `aria-hidden="true"`.
- Iconos funcionales (botones solo-icono): `aria-label` en el botón padre o texto visualmente oculto con `.sr-only`.
- Contraste del icono respecto al fondo: 3:1 mínimo (criterio 1.4.11 AA).

### Focus visible (2.4.7 AA; 2.4.13 AAA [WCAG 2.2])
El indicador de foco debe ser:
- Visible (AA): existe un cambio visual al recibir foco.
- Para AAA en WCAG 2.2 (2.4.13 Focus Appearance, no existe en WCAG 2.1): el área de foco ≥ perímetro del componente × 2px CSS, con ratio de contraste ≥ 3:1 entre el estado enfocado y desenfocado.

**Implementación recomendada**:
```css
/* Nunca hacer esto: */
:focus { outline: none; }

/* Correcto — outline consistente y visible: */
:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
  border-radius: 2px;
}
```

### Tooltips y contenido en hover/focus (1.4.13 AA)
El contenido que aparece al hacer hover o al recibir foco debe:
- Poder ser descartado sin mover el puntero o el foco (tecla Escape).
- Permanecer visible mientras el puntero está sobre él.
- Permanecer visible mientras tiene el foco.

---

## Motion y animaciones (2.3.3 AAA)

Respetar la preferencia del sistema operativo:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Animaciones problemáticas:
- Parpadeos > 3 veces/segundo (riesgo de crisis epilépticas — criterio 2.3.1 A).
- Parallax agresivo (puede causar mareo en usuarios con trastornos vestibulares).
- Transiciones de página que mueven grandes áreas de pantalla.

---

## Dark mode y temas de contraste alto

- Verificar ratios de contraste en TODAS las variantes de tema.
- El dark mode no garantiza accesibilidad automática — verificar siempre.
- Respetar `prefers-color-scheme` del sistema.
- Windows High Contrast Mode (forced-colors): evitar `background-image` para iconos funcionales; usar `border` en lugar de `outline` para elementos de foco si necesario.

---

## Sistemas de diseño accesibles

Al diseñar o auditar un design system:

1. **Tokens de color**: definir tokens semánticos (no solo de valor) que incluyan las parejas verificadas de contraste.
2. **Componentes**: cada componente debe tener especificada su variante de estado: default, hover, focus, active, disabled, error.
3. **Documentación**: incluir las especificaciones de accesibilidad como parte de la documentación del componente, no como anexo.
4. **Testing**: los componentes del design system deben pasar tests de accesibilidad antes de publicarse.

Referencia de componentes accesibles: https://www.w3.org/WAI/ARIA/apg/patterns/
