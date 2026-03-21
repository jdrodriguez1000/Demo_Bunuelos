# Task List — Definiciones y Cimientos: Gobernanza y Estructura Base (`f01_01`)

> **Trazabilidad:** Estas tareas implementan el plan `docs/plans/f01_01_plan.md`.
> **Regla:** Marca `[x]` al completar cada tarea. Nunca eliminar tareas completadas.
> **Última actualización:** 2026-03-20

---

## Bloque 1 — Repositorio Git y Control de Versiones (`[REQ-09]`)

- [x] `[TSK-01-01]` Verificar que el repositorio Git está inicializado (`git status` sin errores).
- [x] `[TSK-01-02]` Verificar que existe `.gitignore` en la raíz del proyecto.
- [x] `[TSK-01-03]` Confirmar que `.gitignore` contiene los patrones de exclusión definidos en SPEC §2.6: `venv/`, `.env`, `*.pkl`, `*.joblib`, `.dvc/cache/`, `__pycache__/`.

---

## Bloque 2 — Constitución del Agente (`[REQ-01]` / `[ARC-01]`)

- [x] `[TSK-01-04]` Verificar que `CLAUDE.md` existe en la raíz del proyecto.
- [x] `[TSK-01-05]` Confirmar que `CLAUDE.md` contiene las 10 secciones obligatorias: §1 Comportamiento, §2 Identidad, §3 Stack, §4 Arquitectura, §5 Estándares, §6 Workflows, §7 Protocolos ML, §8 Dominio, §9 Fases, §10 Gobernanza Estratégica.
- [x] `[TSK-01-06]` Confirmar que §9 Fases contiene la tabla completa de las 4 fases y 12 etapas del proyecto.
- [x] `[TSK-01-07]` Confirmar que §1 incluye el Protocolo de Inicio de Sesión (3 pasos) y el Protocolo de Cierre de Sesión.

---

## Bloque 3 — Estructura de Carpetas SDD (`[REQ-07]` / `[ARC-05]`)

- [x] `[TSK-01-08]` Crear carpeta `docs/reqs/`.
- [x] `[TSK-01-09]` Crear carpeta `docs/specs/`.
- [x] `[TSK-01-10]` Crear carpeta `docs/plans/`. *(Este archivo lo confirma)*
- [x] `[TSK-01-11]` Crear carpeta `docs/tasks/`. *(Este archivo lo confirma)*
- [x] `[TSK-01-12]` Ejecutar `ls docs/` y verificar que las 4 carpetas aparecen listadas (`[MET-03]`).

---

## Bloque 4 — Entorno Python (`[REQ-08]` / `[ARC-06]`)

- [x] `[TSK-01-13]` Crear `requirements.txt` en la raíz con las dependencias y versiones pinneadas definidas en SPEC §3.
- [x] `[TSK-01-14]` Inicializar el ambiente virtual: `python -m venv venv`.
- [x] `[TSK-01-15]` Activar el ambiente virtual e instalar dependencias: `pip install -r requirements.txt`.
- [x] `[TSK-01-16]` Verificar que la instalación termina con exit code 0 y sin errores de compatibilidad (`[MET-04]`).
- [x] `[TSK-01-17]` Crear `.env.example` en la raíz con las claves definidas en SPEC §2.5 (sin valores).
- [x] `[TSK-01-18]` Verificar que `venv/` y `.env` aparecen en `.gitignore` y NO son trackeados por Git.

---

## Bloque 5 — Archivos de Contexto del Proyecto (`[REQ-02]`, `[REQ-03]`)

- [x] `[TSK-01-19]` Verificar que `PROJECT_index.md` existe y contiene las 5 secciones: Coordenadas Actuales, Hitos, Mapa de Arquitectura, Índice SDD, Notas.
- [x] `[TSK-01-20]` Verificar que `PROJECT_index.md` refleja la fase y etapa activa correcta (Fase 1, Etapa 1.1).
- [x] `[TSK-01-21]` Crear `PROJECT_handoff.md` con la estructura de 5 secciones definida en SPEC §2.3 (ejecutar `/session-close` al final de esta sesión).
- [x] `[TSK-01-22]` Verificar que `PROJECT_handoff.md` contiene: timestamp, working set, contexto inmediato, bloqueador y próxima acción concreta.

