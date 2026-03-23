# Task List — Definición del Data Contract (`f01_03`)

> **Trazabilidad:** Estas tareas implementan el plan `docs/plans/f01_03_plan.md`.
> **Fase:** 1 — Definiciones y Cimientos
> **Etapa:** 1.3 — Definición del Data Contract (esquemas, tipos de datos, constraints)
> **Estado:** ✅ Aprobado — Listo para ejecución
> **Fecha:** 2026-03-23
>
> Actualiza este archivo marcando `[x]` cuando completes cada tarea.

---

## Bloque 1 — Prerequisitos y Validación de Entorno

- [ ] `[TSK-1-01]` Verificar que `docs/database/schema.sql` está sincronizado con Supabase real (vía MCP o query directa). Listar discrepancias si existen. → `[RSK-01]`
- [ ] `[TSK-1-02]` Validar acceso de escritura a S3: subir un archivo de prueba (`test_write.txt`) usando credenciales `SUPABASE_S3_*` de `.env`. Confirmar éxito o documentar bloqueador. → `[RSK-04]`
- [ ] `[TSK-1-03]` Verificar que el conector Supabase (`engine/src/connectors/supabase_client.py`) puede ejecutar DDL (`CREATE TABLE`) con service role key. → `[REQ-07]`

**Criterio de salida:** Entorno verificado. Sin bloqueadores para crear tabla en Supabase ni subir archivos a S3.

---

## Bloque 2 — Crear `contracts/data_contract.yaml`

