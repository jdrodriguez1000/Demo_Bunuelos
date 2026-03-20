# [RULE-GLOBAL] - Protocolo de Gobernanza y Mandato Crítico

Estas reglas aplican dogmáticamente a **TODOS** los módulos, agentes, habilidades y scripts del proyecto. Ninguna regla local puede sobreescribir u omitir estas directrices fundacionales.

---

## 1. Mantenimiento del Contexto y Eficiencia del Agente

- **C1.0 (Mandato del Índice):** Es OBLIGATORIO que la primera acción del agente en cada sesión sea leer el archivo de índice del proyecto (ej. `PROJECT_index.md`). No se permite iniciar ninguna acción técnica sin validar previamente el estado de la fase actual y los objetivos pendientes.
- **C1.1 (Carga Selectiva):** No cargar especificaciones de forma indiscriminada. El agente debe cargar únicamente archivos específicos del módulo o etapa de trabajo actual para maximizar la ventana de contexto y evitar la confusión de parámetros.
- **C1.2 (Evitar Ruido):** Ignorar la lógica de otros módulos del sistema a menos que exista una dependencia funcional explícita documentada en el contrato de datos o el orquestador.
- **C1.3 (Autorización Explícita):** NUNCA escribir o generar archivos en disco (código, documentos o configuraciones) sin una petición o confirmación explícita del usuario en el chat. La proactividad se limita exclusivamente a la interacción en el chat y el análisis.
- **C1.4 (Mandato de No-Avance):** Está estrictamente PROHIBIDO que el agente avance autónomamente a una nueva fase o etapa del proyecto sin la orden explícita ("Procede", "Siguiente", "Avanza") por parte del usuario.
- **C1.5 (Idioma y Nomenclatura):**
    - **Archivos/Carpetas/Código:** Ingles (Snake_case para archivos, CamelCase para clases).
    - **Documentación y Comentarios:** Español.
    - **Interfaz/Output al Usuario:** Ingles.

## 2. Seguridad, Credenciales y Referencia Temporal (Golden Rules)

- **S2.1 (Hardcoding Nulo):** Está ESTRICTAMENTE PROHIBIDO empotrar credenciales, tokens de acceso, URLs de APIs o cadenas de conexión directamente en el código fuente.
- **S2.2 (Patrón .env):** El consumo de secretos y configuraciones sensibles es exclusivo mediante variables de entorno y archivos `.env`. Estos archivos deben estar excluidos del control de versiones (Git).
- **S2.3 (Consistencia Temporal):** Se prohíbe el uso de `datetime.now()` local para procesos core de lógica de negocio o forecasting. Toda referencia temporal operativa debe sincronizarse con la base de datos (ej. `SELECT NOW()` en Supabase) para garantizar la integridad y sincronización del forecast entre el backend y el frontend.

## 3. Filosofía "Spec-Driven Development" (SDD) y Cloud-First

- **D3.1 (Acatamiento de Documentos):** El código desarrollado debe ser un reflejo sumiso y exacto de los documentos de especificaciones ubicados en la carpeta `specs/`. Si hay discrepancia, la Specification manda.
- **D3.2 (Cero Hardcoding Lógico):** Nombres de tablas, columnas de bases de datos o rutas de almacenamiento deben parametrizarse obligatoriamente en el archivo `config.yaml`.
- **D3.3 (Persistencia Cloud):** El proyecto prioriza el uso de **Supabase** para metadatos, logs y auditoría, y **S3/DVC** para el almacenamiento de datasets y modelos entrenados. La persistencia local se considera efímera y solo para procesos de cache o temporales.
- **D3.4 (Triple Persistencia de Estado):** Es mandatorio registrar el éxito o fallo de cada proceso crítico en tres canales: 
    1. Archivo local `latest`. 
    2. Log detallado con timestamp. 
    3. Firma de estado persistente en la tabla de orquestación de Supabase.
