# Plan de Implementación — Definición del Data Contract (`f01_03`)

> **Trazabilidad:** Este plan ejecuta los requerimientos de `docs/reqs/f01_03_prd.md` según el diseño de `docs/specs/f01_03_spec.md`.
> **Fase:** 1 — Definiciones y Cimientos
> **Etapa:** 1.3 — Definición del Data Contract (esquemas, tipos de datos, constraints)
> **Estado:** ✅ Aprobado
> **Fecha:** 2026-03-23

---

## 1. Resumen del Plan

Crear el Data Contract como artefacto YAML (`contracts/data_contract.yaml`), establecer la infraestructura de persistencia en nube (tabla `contracts` en Supabase + almacenamiento S3), implementar los módulos Python para carga y validación del contrato siguiendo TDD (CC_00003), y publicar la versión 1.0 del contrato.

**Estrategia general:** Trabajo en 7 bloques secuenciales con paralelismo en B2/B3. Se prioriza la creación del artefacto YAML y la infraestructura Supabase antes del código Python, porque los módulos dependen de ambos para sus tests de integración.

---

## 2. Ruta Crítica

```
B1 (Prerequisitos)
 │
 ├──► B2 (Crear data_contract.yaml)  ──┐
 │                                      ├──► B4 (Módulos Python TDD)
 └──► B3 (Tabla contracts Supabase) ──┘          │
                                                  ▼
                                        B5 (Publicar a S3 + Supabase)
                                                  │
                                                  ▼
                                        B6 (Sincronizar config.yaml)
                                                  │
                                                  ▼
                                        B7 (Cierre de Etapa)
```

| Orden | Bloque | Depende de | Paralelizable con |
|---|---|---|---|
| 1 | B1 — Prerequisitos y validación de entorno | Ninguno | — |
| 2 | B2 — Crear `data_contract.yaml` | B1 | B3 |
| 3 | B3 — Crear tabla `contracts` en Supabase | B1 | B2 |
| 4 | B4 — Módulos Python (TDD) | B2 + B3 | — |
| 5 | B5 — Publicar contrato v1.0 a S3 + Supabase | B4 | — |
| 6 | B6 — Sincronizar `config.yaml` | B2 | — |
| 7 | B7 — Cierre de Etapa | Todos | — |

---

## 3. Backlog de Trabajo (WBS)

### B1 — Prerequisitos y Validación de Entorno

| # | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B1.1 | Verificar que `docs/database/schema.sql` está sincronizado con Supabase real (vía MCP o query directa). Documentar discrepancias si existen. | `[RSK-01]` | Confirmación o lista de discrepancias |
| B1.2 | Validar acceso de escritura a S3 con un archivo de prueba. Confirmar que las credenciales `SUPABASE_S3_*` en `.env` funcionan para upload. | `[RSK-04]` | Test de escritura exitoso a S3 o bloqueador documentado |
| B1.3 | Verificar que el conector Supabase existente (`engine/src/connectors/supabase_client.py`) puede ejecutar DDL (CREATE TABLE) con service role key. | `[REQ-07]` | Confirmación de permisos DDL |

**Criterio de salida:** Entorno verificado. Sin bloqueadores para crear tabla en Supabase ni subir archivos a S3.

---

### B2 — Crear `contracts/data_contract.yaml`

| # | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B2.1 | Crear carpeta `contracts/` en la raíz del proyecto. | `[REQ-01]` | Carpeta existe |
| B2.2 | Escribir `data_contract.yaml` con sección `metadata` (contract_id, version 1.0, pyme_id, status, timestamps). | `[REQ-01]`, `[REQ-06]` | Sección `metadata` completa |
| B2.3 | Escribir sección `objective_variable` con definición de `demanda_teorica`: Regla 1 (sobrantes > 0), Regla 2 (sobrantes = 0 + inferencia), parámetros (lookback 90 días, same_weekday, exclude_holidays), warm-up period. | `[REQ-04]`, `[REQ-05]` | Sección `objective_variable` completa con ambas reglas y parámetros |
| B2.4 | Escribir sección `mandatory_tables` con `usr_ventas` y `usr_produccion`. Cada tabla con todas sus columnas (nombre, tipo PostgreSQL, nullable, default, descripción). Extraer de `schema.sql` y verificar contra Supabase real (resultado de B1.1). | `[REQ-02]`, `[REQ-03]`, `[DAT-01]`, `[DAT-02]` | 2 tablas mandatorias documentadas con diccionario completo |
| B2.5 | Escribir sección `optional_tables` con las 5 tablas restantes: `usr_clima`, `usr_macro_anual`, `usr_macro_diario`, `usr_macro_mensual`, `usr_publicidad`. Misma estructura de columnas. | `[REQ-02]`, `[REQ-03]`, `[DAT-03]`—`[DAT-07]` | 5 tablas opcionales documentadas |
| B2.6 | Escribir sección `changelog` con entrada de versión 1.0. | `[REQ-10]` | Sección `changelog` con entrada inicial |
| B2.7 | Validar que el YAML es parseable con `python -c "import yaml; yaml.safe_load(open('contracts/data_contract.yaml'))"`. | `[MET-01]` | YAML válido sin errores de parseo |

