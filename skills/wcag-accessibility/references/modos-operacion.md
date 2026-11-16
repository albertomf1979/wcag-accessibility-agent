# Modos de operación del agente — Instrucciones detalladas

---

## MODO ANÁLISIS

**Objetivo**: Identificar y priorizar barreras de accesibilidad en un artefacto dado.

**Input aceptado**:
- Código HTML/CSS/JavaScript
- Componentes React, Vue, Angular, Svelte
- URLs de páginas web (con herramienta de fetch)
- Capturas de pantalla
- Descripciones textuales de flujos o pantallas
- Archivos de diseño (descripción o exportación)

**Proceso**:
1. Identificar el tipo de artefacto y el nivel disciplinar activo (UX / UI / Dev).
2. Aplicar el checklist correspondiente al nivel disciplinar.
3. Clasificar hallazgos por severidad:
   - 🔴 **Crítico** — bloquea el uso para usuarios con discapacidad (ej: formulario sin labels, sin navegación por teclado, sin alt text en imagen funcional).
   - 🟠 **Mayor** — degradación significativa de la experiencia (ej: contraste insuficiente, foco no visible, error sin descripción textual).
   - 🟡 **Menor** — mejoras que elevan la calidad sin bloquear el acceso.
4. Mapear cada hallazgo al criterio WCAG 2.1 correspondiente.
5. Indicar el impacto por perfil de usuario afectado.

**Output**:
```
## Análisis de accesibilidad — [Nombre del artefacto]
**Nivel disciplinar**: [UX / UI / Desarrollo / Combinación]
**Nivel WCAG objetivo**: [A / AA / AAA]
**Fecha**: [fecha]

### Resumen
[2-3 frases con el estado general y los gaps más urgentes]

### Hallazgos críticos 🔴
[Lista de problemas que bloquean el acceso]

### Hallazgos mayores 🟠
[Lista de problemas que degradan significativamente la experiencia]

### Hallazgos menores 🟡
[Lista de mejoras de calidad]

### Usuarios más afectados
[Perfiles de usuario impactados por los hallazgos críticos]
```

---

## MODO AUDITORÍA

**Objetivo**: Producir un informe formal de conformidad WCAG referenciable y documentado.

**Metodología base**: WCAG-EM (Evaluation Methodology)
Fuente: https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/

**Proceso**:
1. **Definir el alcance** — ¿Qué páginas, flujos o componentes se auditan?
2. **Explorar el sitio/producto** — identificar tipos de páginas y componentes únicos.
3. **Seleccionar muestra representativa** — incluir páginas clave del flujo del usuario.
4. **Evaluar cada criterio WCAG aplicable** — estado: ✅ Pasa / ❌ Falla / ⚠️ Revisar manualmente / N/A.
5. **Documentar hallazgos** con la plantilla de hallazgo individual.
6. **Producir informe consolidado**.

**Plantilla de hallazgo individual**:
```
### [HAL-001] Criterio 1.4.3 — Contraste (Mínimo) · Nivel AA

**Estado**: ❌ Falla
**Elemento afectado**: Texto de placeholder en campos de búsqueda (`input[type="search"]`)
**Problema**: El color del placeholder (#9E9E9E sobre #FFFFFF) tiene un ratio de contraste de 2.85:1, por debajo del mínimo requerido de 4.5:1 para texto normal.
**Técnica de fallo**: F83 — Failure of Success Criterion 1.4.3 and 1.4.6 due to using background images that do not provide sufficient contrast with foreground text or images of text (adaptación).
**Impacto**: Usuarios con baja visión, usuarios en condiciones de iluminación adversa, usuarios en pantallas de baja calidad.
**Prioridad**: Alta
**Corrección sugerida**: Cambiar el color del placeholder a #767676 o más oscuro sobre fondo blanco (ratio 4.54:1). O usar un label visible en lugar de depender del placeholder.
**Referencia WCAG**: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
```

**Tabla de resultados de auditoría** (incluir siempre al inicio del informe):

| Criterio | Descripción | Nivel | Estado | Hallazgos |
|---|---|---|---|---|
| 1.1.1 | Non-text Content | A | ✅ Pasa | — |
| 1.3.1 | Info and Relationships | A | ❌ Falla | HAL-001 |
| 1.4.3 | Contrast (Minimum) | AA | ⚠️ Manual | HAL-002 |
| ... | ... | ... | ... | ... |

---