- **D3.5 (Sincronización Mandatoria):** Ante la necesidad de realizar cambios lógicos no contemplados en la documentación actual, el agente debe **DETENER LA IMPLEMENTACIÓN** y solicitar primero la actualización de la Specification correspondiente.

## 4. Arquitectura de Tres Capas y Modularidad Atómica

Este mandato define la separación estricta de responsabilidades para evitar la sobrecarga del orquestador y garantizar la reutilización de código entre los modos **Train** y **Forecast**.

### M4.1: Aislamiento de Lógica (Capa de Ejecución)
- **Mandato:** Queda estrictamente PROHIBIDO escribir lógica de transformación, cálculos estadísticos o manipulación de datos dentro de `main.py` o los archivos en `pipelines/`.
- **Ubicación:** Toda la lógica atómica debe residir en la carpeta `src/` en forma de funciones o clases independientes y testeables.
- **Objetivo:** Mantener los orquestadores limpios y enfocados únicamente en el flujo de control.

### M4.2: Idempotencia y Reutilización (Single Logic)
- **Mandato:** Las funciones en `src/` deben ser agnósticas al modo de ejecución.
- **Regla de Oro:** Si un proceso de limpieza (ej. tratamiento de nulos) se usa en el entrenamiento, debe invocarse la **exactamente la misma función** para el pronóstico. Esto garantiza que el modelo sea evaluado y ejecutado bajo las mismas condiciones de datos (*Prevention of Training-Serving Skew*).

### M4.3: Orquestación Ligera (Capa de Control)
- **Mandato:** El archivo `main.py` debe actuar únicamente como un "Switcher" o gatillo ligero.
- **Responsabilidad:** Su código se limita a:
    1. Leer argumentos de ejecución (mode: train/forecast).
    2. Cargar la configuración global desde `config.yaml`.
    3. Importar y ejecutar el pipeline correspondiente desde la carpeta `pipelines/`.

### M4.4: Fuente Única de Verdad (Config Driven)
- **Mandato:** El archivo `config.yaml` es el único lugar autorizado para definir nombres de tablas de Supabase, rutas de archivos, hiperparámetros y variables de entorno. Se prohíbe el "Hardcoding" de rutas o nombres de columnas dentro de los scripts operativos.

