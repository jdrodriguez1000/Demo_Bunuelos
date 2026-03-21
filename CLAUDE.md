# CLAUDE.md - Constitución del Proyecto Demo_Bunuelos

Este archivo define las leyes, límites y terreno de juego para cualquier Agente de IA que interactúe con este repositorio. Es de lectura obligatoria y cumplimiento dogmático.

---

## 1. Comportamiento del Agente (Reglas de Oro) 🛡️

*   **Límites de Autonomía:**
    *   **Prohibido avanzar** autónomamente a una nueva fase o etapa del proyecto sin una orden explícita ("Procede", "Siguiente", "Avanza").
    *   **Prohibido escribir o generar archivos** (código, documentos o configuraciones) sin una petición o confirmación explícita del usuario.
    *   La proactividad se limita exclusivamente al análisis y sugerencias en el chat.
    *   **Mandato SDD (Spec-Driven):** El desarrollo se rige por una jerarquía documental de 4 niveles:
        1. **`docs/reqs/f[F]_[E]_prd.md`** — Qué construir y por qué. Fuente de verdad de negocio.
        2. **`docs/specs/f[F]_[E]_spec.md`** — Cómo construirlo. Contratos de datos, interfaces y comportamiento técnico esperado.
        3. **`docs/plans/f[F]_[E]_plan.md`** — Orden y estrategia de ejecución de la fase/etapa.
        4. **`docs/tasks/f[F]_[E]_task.md`** — Lista atómica de tareas ejecutables de la fase/etapa.

        **Regla de oro:** El código es un reflejo sumiso de estos documentos. Si durante la implementación se requiere un cambio no contemplado, **DETENER** y solicitar la actualización del documento correspondiente antes de continuar. Ante discrepancia entre documentos, la jerarquía PRD → SPEC → Plan → Tareas define quién manda.
*   **Mandato de Control de Cambios (CC):** El agente debe **detener toda implementación** y ejecutar `/change-control` obligatoriamente en dos escenarios:
    1. **Cambio en etapa activa:** Se detecta que algo necesario no está contemplado en ninguno de los 4 documentos SDD de la etapa en curso. Prohibido improvisar o "resolver rápido" — primero el CC.
    2. **Cambio en etapa cerrada:** Cualquier modificación a código, configuración o documentos de una etapa ya completada. Sin importar la magnitud del cambio, si la etapa está cerrada, requiere CC aprobado.
    *   **Flujo obligatorio:** Informar la necesidad → usuario aprueba → crear `docs/changes/CC_XXXXX.md` en estado `Pendiente` → usuario confirma → estado `Aprobado` → ejecutar cambios → informar cierre. Si el usuario rechaza, estado `No Aprobado` y no se toca nada.
*   **Gate de Avance de Etapa:** **Prohibido proponer o ejecutar trabajo de una nueva etapa** si el documento `docs/executives/f[F]_[E]_executive.md` de la etapa anterior no existe. El Resumen Ejecutivo es un prerequisito de avance, no un opcional.
*   **Protocolo de Inicio de Sesión (orden obligatorio):**
    1. Leer `CLAUDE.md` — Reglas globales e invariantes del proyecto.
    2. Leer `PROJECT_index.md` — Entender en qué fase/etapa está el proyecto y qué documentos SDD gobiernan el trabajo actual.
    3. Leer `PROJECT_handoff.md` — Retomar el estado táctico exacto: archivos activos, bloqueador pendiente y próxima acción.
    *   Solo después de completar los 3 pasos el agente está autorizado a escribir código o ejecutar acciones.
*   **Protocolo de Cierre de Sesión:**
    *   Cuando el usuario diga **"Terminamos"** o señale el fin de la sesión, es **OBLIGACIÓN** del agente reescribir `PROJECT_handoff.md` con el estado exacto al momento del cierre: archivos modificados, contexto inmediato, último error/bloqueador y próxima acción concreta.
*   **Idioma:**
    *   **Código/Archivos/Carpetas:** Inglés (snake_case para archivos, CamelCase para clases).
    *   **Documentación/Comentarios/Commits:** Español.
    *   **Interfaz/Output al Usuario:** Inglés.

---

## 2. Identidad y Contexto del Proyecto 🏗️

