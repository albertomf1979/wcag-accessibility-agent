# Criterios de éxito WCAG 2.1 — Índice completo

Fuente oficial: https://www.w3.org/TR/WCAG21/
Quick Reference: https://www.w3.org/WAI/WCAG21/quickref/

Total WCAG 2.1: 78 criterios de éxito — 30 de nivel A, 20 de nivel AA y 28 de nivel AAA.
Los criterios marcados con [2.1] son nuevos en WCAG 2.1 (17 en total; no existían en 2.0).
Los 9 criterios añadidos en WCAG 2.2 se listan aparte, al final, y **no** forman parte de una auditoría WCAG 2.1.

---

## Principio 1: Perceivable

### Guía 1.1 — Text Alternatives
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 1.1.1 Non-text Content | A | Todo contenido no textual tiene alternativa textual |

### Guía 1.2 — Time-based Media
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 1.2.1 Audio-only and Video-only (Prerecorded) | A | Alternativa para audio/video solo pregrabados |
| 1.2.2 Captions (Prerecorded) | A | Subtítulos para audio sincronizado pregrabado |
| 1.2.3 Audio Description or Media Alternative (Prerecorded) | A | Audiodescripción o alternativa para video pregrabado |
| 1.2.4 Captions (Live) | AA | Subtítulos para audio sincronizado en directo |
| 1.2.5 Audio Description (Prerecorded) | AA | Audiodescripción para video pregrabado |
| 1.2.6 Sign Language (Prerecorded) | AAA | Lengua de signos para audio sincronizado pregrabado |
| 1.2.7 Extended Audio Description (Prerecorded) | AAA | Audiodescripción extendida para video pregrabado |
| 1.2.8 Media Alternative (Prerecorded) | AAA | Alternativa en texto para video pregrabado |
| 1.2.9 Audio-only (Live) | AAA | Alternativa en texto para audio solo en directo |

### Guía 1.3 — Adaptable
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 1.3.1 Info and Relationships | A | La estructura e información se puede determinar programáticamente |
| 1.3.2 Meaningful Sequence | A | El orden de lectura correcto es determinable programáticamente |
| 1.3.3 Sensory Characteristics | A | Las instrucciones no dependen solo de características sensoriales |
| 1.3.4 Orientation [2.1] | AA | El contenido no restringe la orientación de pantalla |
| 1.3.5 Identify Input Purpose [2.1] | AA | El propósito de los inputs de datos personales es determinable |
| 1.3.6 Identify Purpose [2.1] | AAA | El propósito de componentes UI, iconos y regiones es determinable |

### Guía 1.4 — Distinguishable
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 1.4.1 Use of Color | A | El color no es el único medio para transmitir información |
| 1.4.2 Audio Control | A | Audio que comienza automáticamente puede pausarse/silenciarse |
| 1.4.3 Contrast (Minimum) | AA | Ratio de contraste mínimo 4.5:1 (texto normal) / 3:1 (texto grande) |
| 1.4.4 Resize Text | AA | El texto puede ampliarse hasta 200% sin pérdida de funcionalidad |
| 1.4.5 Images of Text | AA | No usar imágenes de texto si el texto real es posible |
| 1.4.6 Contrast (Enhanced) | AAA | Ratio de contraste 7:1 (texto normal) / 4.5:1 (texto grande) |
| 1.4.7 Low or No Background Audio | AAA | Audio de fondo silenciable o con bajo nivel |
| 1.4.8 Visual Presentation | AAA | Texto presentable con colores, ancho, alineación y espaciado ajustables |
| 1.4.9 Images of Text (No Exception) | AAA | Solo usar imágenes de texto cuando es esencial |
| 1.4.10 Reflow [2.1] | AA | Contenido sin scroll bidireccional a 320px ancho / 256px alto |
| 1.4.11 Non-text Contrast [2.1] | AA | Ratio 3:1 para componentes UI y gráficos informativos |
| 1.4.12 Text Spacing [2.1] | AA | Sin pérdida de contenido al ajustar espaciado de texto |
| 1.4.13 Content on Hover or Focus [2.1] | AA | Contenido emergente en hover/focus es descartable, hoverable y persistente |

