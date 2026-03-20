# [RULE-BUSINESS] - Reglas de Negocio y Lógica de Dominio
**Proyecto:** Demo_Bunuelos  
**Estado:** Oficial / Aprobado

Este documento formaliza la lógica operativa y comercial de **Demo_Bunuelos**, sirviendo como base única para la ingeniería de características (Feature Engineering) y las simulaciones del modelo de IA.

---

## 1. Operaciones y Horarios

### 1.1 Jornada Laboral
- **RN_OPER_001 (Horario de Operación):** El horario oficial de atención es de **6:00 AM a 6:00 PM**. Las ventas registradas fuera de este rango se consideran atípicas o cierres administrativos.

### 1.2 Producto Terminado
- **RN_OPER_002 (Vida Útil):** El buñuelo frito tiene una vida útil de **un (1) día**. Todo producto no vendido al cierre de las 6:00 PM se considera desperdicio.

---

## 2. Estacionalidad y Comportamiento de Demanda (Calendario)

### 2.1 Jerarquía de Ventas Semanal / Festivos
- **RN_DEM_001 (Nivel Máximo):** Domingos y Festivos Religiosos (Semana Santa, 8 y 25 de diciembre, etc.).
- **RN_DEM_002 (Nivel Alto):** Sábados y Lunes Festivos.
- **RN_DEM_003 (Nivel Base):** Lunes (día laboral con mayor carga de ventas entre semana).
- **RN_DEM_004 (Meses Top):** Diciembre, Enero, Junio y Julio.

### 2.2 Hitos de Consumo Masivo
- **RN_DEM_005 (Inyección de Liquidez):** Días de Quincena (15 y 30) y periodos de Prima Salarial (mitad y fin de año).
- **RN_DEM_006 (Temporada Navideña):** Las Novenas Navideñas (16 al 24 de diciembre) son días de demanda pico constante.

---

## 3. Factores Externos (Contexto)

### 3.1 Clima ("Efecto Antojo")
- **RN_CONT_001 (Prioridad de Clima):** El clima **Frío** es el principal motor de incremento de ventas, seguido de los días con **Lluvia Ligera**.

### 3.2 Impacto Macroeconómico (Contexto Anual)
- **RN_CONT_002 (Consumo):** El Salario Mínimo (SMMLV) tiene un impacto positivo directo en la capacidad de consumo de los clientes de buñuelos.
- **RN_CONT_003 (Sensibilidad de Gasto):** La inflación (IPC) y la tasa de desempleo actúan como frenos en la demanda discrecional.
- **RN_CONT_004 (Contexto):** El modelo debe monitorear la tasa de cambio (TRM) como indicador de presión inflacionaria en costos indirectos.

---

## 4. Estrategia Comercial y Marketing

### 4.1 Promociones 2x1 (Paga 1, Lleva 2)
- **RN_COM_001 (Ciclos Anuales):**
    - **Mayo:** Todo el mes completo.
    - **Septiembre/Octubre:** Desde el 15 de septiembre hasta el 15 de octubre.

### 4.2 Inversión Digital (`publicidad.csv`)
- **RN_COM_002 (Presupuestos Diarios):**
    - **Facebook:** $20k COP / día.
    - **Instagram:** $30k COP / día.
    - **Volantes:** Inversión de campo amortizada.
- **RN_COM_003 (Fase de Expectativa):** Las campañas inician **15 días antes** de cada promoción (Fase de Calentamiento) y finalizan el último día de la promoción.

---

## 5. Glosario de Términos
- **Festivo Religioso:** Fechas de calendario litúrgico con alto impacto en reuniones familiares.
- **Lunes Festivo:** Días festivos que se trasladan al lunes (Ley Emiliani) con alto flujo de retorno de viajes.
- **Prima:** Salario extra legal en Colombia que dispara el consumo en junio y diciembre.

---

## 6. Mandato de Validación Estadística
- **RN_VAL_001 (Hipótesis del Cliente):** Todas las reglas de negocio descritas en este documento (patrones de clima, jerarquía de días y efectos macro) se consideran **hipótesis de dominio** proporcionadas por el cliente. Es OBLIGATORIO validar estadísticamente cada una de estas premisas durante la **Fase 3.1 (EDA)** antes de su uso como variables exógenas en el entrenamiento final del modelo.
