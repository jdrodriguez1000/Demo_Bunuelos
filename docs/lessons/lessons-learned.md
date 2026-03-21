# Lecciones Aprendidas — Demo_Bunuelos
**Proyecto:** Dashboard de Pronóstico de Demanda — Cafetería SAS
> Este documento es un registro vivo. Se actualiza automáticamente al ejecutar `/session-close`.
> Organizado por etapa como contenedor, con entradas individuales por sesión.
> Al cerrar cada etapa, se añade un **Resumen de Etapa** que destila las lecciones más valiosas.

---

## Fase 1 — Etapa 1.1: Gobernanza y Estructura Base

### Sesión: 21 de marzo de 2026

**✅ Lo que funcionó bien:**
- El orden de cierre (close-stage → session-close → git push) resultó ser el más limpio: el gate de avance queda antes del push
- MCP GitHub como alternativa a GitHub Actions fue la decisión correcta para Fase 1: evita costos innecesarios de API y el valor real de Actions es cuando hay código que probar
- Recrear el venv desde cero fue más rápido que intentar diagnosticar la instalación incompleta
- El protocolo de inicio de sesión (3 lecturas en orden) permite retomar el contexto en menos de 2 minutos

**⚠️ Lo que no funcionó / fricción encontrada:**
- El venv fue inicializado pero quedó vacío entre sesiones — causa probable: se creó la carpeta pero no se ejecutó `pip install`
- Una credencial de GitHub fue expuesta en texto plano durante el setup del MCP — ocurrió al no tener claro el flujo correcto con variables de entorno
- GitHub Actions requiere API key de Anthropic de pago — no documentado en el PRD inicial, generó confusión en el setup

**💡 Decisiones clave tomadas:**
- MCP GitHub configurado solo en modo lectura (escritura requiere orden explícita del usuario, según CLAUDE.md §1)
- GitHub Actions pospuesto para cuando haya código activo (Fase 2+), no necesario en fase de documentación
- Skill `/sdd-compliance` pospuesto a Etapa 2.1 — no tiene valor hasta que exista código que validar

### 📋 Resumen de la Etapa

**Lecciones más valiosas:**
1. El gate de avance (Resumen Ejecutivo) debe generarse *antes* del push final, no después — el orden importa
2. Las credenciales deben manejarse desde `.env` desde el primer día; cualquier setup de herramientas externas debe documentar este flujo explícitamente
3. Un venv vacío es difícil de detectar visualmente — agregar verificación de exit code como paso obligatorio en futuros setups de entorno

---

## Fase 1 — Etapa 1.2: Configuración de Supabase

### Sesión: 21 de marzo de 2026 (Pre-Etapa: Educación sobre Git Flow y CI/CD)

**✅ Lo que funcionó bien:**
- Explicar el Git Flow sin código resultó mucho más claro — el usuario entendió el flujo feat/* → dev → test → prod en 5 minutos
- Usar analogía de "estaciones de calidad" para explicar cada rama facilitó la comprensión
- Documentar el plan completo en memoria (github_actions_plan.md) antes de implementar evita decisiones ad-hoc

**⚠️ Lo que no funcionó / fricción encontrada:**
- CLAUDE.md §6 es ambiguo sobre el "Paso Crítico" de sincronización test→dev — requiere reescritura para claridad
- La frase "mergea automático" vs "mergea manual" generó confusión inicial sobre qué GitHub Actions hace vs no hace

**💡 Decisiones clave tomadas:**
- `main` permanecerá como rama de gobernanza (separada de `prod`), no será eliminada
- git-flow-validator implementarse en Etapa 2.1, no en 1.2 (bajo valor sin código real)
- release-please implementarse en Etapa 2.1 cuando existan features que versionar
- Protección de ramas `prod` (stricta), `test` (parcial), `dev` (parcial), `feat/*` (abierta) para implementar en Etapa 2.1

