# Task List — Configuración de Conexión e Infraestructura con Supabase (`f01_02`)

> **Trazabilidad:** Estas tareas implementan el plan `docs/plans/f01_02_plan.md`.
> **Fase:** 1 — Definiciones y Cimientos | **Etapa:** 1.2
> **Fecha:** 2026-03-22
>
> Actualiza este archivo marcando `[x]` cuando completes cada tarea.
> **Nunca borrar tareas completadas** — son registro histórico de la etapa.

---

## Bloque 1 — Preparación del Entorno

- [ ] `[TSK-1-01]` Verificar que `.env` contiene las 9 variables requeridas sin valores vacíos: `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_DB`, `SUPABASE_S3_ENDPOINT`, `SUPABASE_S3_ACCESS_KEY_ID`, `SUPABASE_S3_SECRET_ACCESS_KEY`, `SUPABASE_S3_REGION`, `SUPABASE_S3_BUCKET`. → `[RSK-02]`, `[MET-05]`
- [ ] `[TSK-1-02]` Crear rama de trabajo: `git checkout -b feat/etapa-1-2` desde `main`. Confirmar con `git branch`. → `CLAUDE.md §6`
- [ ] `[TSK-1-03]` Crear entorno virtual Python: `python -m venv venv`. Verificar exit code 0. Activar con `venv/Scripts/activate` (Windows) o `source venv/bin/activate` (Unix). → `[REQ-01]`
- [ ] `[TSK-1-04]` Instalar dependencia: `pip install supabase`. Verificar con `python -c "import supabase; print(supabase.__version__)"` sin error. → `[REQ-01]`, `[ARC-01]`
- [ ] `[TSK-1-05]` Crear archivos `engine/__init__.py`, `engine/src/__init__.py` y `engine/src/connectors/__init__.py` vacíos para declarar paquetes Python. → `[REQ-08]`

---

## Bloque 2 — Tests TDD (Fase Roja)

> ⚠️ **Mandato CC_00003:** Completar este bloque COMPLETO antes de escribir una sola línea de `supabase_client.py`. Los tests deben existir en rojo primero.

- [ ] `[TSK-1-06]` Crear archivos `engine/tests/__init__.py` y `engine/tests/connectors/__init__.py` vacíos. → `[REQ-09]`
- [ ] `[TSK-1-07]` Escribir en `engine/tests/connectors/test_supabase_client.py` el test `test_get_client_returns_client`: importa `get_client` de `engine.src.connectors.supabase_client` y afirma que retorna instancia de `Client`. → `[REQ-09]`, `[REQ-01]`
- [ ] `[TSK-1-08]` Escribir test `test_health_check_success`: llama `health_check(get_client())` contra Supabase real y afirma que retorna `True`. → `[REQ-09]`, `[MET-01]`
- [ ] `[TSK-1-09]` Escribir test `test_health_check_invalid_key_raises`: instancia cliente con key inválida y afirma que `health_check()` lanza excepción identificada (no retorna silenciosamente `False`). → `[REQ-09]`, `[RSK-02]`
- [ ] `[TSK-1-10]` Escribir test `test_paginate_query_respects_limit`: llama `paginate_query()` sobre `usr_ventas` y afirma que el resultado es una lista (incluso si está vacía). Si la tabla tiene más de 1.000 registros, afirmar `len(result) > 1000`. → `[REQ-09]`, `[REQ-05]`, `[RSK-01]`
- [ ] `[TSK-1-11]` Ejecutar `pytest engine/tests/connectors/ -v` y confirmar que los 4 tests fallan con `ImportError` o `ModuleNotFoundError`. Capturar output. **No continuar si algún test pasa por accidente.** → `[REQ-09]`

---

## Bloque 3 — Implementación Python Connector

> Solo escribir código para hacer pasar los tests de B2. Sin lógica extra.

- [ ] `[TSK-1-12]` Implementar `get_client()` en `engine/src/connectors/supabase_client.py`: lee `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` de variables de entorno con `os.environ` (no hardcoding), crea y retorna `supabase.create_client(url, key)`. → `[REQ-01]`, `[REQ-08]`, `[MET-05]`
- [ ] `[TSK-1-13]` Implementar `health_check(client)`: ejecuta `client.rpc('now', {}).execute()` o query equivalente. Retorna `True` si responde exitosamente. Lanza excepción con código de error `ERR_CONN_001` si falla. → `[REQ-01]`, `[MET-01]`, `CLAUDE.md §5`
- [ ] `[TSK-1-14]` Implementar `paginate_query(client, table, columns, filters)`: itera con `.from_(table).select(columns).range(offset, offset+999).order('fecha', desc=False).execute()` hasta respuesta vacía. Consolida y retorna lista completa. → `[REQ-05]`, `[RSK-01]`
- [ ] `[TSK-1-15]` Ejecutar `pytest engine/tests/connectors/ -v` y confirmar que los 4 tests pasan. Exit code 0 obligatorio. **No avanzar a B4 si algún test falla.** → `[REQ-09]`, `[MET-01]`

---

## Bloque 4 — config.yaml

