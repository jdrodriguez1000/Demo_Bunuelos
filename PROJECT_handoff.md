# 🤝 PROJECT_handoff — Bitácora de Cambio de Sesión

> **MANDATO IA:** Este es el estado mental exacto donde se pausó el trabajo. Léelo en el Paso 3 del Protocolo de Inicio de Sesión para retomar la acción táctica de inmediato.

---

## 🕒 Punto de Guardado

- **Última actualización:** 23 de marzo de 2026 — cierre de sesión documentación Etapa 1.3
- **Fase / Etapa:** `Fase 1 — Etapa 1.3` (SDD completo y aprobado — implementación pendiente de inicio)

---

## 📂 Archivos en el Escritorio (Working Set)

- `docs/reqs/f01_03_prd.md` — PRD aprobado. Define 10 REQs, variable objetivo `demanda_teorica` con 2 reglas, 7 tablas (2 mandatorias + 5 opcionales), inmutabilidad de versiones, persistencia híbrida Supabase + S3.
- `docs/specs/f01_03_spec.md` — SPEC aprobada. DDL completo de tabla `contracts` (con partial unique index + trigger), firmas de 11 funciones Python, esquema YAML del contrato, diccionario de columnas de las 7 tablas, discrepancia `config.yaml` vs `schema.sql` documentada.
- `docs/plans/f01_03_plan.md` — Plan aprobado. 7 bloques de trabajo (B2 y B3 paralelizables), ruta crítica definida, 9 tests de integración planificados, DoD de 14 ítems.
- `docs/tasks/f01_03_task.md` — Task list aprobada. 39 tareas atómicas (TSK-1-01 a TSK-1-39), todas en estado `[ ]` — ninguna ejecutada aún.
- `PROJECT_index.md` — Actualizado: SDD de Etapa 1.3 marcados como ✅ Aprobado. Nota de sesión añadida.
- `contracts/` — Carpeta NO creada aún (es tarea TSK-1-04 de la implementación).

---

## 🧠 Contexto Inmediato

Esta sesión fue exclusivamente de **documentación SDD** — no se escribió ni ejecutó código. Los 4 documentos (PRD → SPEC → Plan → Tasks) fueron creados, refinados y aprobados por el usuario. El contrato `data_contract.yaml` aún no existe en el repositorio — se creará en el Bloque 2 de la implementación.

**Decisiones clave de diseño acordadas:**
- `demanda_teorica` se calcula con 2 reglas: si `unidades_sobrantes > 0` → `= unidades_vendidas`; si `= 0` → inferencia horaria con días similares (90 días lookback, mismo día semana, sin festivos).
- Tabla `contracts` en Supabase con partial unique index: solo 1 contrato activo por `pyme_id` en cualquier momento.
- Módulos Python: `contract_loader.py` + `contract_validator.py` bajo `engine/src/contract/`, con TDD obligatorio (CC_00003).
- `config.yaml` tiene 3 tablas incorrectas que deben sincronizarse con `schema.sql` (B6 del plan).

---

## 🚧 Bloqueador / Último Error

Ninguno — la sesión cerró en estado limpio. Los 4 SDD están aprobados y `PROJECT_index.md` actualizado. La implementación puede iniciarse en la próxima sesión.

---

## 🎯 Próxima Acción Inmediata

1. **TSK-1-01:** Verificar que `docs/database/schema.sql` está sincronizado con Supabase real (vía MCP `list_tables` o query directa). Documentar discrepancias. → Prerequisito de todo lo demás.
2. **TSK-1-02:** Validar acceso de escritura a S3: subir archivo de prueba usando credenciales `SUPABASE_S3_*` de `.env`. Confirmar éxito o documentar bloqueador.
3. **TSK-1-03:** Verificar que el conector Supabase puede ejecutar DDL (`CREATE TABLE`) con service role key.
4. **Si B1 está limpio → iniciar B2 y B3 en paralelo:** crear `contracts/data_contract.yaml` Y crear tabla `contracts` en Supabase simultáneamente.
