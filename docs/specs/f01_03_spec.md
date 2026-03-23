# SPEC — Definición del Data Contract (`f01_03`)

> **Trazabilidad:** Este documento implementa los requerimientos definidos en `docs/reqs/f01_03_prd.md`.
> **Fase:** 1 — Definiciones y Cimientos
> **Etapa:** 1.3 — Definición del Data Contract (esquemas, tipos de datos, constraints)
> **Estado:** ✅ Aprobado
> **Fecha:** 2026-03-23

---

## 1. Arquitectura Lógica

### 1.1 Flujo General del Data Contract

```
┌─────────────────────────────────────────────────────────────┐
│                   CREACIÓN (Etapa 1.3)                      │
│                                                             │
│  Desarrollador                                              │
│       │                                                     │
│       ▼                                                     │
│  contracts/data_contract.yaml  ──── Git commit ────┐        │
│       │                                            │        │
│       ▼                                            ▼        │
│  Calcular SHA256 checksum               Repositorio Git     │
│       │                                 (gobernanza)        │
│       ▼                                                     │
│  ┌─────────┐    s3_location    ┌──────────────────┐         │
│  │   S3    │◄──────────────────│   Supabase       │         │
│  │ (DVC)   │   + checksum      │  tabla contracts │         │
│  │         │                   │  is_active=true  │         │
│  └────┬────┘                   └────────┬─────────┘         │
│       │                                 │                   │
└───────┼─────────────────────────────────┼───────────────────┘
        │                                 │
        │         STARTUP (Etapa 2.1+)    │
        │                                 │
        │    ┌────────────────────────┐   │
        │    │     Engine Python      │   │
        │    │                        │   │
        │    │  1. Query Supabase ────┼───┘
        │    │     → s3_location      │
        │    │                        │
        └────┼──2. Download from S3   │
             │                        │
             │  3. Verify checksum    │
             │                        │
             │  4. Parse YAML         │
             │                        │
             │  5. Load in memory     │
             │     → Contract object  │
             │                        │
             │  Si falla cualquier    │
             │  paso → FATAL ERROR    │
             │  Sistema NO inicia     │
             └────────────────────────┘
```

### 1.2 Componentes de Arquitectura

| ID | Componente | Responsabilidad | Archivo / Ubicación |
|---|---|---|---|
| `[ARC-01]` | Archivo de contrato | Artefacto YAML máquina-legible con la definición estructural completa | `contracts/data_contract.yaml` |
| `[ARC-02]` | Tabla `contracts` (Supabase) | Metadatos, auditoría, referencia a S3, constraint de un solo contrato activo | Supabase — `public.contracts` |
| `[ARC-03]` | Almacenamiento S3 (DVC) | Persistencia del artefacto YAML versionado, descargable por el Engine | `s3://bucket/contracts/data_contract_v[X.Y].yaml` |
| `[ARC-04]` | Contract Loader | Descarga contrato activo desde S3, verifica checksum, parsea YAML | `engine/src/contract/contract_loader.py` |
| `[ARC-05]` | Contract Validator | Valida que el YAML tenga la estructura esperada (secciones obligatorias, arrays de tablas) | `engine/src/contract/contract_validator.py` |
| `[ARC-06]` | Flujo de publicación | Proceso manual: crear YAML → calcular checksum → subir S3 → registrar en Supabase | Manual (Etapa 1.3) / CI/CD (Etapa 2.1) |

---

## 2. Especificaciones de Ingeniería de Datos

### 2.1 Esquema YAML del Data Contract (`[ARC-01]`)

Estructura exacta del archivo `contracts/data_contract.yaml`. Cada sección es **obligatoria** salvo que se indique lo contrario.

