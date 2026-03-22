# SPEC — Configuración de Conexión e Infraestructura con Supabase (`f01_02`)

> **Trazabilidad:** Este documento implementa los requerimientos definidos en `docs/reqs/f01_02_prd.md`.
> **Fase:** 1 — Definiciones y Cimientos | **Etapa:** 1.2
> **Estado:** Borrador — Pendiente de revisión y aprobación del usuario
> **Fecha:** 2026-03-22

---

## 1. Arquitectura Lógica

### Diagrama de Conexiones

```
┌─────────────────────────────────────────────────────────────────┐
│                        INFRAESTRUCTURA CLOUD                    │
│                                                                 │
│   ┌──────────────────────┐       ┌─────────────────────────┐   │
│   │       SUPABASE       │       │         AWS S3          │   │
│   │  (PostgreSQL + RLS)  │       │    (DVC / Modelos .pkl) │   │
│   └──────────┬───────────┘       └──────────────┬──────────┘   │
│              │                                  │               │
└──────────────┼──────────────────────────────────┼───────────────┘
               │                                  │
       ┌───────┴──────────────────────────────────┴──────┐
       │                                                  │
       │  service_role_key          S3 credentials (.env) │
       │       ↓                          ↓               │
┌──────┴──────────────┐       ┌───────────────────────┐  │
│   ENGINE PYTHON     │       │   ENGINE PYTHON        │  │
│  [ARC-01]           │       │   [ARC-03]             │  │
│  supabase_client.py │       │   (DVC — Fase 2)       │  │
└─────────────────────┘       └───────────────────────┘  │
                                                          │
       │  anon_key                                        │
       │       ↓                                          │
┌──────┴──────────────┐                                   │
│  DASHBOARD NEXT.JS  │                                   │
│  [ARC-02]           │                                   │
│  web/lib/supabase.ts│                                   │
└─────────────────────┘                                   │
                                                          │
       │  service_role_key (lectura)                      │
       │       ↓                                          │
┌──────┴──────────────┐                                   │
│  CLAUDE CODE (MCP)  │                                   │
│  [ARC-04]           │                                   │
│  .claude/settings   │                                   │
└─────────────────────┘                                   │
```

### Componentes de Arquitectura

| ID | Componente | Archivo | Credencial | Responsabilidad |
|---|---|---|---|---|
| `[ARC-01]` | Engine Python → Supabase | `engine/src/connectors/supabase_client.py` | `SUPABASE_SERVICE_ROLE_KEY` | Lectura/escritura de todas las tablas. Base para pipelines de ingesta e inferencia (Fase 2+). |
| `[ARC-02]` | Dashboard Next.js → Supabase | `web/lib/supabase.ts` | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Solo lectura, con RLS activa. Jamás expone la service role key al navegador. |
| `[ARC-03]` | Engine Python → S3 | Configurado en Fase 2 | `SUPABASE_S3_*` | Almacenamiento de modelos `.pkl` versionados con DVC. Solo documentado en esta etapa. |
| `[ARC-04]` | Claude Code MCP → Supabase | `.claude/settings.json` | `SUPABASE_SERVICE_ROLE_KEY` | Lectura de BD para auditoría durante desarrollo. Solo lectura — escritura requiere orden explícita. |

---

## 2. Especificaciones de Ingeniería de Datos

### 2.1 Control de Acceso por Credencial

| Credencial | Variable `.env` | Consumidor | Operaciones Permitidas | RLS |
|---|---|---|---|---|
| Anon Key | `SUPABASE_KEY` | Dashboard Next.js | SELECT (lectura pública) | Sí — restricciones por tabla activas |
| Service Role Key | `SUPABASE_SERVICE_ROLE_KEY` | Engine Python, MCP | SELECT + INSERT + UPDATE + DELETE | Bypassa RLS — acceso total |

> ⚠️ **Regla de Oro:** La service role key **nunca** debe enviarse al navegador ni incluirse en código de componentes client-side de Next.js. Exclusiva del servidor (Python + API routes de Next.js + MCP).

### 2.2 Política de RLS por Tabla

> RLS (Row Level Security) está habilitado en Supabase para este proyecto. La política base para todas las tablas sigue el patrón de restricción por `pyme_id`.

