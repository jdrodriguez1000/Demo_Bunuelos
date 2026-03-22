# Plan de Implementación — Configuración de Conexión e Infraestructura con Supabase (`f01_02`)

> **Trazabilidad:** Este plan ejecuta los requerimientos de `docs/reqs/f01_02_prd.md` según el diseño de `docs/specs/f01_02_spec.md`.
> **Fase:** 1 — Definiciones y Cimientos | **Etapa:** 1.2
> **Estado:** Borrador — Pendiente de revisión y aprobación del usuario
> **Fecha:** 2026-03-22

---

## 1. Resumen del Plan

Establecer y verificar todas las conexiones cloud del proyecto (Supabase + S3 + MCP) antes de que comience cualquier ingesta de datos. La estrategia es **TDD-first**: los tests de integración Python se escriben y fallan antes de que exista el código de conexión. Solo cuando los tests pasan se avanza al siguiente bloque.

El orden de los bloques respeta dos principios:
1. **Prerequisito primero:** entorno listo antes de escribir código.
2. **TDD obligatorio (CC_00003):** tests antes que implementación, siempre.

---

## 2. Ruta Crítica

```
B1 (Entorno) → B2 (Tests TDD en rojo) → B3 (Implementación Python)
             → B4 (config.yaml)
             → B5 (MCP Supabase)      ← paralelo con B6
             → B6 (Next.js cliente)   ← paralelo con B5
             → B7 (Validación y cierre)
```

| Paso | Bloque | Depende de | Puede paralelizarse con |
|---|---|---|---|
| 1 | B1 — Preparación del entorno | Ninguno | — |
| 2 | B2 — Tests TDD (rojo) | B1 | — |
| 3 | B3 — Implementación Python | B2 | — |
| 4 | B4 — config.yaml | B3 | — |
| 5 | B5 — MCP Supabase | B1 | B6 |
| 6 | B6 — Next.js cliente | B1 | B5 |
| 7 | B7 — Validación y cierre | B3, B4, B5, B6 | — |

> **Nota:** B5 y B6 dependen solo de B1 (credenciales verificadas). Pueden ejecutarse en paralelo mientras B3 y B4 avanzan, optimizando el tiempo de la etapa.

---

## 3. Backlog de Trabajo (WBS)

### B1 — Preparación del Entorno

| Ítem | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B1.1 | Verificar que `.env` contiene todas las variables requeridas: `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_DB`, `SUPABASE_S3_*` (9 variables). Ninguna vacía. | `[RSK-02]`, `[MET-05]` | Checklist de variables confirmado |
| B1.2 | Crear rama de trabajo: `git checkout -b feat/etapa-1-2` desde `main`. | `CLAUDE.md §6` | Rama `feat/etapa-1-2` activa |
| B1.3 | Crear y activar entorno virtual Python: `python -m venv venv`. Verificar exit code 0. | `[REQ-01]`, `[ARC-01]` | `venv/` creado y activo |
| B1.4 | Instalar dependencia Python: `supabase-py`. Verificar versión instalada. | `[REQ-01]` | `supabase` importable sin error |
| B1.5 | Crear `engine/src/__init__.py` y `engine/src/connectors/__init__.py` vacíos para declarar los módulos como paquetes Python. | `[REQ-08]` | Estructura de carpetas lista |

### B2 — Tests TDD (Fase Roja)

> **Mandato CC_00003:** Este bloque PRECEDE al B3. Los tests deben existir y fallar antes de que `supabase_client.py` tenga implementación.

| Ítem | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B2.1 | Crear `engine/tests/__init__.py` y `engine/tests/connectors/__init__.py` vacíos. | `[REQ-09]` | Estructura de tests lista |
| B2.2 | Escribir `test_get_client_returns_client`: verifica que `get_client()` retorna instancia de `Client`. Debe fallar (función no existe aún). | `[REQ-09]`, `[REQ-01]` | Test en rojo confirmado |
| B2.3 | Escribir `test_health_check_success`: verifica que `health_check(client)` conecta a Supabase real y retorna `True`. Debe fallar. | `[REQ-09]`, `[MET-01]` | Test en rojo confirmado |
| B2.4 | Escribir `test_health_check_invalid_key_raises`: verifica que una credencial inválida lanza excepción identificada (no silencio). Debe fallar. | `[REQ-09]`, `[RSK-02]` | Test en rojo confirmado |
| B2.5 | Escribir `test_paginate_query_respects_limit`: verifica que `paginate_query()` no trunca al superar 1.000 registros. Debe fallar. | `[REQ-09]`, `[REQ-05]`, `[RSK-01]` | Test en rojo confirmado |
| B2.6 | Ejecutar `pytest engine/tests/connectors/` y confirmar que los 4 tests fallan por `ImportError` o `AttributeError`. Capturar output. | `[REQ-09]` | Screenshot / log de tests en rojo |

### B3 — Implementación Python Connector

> Solo se escribe código para hacer pasar los tests de B2. Nada más.

| Ítem | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B3.1 | Implementar `get_client()`: crea y retorna `supabase.Client` leyendo `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` de variables de entorno. Cero hardcoding. | `[REQ-01]`, `[REQ-08]`, `[MET-05]` | `get_client()` implementado |
| B3.2 | Implementar `health_check(client)`: ejecuta `SELECT NOW()` vía Supabase RPC. Retorna `True` si responde, lanza excepción identificada si falla. | `[REQ-01]`, `[MET-01]` | `health_check()` implementado |
| B3.3 | Implementar `paginate_query(client, table, columns, filters)`: itera con `.range(offset, offset+999)` en orden `fecha ASC` hasta respuesta vacía. Retorna lista consolidada. | `[REQ-05]`, `[RSK-01]` | `paginate_query()` implementado |
| B3.4 | Ejecutar `pytest engine/tests/connectors/` y confirmar que los 4 tests pasan (verde). Exit code 0 obligatorio para continuar. | `[REQ-09]`, `[MET-01]` | Suite completa en verde |