```yaml
# ============================================================
# SECCIÓN 1: metadata (obligatoria)
# Implementa: [REQ-01], [REQ-06], [REQ-10]
# ============================================================
metadata:
  contract_id: string       # Identificador único del contrato (ej: "contract_cafeteria_sas")
  version: string            # Versión semántica (ej: "1.0", "1.1", "2.0")
  created_at: string         # ISO 8601 (ej: "2026-03-23T00:00:00Z")
  updated_at: string         # ISO 8601 — fecha del último cambio
  updated_by: string         # Autor del cambio (ej: "usuario@email.com" o "AI Agent")
  client_name: string        # Nombre del cliente (ej: "Cafetería SAS")
  pyme_id: string            # Identificador de cliente para multi-tenant (ej: "001_ABC")
  status: string             # Enum: "active" | "deprecated" | "draft"

# ============================================================
# SECCIÓN 2: objective_variable (obligatoria)
# Implementa: [REQ-04], [REQ-05]
# ============================================================
objective_variable:
  name: string               # "demanda_teorica"
  type: string               # "calculated"
  description: string        # Descripción en lenguaje natural

  calculation:
    version: string          # Versión de la fórmula (ej: "1.0")

    rule_1_with_surplus:
      condition: string      # "unidades_sobrantes > 0"
      meaning: string        # Explicación de negocio
      formula: string        # "demanda_teorica = unidades_vendidas"

    rule_2_without_surplus:
      condition: string      # "unidades_sobrantes = 0"
      meaning: string        # Explicación de negocio

      algorithm:             # Pasos secuenciales del cálculo
        step_1: string       # Extraer hora_ultima_venta
        step_2: string       # Buscar días similares
        step_3: string       # Calcular demanda no satisfecha
        step_4: string       # Sumar a unidades vendidas

      parameters:
        similar_days_criteria: string   # "same_weekday"
        exclude_holidays: boolean       # true
        lookback_days: integer          # 90
        minimum_similar_days: integer   # 1
        fallback: string               # Comportamiento si no hay días similares

      warm_up_period:
        days_until_reliable: integer    # 90
        note: string                   # Nota sobre confiabilidad inicial

  depends_on:                # Array de dependencias (tablas + columnas críticas)
    - table: string
      columns: [string]
      reason: string

# ============================================================
# SECCIÓN 3: mandatory_tables (obligatoria, array extensible)
# Implementa: [REQ-02], [REQ-03]
# ============================================================
mandatory_tables:            # Array — mínimo 1 entrada, extensible a N
  - table_name: string       # Nombre exacto en Supabase
    status: string           # Siempre "mandatory"
    reason: string           # Por qué es mandatoria
    description: string      # Propósito de negocio
    grain: string            # Granularidad temporal (ej: "per transaction", "daily")
    update_frequency: string # Frecuencia de actualización del cliente
    owner: string            # Responsable de los datos

    columns:                 # Array de columnas — extensible
      - name: string         # Nombre exacto de la columna
        type: string         # Tipo PostgreSQL exacto (ej: "timestamp with time zone")
        nullable: boolean    # true | false
        default: string|null # Valor default o null si no tiene
        description: string  # Propósito de la columna

# ============================================================
# SECCIÓN 4: optional_tables (obligatoria, array extensible)
# Implementa: [REQ-02], [REQ-03]
# ============================================================
optional_tables:             # Array — puede estar vacío, extensible a N
  - table_name: string       # Misma estructura que mandatory_tables
    status: string           # Siempre "optional"
    reason: string
    description: string
    columns:
      - name: string
        type: string
        nullable: boolean
        default: string|null
        description: string

# ============================================================
# SECCIÓN 5: changelog (obligatoria)
# Implementa: [REQ-10]
# ============================================================
changelog:                   # Array de entradas de cambio
  - version: string          # Versión del contrato
    date: string             # Fecha ISO 8601
    created_by: string       # Autor
    description: string      # Resumen del cambio
    changes:                 # Array de cambios específicos
      - string
```

### 2.2 Diccionario de Columnas — Tablas Mandatorias

#### Tabla: `usr_ventas` (`[DAT-01]`)

> **Rol:** Input principal para `demanda_teorica`. Contiene `unidades_vendidas` y timestamp con hora.
> **Granularidad:** Por transacción (con hora exacta).
> **Actualización:** Diaria, antes de 6:00 PM.
> **Owner:** Cafetería SAS (Punto de Venta).

| Columna | Tipo PostgreSQL | Nullable | Default | Descripción |
|---|---|---|---|---|
| `id` | `bigint` | `false` | `generated by default as identity` | Identificador único (PK) |
| `fecha` | `timestamp with time zone` | `false` | — | Fecha y hora de la venta. **CRÍTICO:** la hora permite extraer `hora_ultima_venta` para Regla 2 de `demanda_teorica`. Formato esperado: `2021-10-01 07:00:00+00` |
| `unidades_vendidas` | `integer` | `false` | — | Unidades vendidas en esta transacción. Input directo de ambas reglas de `demanda_teorica` |
| `unidades_pagadas` | `integer` | `false` | — | Unidades pagadas por el cliente (excluye bonificadas) |
| `unidades_bonificadas` | `integer` | `false` | — | Unidades entregadas sin cobro (promociones 2x1, cortesías) |
| `created_at` | `timestamp with time zone` | `true` | `now()` | Auditoría de sistema: timestamp de creación del registro |
| `updated_at` | `timestamp with time zone` | `true` | `now()` | Auditoría de sistema: timestamp de última actualización |
| `pyme_id` | `text` | `false` | `'001_ABC'` | Identificador del cliente. Habilita multi-tenant |