---

## Bloque 6 — Skills de Claude Code (`[REQ-04]`, `[REQ-05]`, `[REQ-06]`)

- [x] `[TSK-01-23]` Verificar que `.claude/skills/update-index/SKILL.md` existe con frontmatter correcto (`name`, `description`, `invocation`, `triggers`).
- [x] `[TSK-01-24]` Verificar que `.claude/skills/session-close/SKILL.md` existe con frontmatter correcto.
- [x] `[TSK-01-25]` Verificar que `.claude/skills/sdd-doc/SKILL.md` existe con frontmatter correcto y los 4 modos (A/B/C/D).
- [ ] `[TSK-01-26]` Probar invocación de `/update-index`: verificar que actualiza `PROJECT_index.md` sin errores (`[MET-02]`).
- [ ] `[TSK-01-27]` Probar invocación de `/session-close`: verificar que crea/actualiza `PROJECT_handoff.md` sin errores (`[MET-02]`).
- [ ] `[TSK-01-28]` Probar invocación de `/sdd-doc`: verificar que pregunta modo y etapa antes de escribir (`[MET-02]`).

---

## Bloque 7 — Commit Inicial y Verificación Final (`[REQ-09]` / `[MET-01..05]`)

- [ ] `[TSK-01-29]` Revisar el DoD completo del plan (`docs/plans/f01_01_plan.md` §5) y confirmar que todos los ítems están marcados.
- [ ] `[TSK-01-30]` Stagear los archivos de gobernanza: `CLAUDE.md`, `PROJECT_index.md`, `.gitignore`, `requirements.txt`, `.env.example`, `docs/`, `.claude/`.
- [ ] `[TSK-01-31]` Crear commit atómico en `main`: `feat: etapa 1.1 — gobernanza y estructura base completada`.
- [ ] `[TSK-01-32]` Verificar con `git log --oneline` que el commit aparece registrado.

---

## Bloque 8 — Gobernanza Extendida: Lecciones, Ejecutivos y Control de Cambios (`[REQ-10]` al `[REQ-15]`)

- [x] `[TSK-01-36]` Crear carpeta `docs/lessons/`.
- [x] `[TSK-01-37]` Crear carpeta `docs/executives/`.
- [x] `[TSK-01-38]` Crear carpeta `docs/changes/`.
- [x] `[TSK-01-39]` Inicializar `docs/lessons/lessons-learned.md` con estructura base: encabezado del proyecto + sección `## Fase 1 — Etapa 1.1` vacía lista para recibir entradas de sesión.
- [ ] `[TSK-01-40]` Crear skill `/close-stage` en `.claude/skills/close-stage/SKILL.md` con frontmatter correcto y lógica para generar resumen ejecutivo en lenguaje de negocio.
- [ ] `[TSK-01-41]` Crear skill `/change-control` en `.claude/skills/change-control/SKILL.md` con frontmatter correcto y los 4 modos: CREATE, APPROVE, REJECT, LIST.
- [ ] `[TSK-01-42]` Actualizar skill `/session-close` para añadir Paso 4: registro en `docs/lessons/lessons-learned.md` al cierre de cada sesión.
- [ ] `[TSK-01-43]` Probar invocación de `/close-stage`: verificar que solicita etapa y genera el documento ejecutivo sin errores (`[MET-06]`).
- [ ] `[TSK-01-44]` Probar invocación de `/change-control` modo LIST: verificar que responde sin errores aunque no haya CCs (`[MET-06]`).
- [ ] `[TSK-01-45]` Ejecutar `ls docs/` y verificar que las 7 carpetas aparecen: `reqs/`, `specs/`, `plans/`, `tasks/`, `lessons/`, `executives/`, `changes/` (`[MET-07]`).

---

## Cierre de Etapa

- [ ] `[TSK-01-33]` Ejecutar `/update-index` para marcar el hito 1.1 como ✅ en `PROJECT_index.md`.
- [ ] `[TSK-01-34]` Actualizar el estado de los 4 docs SDD de esta etapa a ✅ en `PROJECT_index.md`.
- [ ] `[TSK-01-35]` Ejecutar `/session-close` para reescribir `PROJECT_handoff.md` con el estado de cierre de la etapa y la próxima acción (inicio de Etapa 1.2 — Supabase).
