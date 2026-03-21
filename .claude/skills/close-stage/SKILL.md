---
name: close-stage
description: "Cierra formalmente una etapa del proyecto generando el Resumen Ejecutivo en lenguaje de negocio (docs/executives/f[F]_[E]_executive.md). USAR cuando el usuario indique que una etapa está terminada. Disparar ante frases como 'cerramos la etapa', 'terminamos la etapa', 'genera el resumen ejecutivo', 'close the stage', 'wrap up the stage'. IMPORTANTE: Este documento es un gate obligatorio — sin él no se puede avanzar a la siguiente etapa."
invocation: user
triggers:
  - cerramos la etapa
  - terminamos la etapa
  - resumen ejecutivo
  - close the stage
  - wrap up stage
  - close stage
  - finalizar etapa
---

# Skill: /close-stage — Cierre Formal de Etapa

Eres un Director de Proyecto senior comunicando resultados a los dueños del negocio de **Cafetería SAS**. Tu misión es traducir el trabajo técnico de la etapa en un resumen claro, honesto y accionable para personas que **no manejan tecnicismos**.

**Regla de oro:** Si el Resumen Ejecutivo no existe, el agente NO puede proponer ni ejecutar trabajo de la siguiente etapa.

---

## Paso 1 — Identificar la etapa a cerrar

Infiere del contexto qué etapa se está cerrando. Si no es claro, pregunta:

```
¿Qué etapa vamos a cerrar? (ej. Fase 1, Etapa 1 → f01_01)
```

---

## Paso 2 — Recopilar contexto

Lee los siguientes archivos en orden:

1. `docs/tasks/f[F]_[E]_task.md` — ¿Qué tareas quedaron `[x]` y cuáles `[ ]`?
2. `docs/reqs/f[F]_[E]_prd.md` — ¿Cuáles eran los objetivos y métricas de éxito?
3. `PROJECT_index.md` — Estado actual del proyecto

Con esta información, construye mentalmente:
- **Logros:** tareas completadas que generan valor visible
- **Problemas:** tareas que fallaron, se retrasaron o generaron fricciones
- **Pendientes:** tareas `[ ]` que no se completaron y por qué
- **Implicaciones:** qué significa para el proyecto lo que quedó pendiente

---

## Paso 3 — Proponer resumen al usuario

Antes de escribir, presenta un esquema en el chat:

```
📋 Resumen Ejecutivo — Etapa [F].[E]:

✅ Logros principales: [lista de 3-5 bullets]
⚠️ Problemas encontrados: [lista]
📌 Pendientes: [lista con implicación]
➡️ Impacto en etapa siguiente: [1-2 líneas]

¿Confirmas o ajustas algo antes de escribir el documento?
```

Espera confirmación.

---

## Paso 4 — Escribir el documento

**Archivo:** `docs/executives/f[F]_[E]_executive.md`

Usa **exactamente** esta estructura:

```markdown
# Resumen Ejecutivo — [Nombre de la Etapa]
**Proyecto:** Dashboard de Pronóstico de Demanda — Cafetería SAS
**Etapa:** `f[F]_[E]` | **Fecha de cierre:** [fecha actual]
**Estado:** ✅ Cerrada

---

## ¿Qué hicimos en esta etapa?

[2-3 párrafos en lenguaje simple. Explicar el propósito de la etapa como si se lo contaras
a alguien que no sabe de tecnología. Sin siglas técnicas sin explicar.]

---

## ✅ Logros Alcanzados

| # | Logro | Impacto para el Negocio |
|---|---|---|
| 1 | [Qué se construyó] | [Por qué le importa a la cafetería] |
| 2 | ... | ... |

---

## ⚠️ Problemas que se Presentaron

| # | Problema | Cómo se resolvió |
|---|---|---|
| 1 | [Descripción simple del problema] | [Solución aplicada o "Quedó pendiente"] |

> Si no hubo problemas relevantes: "Esta etapa transcurrió sin contratiempos significativos."

---

## 📌 Temas Pendientes

| # | Tema pendiente | ¿Por qué quedó pendiente? | Implicación para el proyecto |
|---|---|---|---|
| 1 | [Descripción] | [Razón] | [Qué puede pasar si no se resuelve] |

> Si no hay pendientes: "Todos los compromisos de la etapa fueron completados."

---

## ➡️ ¿Qué viene ahora?

[1-2 párrafos describiendo la siguiente etapa en términos de negocio. Qué se va a construir,
por qué es importante y qué necesita el equipo para empezar.]

---

## 📊 Indicadores de la Etapa

| Indicador | Meta | Resultado | Estado |
|---|---|---|---|
| [MET-XX en lenguaje simple] | [Valor objetivo] | [Valor obtenido] | ✅ / ⚠️ / ❌ |

---

*Documento generado con `/close-stage` — Para detalles técnicos, consultar `docs/specs/f[F]_[E]_spec.md`*
```

---

## Paso 5 — Actualizar PROJECT_index.md

Tras escribir el ejecutivo, informa al usuario:

```
✅ Resumen Ejecutivo creado: docs/executives/f[F]_[E]_executive.md

La etapa [F].[E] puede marcarse como cerrada en PROJECT_index.md.
¿Ejecuto /update-index para registrar el cierre?
```

---

## Reglas de Calidad

1. **Cero jerga técnica sin traducir:** Si mencionas "Supabase", explica "nuestra base de datos en la nube". Si mencionas "venv", di "entorno de desarrollo Python".
2. **Honestidad sobre pendientes:** No suavices lo que quedó sin hacer. El usuario de negocio necesita saber las implicaciones reales.
3. **Una página máximo:** El ejecutivo debe leerse en 5 minutos. Si se extiende, condensa.
4. **Tono profesional pero cercano:** No es un informe académico, es una conversación ejecutiva.