| Tabla | Anon Key | Service Role | Política Base |
|---|---|---|---|
| `usr_ventas` | SELECT | SELECT, INSERT, UPDATE, DELETE | Lectura libre para anon; escritura solo service role |
| `usr_produccion` | SELECT | SELECT, INSERT, UPDATE, DELETE | Ídem |
| `usr_clima` | SELECT | SELECT, INSERT, UPDATE, DELETE | Ídem |
| `usr_macro_anual` | SELECT | SELECT, INSERT, UPDATE, DELETE | Ídem |
| `usr_macro_diario` | SELECT | SELECT, INSERT, UPDATE, DELETE | Ídem |
| `usr_macro_mensual` | SELECT | SELECT, INSERT, UPDATE, DELETE | Ídem |
| `usr_publicidad` | SELECT | SELECT, INSERT, UPDATE, DELETE | Ídem |

> **Validación requerida (`[REQ-04]`, `[RSK-03]`):** Confirmar cada política ejecutando una query de lectura desde la anon key sin usar la service role key. Si retorna HTTP 200 o array vacío → RLS configurado correctamente. Si retorna 401/403 → revisar políticas en Supabase dashboard.

### 2.3 Estrategia de Paginación (`[REQ-05]`, `[RSK-01]`)

Supabase impone un límite de **1.000 registros por query**. Para cargas históricas (Fase 2+), el Engine usará paginación por rango:

| Parámetro | Valor | Descripción |
|---|---|---|
| `page_size` | `1000` | Registros por página (límite Supabase) |
| Estrategia | Range-based | `.range(offset, offset + page_size - 1)` iterando hasta respuesta vacía |
| Orden | `fecha ASC` | Garantiza consistencia en la paginación temporal |
| Implementación | Fase 2 (Etapa 2.2) | Esta etapa solo documenta la estrategia |

### 2.4 Diccionario de Columnas (`[REQ-07]`)

#### Tabla: `usr_ventas` — Histórico de Ventas (`[DAT-01]`)

| Columna | Tipo SQL | Constraint | Descripción de Negocio | Granularidad |
|---|---|---|---|---|
| `id` | `bigint` | PK, auto-identity | Identificador único del registro | — |
| `fecha` | `timestamp with time zone` | NOT NULL | Fecha y hora de la venta. Usar como índice temporal del modelo. | Diaria (registrar al cierre: 6:00 PM) |
| `unidades_vendidas` | `integer` | NOT NULL | Total de buñuelos salidos de la cafetería (pagados + bonificados). Variable objetivo del modelo de pronóstico. | Diaria |
| `unidades_pagadas` | `integer` | NOT NULL | Unidades con transacción de pago real (dinero en caja). | Diaria |
| `unidades_bonificadas` | `integer` | NOT NULL | Unidades entregadas sin pago (muestras, promociones, cortesías). | Diaria |
| `created_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de creación del registro en BD. | Automático |
| `updated_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de última modificación. Actualizado por trigger automático. | Automático |
| `pyme_id` | `text` | NOT NULL, DEFAULT '001_ABC' | Identificador de la sede/pyme. Permite escalar a múltiples cafeterías en el futuro. | Fijo por sede |

#### Tabla: `usr_produccion` — Control de Producción (`[DAT-02]`)

| Columna | Tipo SQL | Constraint | Descripción de Negocio | Granularidad |
|---|---|---|---|---|
| `id` | `bigint` | PK, auto-identity | Identificador único del registro | — |
| `fecha` | `date` | NOT NULL | Fecha de producción (sin hora). | Diaria |
| `unidades_vendidas` | `integer` | NOT NULL | Ventas reales del día (referencia para calcular sobrantes). Debe coincidir con `usr_ventas.unidades_vendidas` del mismo día. | Diaria |
| `produccion_estimada` | `integer` | NOT NULL | Cantidad de buñuelos producidos ese día antes de apertura. Insumo para calcular merma. | Diaria |
| `unidades_sobrantes` | `integer` | NOT NULL | `produccion_estimada - unidades_vendidas`. Buñuelos no vendidos al cierre = desperdicio total. | Diaria |
| `porcentaje_merma` | `numeric(5,2)` | NULL | `(unidades_sobrantes / produccion_estimada) * 100`. NULL si produccion_estimada = 0. | Diaria |
| `created_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de creación | Automático |
| `updated_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de modificación | Automático |
| `pyme_id` | `text` | NOT NULL, DEFAULT '001_ABC' | Identificador de sede | Fijo por sede |

#### Tabla: `usr_clima` — Condición Climática (`[DAT-03]`)