### B4 — config.yaml

| Ítem | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B4.1 | Crear `engine/config.yaml` con la estructura definida en SPEC §5: sección `database.supabase` (tabla names, page_size) y sección `database.s3` (purpose, dvc_remote_name). Sin valores sensibles. | `[REQ-06]`, `[MET-05]`, `CLAUDE.md §5` | `engine/config.yaml` creado |
| B4.2 | Verificar que `supabase_client.py` lee los nombres de tabla desde `config.yaml` (no hardcodeados). Si no, refactorizar. | `[MET-05]`, `CLAUDE.md §5` | Cero strings de tabla en código Python |

### B5 — MCP Supabase (Claude Code)

| Ítem | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B5.1 | Instalar el paquete MCP de Supabase: `@supabase/mcp-server-supabase`. | `[REQ-03]`, `[ARC-04]` | Paquete instalado |
| B5.2 | Agregar la configuración `mcpServers` en `.claude/settings.json` con `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` como variables de entorno (no hardcodeadas). | `[REQ-03]`, `[MET-05]` | MCP configurado en settings.json |
| B5.3 | Reiniciar Claude Code y ejecutar query de auditoría sobre `usr_ventas` para confirmar que MCP responde. Capturar resultado. | `[REQ-03]`, `[MET-03]`, `[RSK-04]` | Query exitosa desde MCP |

### B6 — Dashboard Next.js

| Ítem | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B6.1 | Instalar dependencia: `@supabase/supabase-js` en `web/`. | `[REQ-02]`, `[ARC-02]` | Paquete en `web/package.json` |
| B6.2 | Agregar `NEXT_PUBLIC_SUPABASE_URL` y `NEXT_PUBLIC_SUPABASE_ANON_KEY` al `.env` con los mismos valores que `SUPABASE_URL` y `SUPABASE_KEY`. | `[REQ-02]`, `SPEC §3.3` | Variables `NEXT_PUBLIC_*` en `.env` |
| B6.3 | Crear `web/lib/supabase.ts` con `createClient(url, anonKey)` exportando instancia única. | `[REQ-02]`, `[ARC-02]` | `web/lib/supabase.ts` creado |
| B6.4 | Validar conexión: ejecutar query a `usr_ventas` desde Next.js (server action o script de validación). Verificar HTTP 200 sin error 401/403. | `[REQ-02]`, `[MET-02]`, `[RSK-03]` | Query exitosa con anon key |

### B7 — Validación Final y Cierre

| Ítem | Descripción | REQ / ARC | Entregable |
|---|---|---|---|
| B7.1 | Ejecutar suite completa: `pytest engine/tests/connectors/ -v`. Los 4 tests deben pasar. | `[MET-01]`, DoD | Output pytest con 4 passed |
| B7.2 | Confirmar cero credenciales hardcodeadas: inspeccionar archivos trackeados por Git. Ningún secret en código. | `[MET-05]`, `CLAUDE.md §5` | Git grep sin matches de secrets |
| B7.3 | Verificar ping a S3: listar contenido del bucket para confirmar que las credenciales S3 están vigentes. | `[REQ-06]`, `[RSK-05]` | Bucket accesible (vacío o con contenido) |
| B7.4 | Crear commit atómico en `feat/etapa-1-2` con todos los archivos de la etapa. | `CLAUDE.md §6` | Commit en rama feature |
| B7.5 | Actualizar `PROJECT_index.md` marcando Etapa 1.2 como completada. | `CLAUDE.md §4` | Hito ✅ en PROJECT_index.md |

---

## 4. Estrategia de Pruebas

| Tipo | Qué se prueba | Archivo de test | Criterio de éxito |
|---|---|---|---|
| Integration | `get_client()` retorna instancia válida | `engine/tests/connectors/test_supabase_client.py` | `isinstance(client, Client)` → True |
| Integration | `health_check()` conecta a Supabase real | `engine/tests/connectors/test_supabase_client.py` | `SELECT NOW()` responde; retorna True |
| Integration | Credencial inválida lanza excepción | `engine/tests/connectors/test_supabase_client.py` | Raise de excepción — no silencio |
| Integration | `paginate_query()` no trunca en 1.000+ filas | `engine/tests/connectors/test_supabase_client.py` | Resultado completo sin corte |
| Manual | Conexión Next.js con anon key | Validación en B6.4 | HTTP 200, sin 401/403 |
| Manual | MCP Supabase responde queries | Validación en B5.3 | Query desde Claude Code exitosa |

> **Prohibición CC_00003:** Los tests de integración Python prueban contra Supabase real. Ningún mock del cliente Supabase es aceptable en `engine/tests/connectors/`. Un mock que pasa no garantiza que las credenciales funcionen.

---

## 5. Definición de "Hecho" (DoD)

- [ ] `pytest engine/tests/connectors/ -v` → 4 tests passed, 0 failed, exit code 0
- [ ] `health_check()` retorna `True` contra Supabase real en producción
- [ ] Query Next.js desde anon key → HTTP 200 sin error de RLS
- [ ] MCP Supabase responde query de auditoría desde Claude Code
- [ ] `engine/config.yaml` creado con tabla names y page_size sin hardcoding
- [ ] `git grep` sin matches de secrets en archivos trackeados
- [ ] Ping S3 exitoso (bucket accesible)
- [ ] Commit atómico en `feat/etapa-1-2` con todos los entregables
- [ ] `PROJECT_index.md` actualizado con Etapa 1.2 ✅
- [ ] `/close-stage` ejecutado generando `docs/executives/f01_02_executive.md`
