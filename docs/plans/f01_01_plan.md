# Plan de Implementación — Definiciones y Cimientos: Gobernanza y Estructura Base (`f01_01`)

> **Trazabilidad:** Este plan ejecuta los requerimientos de `docs/reqs/f01_01_prd.md` según el diseño de `docs/specs/f01_01_spec.md`.
> **Etapa:** 1.1 — Reglas globales, estructura de archivos e inicialización del `PROJECT_index.md`
> **Estado:** 🟡 En Progreso
> **Última actualización:** 2026-03-20

---

## 1. Resumen del Plan

El objetivo es dejar el repositorio en un estado donde el agente IA pueda operar con autonomía controlada desde la primera instrucción de cualquier sesión futura. La estrategia es **top-down**: primero la base de Git, luego los documentos de gobernanza, luego los mecanismos de automatización, y finalmente el entorno de ejecución Python.

Varios ítems de esta etapa ya fueron completados durante la sesión fundacional del proyecto (2026-03-20). El plan registra su estado real para mantener trazabilidad completa.

---

## 2. Ruta Crítica

```
B1 (Git + .gitignore)
    │
    ├──► B2 (CLAUDE.md completo) ──────────────────────────────────┐
    │                                                               │
    ├──► B3 (Estructura docs/) ────────────────────────────────┐   │
    │                                                           │   │
    └──► B4 (Python env: venv + requirements.txt + .env)       │   │
                                                                │   │
                                                                ▼   ▼
                                                    B5 (Archivos de contexto)
                                                    PROJECT_index.md
                                                    PROJECT_handoff.md
                                                                │
                                                                ▼
                                                    B6 (Skills Claude Code)
                                                    /update-index
                                                    /session-close
                                                    /sdd-doc
                                                                │
                                                                ▼
                                                    B7 (Commit inicial + verificación)
                                                                │
                                                                ▼
                                                    B8 (Gobernanza extendida)
                                                    /close-stage, /change-control
                                                    docs/lessons/, docs/executives/
                                                    docs/changes/, lessons-learned.md
```

**Dependencias críticas:**
- B5 depende de B2 (los archivos de contexto referencian las fases definidas en CLAUDE.md)
- B6 depende de B2 y B5 (los skills leen CLAUDE.md y generan/actualizan los archivos de contexto)
- B7 depende de todos los bloques anteriores

---

## 3. Backlog de Trabajo (WBS)

| Bloque | Descripción | REQ / ARC relacionado | Entregable | Estado |
|---|---|---|---|---|
| **B1** | Inicializar repositorio Git con rama `main` y configurar `.gitignore` con todos los patrones de exclusión definidos en SPEC §2.6 | `[REQ-09]` | `.gitignore` en raíz del repo | ✅ Completo |
| **B2** | Redactar y completar `CLAUDE.md` con las 10 secciones de gobernanza definidas en SPEC §2.1 | `[REQ-01]` / `[ARC-01]` | `CLAUDE.md` con 10 secciones | ✅ Completo |
| **B3** | Crear la estructura de 4 carpetas SDD bajo `docs/`: `reqs/`, `specs/`, `plans/`, `tasks/` | `[REQ-07]` / `[ARC-05]` | 4 carpetas bajo `docs/` | 🟡 Parcial (`reqs/` y `specs/` creadas; `plans/` y `tasks/` pendientes) |
| **B4** | Crear `requirements.txt` con dependencias pinneadas (SPEC §3), inicializar `venv/` y crear `.env.example` con las claves definidas en SPEC §2.5 | `[REQ-08]` / `[DAT-01]` / `[ARC-06]` | `requirements.txt`, `venv/`, `.env.example` | ⬜ Pendiente |
| **B5** | Verificar que `PROJECT_index.md` cumpla la estructura de 5 secciones (SPEC §2.2) y crear `PROJECT_handoff.md` con la estructura de 5 secciones (SPEC §2.3) | `[REQ-02]`, `[REQ-03]` / `[ARC-02]`, `[ARC-03]` | `PROJECT_index.md` validado + `PROJECT_handoff.md` creado | 🟡 Parcial (`PROJECT_index.md` existe; `PROJECT_handoff.md` pendiente) |
| **B6** | Verificar que los 3 skills cumplan el contrato de frontmatter definido en SPEC §2.4 y probar su invocación | `[REQ-04]`, `[REQ-05]`, `[REQ-06]` / `[ARC-04a]`, `[ARC-04b]`, `[ARC-04c]` | 3 skills invocables sin error | 🟡 Parcial (skills creados; prueba de invocación pendiente) |
| **B7** | Hacer commit atómico con todos los archivos de gobernanza y verificar las métricas de éxito del PRD §6 | `[REQ-09]` / `[MET-01..05]` | Commit en `main` + checklist MET validado | ⬜ Pendiente |
| **B8** | Crear skills `/close-stage` y `/change-control`; crear carpetas `docs/lessons/`, `docs/executives/`, `docs/changes/`; inicializar `lessons-learned.md`; actualizar `/session-close` con Paso 4 | `[REQ-10]` al `[REQ-15]` / `[ARC-07..11]` | 2 nuevos skills + 3 nuevas carpetas + `lessons-learned.md` inicializado | ⬜ Pendiente |