| Columna | Tipo SQL | Constraint | Descripción de Negocio | Granularidad |
|---|---|---|---|---|
| `id` | `bigint` | PK, auto-identity | Identificador único | — |
| `fecha` | `timestamp with time zone` | NOT NULL | Fecha y hora de la medición. | Diaria (o por jornada) |
| `estado_clima` | `text` | NOT NULL | Condición climática del día. Valores esperados: `soleado`, `nublado`, `lluvioso`, `tormenta`. Variable exógena candidata para Fase 3 — incluir solo si reduce MAPE. | Diaria |
| `created_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de creación | Automático |
| `updated_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de modificación | Automático |
| `pyme_id` | `text` | NOT NULL, DEFAULT '001_ABC' | Identificador de sede | Fijo por sede |

#### Tabla: `usr_macro_anual` — Indicadores Macroeconómicos Anuales (`[DAT-04]`)

| Columna | Tipo SQL | Constraint | Descripción de Negocio | Granularidad |
|---|---|---|---|---|
| `id` | `bigint` | PK, auto-identity | Identificador único | — |
| `fecha` | `date` | NOT NULL | Primer día del año al que aplica el dato (ej. `2025-01-01`). | Anual |
| `smmlv` | `numeric(12,2)` | NULL | Salario Mínimo Mensual Legal Vigente en COP. Proxy de poder adquisitivo. Afecta demanda según CLAUDE.md §8 (quincenas, primas). | Anual |
| `created_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de creación | Automático |
| `updated_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de modificación | Automático |
| `pyme_id` | `text` | NOT NULL, DEFAULT '001_ABC' | Identificador de sede | Fijo por sede |

#### Tabla: `usr_macro_diario` — Indicadores Macroeconómicos Diarios (`[DAT-05]`)

| Columna | Tipo SQL | Constraint | Descripción de Negocio | Granularidad |
|---|---|---|---|---|
| `id` | `bigint` | PK, auto-identity | Identificador único | — |
| `fecha` | `date` | NOT NULL | Fecha del indicador. | Diaria |
| `trm` | `numeric(10,2)` | NULL | Tasa Representativa del Mercado (USD/COP). Fuente: Banco de la República de Colombia. Variable exógena de referencia macroeconómica. | Diaria |
| `created_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de creación | Automático |
| `updated_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de modificación | Automático |
| `pyme_id` | `text` | NOT NULL, DEFAULT '001_ABC' | Identificador de sede | Fijo por sede |

#### Tabla: `usr_macro_mensual` — Indicadores Macroeconómicos Mensuales (`[DAT-06]`)

| Columna | Tipo SQL | Constraint | Descripción de Negocio | Granularidad |
|---|---|---|---|---|
| `id` | `bigint` | PK, auto-identity | Identificador único | — |
| `fecha` | `date` | NOT NULL | Primer día del mes al que aplica el dato (ej. `2025-03-01`). | Mensual |
| `inflacion_anual` | `numeric(5,2)` | NULL | Inflación anual acumulada en porcentaje. Fuente: DANE. Afecta costo de insumos y precio de venta. | Mensual |
| `desempleo` | `numeric(5,2)` | NULL | Tasa de desempleo en porcentaje. Fuente: DANE. Proxy del poder adquisitivo del consumidor. | Mensual |
| `created_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de creación | Automático |
| `updated_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de modificación | Automático |
| `pyme_id` | `text` | NOT NULL, DEFAULT '001_ABC' | Identificador de sede | Fijo por sede |

#### Tabla: `usr_publicidad` — Inversión Publicitaria (`[DAT-07]`)

