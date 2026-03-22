# Task List — Configuración de Conexión e Infraestructura con Supabase (`f01_02`)

> **Trazabilidad:** Estas tareas implementan el plan `docs/plans/f01_02_plan.md`.
> **Fase:** 1 — Definiciones y Cimientos | **Etapa:** 1.2
> **Fecha:** 2026-03-22
>
> Actualiza este archivo marcando `[x]` cuando completes cada tarea.
> **Nunca borrar tareas completadas** — son registro histórico de la etapa.
>
> **Reordenamiento (2026-03-22):** MCP Supabase movido de B5 a B1 — el agente necesita acceso a la BD desde el inicio del desarrollo, no al final.

---

## Bloque 1 — Preparación del Entorno + MCP Supabase

- [x] `[TSK-1-01]` Verificar que `.env` contiene las 9 variables requeridas sin valores vacíos: `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_DB`, `SUPABASE_S3_ENDPOINT`, `SUPABASE_S3_ACCESS_KEY_ID`, `SUPABASE_S3_SECRET_ACCESS_KEY`, `SUPABASE_S3_REGION`, `SUPABASE_S3_BUCKET`. → `[RSK-02]`, `[MET-05]`
- [x] `[TSK-1-02]` Crear rama de trabajo: `git checkout -b feat/etapa-1-2` desde `main`. Confirmar con `git branch`. → `CLAUDE.md §6`
- [x] `[TSK-1-03]` Crear entorno virtual Python: `python -m venv venv`. Verificar exit code 0. Activar con `venv/Scripts/activate` (Windows) o `source venv/bin/activate` (Unix). → `[REQ-01]`
- [x] `[TSK-1-04]` Instalar dependencia: `pip install supabase`. Verificar con `python -c "import supabase; print(supabase.__version__)"` sin error. → `[REQ-01]`, `[ARC-01]`
- [x] `[TSK-1-05]` Crear archivos `engine/__init__.py`, `engine/src/__init__.py` y `engine/src/connectors/__init__.py` vacíos para declarar paquetes Python. → `[REQ-08]`
- [x] `[TSK-1-06]` Instalar paquete MCP de Supabase siguiendo documentación oficial del paquete `@supabase/mcp-server-supabase`. → `[REQ-03]`, `[ARC-04]`
- [x] `[TSK-1-07]` Agregar bloque `mcpServers` en `.mcp.json` (local, gitignoreado) con token PAT y project-ref. Implementación difiere del spec (usa `.mcp.json` en vez de `settings.json`) — misma seguridad, más confiable en Windows. → `[REQ-03]`, `[MET-05]`
- [x] `[TSK-1-08]` Reiniciar Claude Code y ejecutar query de auditoría: `SELECT NOW()`. MCP retornó `2026-03-22 18:12:17 UTC` sin error. **El agente ya puede usar MCP para el resto de la etapa.** → `[REQ-03]`, `[MET-03]`, `[RSK-04]`

---

## Bloque 2 — Tests TDD (Fase Roja)

> ⚠️ **Mandato CC_00003:** Completar este bloque COMPLETO antes de escribir una sola línea de `supabase_client.py`. Los tests deben existir en rojo primero.

- [x] `[TSK-1-09]` Crear archivos `engine/tests/__init__.py` y `engine/tests/connectors/__init__.py` vacíos. → `[REQ-09]`
- [x] `[TSK-1-10]` Escribir en `engine/tests/connectors/test_supabase_client.py` el test `test_get_client_returns_client`: importa `get_client` de `engine.src.connectors.supabase_client` y afirma que retorna instancia de `Client`. → `[REQ-09]`, `[REQ-01]`
- [x] `[TSK-1-11]` Escribir test `test_health_check_success`: llama `health_check(get_client())` contra Supabase real y afirma que retorna `True`. → `[REQ-09]`, `[MET-01]`
- [x] `[TSK-1-12]` Escribir test `test_health_check_invalid_key_raises`: instancia cliente con key inválida y afirma que `health_check()` lanza excepción identificada (no retorna silenciosamente `False`). → `[REQ-09]`, `[RSK-02]`
- [x] `[TSK-1-13]` Escribir test `test_paginate_query_respects_limit`: llama `paginate_query()` sobre `usr_ventas` y afirma que el resultado es una lista (incluso si está vacía). Si la tabla tiene más de 1.000 registros, afirmar `len(result) > 1000`. → `[REQ-09]`, `[REQ-05]`, `[RSK-01]`
- [x] `[TSK-1-14]` Ejecutar `pytest engine/tests/connectors/ -v` y confirmar que los 4 tests fallan con `ImportError` o `ModuleNotFoundError`. Capturar output. **No continuar si algún test pasa por accidente.** → `[REQ-09]`

---

## Bloque 3 — Implementación Python Connector

> Solo escribir código para hacer pasar los tests de B2. Sin lógica extra.

