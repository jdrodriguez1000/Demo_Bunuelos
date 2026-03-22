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

### Sesión: 21 de marzo de 2026 (Gobernanza avanzada — CC_00001 y CC_00002)

**✅ Lo que funcionó bien:**
- El flujo de `/change-control` funcionó correctamente para modificar una etapa cerrada — el CC como gate impidió cambios improvisados
- Detectar la brecha del Protocolo de Inicio (agente amnésico) fue valioso — resuelto inmediatamente con CC_00002
- Incluir el CI Quality Gate en CC_00001 (no solo release-please) fue una corrección importante que el usuario señaló

**⚠️ Lo que no funcionó / fricción encontrada:**
- CC_00001 se creó sin mencionar el CI Quality Gate — el usuario tuvo que señalarlo explícitamente; el agente debió haberlo incluido desde el inicio al conocer la action del usuario

**💡 Decisiones clave tomadas:**
- Protocolo de Inicio ampliado a 5 pasos: se leen `lessons-learned.md` (etapa activa) y CCs aprobados antes de actuar
- CI Quality Gate adaptado para Demo_Bunuelos: `engine/tests/` (no `tests/`), `web/` (no `dashboard/`), escucha en `dev`/`test`/`prod` (no `main`)
- `/code-review-demo` (skill customizado) preferido sobre `/simplify` genérico — se creará en Etapa 2.1
- Un CC por cambio temático — CC_00001 (§6 CI/CD) y CC_00002 (§1 Protocolo) son independientes y correctamente separados

### Sesión: 22 de marzo de 2026 (SDD completo de Etapa 1.2)

**✅ Lo que funcionó bien:**
- Hacer todo el análisis antes de escribir documentos evitó retrabajo — las 4 decisiones arquitectónicas clave (MCP en F01_E02, TDD obligatorio, solo `engine/src/connectors/`, migrations a F01_E03) quedaron claras antes del primer documento
- El flujo PRD → SPEC → Plan → Tasks con revisión y aprobación en cada paso funcionó bien — el usuario detectó el problema del MCP en B5 antes de aprobar el Task List
- Preguntar en series cortas y esperar respuesta antes de avanzar resultó más eficiente que hacer múltiples asunciones
- CC_00003 (TDD obligatorio) fue detectado y gestionado correctamente antes de modificar CLAUDE.md — el gate de CC funcionó

**⚠️ Lo que no funcionó / fricción encontrada:**
- El MCP Supabase fue ubicado inicialmente en B5 (demasiado tarde) — el usuario lo detectó en revisión; el agente debió haberlo colocado en B1 desde el inicio al entender que es una herramienta de desarrollo activa, no un entregable
- El PRD se actualizó varias veces durante la sesión de análisis (3 commits separados) — hubiera sido más limpio tener todas las decisiones antes de crear el documento

**💡 Decisiones clave tomadas:**
- TDD obligatorio para todos los archivos Python del proyecto (CC_00003) — integration tests, no mocks para conectores
- `engine/src/connectors/` y `engine/tests/connectors/` anticipados en F01_E02; resto de `engine/` permanece en Fase 2
- MCP Supabase configurado en B1 del Task List — el agente necesita acceso a la BD desde el inicio, no al final
- Migrations SQL (versionamiento de schema) pospuestas a F01_E03 — documentado como deuda explícita en PRD §8
- `docs/database/schema.sql` creado como fuente de verdad técnica del schema — regla de mantenimiento añadida a CLAUDE.md §5
- Diccionario de columnas vive en la SPEC (no en un documento separado) — evita duplicación

### Sesión: 22 de marzo de 2026 (Implementación Etapa 1.2)

**✅ Lo que funcionó bien:**
- El ciclo TDD rojo → verde funcionó perfectamente: 4 tests en `ImportError` primero, luego 4 `passed` tras implementar — el proceso CC_00003 se validó en la práctica
- Usar `conftest.py` para cargar `.env` en pytest fue la solución limpia al problema de variables de entorno — evitó contaminar `supabase_client.py` con lógica de carga
- Detectar que `${SUPABASE_ACCESS_TOKEN}` en `.mcp.json` no se expande (se pasa literal) — llevó a la solución correcta: `--access-token` como flag explícito en `.mcp.json` gitignoreado
- Preguntar al usuario antes de scaffoldear Next.js (100+ archivos) fue la decisión correcta — el Bloque 5 se difirió sin fricción
- Refactorizar `supabase_client.py` para leer tablas desde `config.yaml` con PyYAML mantuvo los 4 tests en verde — el test es el árbitro del refactor

**⚠️ Lo que no funcionó / fricción encontrada:**
- El MCP Supabase requirió 3 reinicios de Claude Code para conectarse correctamente: primero `${VAR}` no se expandía, luego el project-ref estaba desactualizado — el setup de MCP es más frágil de lo esperado en Windows
- `settings.local.json` no acepta `mcpServers` (schema validation falla) — la documentación oficial no lo aclara claramente; la solución es `.mcp.json` separado
- `supabase.create_client()` valida formato JWT antes de llamar a la API — el test de key inválida requirió un JWT sintéticamente válido (`eyJ...`) para llegar al error de red real
- `python-dotenv` no estaba instalado en el venv al momento de los tests — dependencia implícita que debió declararse en TSK-1-04

**💡 Decisiones clave tomadas:**
- `.mcp.json` gitignoreado con token literal — más confiable que interpolación de variables en Windows
- `engine/tests/conftest.py` como punto central de carga de `.env` para todos los tests del engine
- Bloque 5 (web/) diferido a primera etapa con componentes reales — crear Next.js sin pantallas que mostrar es desperdicio
- Git Flow completo (`feat/* → dev → test → prod`) se activa en Etapa 2.1; para Etapas 1.x el código va directamente a `main`
- TSK-1-29 y TSK-1-30 no ejecutados en esta sesión — próxima sesión debe empezar por `/update-index` y `/close-stage` antes de cualquier otra acción