| Columna | Tipo SQL | Constraint | Descripción de Negocio | Granularidad |
|---|---|---|---|---|
| `id` | `bigint` | PK, auto-identity | Identificador único | — |
| `fecha` | `date` | NOT NULL | Fecha de la inversión. | Diaria |
| `campaña` | `text` | NULL | Nombre o código de la campaña activa (ej. `PROMO_2x1_MAY`). Permite segmentar por ciclo promocional. | Diaria |
| `pauta_facebook` | `numeric(12,2)` | NULL | Inversión en pauta Facebook ese día en COP. | Diaria |
| `pauta_instagram` | `numeric(12,2)` | NULL | Inversión en pauta Instagram ese día en COP. | Diaria |
| `volantes_impresos` | `numeric(12,2)` | NULL | Costo de volantes físicos impresos ese día en COP. | Diaria |
| `total_diario` | `numeric(12,2)` | NULL | Suma de todas las inversiones del día en COP (`pauta_facebook + pauta_instagram + volantes_impresos`). Campo calculado — mantener en sync. | Diaria |
| `created_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de creación | Automático |
| `updated_at` | `timestamp with time zone` | DEFAULT now() | Timestamp de modificación | Automático |
| `pyme_id` | `text` | NOT NULL, DEFAULT '001_ABC' | Identificador de sede | Fijo por sede |

### 2.5 Configuración S3 / DVC (`[REQ-06]`, `[ARC-03]`)

| Variable `.env` | Descripción | Uso |
|---|---|---|
| `SUPABASE_S3_ENDPOINT` | URL del endpoint S3 (Supabase Storage) | Base URL para operaciones DVC |
| `SUPABASE_S3_ACCESS_KEY_ID` | Credencial de acceso S3 | Autenticación DVC |
| `SUPABASE_S3_SECRET_ACCESS_KEY` | Credencial secreta S3 | Autenticación DVC |
| `SUPABASE_S3_REGION` | Región AWS del bucket | Configuración DVC remote |
| `SUPABASE_S3_BUCKET` | Nombre del bucket | Destino de modelos `.pkl` y datasets |

> **Rol exclusivo de S3 en este proyecto:** Almacenamiento de artefactos de IA versionados con DVC. No se usa para datos transaccionales (esos van en Supabase). Los modelos `.pkl` nunca se suben a Git — solo vía DVC a S3.
> **Configuración DVC activa:** Fase 2, Etapa 2.2.

---

## 3. Diseño del Módulo / Función

### 3.1 Engine Python — `[ARC-01]`

| Función | Módulo | Input | Output | REQ |
|---|---|---|---|---|
| `get_client()` | `engine/src/connectors/supabase_client.py` | Ninguno (lee `.env`) | `supabase.Client` | `[REQ-01]`, `[REQ-08]` |
| `health_check(client)` | `engine/src/connectors/supabase_client.py` | `supabase.Client` | `bool` — True si `SELECT NOW()` responde | `[REQ-01]`, `[MET-01]` |
| `paginate_query(client, table, columns, filters)` | `engine/src/connectors/supabase_client.py` | `client`, nombre de tabla, columnas, filtros opcionales | `list[dict]` — todos los registros paginados | `[REQ-05]`, `[RSK-01]` |

> **Contrato de `paginate_query()`:** Itera internamente en bloques de 1.000 registros usando `.range(offset, offset+999)` con orden `fecha ASC`. Retorna la lista completa consolidada. El consumidor no gestiona paginación — la función la abstrae.

### 3.2 Test de Integración TDD — `[ARC-01]` (`[REQ-09]`, CC_00003)

| Test | Archivo | Qué valida | Criterio de Éxito |
|---|---|---|---|
| `test_get_client_returns_client` | `engine/tests/connectors/test_supabase_client.py` | `get_client()` retorna instancia de `supabase.Client` | `isinstance(client, Client)` → True |
| `test_health_check_success` | `engine/tests/connectors/test_supabase_client.py` | `health_check()` conecta a Supabase real y recibe timestamp | `health_check(client)` → True |
| `test_health_check_invalid_key_raises` | `engine/tests/connectors/test_supabase_client.py` | Credencial inválida lanza excepción controlada | Raise de excepción identificada (no silencio) |
| `test_paginate_query_respects_limit` | `engine/tests/connectors/test_supabase_client.py` | `paginate_query()` no trunca al llegar a 1.000 registros | Resultado > 1.000 si la tabla tiene más datos |

> **Orden TDD obligatorio (CC_00003):** Primero se escribe `test_supabase_client.py` (todos los tests en rojo). Luego se implementa `supabase_client.py` hasta que todos pasen (verde). Ninguna función se considera lista hasta que su test pase.

### 3.3 Dashboard Next.js — `[ARC-02]` (`[REQ-02]`)

| Elemento | Archivo | Descripción |
|---|---|---|
| Cliente Supabase | `web/lib/supabase.ts` | `createClient(url, anonKey)` con variables de entorno públicas (`NEXT_PUBLIC_*`). Instancia única exportada para uso en componentes y server actions. |
| Variables de entorno | `.env.local` (Next.js) | `NEXT_PUBLIC_SUPABASE_URL` y `NEXT_PUBLIC_SUPABASE_ANON_KEY`. Prefijo `NEXT_PUBLIC_` requerido para acceso client-side. |

> **Decisión de Variables Next.js:** El `.env` del proyecto usa `SUPABASE_URL` y `SUPABASE_KEY`. Next.js requiere el prefijo `NEXT_PUBLIC_` para exponer variables al navegador. Se agregan las dos variables `NEXT_PUBLIC_*` al `.env` (o `.env.local`) con los mismos valores. No se duplican secrets — solo la anon key (segura para exponer).

### 3.4 MCP Supabase — `[ARC-04]` (`[REQ-03]`)

| Parámetro | Valor | Descripción |
|---|---|---|
| Servidor MCP | `@supabase/mcp-server-supabase` | Paquete oficial de Supabase para MCP |
| Archivo de config | `.claude/settings.json` | Sección `mcpServers` |
| Credencial | `SUPABASE_SERVICE_ROLE_KEY` | Acceso completo de lectura (bypassa RLS) |
| Modo | Solo lectura durante desarrollo | Escritura requiere orden explícita del usuario (CLAUDE.md §1) |
| Validación | Query a `usr_ventas` desde Claude Code | Agente confirma que MCP responde correctamente |

---

## 4. Contratos de Datos entre Componentes

| Origen | Destino | Protocolo | Credencial | Restricción |
|---|---|---|---|---|
| `engine/src/connectors/supabase_client.py` | Supabase | HTTPS / REST API | `SUPABASE_SERVICE_ROLE_KEY` | Sin límite de filas por credencial; la paginación es de negocio |
| `web/lib/supabase.ts` | Supabase | HTTPS / REST API | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | RLS activa — solo lectura de filas permitidas |
| `.claude/settings.json` (MCP) | Supabase | HTTPS / MCP Protocol | `SUPABASE_SERVICE_ROLE_KEY` | Solo lectura por convención; no INSERT/UPDATE desde MCP |
| Engine Python | S3 (DVC) | HTTPS / S3 Protocol | `SUPABASE_S3_*` | Solo modelos `.pkl` y datasets versionados |

### Rotación de Credenciales (`[RSK-02]`)

Si una credencial expira o es revocada:
1. Generar nueva clave en el dashboard de Supabase.
2. Actualizar el valor en `.env` localmente.
3. Actualizar el secret correspondiente en GitHub (para CI Quality Gate — Etapa 2.1).
4. Reiniciar el servidor MCP en Claude Code.
5. Verificar con `health_check()` que la nueva clave funciona.

---

## 5. Configuración (`engine/config.yaml`)

> **Nota:** `engine/config.yaml` se crea en esta etapa como base de configuración del Engine. Toda ruta a tabla o parámetro estructural vive aquí — nunca hardcodeado en código.

```yaml
# engine/config.yaml
# Configuración global del Engine — Demo_Bunuelos
# Secretos en .env. Este archivo es seguro para Git.