- [ ] `[TSK-1-16]` Crear `engine/config.yaml` con la estructura definida en SPEC §5: sección `database.supabase.tables` (7 nombres de tabla), `database.supabase.pagination.page_size: 1000`, y sección `database.s3` (purpose y dvc_remote_name). Sin valores de credenciales. → `[REQ-06]`, `[MET-05]`
- [ ] `[TSK-1-17]` Refactorizar `supabase_client.py` si tiene strings de tabla hardcodeados: leer nombres de tabla desde `config.yaml` usando `PyYAML`. Verificar que los 4 tests siguen en verde tras el refactor. → `[MET-05]`, `CLAUDE.md §5`

---

## Bloque 5 — MCP Supabase

- [ ] `[TSK-1-18]` Instalar paquete MCP de Supabase: `npx @supabase/mcp-server-supabase` o el método de instalación que indique la documentación oficial del paquete. → `[REQ-03]`, `[ARC-04]`
- [ ] `[TSK-1-19]` Agregar bloque `mcpServers` en `.claude/settings.json` con la configuración del servidor Supabase, referenciando `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` como variables de entorno (no valores literales). → `[REQ-03]`, `[MET-05]`
- [ ] `[TSK-1-20]` Reiniciar Claude Code y ejecutar query de auditoría: `SELECT id, fecha FROM usr_ventas LIMIT 5`. Confirmar que MCP retorna resultado o array vacío sin error. Capturar output. → `[REQ-03]`, `[MET-03]`, `[RSK-04]`

---

## Bloque 6 — Dashboard Next.js

- [ ] `[TSK-1-21]` Instalar dependencia en `web/`: `npm install @supabase/supabase-js`. Verificar que aparece en `web/package.json`. → `[REQ-02]`, `[ARC-02]`
- [ ] `[TSK-1-22]` Agregar al `.env` raíz del proyecto (o crear `web/.env.local`): `NEXT_PUBLIC_SUPABASE_URL` con el mismo valor que `SUPABASE_URL`, y `NEXT_PUBLIC_SUPABASE_ANON_KEY` con el mismo valor que `SUPABASE_KEY`. → `[REQ-02]`, `SPEC §3.3`
- [ ] `[TSK-1-23]` Crear `web/lib/supabase.ts`: importa `createClient` de `@supabase/supabase-js`, lee `NEXT_PUBLIC_SUPABASE_URL` y `NEXT_PUBLIC_SUPABASE_ANON_KEY` de `process.env`, exporta instancia única como `supabaseClient`. → `[REQ-02]`, `[ARC-02]`
- [ ] `[TSK-1-24]` Validar conexión: ejecutar query de prueba a `usr_ventas` usando `supabaseClient` (desde un script Node.js o server action). Confirmar HTTP 200 o array vacío sin error 401/403. Si falla con 403 → revisar políticas RLS `[RSK-03]`. → `[REQ-02]`, `[MET-02]`

---

## Bloque 7 — Validación Final y Cierre

- [ ] `[TSK-1-25]` Ejecutar suite completa: `pytest engine/tests/connectors/ -v --tb=short`. Confirmar 4 passed, 0 failed. Guardar output como referencia. → `[MET-01]`, DoD
- [ ] `[TSK-1-26]` Verificar cero credenciales hardcodeadas: ejecutar `git grep -r "eyJ" engine/ web/ engine/config.yaml` (tokens JWT de Supabase comienzan con `eyJ`). Resultado debe ser vacío. → `[MET-05]`, `CLAUDE.md §5`
- [ ] `[TSK-1-27]` Verificar vigencia de credenciales S3: listar contenido del bucket usando las credenciales de `.env`. Confirmar acceso (vacío o con contenido es válido; error de auth → renovar). → `[REQ-06]`, `[RSK-05]`
- [ ] `[TSK-1-28]` Hacer commit atómico en `feat/etapa-1-2` con todos los archivos nuevos: `engine/src/connectors/supabase_client.py`, `engine/tests/connectors/test_supabase_client.py`, `engine/config.yaml`, `web/lib/supabase.ts`, todos los `__init__.py`. Mensaje: `feat: etapa 1.2 — conexión Supabase + S3 verificada`. → `CLAUDE.md §6`
- [ ] `[TSK-1-29]` Actualizar `PROJECT_index.md` marcando Etapa 1.2 como ✅ completada. Ejecutar `/update-index`. → `CLAUDE.md §4`

---

## Cierre de Etapa

- [ ] `[TSK-1-30]` Ejecutar `/close-stage` para generar `docs/executives/f01_02_executive.md`. **Gate obligatorio:** sin este documento no se puede iniciar Etapa 1.3. → `CLAUDE.md §1`
- [ ] `[TSK-1-31]` Mergear `feat/etapa-1-2` → `main` (gobernanza) con PR o merge directo. Confirmar que `main` está actualizado. → `CLAUDE.md §6`
- [ ] `[TSK-1-32]` Ejecutar `/session-close` para actualizar `PROJECT_handoff.md` con estado exacto al cierre: archivos modificados, próxima acción (Etapa 1.3), bloqueadores si existen. → `CLAUDE.md §1`