- [ ] `[TSK-1-04]` Crear carpeta `contracts/` en la raíz del proyecto. → `[REQ-01]`
- [ ] `[TSK-1-05]` Escribir sección `metadata` en `contracts/data_contract.yaml`: `contract_id`, `version: "1.0"`, `pyme_id: "001_ABC"`, `status: "active"`, `created_at`, `updated_at`, `updated_by`, `client_name: "Cafetería SAS"`. → `[REQ-01]`, `[REQ-06]`
- [ ] `[TSK-1-06]` Escribir sección `objective_variable` con definición de `demanda_teorica`: nombre, tipo `calculated`, descripción, y subsección `calculation` con `version: "1.0"`. → `[REQ-04]`
- [ ] `[TSK-1-07]` Escribir `rule_1_with_surplus` dentro de `calculation`: condición (`unidades_sobrantes > 0`), significado de negocio, fórmula (`demanda_teorica = unidades_vendidas`). → `[REQ-04]`
- [ ] `[TSK-1-08]` Escribir `rule_2_without_surplus` dentro de `calculation`: condición (`unidades_sobrantes = 0`), significado de negocio, algoritmo de 4 pasos (extraer hora, buscar días similares, calcular demanda no satisfecha, sumar). → `[REQ-04]`
- [ ] `[TSK-1-09]` Escribir `parameters` dentro de `rule_2_without_surplus`: `similar_days_criteria: same_weekday`, `exclude_holidays: true`, `lookback_days: 90`, `minimum_similar_days: 1`, `fallback`. → `[REQ-05]`
- [ ] `[TSK-1-10]` Escribir `warm_up_period` dentro de `calculation`: `days_until_reliable: 90`, nota sobre confiabilidad inicial. → `[REQ-05]`
- [ ] `[TSK-1-11]` Escribir `depends_on` dentro de `objective_variable`: array con dependencias a `usr_ventas` (columnas: `fecha`, `unidades_vendidas`) y `usr_produccion` (columnas: `fecha`, `unidades_sobrantes`). → `[REQ-04]`
- [ ] `[TSK-1-12]` Escribir sección `mandatory_tables` con tabla `usr_ventas`: `status: mandatory`, `reason`, `description`, `grain: per transaction`, `update_frequency: daily`, `owner: Cafetería SAS (Punto de Venta)`, y array `columns` con las 8 columnas según SPEC §2.2 (`id`, `fecha`, `unidades_vendidas`, `unidades_pagadas`, `unidades_bonificadas`, `created_at`, `updated_at`, `pyme_id`). → `[REQ-02]`, `[REQ-03]`, `[DAT-01]`
- [ ] `[TSK-1-13]` Escribir tabla `usr_produccion` dentro de `mandatory_tables`: misma estructura, 9 columnas según SPEC §2.2 (`id`, `fecha`, `unidades_vendidas`, `produccion_estimada`, `unidades_sobrantes`, `porcentaje_merma`, `created_at`, `updated_at`, `pyme_id`). → `[REQ-02]`, `[REQ-03]`, `[DAT-02]`
- [ ] `[TSK-1-14]` Escribir sección `optional_tables` con tabla `usr_clima`: `status: optional`, columnas según SPEC §2.3 (`id`, `fecha`, `estado_clima`, `created_at`, `updated_at`, `pyme_id`). → `[REQ-02]`, `[DAT-03]`
- [ ] `[TSK-1-15]` Escribir tabla `usr_macro_anual` dentro de `optional_tables`: columnas según SPEC §2.3 (`id`, `fecha`, `smmlv`, `created_at`, `updated_at`, `pyme_id`). → `[REQ-02]`, `[DAT-04]`
- [ ] `[TSK-1-16]` Escribir tabla `usr_macro_diario` dentro de `optional_tables`: columnas según SPEC §2.3 (`id`, `fecha`, `trm`, `created_at`, `updated_at`, `pyme_id`). → `[REQ-02]`, `[DAT-05]`
- [ ] `[TSK-1-17]` Escribir tabla `usr_macro_mensual` dentro de `optional_tables`: columnas según SPEC §2.3 (`id`, `fecha`, `inflacion_anual`, `desempleo`, `created_at`, `updated_at`, `pyme_id`). → `[REQ-02]`, `[DAT-06]`
- [ ] `[TSK-1-18]` Escribir tabla `usr_publicidad` dentro de `optional_tables`: columnas según SPEC §2.3 (`id`, `fecha`, `campaña`, `pauta_facebook`, `pauta_instagram`, `volantes_impresos`, `total_diario`, `created_at`, `updated_at`, `pyme_id`). → `[REQ-02]`, `[DAT-07]`
- [ ] `[TSK-1-19]` Escribir sección `changelog` con entrada de versión 1.0: fecha, autor, descripción, lista de cambios iniciales. → `[REQ-10]`
- [ ] `[TSK-1-20]` Validar que el YAML es parseable: `python -c "import yaml; yaml.safe_load(open('contracts/data_contract.yaml'))"`. → `[MET-01]`

**Criterio de salida:** `contracts/data_contract.yaml` existe, es YAML válido, contiene las 5 secciones obligatorias con 7 tablas documentadas.

---

## Bloque 3 — Crear Tabla `contracts` en Supabase

- [ ] `[TSK-1-21]` Ejecutar DDL completo de la tabla `contracts` en Supabase según SPEC §2.4: tabla con 9 columnas, constraint `contracts_version_pyme_unique`, partial unique index `idx_one_active_contract_per_pyme`, función `activate_contract_version()`, trigger `trg_activate_contract`, trigger `update_contracts_updated_at`. → `[REQ-07]`, `[ARC-02]`
- [ ] `[TSK-1-22]` Verificar trigger de activación: insertar 2 registros con `is_active=true` para `pyme_id='001_ABC'`. Confirmar que solo el último tiene `is_active=true`. → `[MET-05]`, `[MET-07]`
- [ ] `[TSK-1-23]` Actualizar `docs/database/schema.sql` con el DDL completo de la tabla `contracts` (incluyendo comentarios, triggers y notas de mantenimiento — mandato CLAUDE.md §5). → `[ARC-02]`

**Criterio de salida:** Tabla `contracts` operativa en Supabase con trigger verificado. `schema.sql` actualizado.

---

## Bloque 4 — Módulos Python (TDD)

> **Mandato CC_00003:** Tests de integración escritos ANTES del código. Ciclo: rojo → implementación → verde.