database:
  supabase:
    pagination:
      page_size: 1000        # Límite Supabase por query. No modificar sin revisar RSK-01.
    tables:
      ventas:       usr_ventas
      produccion:   usr_produccion
      clima:        usr_clima
      macro_anual:  usr_macro_anual
      macro_diario: usr_macro_diario
      macro_mensual: usr_macro_mensual
      publicidad:   usr_publicidad

  s3:
    # Valores reales en .env (SUPABASE_S3_*)
    # Este bloque documenta las claves esperadas en config — sin valores sensibles.
    purpose: dvc_model_storage   # Exclusivo para modelos .pkl versionados con DVC
    dvc_remote_name: s3_models   # Nombre del remote DVC a configurar en Fase 2
```

---

## 6. Matriz de Diseño vs PRD

| REQ | Componente que lo implementa | Archivo | Notas |
|---|---|---|---|
| `[REQ-01]` | `get_client()` + `health_check()` | `engine/src/connectors/supabase_client.py` | Valida con `SELECT NOW()` contra Supabase real |
| `[REQ-02]` | `createClient()` con anon key | `web/lib/supabase.ts` | Requiere variables `NEXT_PUBLIC_*` en `.env` |
| `[REQ-03]` | Configuración MCP | `.claude/settings.json` | Paquete `@supabase/mcp-server-supabase` |
| `[REQ-04]` | Tabla de políticas RLS | §2.2 de este documento | Validación requerida con query desde anon key |
| `[REQ-05]` | `paginate_query()` | `engine/src/connectors/supabase_client.py` | Implementa range-based pagination; uso en Fase 2 |
| `[REQ-06]` | Tabla de configuración S3 | §2.5 de este documento + `config.yaml` | DVC activo en Fase 2 |
| `[REQ-07]` | Diccionario de columnas | §2.4 de este documento | 7 tablas × todas las columnas documentadas |
| `[REQ-08]` | Estructura de carpetas | `engine/src/connectors/` | Solo esta subcarpeta en F01_E02 |
| `[REQ-09]` | Tests de integración TDD | `engine/tests/connectors/test_supabase_client.py` | 4 tests escritos antes del código (CC_00003) |

---

> **Control de Cambio:** Este documento fue creado durante la Etapa 1.2. Los tags `[ARC-01]` a `[ARC-04]` son nuevos en esta SPEC — no existían en el PRD.
