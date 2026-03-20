# [RULE-STRAT] - Reglas Estratégicas y Alineación de Negocio
**Proyecto:** Demo_Bunuelos  
**Estado:** Oficial / Aprobado

Este documento define las directrices de alto nivel para la toma de decisiones, la adopción del sistema y la gestión de la neutralidad en el proceso de pronóstico de **Demo_Bunuelos**.

---

## 1. Principios de Neutralidad Analítica

### 1.1 Objetividad frente a la Intuición
- **RE_STRAT_001 (Prioridad del Dato):** Las decisiones de abastecimiento y producción deben basarse primordialmente en las tendencias detectadas por el modelo. No se permite la alteración manual de los datos históricos bajo ninguna circunstancia.
- **RE_STRAT_002 (Gestión de Discrepancias):** Si la opinión subjetiva de un experto difiere en más de un **20%** con respecto al pronóstico del modelo, dicha discrepancia debe documentarse y someterse a revisión por el comité de métricas. El modelo siempre actuará como el "Ancla de Verdad".

---

## 2. Protocolo de Adopción Operacional

### 2.1 El Modelo como Referencia Estratégica
- **RE_STRAT_003 (Insumo Principal):** El pronóstico generado por el sistema será el insumo oficial para las reuniones de planeación y compra de insumos. Cualquier ajuste manual posterior debe ser auditado.
- **RE_STRAT_004 (Transparencia en el Sesgo Humano):** Todo cambio manual realizado sobre las cifras del modelo debe registrarse con su respectiva justificación. Esto permitirá realizar auditorías de "Bias" (sesgo) para comparar si el ajuste humano mejoró o empeoró la precisión del modelo original.

---

## 3. Gestión de Escenarios y Simulaciones de Negocio

### 3.1 Análisis "What-If"
- **RE_STRAT_005 (Propósito de la Simulación):** Las herramientas de simulación (impacto de precios, promociones 2x1, eventos) son instrumentos de apoyo estratégico para la planificación, no garantías de venta. Su uso busca identificar riesgos y oportunidades.
- **RE_STRAT_006 (Horizonte de Negocio):** Para facilitar la toma de decisiones tácticas, el Dashboard presentará una visión consolidada de **30 días**, alineada con el horizonte técnico del motor de IA.

---

## 4. Gobernanza de IA y Mejora Continua

### 4.1 Evaluación de Impacto
- **RE_STRAT_007 (Auditabilidad de Desempeño):** Se realizará una revisión mensual obligatoria si el MAPE supera el 15%. Se evaluará si la desviación responde a anomalías externas (Data Drift) o a fallos estructurales del modelo.
- **RE_STRAT_008 (Claridad en KPIs):** Para evitar confusiones tácticas, el indicador principal de salud del proyecto se denominará **'Overall Quality'**. Este KPI resume la precisión del modelo y la integridad de los datos procesados, diferenciándose claramente de las métricas puramente técnicas.
- **RE_STRAT_009 (Evolución por Fases):** Se prohíbe el salto de fases en el desarrollo del ecosistema. El crecimiento del modelo (de endógeno a multivariado) debe seguir estrictamente la validación estadística previa.

---

## 5. Gestión de Riesgos y Resiliencia del Modelo

### 5.1 Desperdicio vs. Quiebre de Stock
- **RE_STRAT_010 (Prioridad del Sesgo de Pronóstico):** Dado que los buñuelos son productos perecederos de vida útil corta, ante escenarios de incertidumbre estadística, el modelo debe configurarse para **priorizar la minimización del desperdicio (waste)** sobre el riesgo de quiebre de stock (stockout). Es preferible una subestimación controlada del 5% que una sobreestimación del 10%.

### 5.2 Continuidad Operativa
- **RE_STRAT_011 (Umbral de Acción por Error Crítico):** Si el error diario (MAPE) supera el **25%** durante dos (2) días hábiles consecutivos, el equipo de IA debe realizar un diagnóstico obligatorio de la calidad de datos y factores externos. El resultado de este diagnóstico debe comunicarse al Panel de Expertos para ajustar la estrategia de abastecimiento inmediata.

### 5.3 Lanzamientos y Nuevas Aperturas
- **RE_STRAT_012 (Protocolo de 'Arranque en Frío' / Cold Start):** Para el lanzamiento de nuevos productos o apertura de sedes de **Demo_Bunuelos** sin trayectoria, se utilizarán los datos de una "sede gemela" o un "producto referente" durante los primeros 14 días. El modelo autónomo solo tomará el control total una vez se complete este periodo de maduración de datos.