- [ ] `[TSK-1-24]` Crear estructura de carpetas: `engine/src/contract/` con `__init__.py`, `engine/tests/contract/` con `__init__.py`. → `[ARC-04]`, `[ARC-05]`
- [ ] `[TSK-1-25]` **TDD — Tests primero (ROJO):** Escribir `engine/tests/contract/test_contract_validator.py` con tests para: `validate_contract_structure()` (YAML con 5 secciones, falla sin ellas), `validate_mandatory_tables()` (mínimo 1 mandatoria, falla sin mandatorias), `get_mandatory_table_names()` (retorna `['usr_ventas', 'usr_produccion']`), `get_optional_table_names()` (retorna 5 tablas opcionales), `get_all_table_names()` (retorna 7 tablas). Ejecutar tests → deben fallar con `ImportError`. → `[ARC-05]`, `[REQ-01]`, `[REQ-03]`
- [ ] `[TSK-1-26]` **TDD — Implementar (VERDE):** Escribir `engine/src/contract/contract_validator.py` con funciones: `validate_contract_structure()`, `validate_mandatory_tables()`, `get_mandatory_table_names()`, `get_optional_table_names()`, `get_all_table_names()`. Incluir excepción `ContractValidationError` (`ERR_CNTR_005`). Ejecutar tests → deben pasar. → `[ARC-05]`
- [ ] `[TSK-1-27]` **TDD — Tests primero (ROJO):** Escribir `engine/tests/contract/test_contract_loader.py` con tests para: `load_contract_from_file()` (carga local retorna dict), `verify_checksum()` (SHA256 correcto retorna `True`, incorrecto retorna `False`), `publish_contract()` (integración contra Supabase + S3 real — archivo sube, registro se crea con `is_active=true` y checksum correcto). Ejecutar tests → deben fallar con `ImportError`. → `[ARC-04]`, `[REQ-08]`, `[REQ-09]`
- [ ] `[TSK-1-28]` **TDD — Implementar (VERDE):** Escribir `engine/src/contract/contract_loader.py` con funciones: `load_contract_from_file()`, `load_contract_from_cloud()`, `get_active_contract_location()`, `download_from_s3()`, `verify_checksum()`, `publish_contract()`. Incluir excepciones `ContractNotFoundError` (`ERR_CNTR_001`), `S3DownloadError` (`ERR_CNTR_002`), `ChecksumMismatchError` (`ERR_CNTR_003`), `ContractParseError` (`ERR_CNTR_004`), `MandatoryTableRemovalError` (`ERR_CNTR_006`). Ejecutar tests → deben pasar. → `[ARC-04]`

**Criterio de salida:** Todos los tests de `engine/tests/contract/` pasan. Módulos implementados.

---

## Bloque 5 — Publicar Contrato v1.0 a S3 + Supabase

- [ ] `[TSK-1-29]` Ejecutar `publish_contract('contracts/data_contract.yaml', '001_ABC', 'AI Agent')` para subir el contrato a S3 como `data_contract_v1.0.yaml` y registrar en Supabase. → `[REQ-08]`, `[ARC-03]`
- [ ] `[TSK-1-30]` Verificar registro en tabla `contracts` de Supabase: `is_active=true`, `s3_location` apunta a `contracts/data_contract_v1.0.yaml`, `checksum` coincide con SHA256 del archivo local. → `[MET-06]`
- [ ] `[TSK-1-31]` Ejecutar `load_contract_from_cloud('001_ABC')` como test end-to-end: descarga de S3, verificación de checksum, parseo YAML, validación de estructura. Confirmar que retorna dict válido. → `[REQ-09]`, `[MET-01]`

**Criterio de salida:** Contrato v1.0 publicado y verificable end-to-end desde la nube.

---

## Bloque 6 — Sincronizar `config.yaml`