---

## 4. Estrategia de Verificación

> Esta etapa no produce código Python ni componentes testables con `pytest`. Las verificaciones son manuales y de comportamiento del agente.

| Tipo | Qué se verifica | Cómo | Criterio de éxito |
|---|---|---|---|
| Estructural | `CLAUDE.md` tiene 10 secciones | Revisión manual del índice del documento | 10/10 secciones presentes (`[MET-01]`) |
| Estructural | Las 4 carpetas `docs/` existen | `ls docs/` en terminal | 4 carpetas listadas (`[MET-03]`) |
| Funcional | Skill `/update-index` opera correctamente | Invocar `/update-index` y verificar que `PROJECT_index.md` se actualiza | Sin errores, archivo actualizado (`[MET-02]`) |
| Funcional | Skill `/session-close` opera correctamente | Invocar `/session-close` y verificar que `PROJECT_handoff.md` se crea/actualiza | Sin errores, archivo con las 5 secciones (`[MET-02]`) |
| Funcional | Skill `/sdd-doc` opera correctamente | Invocar `/sdd-doc` y verificar que pregunta modo y etapa antes de escribir | Sin errores, trazabilidad correcta (`[MET-02]`) |
| Ejecución | `pip install -r requirements.txt` sin errores | Ejecutar en terminal con `venv` activado en Python 3.12+ | Exit code 0 (`[MET-04]`) |
| Protocolo | Simulación del Protocolo de Inicio | Nueva sesión: leer CLAUDE.md → PROJECT_index → PROJECT_handoff → ejecutar Próxima Acción | Agente retoma contexto en ≤ 3 lecturas (`[MET-05]`) |

---

## 5. Definición de "Hecho" (DoD)

La Etapa 1.1 se considera **completada** cuando todos los siguientes criterios son verdaderos:

- [ ] `CLAUDE.md` tiene las 10 secciones y ha sido revisado manualmente (`[MET-01]`)
- [ ] `docs/reqs/`, `docs/specs/`, `docs/plans/`, `docs/tasks/` existen en el repositorio (`[MET-03]`)
- [ ] `PROJECT_index.md` sigue la estructura de 5 secciones definida en SPEC §2.2
- [ ] `PROJECT_handoff.md` existe con la estructura de 5 secciones definida en SPEC §2.3
- [ ] Los 3 skills (`/update-index`, `/session-close`, `/sdd-doc`) se invocan sin errores (`[MET-02]`)
- [ ] `requirements.txt` existe con versiones pinneadas y `pip install` pasa sin errores (`[MET-04]`)
- [ ] `.env.example` existe en la raíz con las claves definidas en SPEC §2.5
- [ ] `.gitignore` excluye `venv/`, `.env`, `*.pkl` y artefactos DVC (SPEC §2.6)
- [ ] Commit atómico en `main` con mensaje: `feat: etapa 1.1 — gobernanza y estructura base completada`
- [ ] Skills `/close-stage` y `/change-control` invocables sin error (`[MET-06]`)
- [ ] Carpetas `docs/lessons/`, `docs/executives/`, `docs/changes/` existen (`[MET-07]`)
- [ ] `docs/lessons/lessons-learned.md` inicializado con estructura correcta (`[REQ-13]`)
- [ ] `/session-close` actualizado con Paso 4 de lecciones aprendidas (`[REQ-10]`)
- [ ] `PROJECT_handoff.md` actualizado con `/session-close` al cerrar la sesión de implementación
