# 🗺️ PROJECT_index — Dashboard Demanda Buñuelos

> **MANDATO IA:** Lee este archivo en el Paso 2 del Protocolo de Inicio de Sesión. Úsalo para ubicar los documentos SDD activos y entender el estado macro del proyecto. Actualiza el checklist de hitos SOLO cuando el usuario apruebe el cierre de una tarea mayor.

---

## 📍 1. Coordenadas Actuales

- **Fase Activa:** `Fase 1 — Definiciones y Cimientos`
- **Etapa Activa:** `Etapa 1.1 — Reglas globales, estructura de archivos e inicialización del PROJECT_index.md`
- **Capa Medallón Activa:** `N/A`
- **Documentos SDD Gobernantes:**
  - PRD:    `docs/reqs/f01_01_prd.md` ✅
  - SPEC:   `docs/specs/f01_01_spec.md` ✅
  - Plan:   `docs/plans/f01_01_plan.md` ✅
  - Tareas: `docs/tasks/f01_01_task.md` ✅

---

## 🏁 2. Hitos de la Fase Actual

### Fase 1 — Definiciones y Cimientos
- ⬜ **1.1** Reglas globales, estructura de archivos e inicialización del `PROJECT_index.md`
- ⬜ **1.2** Configuración de conexión e infraestructura con Supabase
- ⬜ **1.3** Definición del Data Contract (esquemas, tipos de datos, constraints)

---

## 🏗️ 3. Mapa de Arquitectura (Rutas Clave)

| Componente | Ruta | Estado |
|---|---|---|
| Constitución del Proyecto | `CLAUDE.md` | ✅ Existe |
| Índice del Proyecto | `PROJECT_index.md` | ✅ Existe |
| Bitácora de Sesión | `PROJECT_handoff.md` | ⬜ Pendiente |
| Skill: update-index | `.claude/skills/update-index/SKILL.md` | ✅ Existe |
| Skill: session-close | `.claude/skills/session-close/SKILL.md` | ✅ Existe |
| Orquestador Engine | `engine/main.py` | ⬜ Fase 2 |
| Configuración Global | `engine/config.yaml` | ⬜ Fase 2 |
| Pipelines | `engine/pipelines/` | ⬜ Fase 2 |
| Lógica Atómica | `engine/src/` | ⬜ Fase 2 |
| Dashboard Web | `web/` | ⬜ Transversal |
| Requerimientos (reqs) | `docs/reqs/` | ✅ Existe |
| Especificaciones (specs) | `docs/specs/` | ✅ Existe |
| Planes (plans) | `docs/plans/` | ✅ Existe |
| Tareas (tasks) | `docs/tasks/` | ✅ Existe |

---

## 📚 4. Índice de Documentos SDD

> Sin documentos SDD creados aún. Se generarán a partir de la Etapa 1.1.

---

## 📝 5. Notas y Decisiones Registradas

- **2026-03-20** — Se decidió implementar la gestión del `PROJECT_index.md` mediante un skill de Claude Code (`/update-index`), automatizando la creación y actualización del mapa macro del proyecto como parte de la gobernanza del agente.
