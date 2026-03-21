# SPEC — Definiciones y Cimientos: Gobernanza y Estructura Base (`f01_01`)

> **Trazabilidad:** Este documento implementa los requerimientos definidos en `docs/reqs/f01_01_prd.md`.
> **Etapa:** 1.1 — Reglas globales, estructura de archivos e inicialización del `PROJECT_index.md`
> **Estado:** 🟡 En Progreso
> **Última actualización:** 2026-03-20

---

## 1. Arquitectura Lógica

Esta etapa no construye pipelines de datos ni modelos. Su arquitectura es **documental y de configuración**: define los componentes de gobernanza que todo agente IA debe leer antes de ejecutar cualquier acción.

```
Demo_Bunuelos/
│
├── CLAUDE.md                          ← [ARC-01] Constitución del agente IA
├── PROJECT_index.md                   ← [ARC-02] Mapa macro del proyecto
├── PROJECT_handoff.md                 ← [ARC-03] Bitácora de sesión (micro)
│
├── .claude/
│   └── skills/
│       ├── update-index/
│       │   └── SKILL.md              ← [ARC-04a] Skill: /update-index
│       ├── session-close/
│       │   └── SKILL.md              ← [ARC-04b] Skill: /session-close
│       └── sdd-doc/
│           └── SKILL.md              ← [ARC-04c] Skill: /sdd-doc
│
├── docs/                              ← [ARC-05] Repositorio de documentación SDD
│   ├── reqs/                          ← PRDs por etapa (f[F]_[E]_prd.md)
│   ├── specs/                         ← SPECs por etapa (f[F]_[E]_spec.md)
│   ├── plans/                         ← Planes por etapa (f[F]_[E]_plan.md)
│   ├── tasks/                         ← Task Lists por etapa (f[F]_[E]_task.md)
│   ├── lessons/                       ← [ARC-09] Lecciones aprendidas (lessons-learned.md)
│   ├── executives/                    ← [ARC-10] Resúmenes ejecutivos por etapa (f[F]_[E]_executive.md)
│   └── changes/                       ← [ARC-11] Controles de cambio (CC_XXXXX.md)
│
├── requirements.txt                   ← [ARC-06] Dependencias del motor Python
├── .env                               ← Secretos locales (NO trackeado en Git)
├── .env.example                       ← Plantilla de variables de entorno
└── .gitignore                         ← Patrones de exclusión del repositorio
```

### Componentes y responsabilidades

| ID | Componente | Ruta | Responsabilidad |
|---|---|---|---|
| `[ARC-01]` | Constitución del Agente | `CLAUDE.md` | Fuente de verdad única para el comportamiento del agente IA. Lectura obligatoria en el Paso 1 del Protocolo de Inicio. |
| `[ARC-02]` | Índice Macro | `PROJECT_index.md` | Estado del proyecto a gran escala: fase activa, hitos, rutas críticas e índice de documentos SDD. Lectura obligatoria en el Paso 2 del Protocolo de Inicio. |
| `[ARC-03]` | Bitácora de Sesión | `PROJECT_handoff.md` | Estado táctico inmediato: archivos activos, contexto, último error y próxima acción. Lectura obligatoria en el Paso 3. Se reescribe al cierre de cada sesión. |
| `[ARC-04a]` | Skill update-index | `.claude/skills/update-index/SKILL.md` | Automatiza la creación y actualización de `PROJECT_index.md`. |
| `[ARC-04b]` | Skill session-close | `.claude/skills/session-close/SKILL.md` | Automatiza el cierre de sesión reescribiendo `PROJECT_handoff.md`. |
| `[ARC-04c]` | Skill sdd-doc | `.claude/skills/sdd-doc/SKILL.md` | Crea o actualiza cualquiera de los 4 documentos SDD (PRD/SPEC/Plan/Tasks) con trazabilidad por tags. |
| `[ARC-05]` | Documentación SDD | `docs/` | Repositorio de los 4 tipos de documentos que gobiernan cada etapa. Convención: `f[F]_[E]_[tipo].md`. |
| `[ARC-06]` | Entorno Python | `requirements.txt` + `venv/` | Dependencias del motor de IA. `venv/` se excluye de Git. |
| `[ARC-07]` | Skill close-stage | `.claude/skills/close-stage/SKILL.md` | Genera el resumen ejecutivo de etapa en lenguaje de negocio al ejecutar `/close-stage`. |
| `[ARC-08]` | Skill change-control | `.claude/skills/change-control/SKILL.md` | Gestiona el ciclo de vida completo de Controles de Cambio al ejecutar `/change-control`. |
| `[ARC-09]` | Lecciones Aprendidas | `docs/lessons/lessons-learned.md` | Registro acumulativo por etapa/sesión. Actualizado por `/session-close`. |
| `[ARC-10]` | Resúmenes Ejecutivos | `docs/executives/f[F]_[E]_executive.md` | Un documento por etapa. Gate obligatorio de avance. Generado por `/close-stage`. |
| `[ARC-11]` | Controles de Cambio | `docs/changes/CC_XXXXX.md` | Numeración secuencial. Estados: Pendiente/Aprobado/No Aprobado. Gestionado por `/change-control`. |