- [x] `[TSK-1-15]` Implementar `get_client()` en `engine/src/connectors/supabase_client.py`: lee `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` de variables de entorno con `os.environ` (no hardcoding), crea y retorna `supabase.create_client(url, key)`. → `[REQ-01]`, `[REQ-08]`, `[MET-05]`
- [x] `[TSK-1-16]` Implementar `health_check(client)`: ejecuta query de validación contra Supabase real. Retorna `True` si responde exitosamente. Lanza excepción con código `ERR_CONN_001` si falla. → `[REQ-01]`, `[MET-01]`, `CLAUDE.md §5`
- [x] `[TSK-1-17]` Implementar `paginate_query(client, table, columns, filters)`: itera con `.range(offset, offset+999)` en orden `fecha ASC` hasta respuesta vacía. Consolida y retorna lista completa. → `[REQ-05]`, `[RSK-01]`
- [x] `[TSK-1-18]` Ejecutar `pytest engine/tests/connectors/ -v` y confirmar que los 4 tests pasan. Exit code 0 obligatorio. **No avanzar a B4 si algún test falla.** → `[REQ-09]`, `[MET-01]`

---

## Bloque 4 — config.yaml

- [x] `[TSK-1-19]` Crear `engine/config.yaml` con la estructura definida en SPEC §5: sección `database.supabase.tables` (7 nombres de tabla), `database.supabase.pagination.page_size: 1000`, y sección `database.s3` (purpose y dvc_remote_name). Sin valores de credenciales. → `[REQ-06]`, `[MET-05]`
- [x] `[TSK-1-20]` Refactorizar `supabase_client.py` si tiene strings de tabla hardcodeados: leer nombres de tabla desde `config.yaml` usando `PyYAML`. Verificar que los 4 tests siguen en verde tras el refactor. → `[MET-05]`, `CLAUDE.md §5`

---

## Bloque 5 — Dashboard Next.js

> **[DIFERIDO — 2026-03-22]** El proyecto `web/` no existe aún. Scaffoldear Next.js en esta etapa crearía ~100 archivos sin valor verificable hasta que exista una pantalla real que consuma datos. Estas tareas se retoman en la primera etapa que produzca componentes de dashboard.

- [DIFERIDO] `[TSK-1-21]` Instalar dependencia en `web/`: `npm install @supabase/supabase-js`. Verificar que aparece en `web/package.json`. → `[REQ-02]`, `[ARC-02]`
- [DIFERIDO] `[TSK-1-22]` Agregar al `.env` raíz del proyecto (o crear `web/.env.local`): `NEXT_PUBLIC_SUPABASE_URL` con el mismo valor que `SUPABASE_URL`, y `NEXT_PUBLIC_SUPABASE_ANON_KEY` con el mismo valor que `SUPABASE_KEY`. → `[REQ-02]`, `SPEC §3.3`
- [DIFERIDO] `[TSK-1-23]` Crear `web/lib/supabase.ts`: importa `createClient` de `@supabase/supabase-js`, lee `NEXT_PUBLIC_SUPABASE_URL` y `NEXT_PUBLIC_SUPABASE_ANON_KEY` de `process.env`, exporta instancia única como `supabaseClient`. → `[REQ-02]`, `[ARC-02]`
- [DIFERIDO] `[TSK-1-24]` Validar conexión: ejecutar query de prueba a `usr_ventas` usando `supabaseClient`. Confirmar HTTP 200 o array vacío sin error 401/403. Si falla con 403 → revisar políticas RLS `[RSK-03]`. → `[REQ-02]`, `[MET-02]`

---

## Bloque 6 — Validación Final y Cierre

- [x] `[TSK-1-25]` Ejecutar suite completa: `pytest engine/tests/connectors/ -v --tb=short`. Confirmar 4 passed, 0 failed. Guardar output como referencia. → `[MET-01]`, DoD
- [x] `[TSK-1-26]` Verificar cero credenciales hardcodeadas: ejecutar `git grep -r "eyJ" engine/ engine/config.yaml`. Resultado vacío confirmado. → `[MET-05]`, `CLAUDE.md §5`
- [x] `[TSK-1-27]` Verificar vigencia de credenciales S3: bucket accesible, 0 objetos (correcto en esta etapa). → `[REQ-06]`, `[RSK-05]`
- [x] `[TSK-1-28]` Commit atómico en `feat/etapa-1-2`: 12 archivos, mensaje `feat: etapa 1.2 — conexión Supabase + S3 verificada`. → `CLAUDE.md §6`
- [x] `[TSK-1-29]` `PROJECT_index.md` actualizado al cierre de etapa via `/update-index`. → `CLAUDE.md §4`

---

## Cierre de Etapa

- [x] `[TSK-1-30]` `/close-stage` ejecutado — `docs/executives/f01_02_executive.md` generado. Gate de avance a Etapa 1.3 desbloqueado. → `CLAUDE.md §1`
- [x] `[TSK-1-31]` `feat/etapa-1-2` mergeado a `main` — 12 archivos integrados, `main` actualizado. → `CLAUDE.md §6`
- [x] `[TSK-1-32]` `/session-close` ejecutado — `PROJECT_handoff.md` y `lessons-learned.md` actualizados. → `CLAUDE.md §1`