*   **Propósito:** Dashboard de pronóstico de demanda de buñuelos para **Cafetería SAS**. El objetivo es optimizar el abastecimiento y producción diaria (30 días de horizonte).
*   **Reglas de Negocio Críticas:**
    *   **Prioridad del Dato:** Las decisiones se basan en tendencias del modelo, no en la intuición.
    *   **Minimización de Desperdicio:** Ante la duda, el modelo prioriza subestimar ligeramente para evitar desperdicio de producto perecedero.
    *   **Persistencia Cloud:** Todo es efímero localmente. La verdad reside en **Supabase** (metadatos/logs) y **S3/DVC** (modelos/datasets).

---

## 3. Stack Tecnológico Exacto 💻

*   **Engine (IA):** Python 3.12+ (ambiente virtual `venv`).
    *   *Librerías:* `skforecast`, `pandera`, `scikit-learn` (Ridge, RandomForest, GBM), `xgboost`, `lightgbm`.
*   **Dashboard (Web):** Next.js + TypeScript (App Router).
    *   *Estilo:* Tailwind CSS (según requerimiento).
    *   *Tipado:* Strict Type Safety sincronizado con Supabase.
*   **Infraestructura:**
    *   *Base de Datos:* Supabase (PostgreSQL).
    *   *Almacenamiento:* AWS S3 / DVC para versionamiento de datos de IA.
    *   *CI/CD:* GitHub Actions.

---

## 4. Arquitectura y Estructura de Carpetas 📂

*   **`PROJECT_index.md`** *(El Mapa — Macro):* Estado del proyecto a gran escala. Contiene: fase/etapa activa, punteros a documentos SDD gobernantes, checklist de hitos (Milestones) y diccionario de rutas críticas de la arquitectura. Se actualiza al cerrar un Sprint o Fase.
    *   Secciones obligatorias: `Coordenadas Actuales` | `Hitos de la Fase Actual` | `Mapa de Arquitectura (Rutas Clave)` | `Índice de Documentos SDD`.
*   **`PROJECT_handoff.md`** *(La Lupa — Micro):* Memoria a corto plazo de la sesión. Contiene: timestamp del último guardado, archivos activos (Working Set), contexto inmediato, último error/bloqueador y próxima acción exacta. Se reescribe al cerrar cada sesión.
    *   Secciones obligatorias: `Punto de Guardado` | `Archivos en el Escritorio (Working Set)` | `Contexto Inmediato` | `Bloqueador / Último Error` | `Próxima Acción Inmediata`.
*   **`engine/`**: Inteligencia Artificial (Python). *(Se crea en Fase 2)*
    *   `main.py`: Gateway/Switcher para modos `train` o `forecast`.
    *   `pipelines/`: Orquestadores que definen el orden de los pasos.
    *   `src/`: Lógica atómica, funciones y clases (transformaciones, loaders).
    *   `tests/`: Pruebas unitarias e integrales del motor.
*   **`web/`**: Interfaz de Usuario (Next.js). *(Construcción transversal, se inicia cuando hay datos verificables)*
    *   `components/`: Componentes UI y gráficos.
    *   `app/`: Rutas del dashboard (App Router).
    *   `tests/`: Pruebas de componentes y E2E.
*   **`docs/`**: Documentación técnica y gobernanza SDD.
    *   Convención de nombres SDD: `f[fase]_[etapa]_[tipo].md` (ej. Fase 1, Etapa 1 → `f01_01_*.md`).
    *   `reqs/f[F]_[E]_prd.md`: Product Requirements Document (fuente de verdad de negocio).
    *   `specs/f[F]_[E]_spec.md`: Technical Specification (contratos de datos e interfaces).
    *   `plans/f[F]_[E]_plan.md`: Plan de implementación de la fase/etapa.
    *   `tasks/f[F]_[E]_task.md`: Documento de tareas atómicas de la fase/etapa.
    *   `lessons/lessons-learned.md`: Registro acumulativo de lecciones aprendidas. Organizado por etapa con entradas por sesión. Actualizado automáticamente por `/session-close`.
    *   `executives/f[F]_[E]_executive.md`: Resumen ejecutivo en lenguaje de negocio al cerrar cada etapa. Generado por `/close-stage`. **Prerequisito obligatorio para avanzar a la siguiente etapa.**
    *   `changes/CC_XXXXX.md`: Documentos de Control de Cambios. Numeración secuencial (`CC_00001`, `CC_00002`, ...). Estados: `Pendiente` → `Aprobado` / `No Aprobado`. Gestionados por `/change-control`.