---

## 2. Especificaciones de Archivos de Configuración

> Esta etapa no tiene tablas Supabase ni esquemas Pandera. En su lugar se especifican los archivos de configuración de infraestructura.

### 2.1 Estructura de `CLAUDE.md` — Secciones obligatorias (`[REQ-01]`)

| # | Sección | Propósito |
|---|---|---|
| 1 | Comportamiento del Agente | Límites de autonomía, mandato SDD, protocolo de inicio y cierre |
| 2 | Identidad y Contexto | Propósito del proyecto, reglas de negocio críticas |
| 3 | Stack Tecnológico | Python, Next.js, Supabase, S3, GitHub Actions |
| 4 | Arquitectura y Estructura | Descripción de archivos de gobernanza y carpetas del proyecto |
| 5 | Estándares y Convenciones | Medallion, Pandera, gestión de errores, seguridad, DVC |
| 6 | Flujos de Trabajo | Git Flow, reglas de commits, comandos recurrentes |
| 7 | Protocolos IA/ML | ForecasterDirect, MAPE threshold, variables exógenas |
| 8 | Conocimiento de Dominio | Cafetería SAS, horarios, ciclos, cold start |
| 9 | Fases y Etapas | Tabla completa de las 4 fases y 12 etapas del proyecto |
| 10 | Gobernanza Estratégica | KPIs, umbrales de acción, revisiones obligatorias |

### 2.2 Estructura de `PROJECT_index.md` — Secciones obligatorias (`[REQ-02]`)

| # | Sección | Contenido esperado |
|---|---|---|
| 1 | Coordenadas Actuales | Fase activa, etapa activa, capa medallón, punteros a docs SDD con estado |
| 2 | Hitos de la Fase Actual | Checklist de etapas con emoji de estado (⬜ / 🟡 / ✅) |
| 3 | Mapa de Arquitectura | Tabla de componentes, rutas y estado de existencia |
| 4 | Índice de Documentos SDD | Tabla de todos los docs generados con enlaces y estado |
| 5 | Notas y Decisiones | Log de decisiones importantes con fecha |

### 2.3 Estructura de `PROJECT_handoff.md` — Secciones obligatorias (`[REQ-03]`)

| # | Sección | Contenido esperado |
|---|---|---|
| 1 | Punto de Guardado | Timestamp de la última actualización |
| 2 | Working Set | Lista de 2-4 archivos activos en la sesión |
| 3 | Contexto Inmediato | Qué lógica se estaba desarrollando o discutiendo |
| 4 | Bloqueador / Último Error | Mensaje de error exacto o descripción del bloqueo |
| 5 | Próxima Acción Inmediata | Micro-tarea exacta y ejecutable para la próxima sesión |

### 2.4 Especificación de Skills (`[REQ-04]`, `[REQ-05]`, `[REQ-06]`)

Cada skill DEBE cumplir el siguiente contrato de frontmatter:

```yaml
---
name: <nombre-del-skill>          # Identificador del skill (sin espacios)
description: "<descripción>"      # Cuándo usarlo (guía para Claude)
invocation: user                  # "user" = solo el usuario lo invoca con /nombre
triggers:                         # Palabras clave que hacen que Claude lo auto-cargue
  - "<keyword-1>"
  - "<keyword-2>"
---
```

| Skill | `name` | `invocation` | Triggers principales |
|---|---|---|---|
| `/update-index` | `update-index` | `user` | `PROJECT_index`, `actualizar índice`, `estado del proyecto` |
| `/session-close` | `session-close` | `user` | `Terminamos`, `session close`, `cierre de sesión` |
| `/sdd-doc` | `sdd-doc` | `user` | `PRD`, `SPEC`, `plan de implementacion`, `lista de tareas`, `sdd` |
| `/close-stage` | `close-stage` | `user` | `cerrar etapa`, `resumen ejecutivo`, `terminamos la etapa`, `close stage` |
| `/change-control` | `change-control` | `user` | `control de cambios`, `CC`, `cambio no contemplado`, `change control`, `modificar etapa cerrada` |

### 2.5 Plantilla `.env.example` (`[DAT-01]`)

Este archivo SÍ se trackea en Git como referencia. El `.env` real NO se trackea.

```dotenv
# Supabase
SUPABASE_URL=
SUPABASE_KEY=

# AWS S3 / DVC
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET=

# Configuración general
ENVIRONMENT=development
```

### 2.6 Patrones de `.gitignore` (`[REQ-09]`)