**Constraint:** `usr_ventas_pkey PRIMARY KEY (id)`
**Trigger:** `update_usr_ventas_updated_at` — actualiza `updated_at` automáticamente en cada `UPDATE`.

---

#### Tabla: `usr_produccion` (`[DAT-02]`)

> **Rol:** Determina si se aplica Regla 1 o Regla 2 de `demanda_teorica` (a través de `unidades_sobrantes`).
> **Granularidad:** Diaria (1 registro por día).
> **Actualización:** Diaria, después de ventas confirmadas.
> **Owner:** Cafetería SAS (Producción).

| Columna | Tipo PostgreSQL | Nullable | Default | Descripción |
|---|---|---|---|---|
| `id` | `bigint` | `false` | `generated by default as identity` | Identificador único (PK) |
| `fecha` | `date` | `false` | — | Fecha del registro de producción. Debe alinearse con fechas de `usr_ventas` |
| `unidades_vendidas` | `integer` | `false` | — | Total unidades vendidas ese día (agregado de `usr_ventas`) |
| `produccion_estimada` | `integer` | `false` | — | Meta de producción para el día |
| `unidades_sobrantes` | `integer` | `false` | — | Unidades no vendidas al cierre. **CRÍTICO:** si `= 0`, activa Regla 2 de `demanda_teorica` |
| `porcentaje_merma` | `numeric(5, 2)` | `true` | — | Porcentaje de desperdicio (calculado o manual) |
| `created_at` | `timestamp with time zone` | `true` | `now()` | Auditoría de sistema |
| `updated_at` | `timestamp with time zone` | `true` | `now()` | Auditoría de sistema |
| `pyme_id` | `text` | `false` | `'001_ABC'` | Identificador del cliente |

**Constraint:** `usr_produccion_pkey PRIMARY KEY (id)`
**Trigger:** `update_usr_produccion_updated_at` — actualiza `updated_at` automáticamente.

---

### 2.3 Diccionario de Columnas — Tablas Opcionales

#### Tabla: `usr_clima` (`[DAT-03]`)

> **Rol:** Variable exógena candidata (condiciones climáticas).
> **Granularidad:** Diaria.

| Columna | Tipo PostgreSQL | Nullable | Default | Descripción |
|---|---|---|---|---|
| `id` | `bigint` | `false` | `generated by default as identity` | PK |
| `fecha` | `timestamp with time zone` | `false` | — | Fecha y hora del registro climático |
| `estado_clima` | `text` | `false` | — | Descripción del clima (ej: "soleado", "lluvioso") |
| `created_at` | `timestamp with time zone` | `true` | `now()` | Auditoría |
| `updated_at` | `timestamp with time zone` | `true` | `now()` | Auditoría |
| `pyme_id` | `text` | `false` | `'001_ABC'` | Identificador del cliente |

**Constraint:** `usr_clima_pkey PRIMARY KEY (id)`

---

#### Tabla: `usr_macro_anual` (`[DAT-04]`)

> **Rol:** Variable exógena candidata (SMMLV — Salario Mínimo).
> **Granularidad:** Anual.

| Columna | Tipo PostgreSQL | Nullable | Default | Descripción |
|---|---|---|---|---|
| `id` | `bigint` | `false` | `generated by default as identity` | PK |
| `fecha` | `date` | `false` | — | Año de referencia |
| `smmlv` | `numeric(12, 2)` | `true` | — | Salario Mínimo Mensual Legal Vigente (COP) |
| `created_at` | `timestamp with time zone` | `true` | `now()` | Auditoría |
| `updated_at` | `timestamp with time zone` | `true` | `now()` | Auditoría |
| `pyme_id` | `text` | `false` | `'001_ABC'` | Identificador del cliente |

**Constraint:** `usr_macro_anual_pkey PRIMARY KEY (id)`

---

#### Tabla: `usr_macro_diario` (`[DAT-05]`)