---

## Principio 2: Operable

### Guía 2.1 — Keyboard Accessible
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 2.1.1 Keyboard | A | Toda funcionalidad operable por teclado |
| 2.1.2 No Keyboard Trap | A | El foco de teclado no queda atrapado |
| 2.1.3 Keyboard (No Exception) | AAA | Toda funcionalidad operable por teclado sin excepciones |
| 2.1.4 Character Key Shortcuts [2.1] | A | Los atajos de tecla única son desactivables o remapeables |

### Guía 2.2 — Enough Time
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 2.2.1 Timing Adjustable | A | Los límites de tiempo son ajustables, desactivables o extensibles |
| 2.2.2 Pause, Stop, Hide | A | El contenido en movimiento puede pausarse, detenerse u ocultarse |
| 2.2.3 No Timing | AAA | Sin límites de tiempo para la actividad del usuario |
| 2.2.4 Interruptions | AAA | Las interrupciones pueden posponerse o suprimirse |
| 2.2.5 Re-authenticating | AAA | Los datos del usuario se preservan tras re-autenticación |
| 2.2.6 Timeouts [2.1] | AAA | Se avisa de los timeouts que pueden causar pérdida de datos |

### Guía 2.3 — Seizures and Physical Reactions
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 2.3.1 Three Flashes or Below Threshold | A | Sin contenido que destelle más de 3 veces/segundo |
| 2.3.2 Three Flashes | AAA | Sin contenido que destelle más de 3 veces/segundo (sin excepciones) |
| 2.3.3 Animation from Interactions [2.1] | AAA | Las animaciones de interacción pueden desactivarse |

### Guía 2.4 — Navigable
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 2.4.1 Bypass Blocks | A | Mecanismo para saltar bloques de contenido repetitivo |
| 2.4.2 Page Titled | A | Las páginas tienen títulos descriptivos |
| 2.4.3 Focus Order | A | El orden de foco preserva el significado y la operabilidad |
| 2.4.4 Link Purpose (In Context) | A | El propósito del enlace es determinable en contexto |
| 2.4.5 Multiple Ways | AA | Múltiples formas de llegar al mismo contenido |
| 2.4.6 Headings and Labels | AA | Los encabezados y labels son descriptivos |
| 2.4.7 Focus Visible | AA | El indicador de foco de teclado es visible |
| 2.4.8 Location | AAA | El usuario sabe dónde se encuentra dentro del sitio |
| 2.4.9 Link Purpose (Link Only) | AAA | El propósito del enlace es determinable sin contexto |
| 2.4.10 Section Headings | AAA | Los encabezados organizan el contenido |

### Guía 2.5 — Input Modalities
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 2.5.1 Pointer Gestures [2.1] | A | Los gestos de varios puntos/trayectoria tienen alternativa de un punto |
| 2.5.2 Pointer Cancellation [2.1] | A | La activación en down-event puede cancelarse o revertirse |
| 2.5.3 Label in Name [2.1] | A | El nombre accesible contiene el texto visible |
| 2.5.4 Motion Actuation [2.1] | A | Las funciones activadas por movimiento tienen alternativa de interfaz |
| 2.5.5 Target Size [2.1] | AAA | Área táctil mínima 44×44 CSS px |
| 2.5.6 Concurrent Input Mechanisms [2.1] | AAA | No se restringe el uso de mecanismos de entrada |

---

## Principio 3: Understandable

### Guía 3.1 — Readable
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 3.1.1 Language of Page | A | El idioma de la página está declarado en el código |
| 3.1.2 Language of Parts | AA | El idioma de fragmentos de texto está declarado |
| 3.1.3 Unusual Words | AAA | Se proporciona definición de palabras inusuales o jerga |
| 3.1.4 Abbreviations | AAA | Se proporciona expansión de abreviaturas |
| 3.1.5 Reading Level | AAA | Se proporciona versión simplificada para texto de nivel educativo superior |
| 3.1.6 Pronunciation | AAA | Se proporciona pronunciación cuando es necesaria para el significado |

