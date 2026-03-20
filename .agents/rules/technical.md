# [RULE-TECH] - Reglas Técnicas de Procesamiento, Modelado y Stack
**Proyecto:** Demo_Bunuelos  

Este documento complementa al protocolo global, definiendo las reglas técnicas específicas para la ejecución de proyectos de forecasting y la implementación particular de Demo_Bunuelos.

---

## 1. Reglas Generales de Forecasting (Agnósticas al Proyecto)

### 1.1 Ingeniería de Datos e Investigación de Exogeneidad
- **RT_GEN_DATA_001 (Alineación Temporal):** Todo archivo o fuente de datos con frecuencia distinta a la diaria (ej. mensual, semanal) debe transformarse a frecuencia diaria obligatoriamente durante la etapa de **preprocesamiento (Capa Silver)**. Se utilizarán métodos de interpolación o *Forward Fill* según la naturaleza del dato.
- **RT_GEN_DATA_002 (Protocolo de Investigación de Exógenas):** No se permite la inclusión ciega de variables. Es obligatorio realizar un análisis de correlación y aporte estadístico para determinar si las siguientes variables candidatas mejoran el forecast:
    - **Calendario:** `is_weekend`, `is_holiday`, `is_payday` (efecto quincena).
    - **Entorno:** Clima (precipitación, temperatura).
    - **Macroeconómicas:** IPC, Salario Mínimo.
    - **Negocio:** Inversión publicitaria, promociones y eventos especiales.
- **RT_GEN_DATA_003 (Validación de Aporte):** Solo las variables que demuestren un incremento real en la precisión (reducción de MAPE) en la etapa de entrenamiento (Capa Gold) serán integradas permanentemente al modelo de producción.
- **RT_GEN_DATA_004 (Esquemas Pandera Mandatorios):** Es OBLIGATORIO definir un esquema de validación (`DataFrameSchema`) con Pandera para las capas Silver y Gold. Ningún proceso de entrenamiento o inferencia puede ejecutarse si los datos de entrada no cumplen con el contrato de datos definido.

### 1.2 Protocolo de Modelado (ML)
- **RT_GEN_ML_001 (Estrategia Multi-Step):** Se prioriza el uso de modelos con estrategia de **predicción directa por día** (tipo `ForecasterDirect`) para mitigar la propagación del error acumulado en horizontes largos.
- **RT_GEN_ML_002 (Horizonte Operativo):** La salida estándar de los modelos será de **30 días** con una granularidad de un (1) día, a menos que se especifique lo contrario en la Spec.
- **RT_GEN_ML_003 (Métrica de Verdad):** La precisión del modelo se validará mediante **MAPE** (Mean Absolute Percentage Error). Un modelo en producción debe aspirar a un MAPE < 15%.

---

## 2. Especificaciones Técnicas Demo_Bunuelos

### 2.1 Stack Tecnológico (Dual-Core)
- **Engine (IA):** Python 3.12+. Uso mandatorio de `skforecast` y `pandera` (validación de esquemas). Los modelos candidatos incluirán:
    - **Lineales y Ensambles:** `Ridge`, `RandomForest`, `GradientBoosting` e `HistGradientBoosting`.
    - **Boosting Avanzado:** `XGBoost` y `LightGBM`.
- **Web (Dashboard):** **Next.js** con **TypeScript**. Se requiere tipado estricto (`Type Safety`) en toda la comunicación con la base de datos.
- **Persistencia:** Supabase (PostgreSQL) para metadatos y control de estados; S3/DVC para almacenamiento de modelos (PKL) y datasets pesados.

### 2.2 Protocolo de Integración Web/IA
- **RT_PRO_001 (Multi-Layer Visibility):** El Dashboard web debe tener la capacidad de consumir y visualizar datos de las capas **Bronze, Silver y Gold** alojadas en Supabase.
    - **Objetivo:** Permitir auditoría de la salud de los datos originales (Bronze), validación de transformaciones (Silver) y visualización de resultados predictivos (Gold).
- **RT_PRO_002 (Type Mapping):** Cada tabla o respuesta de la base de datos debe tener una `interface` definida en TypeScript para garantizar que el renderizado de gráficos y tablas sea consistente con el esquema de datos.
- **RT_PRO_003 (Versionamiento de Artefactos de IA):** Los modelos persistidos en S3/DVC deben seguir la nomenclatura `model_[feature]_[version]_[timestamp].pkl`. El estado del "modelo activo" junto con sus metadatos de entrenamiento debe registrarse en la tabla de orquestación de Supabase.
- **RT_PRO_004 (Sincronización de Tipados Web):** Las interfaces de TypeScript en el Dashboard deben mantenerse sincronizadas con el esquema oficial de Supabase. Se recomienda el uso de herramientas de autogeneración de tipos o validación manual rigurosa para evitar errores de renderizado.

### 2.3 Estructura del Repositorio Único
```text
Demo_Bunuelos/
├── .agents/                # Inteligencia del Agente y Reglas
│   └── rules/              # Gobernanza (global, technical, etc.)
├── engine/                 # Inteligencia Artificial (Python)
│   ├── main.py             # Switcher (train/forecast)
│   ├── src/                # Funciones atómicas (loaders, preprocessors)
│   ├── pipelines/          # Guiones de entrenamiento e inferencia
│   ├── tests/              # Pruebas Unitarias, Integrales y Funcionales (Engine)
│   └── config.yaml         # Configuración técnica del motor (Hyperparams, Tablas)
├── web/                    # Interfaz de Usuario (Next.js + TypeScript)
│   ├── components/         # Componentes UI (Gráficos, Tablas)
│   ├── pages/              # Rutas del Dashboard
│   ├── styles/             # Estilos CSS/Tailwind
│   └── tests/              # Pruebas Unitarias, Integrales y Funcionales (Web)
├── docs/                   # Documentación técnica y Specs (Project_Charter, etc.)
└── PROJECT_index.md        # Bitácora oficial de estado y fases
```

---

## 3. Protocolo de Pruebas (QA & Validation)

### 3.1 Pruebas del Motor (Engine IA - Python)
- **Unitarias:** Validación de funciones atómicas en `src/`.
- **Integrales:** Validación del flujo completo entre capas (**Bronze ➔ Silver ➔ Gold**).
- **Funcionales:** Validación del pronóstico generado (*Inference-to-DB*).

### 3.2 Pruebas de la Interfaz (Web - Next.js)
- **Unitarias:** Pruebas de componentes visuales aislados.
- **Integrales:** Validación de la conexión con Supabase (Type safety).
- **Funcionales (E2E):** Validación de flujos de usuario (Gráficos, Alertas).