> **Rol:** Variable exógena candidata (TRM — Tasa Representativa del Mercado).
> **Granularidad:** Diaria.

| Columna | Tipo PostgreSQL | Nullable | Default | Descripción |
|---|---|---|---|---|
| `id` | `bigint` | `false` | `generated by default as identity` | PK |
| `fecha` | `date` | `false` | — | Fecha del registro |
| `trm` | `numeric(10, 2)` | `true` | — | Tipo de cambio USD/COP |
| `created_at` | `timestamp with time zone` | `true` | `now()` | Auditoría |
| `updated_at` | `timestamp with time zone` | `true` | `now()` | Auditoría |
| `pyme_id` | `text` | `false` | `'001_ABC'` | Identificador del cliente |

**Constraint:** `usr_macro_diario_pkey PRIMARY KEY (id)`

---

#### Tabla: `usr_macro_mensual` (`[DAT-06]`)

> **Rol:** Variables exógenas candidatas (inflación, desempleo).
> **Granularidad:** Mensual.

| Columna | Tipo PostgreSQL | Nullable | Default | Descripción |
|---|---|---|---|---|
| `id` | `bigint` | `false` | `generated by default as identity` | PK |
| `fecha` | `date` | `false` | — | Primer día del mes de referencia |
| `inflacion_anual` | `numeric(5, 2)` | `true` | — | Inflación anual acumulada (%) |
| `desempleo` | `numeric(5, 2)` | `true` | — | Tasa de desempleo (%) |
| `created_at` | `timestamp with time zone` | `true` | `now()` | Auditoría |
| `updated_at` | `timestamp with time zone` | `true` | `now()` | Auditoría |
| `pyme_id` | `text` | `false` | `'001_ABC'` | Identificador del cliente |

**Constraint:** `usr_macro_mensual_pkey PRIMARY KEY (id)`

---

#### Tabla: `usr_publicidad` (`[DAT-07]`)

> **Rol:** Variable exógena candidata (inversión publicitaria y campañas 2x1).
> **Granularidad:** Diaria.

| Columna | Tipo PostgreSQL | Nullable | Default | Descripción |
|---|---|---|---|---|
| `id` | `bigint` | `false` | `generated by default as identity` | PK |
| `fecha` | `date` | `false` | — | Fecha del gasto publicitario |
| `campaña` | `text` | `true` | — | Nombre de la campaña activa (null si no hay) |
| `pauta_facebook` | `numeric(12, 2)` | `true` | — | Inversión en Facebook (COP) |
| `pauta_instagram` | `numeric(12, 2)` | `true` | — | Inversión en Instagram (COP) |
| `volantes_impresos` | `numeric(12, 2)` | `true` | — | Gasto en volantes físicos (COP) |
| `total_diario` | `numeric(12, 2)` | `true` | — | Total inversión publicitaria del día (COP) |
| `created_at` | `timestamp with time zone` | `true` | `now()` | Auditoría |
| `updated_at` | `timestamp with time zone` | `true` | `now()` | Auditoría |
| `pyme_id` | `text` | `false` | `'001_ABC'` | Identificador del cliente |

**Constraint:** `usr_publicidad_pkey PRIMARY KEY (id)`

---

### 2.4 Tabla `contracts` en Supabase (`[ARC-02]`)

> **Implementa:** `[REQ-07]`, `[REQ-06]`
> **Propósito:** Almacenar metadatos de cada versión del contrato, con constraint de un solo contrato activo por `pyme_id`.

#### DDL