*   **Skills de Claude Code** (`.claude/skills/`):
    *   `/update-index`: Crea o actualiza `PROJECT_index.md`.
    *   `/session-close`: Cierra la sesión actualizando `PROJECT_handoff.md` y `docs/lessons/lessons-learned.md`.
    *   `/sdd-doc`: Crea o actualiza cualquiera de los 4 documentos SDD (PRD/SPEC/Plan/Tasks).
    *   `/close-stage`: Cierra formalmente una etapa generando `docs/executives/f[F]_[E]_executive.md`.
    *   `/change-control`: Gestiona el ciclo de vida completo de un Control de Cambios (crear, aprobar, rechazar, ejecutar).

---

## 5. Estándares y Convenciones de Código 📏

*   **Arquitectura Medallion:** Los datos deben fluir por capas: **Bronze** (Raw) ➔ **Silver** (Clean) ➔ **Gold** (Features/Inference).
*   **Validación Mandatoria:** Uso obligatorio de esquemas **Pandera** para validar datos en capas Silver y Gold.
*   **Gestión de Errores:** Prohibido usar `pass`. Errores deben mapearse a códigos (ej. `ERR_FCST_001`) y registrarse en logs locales y cloud.
*   **Seguridad:** Cero hardcoding. Secretos en `.env` (no trackeado), rutas y nombres de tablas en `config.yaml`.
*   **Consistencia Temporal:** Sincronización horaria obligatoria con `SELECT NOW()` de la base de datos.
*   **Separación de Responsabilidades:** Prohibido escribir lógica de transformación en `main.py` o los orquestadores de `pipelines/`. Toda la "fuerza" debe estar en `src/`.
*   **Triple Persistencia de Estado:** El éxito o fallo de cada proceso crítico debe registrarse en 3 canales obligatorios: (1) archivo local `latest`, (2) log detallado con timestamp, (3) tabla de orquestación en Supabase.
*   **DVC Obligatorio:** Prohibido subir datasets o modelos entrenados (`.pkl`) al repositorio Git. Todo artefacto pesado de IA debe versionarse con DVC y almacenarse en S3.
*   **Pushdown Operacional (SQL-First):** Las transformaciones pesadas de datos deben ejecutarse en la base de datos (SQL) siempre que sea posible, para evitar saturar la memoria local con DataFrames.
*   **Prevención de Training-Serving Skew:** La misma función atómica en `src/` que se usa para limpiar/transformar datos en entrenamiento **debe invocarse exactamente igual** en inferencia. Prohibido duplicar lógica entre pipelines.

---

## 6. Flujos de Trabajo (Workflow y Git) 🔄

*   **Git Flow:** `feat/*` ➔ `dev` ➔ `test` ➔ `prod`.
    *   *Paso Crítico:* Al finalizar pruebas en `test`, sincronizar cambios de vuelta a `dev` antes del merge final a `prod`.
*   **Reglas de Commits:** Commits atómicos, en **español**, con prefijos:
    *   `feat:` (Nueva funcionalidad)
    *   `fix:` (Corrección de errores)
    *   `docs:` (Documentación)
    *   `refactor:` (Cambios de código que no corrigen ni añaden)
*   **Comandos Recurrentes:**
    *   *Engine:* `python engine/main.py --mode [train|forecast]`
    *   *Web:* `npm run dev` (Dashboard local)
    *   *Tests:* `pytest engine/tests` | `npm test`

---

## 7. Protocolos IA/ML 🤖

*   **Estrategia Multi-Step:** Usar `ForecasterDirect` de `skforecast` para predicción directa por día. Minimiza la propagación del error en horizontes largos.
*   **Horizonte Operativo:** Salida estándar de **30 días** con granularidad diaria.
*   **Umbral de Producción:** Un modelo solo pasa a producción si alcanza **MAPE < 15%** en validación cruzada.
*   **Protocolo de Variables Exógenas:** Prohibida la inclusión ciega de variables. Candidatas obligatorias a evaluar: `is_weekend`, `is_holiday`, `is_payday`, clima (precipitación/temperatura), IPC, SMMLV, inversión publicitaria. Solo se integran si demuestran reducción real del MAPE en la Fase 3.