- [ ] `[TSK-1-32]` Actualizar sección `tables` de `engine/config.yaml`: reemplazar `usr_inventario` → `usr_macro_anual`, `usr_festivos` → `usr_macro_diario`, `usr_ipc` → `usr_macro_mensual`. Resultado: 7 tablas que coinciden con `schema.sql`. → `[ARC-01]`
- [ ] `[TSK-1-33]` Agregar sección `contract` en `engine/config.yaml` con: `pyme_id: "001_ABC"`, `local_path: "contracts/data_contract.yaml"`, `s3_prefix: "contracts/"`, `startup_required: true`. → `[REQ-09]`
- [ ] `[TSK-1-34]` Ejecutar tests de Etapa 1.2 (`pytest engine/tests/connectors/test_supabase_client.py`) y confirmar que los 4 tests existentes siguen en verde tras los cambios en `config.yaml`. → Regresión

**Criterio de salida:** `config.yaml` alineado con el contrato y `schema.sql`. Tests existentes no rotos.

---

## Cierre de Etapa

- [ ] `[TSK-1-35]` Ejecutar suite completa de tests: `pytest engine/tests/`. Incluye tests de Etapa 1.2 (connectors) y Etapa 1.3 (contract). Todos deben estar en verde.
- [ ] `[TSK-1-36]` Actualizar `PROJECT_index.md` con hitos completados (`/update-index`).
- [ ] `[TSK-1-37]` Crear commit atómico: `feat: etapa 1.3 — definición del Data Contract`.
- [ ] `[TSK-1-38]` Generar Resumen Ejecutivo: `docs/executives/f01_03_executive.md` (`/close-stage`).
- [ ] `[TSK-1-39]` Actualizar `PROJECT_handoff.md` (`/session-close`).

**Criterio de salida:** Etapa 1.3 completada, commiteada y documentada. Gate de avance a Etapa 2.1 desbloqueado.

---

## Matriz de Trazabilidad — Tareas → REQs

| Tarea | REQ / ARC / MET | Bloque |
|---|---|---|
| `[TSK-1-01]` | `[RSK-01]` | B1 |
| `[TSK-1-02]` | `[RSK-04]` | B1 |
| `[TSK-1-03]` | `[REQ-07]` | B1 |
| `[TSK-1-04]` | `[REQ-01]` | B2 |
| `[TSK-1-05]` | `[REQ-01]`, `[REQ-06]` | B2 |
| `[TSK-1-06]` — `[TSK-1-11]` | `[REQ-04]`, `[REQ-05]` | B2 |
| `[TSK-1-12]` — `[TSK-1-13]` | `[REQ-02]`, `[REQ-03]`, `[DAT-01]`, `[DAT-02]` | B2 |
| `[TSK-1-14]` — `[TSK-1-18]` | `[REQ-02]`, `[DAT-03]` — `[DAT-07]` | B2 |
| `[TSK-1-19]` | `[REQ-10]` | B2 |
| `[TSK-1-20]` | `[MET-01]` | B2 |
| `[TSK-1-21]` | `[REQ-07]`, `[ARC-02]` | B3 |
| `[TSK-1-22]` | `[MET-05]`, `[MET-07]` | B3 |
| `[TSK-1-23]` | `[ARC-02]` | B3 |
| `[TSK-1-24]` | `[ARC-04]`, `[ARC-05]` | B4 |
| `[TSK-1-25]` — `[TSK-1-26]` | `[ARC-05]`, `[REQ-01]`, `[REQ-03]` | B4 |
| `[TSK-1-27]` — `[TSK-1-28]` | `[ARC-04]`, `[REQ-08]`, `[REQ-09]` | B4 |
| `[TSK-1-29]` | `[REQ-08]`, `[ARC-03]` | B5 |
| `[TSK-1-30]` | `[MET-06]` | B5 |
| `[TSK-1-31]` | `[REQ-09]`, `[MET-01]` | B5 |
| `[TSK-1-32]` | `[ARC-01]` | B6 |
| `[TSK-1-33]` | `[REQ-09]` | B6 |
| `[TSK-1-34]` | Regresión | B6 |
| `[TSK-1-35]` — `[TSK-1-39]` | Cierre | B7 |