## MODO EVALUACIÓN

**Objetivo**: Calcular el nivel de conformidad actual y las brechas para alcanzar el objetivo.

**Output**:

```
## Evaluación de conformidad WCAG 2.1

### Score de conformidad
| Nivel | Criterios evaluados | Pasan | Fallan | Manual | Score |
|---|---|---|---|---|---|
| A (25 criterios) | 25 | 19 | 4 | 2 | 76% |
| AA (adicionales, 13) | 13 | 8 | 3 | 2 | 62% |
| AAA (adicionales, 28) | 28 | 5 | 12 | 11 | 18% |

### Madurez de accesibilidad
- **Inicial**: Sin accesibilidad formal. < 30% en nivel A.
- **Básico**: Cumple parcialmente nivel A. 30-70% en nivel A.
- **Intermedio**: Cumple nivel A. Progreso hacia AA.
- **Avanzado**: Cumple nivel AA. Algunos criterios AAA.
- **Excelente**: Cumple nivel AA completo. Avance significativo en AAA.

### Brechas críticas para alcanzar nivel AA
[Lista de los criterios AA que fallan, priorizados por impacto y esfuerzo]

### Roadmap de remediación sugerido
**Sprint 1** (semana 1-2): Problemas críticos que bloquean acceso
**Sprint 2** (semana 3-4): Problemas mayores de nivel A
**Sprint 3** (semana 5-6): Problemas de nivel AA
**Sprint 4**: Mejoras de nivel AAA
```

---

## MODO CORRECCIÓN

**Objetivo**: Proporcionar código o especificaciones corregidas, con explicación.

**Reglas**:
- Mostrar siempre el código/especificación actual (incorrecto) y la versión corregida.
- Explicar QUÉ cambió y POR QUÉ es la solución correcta.
- Referenciar el criterio WCAG que se satisface.
- Si hay varias formas correctas, mostrar la preferida y mencionar las alternativas.

**Formato de corrección**:

```
### Corrección: [descripción del problema]
**Criterio**: 4.1.2 Name, Role, Value — Nivel A

#### Código actual ❌
```html
<div class="btn-cerrar" onclick="cerrarModal()">✕</div>
```

#### Código corregido ✅
```html
<button type="button"
        class="btn-cerrar"
        aria-label="Cerrar diálogo de confirmación"
        onclick="cerrarModal()">
  <span aria-hidden="true">✕</span>
</button>
```

#### Qué cambió y por qué
1. `<div>` → `<button>`: el elemento nativo `<button>` aporta automáticamente `role="button"`, es focusable por teclado y responde a Enter y Space. Un `<div>` con `onclick` no tiene ninguna de estas propiedades.
2. `aria-label="Cerrar diálogo de confirmación"`: el icono ✕ no tiene nombre accesible para lectores de pantalla. El `aria-label` proporciona un nombre descriptivo.
3. `aria-hidden="true"` en el ✕: evita que el lector de pantalla anuncie el símbolo además del `aria-label`.

**Referencia**: https://www.w3.org/WAI/WCAG21/Understanding/name-role-value
```

---

## MODO HANDOFF

**Objetivo**: Generar documentación entregable para equipos de diseño, desarrollo o QA que aplicarán la accesibilidad de forma manual, sin necesidad del agente.

**Principios del handoff**:
- Lenguaje claro y sin jerga innecesaria para no especialistas.
- Criterios de aceptación objetivos y testeables.
- Separación por rol: qué hace UX, qué hace UI/Diseño, qué hace Desarrollo, qué verifica QA.
- Incluir los recursos y herramientas que el equipo necesita para implementar.

**Cuándo generar un handoff**:
- El equipo necesita trabajar de forma autónoma sin el agente.
- Se necesita documentación formal para un proyecto o sprint.
- Hay múltiples personas con roles diferentes implementando la accesibilidad.
- Se necesita dejar trazabilidad de las decisiones de accesibilidad.

**Estructura completa del handoff** → ver sección correspondiente en `SKILL.md`.

**Tips para hacer el handoff efectivo**:
1. Incluir capturas o referencias visuales de cada hallazgo cuando sea posible.
2. Ordenar los hallazgos por prioridad, no por criterio WCAG (facilita el sprint planning).
3. Los criterios de aceptación deben ser binarios: pasa / no pasa.
4. Incluir ejemplos de código correcto, no solo descripciones.
5. Señalar qué herramientas usar para verificar cada corrección.
