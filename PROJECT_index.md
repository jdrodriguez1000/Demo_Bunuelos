# 🗺️ PROJECT_index — Dashboard Demanda Buñuelos

> **MANDATO IA:** Lee este archivo en el Paso 2 del Protocolo de Inicio de Sesión. Úsalo para ubicar los documentos SDD activos y entender el estado macro del proyecto. Actualiza el checklist de hitos SOLO cuando el usuario apruebe el cierre de una tarea mayor.

---

## 📍 1. Coordenadas Actuales

- **Fase Activa:** `Fase 1 — Definiciones y Cimientos`
- **Etapa Activa:** `Etapa 1.2 — Configuración de conexión e infraestructura con Supabase`
- **Capa Medallón Activa:** `N/A`
- **Documentos SDD Gobernantes:** Leer obligatoriamente antes de tomar decisiones arquitectónicas:
  - PRD:    `docs/reqs/f01_02_prd.md` ⬜ (pendiente de crear)
  - SPEC:   `docs/specs/f01_02_spec.md` ⬜ (pendiente de crear)
  - Plan:   `docs/plans/f01_02_plan.md` ⬜ (pendiente de crear)
  - Tareas: `docs/tasks/f01_02_task.md` ⬜ (pendiente de crear)

---

## 🏁 2. Hitos de la Fase Actual

### Fase 1 — Definiciones y Cimientos
- ✅ **1.1** Reglas globales, estructura de archivos e inicialización del `PROJECT_index.md`
- ⬜ **1.2** Configuración de conexión e infraestructura con Supabase
- ⬜ **1.3** Definición del Data Contract (esquemas, tipos de datos, constraints)

---

## 🏗️ 3. Mapa de Arquitectura (Rutas Clave)

| Componente | Ruta | Estado |
|---|---|---|
| Constitución del Proyecto | `CLAUDE.md` | ✅ Existe |
| Índice del Proyecto | `PROJECT_index.md` | ✅ Existe |
| Bitácora de Sesión | `PROJECT_handoff.md` | ✅ Existe |
| Skill: update-index | `.claude/skills/update-index/SKILL.md` | ✅ Existe |
| Skill: session-close | `.claude/skills/session-close/SKILL.md` | ✅ Existe |
| Skill: sdd-doc | `.claude/skills/sdd-doc/SKILL.md` | ✅ Existe |
| Skill: close-stage | `.claude/skills/close-stage/SKILL.md` | ✅ Existe |
| Skill: change-control | `.claude/skills/change-control/SKILL.md` | ✅ Existe |
| Orquestador Engine | `engine/main.py` | ⬜ Fase 2 |
| Configuración Global | `engine/config.yaml` | ⬜ Fase 2 |
| Pipelines | `engine/pipelines/` | ⬜ Fase 2 |
| Lógica Atómica | `engine/src/` | ⬜ Fase 2 |
| Dashboard Web | `web/` | ⬜ Transversal |
| Requerimientos (reqs) | `docs/reqs/` | ✅ Existe |
| Especificaciones (specs) | `docs/specs/` | ✅ Existe |
| Planes (plans) | `docs/plans/` | ✅ Existe |
| Tareas (tasks) | `docs/tasks/` | ✅ Existe |
| Lecciones Aprendidas | `docs/lessons/` | ✅ Existe |
| Resúmenes Ejecutivos | `docs/executives/` | ✅ Existe |
| Control de Cambios | `docs/changes/` | ✅ Existe |

---

## 📚 4. Índice de Documentos SDD

### Fase 1 — Definiciones y Cimientos

| Documento | Ruta | Estado |
|---|---|---|
| PRD Etapa 1.1 | `docs/reqs/f01_01_prd.md` | ✅ Cerrado |
| SPEC Etapa 1.1 | `docs/specs/f01_01_spec.md` | ✅ Cerrado |
| Plan Etapa 1.1 | `docs/plans/f01_01_plan.md` | ✅ Cerrado |
| Tareas Etapa 1.1 | `docs/tasks/f01_01_task.md` | ✅ Cerrado |
| Ejecutivo Etapa 1.1 | `docs/executives/f01_01_executive.md` | ✅ Cerrado |
| PRD Etapa 1.2 | `docs/reqs/f01_02_prd.md` | ⬜ Pendiente |
| SPEC Etapa 1.2 | `docs/specs/f01_02_spec.md` | ⬜ Pendiente |
| Plan Etapa 1.2 | `docs/plans/f01_02_plan.md` | ⬜ Pendiente |
| Tareas Etapa 1.2 | `docs/tasks/f01_02_task.md` | ⬜ Pendiente |

---

## 📝 5. Notas y Decisiones Registradas

- **2026-03-20** — Se decidió implementar la gestión del `PROJECT_index.md` mediante un skill de Claude Code (`/update-index`), automatizando la creación y actualización del mapa macro del proyecto como parte de la gobernanza del agente.
- **2026-03-21** — Etapa 1.1 cerrada formalmente. Resumen Ejecutivo generado: `docs/executives/f01_01_executive.md`. Gate de avance cumplido.
- **2026-03-21** — MCP GitHub configurado (modo lectura) para auditoría de estado del repositorio. Restricción: escritura solo con orden explícita del usuario (según CLAUDE.md §1).
- **2026-03-21** — Credencial de acceso a GitHub expuesta accidentalmente durante setup → revocada y reemplazada de forma segura.
