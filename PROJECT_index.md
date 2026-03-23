# 🗺️ PROJECT_index — Dashboard Demanda Buñuelos

> **MANDATO IA:** Lee este archivo en el Paso 2 del Protocolo de Inicio de Sesión. Úsalo para ubicar los documentos SDD activos y entender el estado macro del proyecto. Actualiza el checklist de hitos SOLO cuando el usuario apruebe el cierre de una tarea mayor.

---

## 📍 1. Coordenadas Actuales

- **Fase Activa:** `Fase 1 — Definiciones y Cimientos`
- **Etapa Activa:** `Etapa 1.3 — Definición del Data Contract (esquemas, tipos de datos, constraints)`
- **Capa Medallón Activa:** `N/A`
- **Documentos SDD Gobernantes:** Leer obligatoriamente antes de tomar decisiones arquitectónicas:
  - PRD:    `docs/reqs/f01_03_prd.md` ✅ Aprobado
  - SPEC:   `docs/specs/f01_03_spec.md` ✅ Aprobado
  - Plan:   `docs/plans/f01_03_plan.md` ✅ Aprobado
  - Tareas: `docs/tasks/f01_03_task.md` ✅ Aprobado

---

## 🏁 2. Hitos de la Fase Actual

### Fase 1 — Definiciones y Cimientos
- ✅ **1.1** Reglas globales, estructura de archivos e inicialización del `PROJECT_index.md`
- ✅ **1.2** Configuración de conexión e infraestructura con Supabase
- ⬜ **1.3** Definición del Data Contract (esquemas, tipos de datos, constraints)

---

## 🏗️ 3. Mapa de Arquitectura (Rutas Clave)

| Componente | Ruta | Estado |
|---|---|---|
| Constitución del Proyecto | `CLAUDE.md` | ✅ Existe |
| Índice del Proyecto | `PROJECT_index.md` | ✅ Existe |
| Bitácora de Sesión | `PROJECT_handoff.md` | ✅ Existe |
| Conector Supabase | `engine/src/connectors/supabase_client.py` | ✅ Existe |
| Configuración Global | `engine/config.yaml` | ✅ Existe |
| Tests Conector | `engine/tests/connectors/test_supabase_client.py` | ✅ Existe |
| Orquestador Engine | `engine/main.py` | ⬜ Fase 2 |
| Pipelines | `engine/pipelines/` | ⬜ Fase 2 |
| Lógica Atómica (src) | `engine/src/` | 🔄 Parcial (solo connectors) |
| Dashboard Web | `web/` | ⬜ Transversal (diferido) |
| Skill: update-index | `.claude/skills/update-index/SKILL.md` | ✅ Existe |
| Skill: session-close | `.claude/skills/session-close/SKILL.md` | ✅ Existe |
| Skill: sdd-doc | `.claude/skills/sdd-doc/SKILL.md` | ✅ Existe |
| Skill: close-stage | `.claude/skills/close-stage/SKILL.md` | ✅ Existe |
| Skill: change-control | `.claude/skills/change-control/SKILL.md` | ✅ Existe |
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
| PRD Etapa 1.2 | `docs/reqs/f01_02_prd.md` | ✅ Cerrado |
| SPEC Etapa 1.2 | `docs/specs/f01_02_spec.md` | ✅ Cerrado |
| Plan Etapa 1.2 | `docs/plans/f01_02_plan.md` | ✅ Cerrado |
| Tareas Etapa 1.2 | `docs/tasks/f01_02_task.md` | ✅ Cerrado |
| Ejecutivo Etapa 1.2 | `docs/executives/f01_02_executive.md` | ✅ Cerrado |
| PRD Etapa 1.3 | `docs/reqs/f01_03_prd.md` | ✅ Aprobado |
| SPEC Etapa 1.3 | `docs/specs/f01_03_spec.md` | ✅ Aprobado |
| Plan Etapa 1.3 | `docs/plans/f01_03_plan.md` | ✅ Aprobado |
| Tareas Etapa 1.3 | `docs/tasks/f01_03_task.md` | ✅ Aprobado |

---

## 📝 5. Notas y Decisiones Registradas

- **2026-03-20** — Se decidió implementar la gestión del `PROJECT_index.md` mediante un skill de Claude Code (`/update-index`), automatizando la creación y actualización del mapa macro del proyecto como parte de la gobernanza del agente.
- **2026-03-21** — Etapa 1.1 cerrada formalmente. Resumen Ejecutivo generado: `docs/executives/f01_01_executive.md`. Gate de avance cumplido.
- **2026-03-21** — MCP GitHub configurado (modo lectura) para auditoría de estado del repositorio. Restricción: escritura solo con orden explícita del usuario (según CLAUDE.md §1).
- **2026-03-21** — Credencial de acceso a GitHub expuesta accidentalmente durante setup → revocada y reemplazada de forma segura.
- **2026-03-22** — Etapa 1.2 cerrada formalmente. Resumen Ejecutivo generado: `docs/executives/f01_02_executive.md`. Gate de avance a Etapa 1.3 desbloqueado.
- **2026-03-22** — MCP Supabase configurado via `.mcp.json` (local, gitignoreado) — estrategia más confiable en Windows que interpolación de variables en `settings.json`.
- **2026-03-22** — Git Flow completo (`feat/* → dev → test → prod`) se activa en Etapa 2.1. Para Etapas 1.x el código va directamente a `main`.
- **2026-03-22** — Bloque 5 (web/) diferido: conexión Next.js → Supabase se implementa en la primera etapa que produzca componentes de dashboard reales.
- **2026-03-22** — TDD obligatorio (CC_00003) validado en práctica: 4 tests en rojo → implementación → 4 tests en verde. Ciclo completo ejecutado correctamente.
- **2026-03-22** — CC_00004 aprobado: indicador de progreso del proyecto añadido a la gobernanza. Metodología: `Avance = Σ (Etapas Cerradas / E_i) × (100% / N)`. N y E_i son dinámicos — leídos de `PROJECT_index.md` al cerrar cada etapa. Impacto: `/close-stage` ahora inyecta el indicador automáticamente en cada ejecutivo.
- **2026-03-23** — Etapa 1.3: los 4 documentos SDD (PRD, SPEC, Plan, Tasks) creados y aprobados. Artefactos: `contracts/data_contract.yaml` (estructura), tabla `contracts` en Supabase (con trigger de activación), módulos Python TDD (`contract_loader.py`, `contract_validator.py`). Implementación pendiente de ejecución.