```gitignore
# Entorno Python
venv/
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/

# Secretos
.env

# Artefactos de IA (gestionados por DVC)
*.pkl
*.joblib
*.h5
/data/

# DVC
.dvc/cache/
.dvc/tmp/

# IDEs
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## 3. Especificación del Entorno Python (`[REQ-08]`)

Archivo: `requirements.txt` — Python **3.12+** requerido.

```txt
# Motor de Forecasting
skforecast==0.13.0
scikit-learn==1.5.2
xgboost==2.1.1
lightgbm==4.5.0

# Validación de Datos
pandera==0.20.4

# Manipulación de Datos
pandas==2.2.3
numpy==1.26.4

# Infraestructura
supabase==2.7.4
python-dotenv==1.0.1

# Versionamiento de Datos y Modelos
dvc[s3]==3.55.2
```

> **Nota:** Los números de versión son los estables recomendados a la fecha de creación de esta etapa (2026-03-20). Deben validarse con `pip install -r requirements.txt` en Python 3.12+ antes de marcar `[MET-04]` como cumplida.

---

## 4. Contratos entre Componentes de Gobernanza

| Componente Origen | Componente Destino | Interfaz | Validación |
|---|---|---|---|
| `CLAUDE.md` | Agente IA | Lectura en Paso 1 del Protocolo de Inicio | El agente confirma haber leído las 10 secciones |
| `PROJECT_index.md` | Agente IA | Lectura en Paso 2 del Protocolo de Inicio | El agente identifica la etapa activa y los docs SDD gobernantes |
| `PROJECT_handoff.md` | Agente IA | Lectura en Paso 3 del Protocolo de Inicio | El agente ejecuta la Próxima Acción Inmediata sin preguntar |
| Skill `/session-close` | `PROJECT_handoff.md` | Reescritura al cierre de sesión | El archivo tiene timestamp actualizado y próxima acción concreta |
| Skill `/update-index` | `PROJECT_index.md` | Creación o actualización | El archivo refleja el hito recién completado |
| Skill `/sdd-doc` | `docs/reqs/`, `docs/specs/`, `docs/plans/`, `docs/tasks/` | Creación o actualización según modo A/B/C/D | El archivo generado sigue la estructura y nomenclatura `f[F]_[E]_[tipo].md` |

---

## 5. Configuración Global (`config.yaml`)

> Esta etapa no requiere `config.yaml`. El archivo se creará en la **Etapa 2.1** cuando se establezca la conexión a Supabase y se definan los nombres de tablas y rutas S3.

---

## 6. Matriz de Diseño vs PRD

| REQ | Componente que lo implementa | Archivo(s) | Notas |
|---|---|---|---|
| `[REQ-01]` | `[ARC-01]` Constitución del Agente | `CLAUDE.md` | Verificación manual de 10 secciones |
| `[REQ-02]` | `[ARC-02]` Índice Macro | `PROJECT_index.md` | Generado/actualizado con `/update-index` |
| `[REQ-03]` | `[ARC-03]` Bitácora de Sesión | `PROJECT_handoff.md` | Generado/actualizado con `/session-close` |
| `[REQ-04]` | `[ARC-04a]` Skill update-index | `.claude/skills/update-index/SKILL.md` | Frontmatter y contenido según §2.4 |
| `[REQ-05]` | `[ARC-04b]` Skill session-close | `.claude/skills/session-close/SKILL.md` | Frontmatter y contenido según §2.4 |
| `[REQ-06]` | `[ARC-04c]` Skill sdd-doc | `.claude/skills/sdd-doc/SKILL.md` | 4 modos A/B/C/D con trazabilidad por tags |
| `[REQ-07]` | `[ARC-05]` Documentación SDD | `docs/reqs/`, `docs/specs/`, `docs/plans/`, `docs/tasks/` | Carpetas creadas vacías (sin `.gitkeep` requerido) |
| `[REQ-08]` | `[ARC-06]` Entorno Python | `requirements.txt` + `venv/` | Versiones pinneadas según §3 |
| `[REQ-09]` | Repositorio Git | `.gitignore` + commit inicial | Patrones de exclusión según §2.6 |
| `[REQ-10]` | `/session-close` actualizado | `.claude/skills/session-close/SKILL.md` | Paso 4 añadido: actualiza `docs/lessons/lessons-learned.md` |
| `[REQ-11]` | `[ARC-07]` Skill close-stage | `.claude/skills/close-stage/SKILL.md` | Genera resumen ejecutivo en lenguaje de negocio |
| `[REQ-12]` | `[ARC-08]` Skill change-control | `.claude/skills/change-control/SKILL.md` | 4 modos: CREATE, APPROVE, REJECT, LIST |
| `[REQ-13]` | `[ARC-09]` Lecciones Aprendidas | `docs/lessons/lessons-learned.md` | Estructura: sección por etapa → entradas por sesión → resumen de etapa |
| `[REQ-14]` | `[ARC-10]` Carpeta ejecutivos | `docs/executives/` | Creada vacía; se puebla con `/close-stage` |
| `[REQ-15]` | `[ARC-11]` Carpeta cambios | `docs/changes/` | Creada vacía; se puebla con `/change-control` |