```sql
-- TABLE: contracts
-- DESCRIPCIÓN: Registro de versiones del Data Contract.
--              Solo un contrato activo por pyme_id en cualquier momento.
-- PROPÓSITO:   Auditoría + referencia al artefacto YAML en S3.
-- GRANULARIDAD: 1 registro por versión publicada.
-- ACTUALIZACIÓN: Al publicar nueva versión del contrato.

CREATE TABLE public.contracts (
  id bigint GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  version text NOT NULL,
  s3_location text NOT NULL,
  checksum text NOT NULL,
  is_active boolean NOT NULL DEFAULT false,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by text NOT NULL,
  description text,
  pyme_id text NOT NULL DEFAULT '001_ABC',

  CONSTRAINT contracts_pkey PRIMARY KEY (id),
  CONSTRAINT contracts_version_pyme_unique UNIQUE (version, pyme_id)
) TABLESPACE pg_default;

-- CONSTRAINT: Solo un contrato activo por pyme_id
-- Implementado via partial unique index (PostgreSQL)
CREATE UNIQUE INDEX idx_one_active_contract_per_pyme
ON public.contracts (pyme_id)
WHERE is_active = true;

-- TRIGGER: Al activar una nueva versión, desactivar todas las anteriores del mismo pyme_id
CREATE OR REPLACE FUNCTION activate_contract_version()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.is_active = true THEN
    UPDATE public.contracts
    SET is_active = false
    WHERE pyme_id = NEW.pyme_id
      AND id != NEW.id
      AND is_active = true;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_activate_contract
BEFORE INSERT OR UPDATE ON public.contracts
FOR EACH ROW
EXECUTE FUNCTION activate_contract_version();

-- Trigger de auditoría (updated_at)
CREATE TRIGGER update_contracts_updated_at
BEFORE UPDATE ON public.contracts
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

#### Diccionario de Columnas

| Columna | Tipo | Nullable | Default | Descripción |
|---|---|---|---|---|
| `id` | `bigint` | `false` | `identity` | PK |
| `version` | `text` | `false` | — | Versión del contrato (ej: "1.0", "1.1"). Única por `pyme_id` |
| `s3_location` | `text` | `false` | — | Ruta completa en S3 (ej: `s3://bucket/contracts/data_contract_v1.0.yaml`) |
| `checksum` | `text` | `false` | — | SHA256 del archivo YAML para verificación de integridad |
| `is_active` | `boolean` | `false` | `false` | Solo una fila con `true` por `pyme_id` (enforced por partial unique index) |
| `created_at` | `timestamp with time zone` | `false` | `now()` | Fecha de publicación de esta versión |
| `created_by` | `text` | `false` | — | Autor que publicó (email o "CI/CD") |
| `description` | `text` | `true` | — | Resumen del cambio en esta versión |
| `pyme_id` | `text` | `false` | `'001_ABC'` | Identificador del cliente |

---

### 2.5 Estructura de Almacenamiento S3 (`[ARC-03]`)

```
s3://{SUPABASE_S3_BUCKET}/
└── contracts/
    ├── data_contract_v1.0.yaml     # Versión inicial (Etapa 1.3)
    ├── data_contract_v1.1.yaml     # Futuras versiones...
    └── data_contract_v2.0.yaml
```

**Convención de nombres:** `data_contract_v{VERSION}.yaml`
**Versionamiento:** Cada archivo es inmutable. Nuevas versiones = nuevos archivos.
**Acceso:** Engine usa credenciales S3 de `.env` (`SUPABASE_S3_*`).

---

## 3. Diseño del Módulo / Función

### 3.1 Estructura de Carpetas (Nuevas)

```
engine/
├── src/
│   ├── connectors/
│   │   └── supabase_client.py       # Existente (Etapa 1.2)
│   └── contract/                    # NUEVO
│       ├── __init__.py
│       ├── contract_loader.py       # [ARC-04]
│       └── contract_validator.py    # [ARC-05]
│
├── tests/
│   ├── connectors/
│   │   └── test_supabase_client.py  # Existente (Etapa 1.2)
│   └── contract/                    # NUEVO
│       ├── test_contract_loader.py
│       └── test_contract_validator.py
│
└── config.yaml
```

### 3.2 Funciones

| Función | Módulo | Input | Output | REQ |
|---|---|---|---|---|
| `load_contract_from_cloud()` | `contract_loader.py` | `pyme_id: str` | `dict` (contrato parseado) o `SystemExit` | `[REQ-09]` |
| `load_contract_from_file()` | `contract_loader.py` | `file_path: str` | `dict` (contrato parseado) | `[REQ-01]` |
| `get_active_contract_location()` | `contract_loader.py` | `pyme_id: str` | `tuple(s3_location, checksum)` | `[REQ-07]` |
| `download_from_s3()` | `contract_loader.py` | `s3_location: str` | `bytes` (contenido del archivo) | `[REQ-08]` |
| `verify_checksum()` | `contract_loader.py` | `content: bytes, expected: str` | `bool` | `[REQ-08]` |
| `validate_contract_structure()` | `contract_validator.py` | `contract: dict` | `bool` o `raise ContractValidationError` | `[REQ-01]` |
| `validate_mandatory_tables()` | `contract_validator.py` | `contract: dict` | `bool` o `raise ContractValidationError` | `[REQ-03]` |
| `get_mandatory_table_names()` | `contract_validator.py` | `contract: dict` | `list[str]` | `[REQ-03]` |
| `get_optional_table_names()` | `contract_validator.py` | `contract: dict` | `list[str]` | `[REQ-03]` |
| `get_all_table_names()` | `contract_validator.py` | `contract: dict` | `list[str]` | `[REQ-02]` |
| `publish_contract()` | `contract_loader.py` | `file_path: str, pyme_id: str, created_by: str` | `dict` (registro insertado en Supabase) | `[REQ-06]`, `[REQ-08]` |