**Criterio de salida:** `contracts/data_contract.yaml` existe, es YAML válido, contiene las 5 secciones obligatorias con 7 tablas documentadas.

---

### B3 — Crear Tabla `contracts` en Supabase

| # | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B3.1 | Ejecutar DDL de la tabla `contracts` en Supabase (SPEC §2.4). Incluye tabla, constraints, partial unique index, trigger de activación y trigger de auditoría. | `[REQ-07]`, `[ARC-02]` | Tabla `contracts` creada en Supabase |
| B3.2 | Verificar trigger: insertar 2 registros con `is_active=true` para el mismo `pyme_id`. Confirmar que solo el último queda activo. | `[MET-05]`, `[MET-07]` | Test de trigger exitoso |
| B3.3 | Actualizar `docs/database/schema.sql` con el DDL de la tabla `contracts` (mandato CLAUDE.md §5). | `[ARC-02]` | `schema.sql` actualizado |

**Criterio de salida:** Tabla `contracts` operativa en Supabase con trigger verificado. `schema.sql` actualizado.

---

### B4 — Módulos Python (TDD)

> **Mandato CC_00003:** Tests de integración escritos ANTES del código. Ciclo: rojo → implementación → verde.

| # | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B4.1 | Crear estructura de carpetas: `engine/src/contract/` con `__init__.py`, y `engine/tests/contract/`. | `[ARC-04]`, `[ARC-05]` | Carpetas creadas |
| B4.2 | **TDD — Tests primero:** Escribir `engine/tests/contract/test_contract_validator.py` con tests para: `validate_contract_structure()` (YAML con 5 secciones), `validate_mandatory_tables()` (mínimo 1 tabla mandatoria), `get_mandatory_table_names()`, `get_optional_table_names()`, `get_all_table_names()`. Tests en ROJO. | `[ARC-05]`, `[REQ-01]`, `[REQ-03]` | Tests escritos, fallando (ImportError) |
| B4.3 | **TDD — Implementar:** Escribir `engine/src/contract/contract_validator.py` con las funciones validadoras. Tests en VERDE. | `[ARC-05]` | Tests pasando |
| B4.4 | **TDD — Tests primero:** Escribir `engine/tests/contract/test_contract_loader.py` con tests para: `load_contract_from_file()` (carga local), `verify_checksum()` (SHA256), `publish_contract()` (integración contra Supabase + S3 real). Tests en ROJO. | `[ARC-04]`, `[REQ-08]`, `[REQ-09]` | Tests escritos, fallando (ImportError) |
| B4.5 | **TDD — Implementar:** Escribir `engine/src/contract/contract_loader.py` con las funciones de carga, checksum y publicación. Tests en VERDE. | `[ARC-04]` | Tests pasando |

**Criterio de salida:** Todos los tests de `engine/tests/contract/` pasan. Módulos `contract_loader.py` y `contract_validator.py` implementados.

---

### B5 — Publicar Contrato v1.0 a S3 + Supabase

| # | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B5.1 | Ejecutar `publish_contract()` para subir `contracts/data_contract.yaml` a S3 como `data_contract_v1.0.yaml`. | `[REQ-08]`, `[ARC-03]` | Archivo en S3 |
| B5.2 | Verificar que el registro en tabla `contracts` de Supabase tiene `is_active=true`, `s3_location` correcta y `checksum` coincidente con SHA256 del archivo local. | `[MET-06]` | Registro verificado |
| B5.3 | Ejecutar `load_contract_from_cloud()` como test end-to-end: descargar desde S3, verificar checksum, parsear, validar estructura. | `[REQ-09]`, `[MET-01]` | Flujo completo exitoso |

**Criterio de salida:** Contrato v1.0 publicado y verificable end-to-end desde la nube.

---

### B6 — Sincronizar `config.yaml`

| # | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B6.1 | Resolver discrepancia detectada en SPEC §6.1: actualizar `engine/config.yaml` para que las tablas listadas coincidan con `schema.sql` (reemplazar `usr_inventario`→`usr_macro_anual`, `usr_festivos`→`usr_macro_diario`, `usr_ipc`→`usr_macro_mensual`). | `[ARC-01]` | `config.yaml` sincronizado |
| B6.2 | Agregar sección `contract` en `config.yaml` con las claves definidas en SPEC §5: `pyme_id`, `local_path`, `s3_prefix`, `startup_required`. | `[REQ-09]` | Sección `contract` presente |
| B6.3 | Verificar que los tests existentes de Etapa 1.2 (`engine/tests/connectors/test_supabase_client.py`) siguen pasando tras los cambios en `config.yaml`. | — | 4 tests existentes en verde |

**Criterio de salida:** `config.yaml` alineado con el contrato y schema.sql. Tests existentes no rotos.

---

### B7 — Cierre de Etapa

| # | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B7.1 | Ejecutar suite completa de tests: `pytest engine/tests/`. Incluye tests de Etapa 1.2 (connectors) y Etapa 1.3 (contract). | Todos | Todos los tests en verde |
| B7.2 | Actualizar `PROJECT_index.md` con hitos completados (`/update-index`). | — | `PROJECT_index.md` actualizado |
| B7.3 | Crear commit atómico: `feat: etapa 1.3 — definición del Data Contract`. | — | Commit en `main` |
| B7.4 | Actualizar `PROJECT_handoff.md` (`/session-close`). | — | `PROJECT_handoff.md` actualizado |

**Criterio de salida:** Etapa 1.3 completada, commiteada y documentada.

---

## 4. Estrategia de Pruebas

> **Mandato CC_00003:** TDD obligatorio. Integration tests contra servicios reales (no mocks).

| Tipo | Qué se prueba | Archivo de test | Criterio de éxito |
|---|---|---|---|
| Integración | `validate_contract_structure()` — YAML con 5 secciones obligatorias | `engine/tests/contract/test_contract_validator.py` | Contrato válido pasa. Contrato incompleto lanza `ContractValidationError` |
| Integración | `validate_mandatory_tables()` — Al menos 1 tabla mandatoria presente | `engine/tests/contract/test_contract_validator.py` | Contrato sin mandatorias lanza error. Con mandatorias pasa |
| Integración | `get_mandatory_table_names()` / `get_optional_table_names()` / `get_all_table_names()` | `engine/tests/contract/test_contract_validator.py` | Retorna listas correctas para contrato v1.0 |
| Integración | `load_contract_from_file()` — Carga local de YAML | `engine/tests/contract/test_contract_loader.py` | Retorna dict parseado con estructura correcta |
| Integración | `verify_checksum()` — SHA256 de archivo | `engine/tests/contract/test_contract_loader.py` | True con checksum correcto. False con checksum incorrecto |
| Integración | `publish_contract()` — Publicar a S3 + registrar en Supabase real | `engine/tests/contract/test_contract_loader.py` | Archivo existe en S3. Registro en Supabase con `is_active=true` y checksum correcto |
| Integración | Trigger de tabla `contracts` — Solo un activo por `pyme_id` | `engine/tests/contract/test_contract_loader.py` | Insertar 2 versiones → solo la última tiene `is_active=true` |
| End-to-end | `load_contract_from_cloud()` — Flujo completo de startup | `engine/tests/contract/test_contract_loader.py` | Descarga de S3, verifica checksum, parsea, valida estructura. Retorna dict |
| Regresión | Tests existentes de Etapa 1.2 | `engine/tests/connectors/test_supabase_client.py` | 4 tests existentes siguen en verde |

---

## 5. Definición de "Hecho" (DoD)

- [ ] `contracts/data_contract.yaml` existe y es YAML válido (`[MET-01]`)
- [ ] Todas las tablas actuales documentadas con diccionario completo de columnas (`[MET-02]`)
- [ ] `usr_ventas` y `usr_produccion` clasificadas como mandatorias (`[MET-03]`)
- [ ] `demanda_teorica` documentada con 2 reglas y parámetros de inferencia (`[MET-04]`)
- [ ] Tabla `contracts` creada en Supabase con trigger de activación (`[MET-05]`)
- [ ] Contrato v1.0 publicado en S3 y registrado en Supabase (`[MET-06]`)
- [ ] Solo un contrato activo por `pyme_id` enforced (`[MET-07]`)
- [ ] `engine/src/contract/contract_validator.py` implementado con tests en verde
- [ ] `engine/src/contract/contract_loader.py` implementado con tests en verde
- [ ] `engine/config.yaml` sincronizado con `schema.sql` y contrato
- [ ] `docs/database/schema.sql` actualizado con DDL de tabla `contracts`
- [ ] Todos los tests pasan: `pytest engine/tests/` (Etapas 1.2 + 1.3)
- [ ] Commit atómico en `main`
- [ ] `PROJECT_index.md` y `PROJECT_handoff.md` actualizados