---

## 8. Conocimiento de Dominio (Cafetería SAS) ☕

*   **Operación:** Horario oficial 6:00 AM – 6:00 PM. Producto perecedero: vida útil de **1 día**. Todo no vendido al cierre = desperdicio.
*   **Jerarquía de Demanda Semanal:** Domingos/Festivos religiosos > Sábados/Lunes festivos > Lunes laboral (mayor venta entre semana).
*   **Meses Pico:** Diciembre, Enero, Junio y Julio.
*   **Hitos de Consumo:** Días de quincena (15 y 30), primas salariales (junio/diciembre), Novenas Navideñas (16–24 dic).
*   **Ciclos Promocionales 2x1:** Mayo completo | 15 de septiembre – 15 de octubre. Las campañas digitales inician **15 días antes** de cada promoción.
*   **Cold Start:** Para nuevos productos o sedes sin historial, usar datos de una "sede/producto gemelo" durante los primeros 14 días. El modelo autónomo toma control total solo después de ese período.

---

## 9. Fases y Etapas del Proyecto 🗺️

> **Mandato:** El avance entre fases y etapas requiere orden explícita del usuario. Cada etapa tiene su propio conjunto de documentos SDD (`f[F]_[E]_prd.md`, `_spec.md`, `_plan.md`, `_task.md`).

> **Dashboard Transversal:** La construcción del `web/` no es exclusiva de ninguna fase. A medida que cada etapa produce datos o contratos verificables, se desarrolla el componente de dashboard correspondiente en paralelo.

### Fase 1 — Definiciones y Cimientos
| Etapa | Descripción | Docs SDD |
|---|---|---|
| **1.1** | Reglas globales, estructura de archivos e inicialización de `PROJECT_index.md` | `f01_01_*.md` |
| **1.2** | Configuración de conexión e infraestructura con Supabase | `f01_02_*.md` |
| **1.3** | Definición del Data Contract (esquemas, tipos de datos, constraints) | `f01_03_*.md` |

### Fase 2 — Ingeniería e Ingestión
| Etapa | Descripción | Docs SDD |
|---|---|---|
| **2.1** | Validación de integridad de datos entrantes contra el Data Contract | `f02_01_*.md` |
| **2.2** | Carga y persistencia de datos crudos en Capa Bronze | `f02_02_*.md` |
| **2.3** | Limpieza, tratamiento de outliers y gestión de nulos (Capa Silver) | `f02_03_*.md` |

### Fase 3 — Modelado y Optimización
| Etapa | Descripción | Docs SDD |
|---|---|---|
| **3.1** | EDA estadístico y detección de estacionalidades | `f03_01_*.md` |
| **3.2** | Feature Engineering: variables temporales y exógenas | `f03_02_*.md` |
| **3.3** | Entrenamiento, validación cruzada y optimización de hiperparámetros | `f03_03_*.md` |

### Fase 4 — Operación y Analítica de Escenarios
| Etapa | Descripción | Docs SDD |
|---|---|---|
| **4.1** | Inferencia: producción y persistencia de pronósticos en tiempo real | `f04_01_*.md` |
| **4.2** | Simulación: análisis de sensibilidad y escenarios "What-if" | `f04_02_*.md` |
| **4.3** | Monitoreo: tracking de MAPE/Bias y detección de Data Drift | `f04_03_*.md` |

---

## 10. Gobernanza Estratégica 📊

*   **Ancla de Verdad:** El pronóstico del modelo es el insumo oficial para planeación y compras. Cualquier ajuste manual debe registrarse con justificación para auditoría de sesgo humano.
*   **Umbral de Discrepancia:** Si la opinión de un experto difiere en más del **20%** del pronóstico, la discrepancia debe documentarse y someterse a revisión del comité de métricas.
*   **KPI Principal:** `Overall Quality` — resume precisión del modelo e integridad de datos. Es el indicador de salud oficial del proyecto.
*   **Revisión Mensual Obligatoria:** Si el MAPE supera el 15% en producción, se realiza diagnóstico de Data Drift o fallo estructural del modelo.
*   **Umbral de Acción Crítica:** Si el MAPE supera el **25%** durante **2 días hábiles consecutivos**, el equipo de IA ejecuta diagnóstico de emergencia y comunica resultados al Panel de Expertos.