### 3.3 Flujo de Startup del Engine (`[REQ-09]`)

```python
# Pseudocódigo — engine/main.py (futuro, Fase 2)
def startup():
    """
    Paso obligatorio antes de cualquier pipeline.
    Si falla → sys.exit(1).
    """
    pyme_id = config['database']['supabase']['pyme_id']

    # 1. Obtener ubicación del contrato activo
    s3_location, expected_checksum = get_active_contract_location(pyme_id)
    #    → Si no existe: raise ContractNotFoundError
    #    → "FATAL: No active data contract found for pyme_id '001_ABC'."

    # 2. Descargar desde S3
    content = download_from_s3(s3_location)
    #    → Si falla: raise S3DownloadError

    # 3. Verificar integridad
    if not verify_checksum(content, expected_checksum):
        raise ChecksumMismatchError(
            f"Contract checksum mismatch. Expected: {expected_checksum}"
        )

    # 4. Parsear YAML
    contract = yaml.safe_load(content)

    # 5. Validar estructura
    validate_contract_structure(contract)
    validate_mandatory_tables(contract)

    # 6. Contrato cargado — continuar
    log.info(f"✓ Contract v{contract['metadata']['version']} loaded for {pyme_id}")
    return contract
```

### 3.4 Flujo de Publicación Manual (`[ARC-06]`)

```python
# Pseudocódigo — invocado manualmente o por CI/CD
def publish_contract(file_path: str, pyme_id: str, created_by: str):
    """
    1. Leer archivo local
    2. Parsear y validar estructura
    3. Extraer versión de metadata
    4. Calcular checksum SHA256
    5. Subir a S3 con nombre versionado
    6. Insertar registro en Supabase con is_active=true
       (trigger desactiva versiones anteriores automáticamente)
    """
    # Leer y validar
    with open(file_path, 'rb') as f:
        content = f.read()
    contract = yaml.safe_load(content)
    validate_contract_structure(contract)

    version = contract['metadata']['version']
    checksum = hashlib.sha256(content).hexdigest()

    # Subir a S3
    s3_key = f"contracts/data_contract_v{version}.yaml"
    s3_client.upload(content, s3_key)

    # Registrar en Supabase (trigger desactiva versión anterior)
    record = supabase.table('contracts').insert({
        'version': version,
        's3_location': f"s3://{bucket}/{s3_key}",
        'checksum': checksum,
        'is_active': True,
        'created_by': created_by,
        'description': f"Contract v{version} published",
        'pyme_id': pyme_id
    }).execute()

    return record
```

### 3.5 Errores Definidos

| Error | Código | Cuándo se lanza | Efecto |
|---|---|---|---|
| `ContractNotFoundError` | `ERR_CNTR_001` | No hay contrato activo en Supabase para el `pyme_id` | Engine no inicia |
| `S3DownloadError` | `ERR_CNTR_002` | Fallo al descargar archivo desde S3 | Engine no inicia |
| `ChecksumMismatchError` | `ERR_CNTR_003` | SHA256 del archivo descargado no coincide con el registrado | Engine no inicia |
| `ContractParseError` | `ERR_CNTR_004` | YAML inválido o no parseable | Engine no inicia |
| `ContractValidationError` | `ERR_CNTR_005` | YAML válido pero estructura incorrecta (faltan secciones o tablas mandatorias) | Engine no inicia |
| `MandatoryTableRemovalError` | `ERR_CNTR_006` | Se intenta publicar un contrato sin una tabla mandatoria que existía en la versión anterior | Publicación rechazada |

---

## 4. Contratos de Datos entre Capas