### Guía 3.2 — Predictable
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 3.2.1 On Focus | A | El foco no produce cambios de contexto |
| 3.2.2 On Input | A | La entrada de datos no produce cambios de contexto automáticos |
| 3.2.3 Consistent Navigation | AA | La navegación es consistente en todo el sitio |
| 3.2.4 Consistent Identification | AA | Los componentes con la misma función se identifican consistentemente |
| 3.2.5 Change on Request | AAA | Los cambios de contexto solo se producen a petición del usuario |

### Guía 3.3 — Input Assistance
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 3.3.1 Error Identification | A | Los errores de entrada se identifican y describen en texto |
| 3.3.2 Labels or Instructions | A | Se proporcionan etiquetas o instrucciones para la entrada de datos |
| 3.3.3 Error Suggestion | AA | Se sugiere cómo corregir los errores cuando se sabe cómo |
| 3.3.4 Error Prevention (Legal, Financial, Data) | AA | En datos críticos: reversible, verificable o confirmable |
| 3.3.5 Help | AAA | Se proporciona ayuda contextual |
| 3.3.6 Error Prevention (All) | AAA | Todas las entradas son reversibles, verificables o confirmables |

---

## Principio 4: Robust

### Guía 4.1 — Compatible
| Criterio | Nivel | Descripción breve |
|---|---|---|
| 4.1.1 Parsing | A | Marcado sin código válido/bien formado. Una errata de WCAG 2.1 indica que para HTML/XML se considera siempre satisfecho; eliminado (obsoleto) en WCAG 2.2 |
| 4.1.2 Name, Role, Value | A | Los componentes UI tienen nombre, rol y valor determinables programáticamente |
| 4.1.3 Status Messages [2.1] | AA | Los mensajes de estado son determinables programáticamente sin recibir foco |

---

## Criterios añadidos en WCAG 2.2 (fuera del alcance WCAG 2.1)

Fuente oficial: https://www.w3.org/TR/WCAG22/ — evaluar solo si se pide WCAG 2.2 expresamente.

| Criterio | Nivel | Descripción breve |
|---|---|---|
| 2.4.11 Focus Not Obscured (Minimum) [2.2] | AA | El componente con foco no queda completamente oculto |
| 2.4.12 Focus Not Obscured (Enhanced) [2.2] | AAA | El componente con foco está completamente visible |
| 2.4.13 Focus Appearance [2.2] | AAA | El indicador de foco cumple requisitos de área y contraste |
| 2.5.7 Dragging Movements [2.2] | AA | Las operaciones de arrastre tienen alternativa de un solo punto |
| 2.5.8 Target Size (Minimum) [2.2] | AA | Área táctil mínima 24×24 CSS px |
| 3.2.6 Consistent Help [2.2] | A | Los mecanismos de ayuda aparecen en el mismo lugar relativo |
| 3.3.7 Redundant Entry [2.2] | A | No se pide información ya proporcionada en el mismo proceso |
| 3.3.8 Accessible Authentication (Minimum) [2.2] | AA | La autenticación no requiere prueba cognitiva sin alternativa |
| 3.3.9 Accessible Authentication (Enhanced) [2.2] | AAA | La autenticación no requiere prueba cognitiva |

En WCAG 2.2, 2.5.5 pasa a llamarse "Target Size (Enhanced)" y 4.1.1 Parsing queda obsoleto: WCAG 2.2 tiene 86 criterios.

---

## Notas sobre versiones

- Los criterios marcados **[2.1]** son nuevos en WCAG 2.1 (añadidos a los 61 de WCAG 2.0).
- Los criterios marcados **[2.2]** son nuevos en WCAG 2.2, no forman parte de WCAG 2.1 y se listan en su propia sección.
- **4.1.1 Parsing** está obsoleto en WCAG 2.2; WCAG 2.1 lo mantiene con una nota de errata.
- WCAG 2.2 es backwards-compatible: cumplir 2.2 implica cumplir 2.1 y 2.0.
- La referencia legal en España y Europa (EN 301 549) actualmente usa **WCAG 2.1 AA**.