| Componente | Nivel | Función Principal |
| :--- | :--- | :--- |
| **main.py** | Entrada | Recibe la orden y carga el entorno conceptual. |
| **pipelines/**| Orquestación| Define el orden secuencial de los pasos (el "guion"). |
| **src/** | Ejecución | Realiza el trabajo pesado y la manipulación (los "músculos"). |

## 5. Arquitectura de Datos: Capas Medallion

Para garantizar la madurez y trazabilidad de la información, el procesamiento se divide en:

1.  **Capa Bronze (Raw):** Datos del cliente o fuentes externas en su estado original sin ninguna transformación. Propósito: Auditoría, reconstrucción histórica y trazabilidad.
2.  **Capa Silver (Processed):** Datos tras pasar por limpieza de nulos, corrección de tipos de datos, normalización de esquemas y validación contra el Data Contract.
3.  **Capa Gold (Enriched/Feature):** Datos enriquecidos tras aplicar ingeniería de características (lags, estacionalidad, variables exógenas), listos para el entrenamiento de modelos o ejecución de inferencia.

## 6. Estructura de Ejecución: Fases del Proyecto

El desarrollo se rige estrictamente por el siguiente flujo de trabajo secuencial:

### Fase 1: Definiciones y Cimientos
- **1.1:** Establecimiento de reglas globales, estructura de archivos e inicialización del `PROJECT_index.md`.
- **1.2:** Configuración de la conexión e infraestructura de túnel de datos con Supabase.
- **1.3:** Definición del Data Contract (Esquemas de tablas, tipos de datos y constraints).

### Fase 2: Ingeniería e Ingestión
- **2.1:** Validación de integridad de los datos entrantes contra el Data Contract.
- **2.2:** Carga y persistencia de datos crudos en la Capa Bronze.
- **2.3:** Ejecución de procesos de limpieza, tratamiento de outliers y gestión de valores nulos (Capa Silver).

### Fase 3: Modelado y Optimización
- **3.1:** Análisis Exploratorio de Datos (EDA) estadístico y detección de estacionalidades.
- **3.2:** Feature Engineering: Generación de variables temporales y consumo de variables exógenas.
- **3.3:** Entrenamiento de modelos, validación cruzada y optimización de hiperparámetros.

### Fase 4: Operación y Analítica de Escenarios
- **4.1:** Inferencia: Producción y persistencia de pronósticos en tiempo real.
- **4.2:** Simulación: Análisis de sensibilidad y escenarios "What-if" basados en variables controlables.
- **4.3:** Monitoreo: Tracking continuo de métricas de desempeño (MAPE, Bias) y detección de Data Drift.

## 7. Ingeniería de Software de Alta Calidad y Producción

- **Q7.1 (Entorno Hermético):** Uso obligatorio de ambiente virtual `venv` con Python 3.12 o superior.
- **Q7.2 (Pushdown Operacional):** Las transformaciones pesadas de datos deben ejecutarse en la base de datos (SQL) siempre que sea posible para evitar saturar la memoria local con DataFrames.
- **Q7.3 (Gobernanza de Datos - DVC):** Es OBLIGATORIO versionar datasets y modelos pesados con DVC (Data Version Control). Nunca subir binarios pesados al repositorio Git.
- **Q7.4 (Control de Excepciones):** Prohibido el uso de `pass`. Todos los errores deben capturarse y mapearse a códigos legibles (ej. `ERR_FCST_001`), registrándose inmediatamente en los logs de la nube.
- **Q7.5 (Filosofía Production-First):** El modelo se construirá prioritariamente sobre comportamiento endógeno. Variables exógenas solo se integrarán si aportan valor estadístico incrementado real. 

## 8. Estrategia de Ramificación (Git Flow Modificado)

### 8.1 Estructura de Ramas Permanentes
1. **`prod` (Production):** Código estable. Solo recibe cambios mediante merges controlados desde `test`. Cada merge genera un "Release Tag".
2. **`test` (Staging):** Espejo de producción para validación y QA final.
3. **`dev` (Development):** Rama principal de integración diaria del equipo de desarrollo.

### 8.2 Ciclo de Vida del Código y PRs
- **W.1 (Feature Branches):** Los desarrollos nuevos inician en una rama secundaria nacida de `dev` (ej. `feat/new-model`).
- **W.2 (Promoción a Test):** Al finalizar en `dev`, se realiza un PR hacia `test` para pruebas en entorno controlado.
- **W.3 (Sincronización de Seguridad):** Tras pruebas exitosas en `test`, el código debe integrarse **obligatoriamente** de vuelta a `dev` antes de la promoción final.
- **W.4 (Merge a Prod):** Tras el visto bueno final en `test`, se realiza el merge a `prod` y se marca la versión.

### 8.3 Resumen del Orden de Merges (Si todo sale bien)
- **feat/ramita ➔ dev** (Terminé mi tarea).
- **dev ➔ test/auxiliar** (Voy a probar esto).
- **test/auxiliar ➔ test** (Las pruebas pasaron).
- **test ➔ dev** (Sincronizo para que desarrollo tenga los arreglos de las pruebas) **<-- ¡Paso Clave!**
- **test ➔ prod** (Lanzamiento oficial).

### 8.4 Mandatos de Commits
- **C8.1 (Mensajes Atómicos):** Commits descriptivos en español detallando el cambio (ej. `feat: implementada limpieza de nulos en silver_layer`).
- **C8.2 (Merge No-Fast-Forward):** Prohibido el fast-forward en merges a `prod` y `test` para mantener la historia visual de las ramas.