| Origen | Destino | Formato | Descripción |
|---|---|---|---|
| `contracts/data_contract.yaml` (local) | S3 `contracts/` | YAML | Publicación manual del artefacto |
| S3 `contracts/` | Engine (memoria) | `dict` Python | Descarga en startup |
| Supabase `contracts` table | Engine (query) | JSON → `tuple` | Obtener `s3_location` + `checksum` del contrato activo |
| Engine (memoria) | Etapa 2.1+ (validación) | `dict` Python | Contrato cargado se usa para validar estructura de tablas en Supabase |

**Nota importante:** En esta etapa el contrato se **crea y publica**. Las etapas posteriores lo **consumen**:
- **Etapa de validación del contrato:** Usa el contrato para verificar que las tablas, columnas y tipos en Supabase coinciden con lo estipulado.
- **Etapa de validación de calidad:** Usa reglas de negocio (no definidas en el contrato) para verificar valores, nulos, centinelas.

---

## 5. Configuración (`config.yaml`)

Claves a añadir en `engine/config.yaml` para esta etapa:

```yaml
# Sección a agregar en config.yaml
contract:
  pyme_id: "001_ABC"                    # Identificador del cliente
  local_path: "contracts/data_contract.yaml"  # Ruta local del contrato
  s3_prefix: "contracts/"               # Prefijo en S3 para artefactos de contrato
  startup_required: true                # Si true, Engine no inicia sin contrato activo
```

**Nota:** `engine/config.yaml` actualmente tiene tablas listadas bajo `database.supabase.tables`. Esa lista debe mantenerse sincronizada con el contrato, pero el contrato es la **fuente de verdad** para la definición estructural. El `config.yaml` es un atajo operativo para el Engine.

---

## 6. Observaciones Técnicas

### 6.1 Discrepancia `config.yaml` vs `schema.sql`

Se detectó que `engine/config.yaml` lista tablas diferentes a `docs/database/schema.sql`:

| `config.yaml` | `schema.sql` | Notas |
|---|---|---|
| `usr_ventas` | `usr_ventas` | OK |
| `usr_produccion` | `usr_produccion` | OK |
| `usr_inventario` | — | No existe en `schema.sql` |
| `usr_clima` | `usr_clima` | OK |
| `usr_festivos` | — | No existe en `schema.sql` |
| `usr_ipc` | — | No existe en `schema.sql` |
| `usr_publicidad` | `usr_publicidad` | OK |
| — | `usr_macro_anual` | No existe en `config.yaml` |
| — | `usr_macro_diario` | No existe en `config.yaml` |
| — | `usr_macro_mensual` | No existe en `config.yaml` |

**Acción requerida:** Sincronizar `config.yaml` con `schema.sql` durante la implementación. El contrato (`data_contract.yaml`) usa los nombres de `schema.sql` como fuente de verdad.

---

## 7. Matriz de Diseño vs PRD

| REQ | Componente que lo implementa | Archivo | Notas |
|---|---|---|---|
| `[REQ-01]` | Archivo YAML con 5 secciones obligatorias | `contracts/data_contract.yaml` | Estructura definida en §2.1 |
| `[REQ-02]` | Diccionario de columnas de 7 tablas | `contracts/data_contract.yaml` (arrays `mandatory_tables` + `optional_tables`) | Arrays extensibles a N tablas. Detalle en §2.2 y §2.3 |
| `[REQ-03]` | Clasificación mandatoria/opcional | Secciones `mandatory_tables` y `optional_tables` del YAML | `usr_ventas` y `usr_produccion` = mandatorias |
| `[REQ-04]` | Fórmula de `demanda_teorica` | Sección `objective_variable.calculation` del YAML | 2 reglas + algoritmo paso a paso |
| `[REQ-05]` | Parámetros de inferencia | Sección `objective_variable.calculation.parameters` del YAML | `lookback_days: 90`, `same_weekday`, `exclude_holidays: true` |
| `[REQ-06]` | Versionamiento estricto + un solo activo | Tabla `contracts` con partial unique index + trigger | §2.4 DDL completo |
| `[REQ-07]` | Tabla `contracts` en Supabase | `public.contracts` | DDL en §2.4, diccionario de columnas incluido |
| `[REQ-08]` | Artefacto en S3 + registro en Supabase | `publish_contract()` en `contract_loader.py` | Flujo en §3.4 |
| `[REQ-09]` | Startup del Engine con error bloqueador | `load_contract_from_cloud()` en `contract_loader.py` | Flujo en §3.3, errores en §3.5 |
| `[REQ-10]` | Changelog en YAML | Sección `changelog` del YAML | Array extensible con entrada por versión |
